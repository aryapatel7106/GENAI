#pip install langchain_community
#pip install langchain_text_splitters
#pip install pymongo
#pip install pypdf


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

loader = PyPDFLoader("cv.pdf")
documents = loader.load()  #load pdf into document variable

#print(documents)

text_splitter = RecursiveCharacterTextSplitter(             
    chunk_size=500,
    chunk_overlap=100             
)

docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(                       #use llm model
    api_key=os.getenv("OPENAI_API_KEY")
)

client = MongoClient("mongodb+srv://admin:admin@cluster0.6a12qs1.mongodb.net/?appName=Cluster0")  #connectionestablish

db = client["CV_RAG"]  #database
collection = db["documents"] #table

for doc in docs:
    embedding = embeddings.embed_query(doc.page_content) #vector
    document_data = {
        "text": doc.page_content,
        "embedding": embedding
    }
    collection.insert_one(document_data)
print("Document ingested and embeddings stored in MongoDB.")
