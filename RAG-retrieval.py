#pip install langchain_mongodb

from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_mongodb import MongoDBAtlasVectorSearch   
import os

load_dotenv()

client = MongoClient("mongodb+srv://admin:admin@cluster0.6a12qs1.mongodb.net/?appName=Cluster0")

db = client["CV_RAG"]  #database
collection = db["documents"] #table

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY")
)

#document retrieve
vector_store = MongoDBAtlasVectorSearch(
   collection=collection,
   embedding=embeddings,
   index_name="rag_index"

)

query = "What are the education mentioned in the CV?"

ans = vector_store.similarity_search(query=query, k=3)

#print("Top 3 relevant documents:")
#print(ans)

context = " ".join(                                       #join top 3 data
    doc.page_content for doc in ans
)                          

prompt = f"""
Answer only based on the fillowing context.

if answer is not found in the context, say you don't know.

context: {context}
Question: {query}

"""

llm = ChatOpenAI(
     model="gpt-3.5-turbo"
)
response = llm.invoke(prompt)
print("Answer:",response.content)

