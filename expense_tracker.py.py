from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

exp = []
expense_id = 0

class expenses(BaseModel):
    #expense_id: int
    expense_name: str
    expense_type: str
    expense_description: str
    expense_price: float
    expense_payment_type: str

@app.post("/postexpense/")
def create_expense(expense: expenses):
    global expense_id 
    expense_id +=1
    expense_data = expense.dict()
    expense_data["expense_id"] = expense_id
    
    exp.append(expense_data)
    return {
        "msg": "expense added successfully",
        "data": exp
    }


@app.get("/getexpense/")
def get_expense():
    return {
        "msg": "expense data retrived successfully",
        "data": exp
    }

@app.get("/getexpenseById/{expense_id}")
def get_expense_By_id(expense_id: int):
    for expense in exp:
        if expense["expense_id"] == expense_id:
            return {
                "msg": "expense data retrived successfully",
                "data": expense
            }
    return{
             "msg": "expense not found"   
        }
    
@app.put("/putexpense/{expense_id}")
def update(expense_id: int,updates_expense: expenses):
    for expense in exp:
        if expense["expense_id"] == expense_id:
            expense["expense_name"] = updates_expense.expense_name
            expense["expense_type"] = updates_expense.expense_type
            expense["expense_description"] = updates_expense.expense_description
            expense["expense_price"] = updates_expense.expense_price
            expense["expense_payment_type"] = updates_expense.expense_payment_type
            return {
                "msg": "expense data updated successfully",
                "data": expense
            }
    return{
            "msg": "expense not found"
        }
    
@app.delete("/deleteexpense/{expense_id}")
def delete_expense(expense_id: int):
    for expense in exp:
        if expense["expense_id"] == expense_id:
            exp.remove(expense)
            return {
                "msg": "expense data deleted successfully",
                "data": exp
            }
    return{
            "msg": "expense data not found"
        }
        
@app.delete("/deleteAllexpense/")
def delete_all_expense():
    exp.clear()
    return {
        "msg": "All expense deleted successfully",
        "data": exp
    }

@app.delete("/softDeleteexpense/{expense_id}")
def soft_delete_expense(expense_id: int):
    for expense in exp:
            if expense["expense_id"] == expense_id:
                expense["is_deleted"] = True
                return {
                    "msg": "expense soft data deleted successfully",
                    "data": exp
                }
    return{
                "msg": "expense data not found"
            }
        
