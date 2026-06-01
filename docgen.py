from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
import os

app = FastAPI()



load_dotenv()

client = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# ------------------------MODEL---------------------------------

class projectdocumentbody(BaseModel):
    projectTitle: str
    technology: str
    totalModules: int
    projectType: str


class Module(BaseModel):
    module_name: str
    description: str


class ProjectDocument(BaseModel):
    project_title: str
    project_type: str
    technology: str
    total_modules: int
    modules: list[Module]
    conclusion: str


@app.post("/projectDocumentGenerator/")
def post_data(data: projectdocumentbody):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Project Document Generator. Give output in {format} format."
            ),
            (
                "user",
                "Create a project document for project title {projectTitle}, "
                "using technology {technology}, with {totalModules} modules, "
                "and project type {projectType}"
            )
        ]
    )

    parser = PydanticOutputParser(pydantic_object=ProjectDocument)

    chain = prompt | client | parser

    response = chain.invoke(
        {
            "projectTitle": data.projectTitle,
            "technology": data.technology,
            "totalModules": data.totalModules,
            "projectType": data.projectType,
            "format": parser.get_format_instructions()
        }
    )

    print(response)

    # JSON format
    return {
        "projectTitle": data.projectTitle,
        "technology": data.technology,
        "projectType": data.projectType,
        "totalModules": data.totalModules,
        "projectDocument": response
    }


        
    