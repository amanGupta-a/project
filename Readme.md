# Insurance Premium Category Predictor

A small web application that predicts an insurance premium category from a user's age, weight, height, smoking status, city, annual income, and occupation. The Streamlit interface sends the inputs to a FastAPI service, which derives features such as BMI, age group, lifestyle risk, and city tier before calling the trained model in `model.pkl`.

## Project files

- `main.py` — FastAPI application and `/predict` endpoint.
- `frontend.py` — Streamlit user interface.
- `model.pkl` — serialized trained prediction model; required to start the API.

## Requirements

- Python 3.9 or newer
- The Python packages below

From the project directory, create and activate a virtual environment in PowerShell, then install the packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi "uvicorn[standard]" pandas pydantic scikit-learn streamlit requests
```

The model was serialized with `pickle`. If loading it fails, install a scikit-learn version compatible with the one used when the model was created.

## Run the application

Start the API from the project directory:

```powershell
python -m uvicorn main:app --reload
```

In a second terminal, activate the same virtual environment and start the frontend:

```powershell
python -m streamlit run frontend.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`). The API runs at `http://127.0.0.1:8000`; its interactive documentation is available at `http://127.0.0.1:8000/docs`.

Start the API before making predictions. `main.py` loads `model.pkl` using a relative path, so run Uvicorn from the directory containing that file.

## Prediction API

`POST /predict` accepts a JSON object with these fields:

| Field | Type | Constraints / values |
| --- | --- | --- |
| `age` | integer | 0–120 |
| `weight` | number | Non-negative; kilograms |
| `height` | number | Greater than 0; meters |
| `smoker` | boolean | `true` or `false` |
| `city` | string | City name |
| `income_lpa` | number | Non-negative; annual income in LPA |
| `occupation` | string | `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, or `private_job` |

Example request:

```json
{
  "age": 30,
  "weight": 65,
  "height": 1.7,
  "smoker": false,
  "city": "Mumbai",
  "income_lpa": 10,
  "occupation": "private_job"
}
```

The response contains the predicted category:

```json
{
  "predicted_category": "example category"
}
```

The actual category is determined by the model. Invalid or missing request fields result in a `422 Unprocessable Entity` response with validation details.