from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
import os

load_dotenv()

app = FastAPI()

qp = []

#---------------------------openai-----------------
client = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

#-----------------------------MODEL------------------------------------------------
class questionpaperbody(BaseModel):
    topic: str
    totalmarks: int
    questiontype: str
    marksPerQuestion: int

class Question(BaseModel):
    Ques: str
    Options: list[str]
    answer: str

class QuestionPaper(BaseModel):
       topic: str
       passing_marks: int
       questions: list[Question]


#------------------------------API-------------------------------------------------
@app.post("/questionpaperGenerator/")
def post_data(data: questionpaperbody):
    
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a question paper generator . Give output in {format} format."),
        ("user", "Create a question paper on {topic}, of marks {totalmarks}, of question type {questiontype} and marks per question {marksPerQuestion}")
    ]
)    
    parser = PydanticOutputParser(pydantic_object=QuestionPaper)
    chain = prompt | client | parser
    #qp.append(data)
    response = chain.invoke(
    {
        "topic": data.topic,
        "totalmarks": data.totalmarks,
        "questiontype": data.questiontype,
        "marksPerQuestion": data.marksPerQuestion,
        "format": parser.get_format_instructions()
    }
) 
    
    #string format in terminal
    print("\n=========QUESTION PAPER===========\n")
    print(response)

    #JSON FORMAT
    return {
        "topic": data.topic,
        "questiontype": data.questiontype,
        "totalmarks": data.totalmarks,
        "questionpaper": response
    }
