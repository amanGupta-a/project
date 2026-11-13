from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import pickle
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated

with open("model.pkl", "rb") as f:
    model = pickle.load(f) 

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
"Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
"Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
"Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
"Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
"Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
"Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]
class UserInput(BaseModel):
    
    
    age:Annotated[int, Field(...,ge=0, le=120, description="Age of the user in years")]
    weight:Annotated[float, Field(...,ge=0, description="Weight of the user in kg")]
    height:Annotated[float, Field(...,gt=0, description="Height of the user in meters")]
    smoker:Annotated[bool, Field(..., description="Whether the user smokes")]
    city:Annotated[str, Field(..., description="City of the user")]
    income_lpa:Annotated[float, Field(...,ge=0, description="Annual income of the user")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
        'business_owner', 'unemployed', 'private_job'], Field(...,description="Occupation of the user")]
    
    @computed_field
    @property
    def bmi(self)->float:
        return round((self.weight/(self.height**2)),2)
    
    @computed_field
    @property 
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        return "low"
    
    @computed_field
    @property 
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property 
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    
@app.get("/")
def hello():
    return {"message": "Welcome to Prediction API!"}

@app.post("/predict")
def predict_premium(data:UserInput):
    input_df=pd.DataFrame([{
        "bmi":data.bmi,
        "age_group":data.age_group,
        "income_lpa":data.income_lpa,
        "smoker":data.smoker,
        "city_tier":data.city_tier,
        "lifestyle_risk":data.lifestyle_risk,
        "occupation":data.occupation
    }])
    prediction=model.predict(input_df)[0]
    
    return JSONResponse(status_code=200, content={'predicted_category': prediction})
    