
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
import os
load_dotenv()

client = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a question paper generator . Give output in Json format."),
        ("user", "Create a question paper on {topic}, of marks {totalmarks}, of question type {questiontype} and marks per question {marksPerQuestion}")
    ]
 )

parser = JsonOutputParser()
chain = prompt | client | parser
response = chain.invoke(
 {
        "topic": "python",
        "totalmarks": 10,
        "questiontype": "MCQ",
        "marksPerQuestion": 1
        
    }
) 
print(response)