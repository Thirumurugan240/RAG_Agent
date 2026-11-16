import os
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from agent import crew

cart_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cart.xlsx")

app = FastAPI(title="ShopEasy Agent API")


class Question(BaseModel):
    question: str
    history: str = ""


@app.get("/")
def home():
    return {"message": "Shopping agent API is running. POST your question to /ask"}


@app.post("/ask")
def ask(body: Question):
    result = crew.kickoff(inputs={"history": body.history, "question": body.question})
    return {"question": body.question, "answer": result.raw}


@app.get("/cart")
def get_cart():
    cart = pd.read_excel(cart_file)
    return {"items": cart.to_dict(orient="records"), "grand_total": float(cart["total"].sum())}
