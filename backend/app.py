from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal
import pandas as pd
import pickle


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    loan_amnt:Annotated[float,Field(...,gt = 0,description = 'Loan Amount')]
    int_rate:Annotated[float,Field(...,gt = 0,description = 'Interest Rate')]
    installment:Annotated[float,Field(...,gt = 0,description = 'Monthly installment')]
    grade:Annotated[Literal['A','B','C','D','E','F','G'],Field(...,description = 'Grade of the loan borrower')]
    home_ownership:Annotated[Literal['MORTGAGE', 'RENT', 'OWN', 'ANY', 'NONE', 'OTHER'],Field(...,description = 'Ownership type the home')]
    annual_inc:Annotated[float,Field(...,gt = 0,description = 'Annual income of the loan borrower')]
    verification_status:Annotated[Literal['Not Verified', 'Source Verified', 'Verified'],Field(...,description = 'Verification status of the income')]
    purpose:Annotated[Literal['debt_consolidation', 'small_business', 'home_improvement',
       'major_purchase', 'credit_card', 'other', 'house', 'vacation',
       'car', 'medical', 'moving', 'renewable_energy', 'wedding',
       'educational'],Field(...,description = 'Purpose to take loan')]
    dti:Annotated[float,Field(...,description = 'Debt-to-income ratio')]
    term_class:Annotated[Literal['Short-term','Long-term'],Field(...,description = 'Term period of the loan')]
    emp_class:Annotated[Literal['Junior','Intermediate','Experienced','Veteran'],Field(...,description = 'Experience type of the borrower')]
   
@app.get("/")
def home():
    return {'message':'Welcome to Loan default prediction system!'}


@app.post("/predict")
def predict_default(data: UserInput):
    try:
        input_df = pd.DataFrame([{
            "loan_amnt": data.loan_amnt,
            "int_rate": data.int_rate,
            "installment": data.installment,
            "grade": data.grade,
            "home_ownership": data.home_ownership,
            "annual_inc": data.annual_inc,
            "verification_status": data.verification_status,
            "purpose": data.purpose,
            "dti": data.dti,
            "term_class": data.term_class,
            "emp_class": data.emp_class,
        }])

        print(input_df)
        print(input_df.dtypes)
        
        not_paid_index = list(model.classes_).index("Not Paid")
        probability = model.predict_proba(input_df)[0][not_paid_index]
        threshold = 0.5
        if probability >= threshold:
            prediction = "Not Paid"
        else:
            prediction = "Paid"
        return {
            "prediction": prediction,
            "default_probability": round(float(probability), 4)
            }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}