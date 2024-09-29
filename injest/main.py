from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

from pdf_loader_local_refac import ingest_semi_structured_data

_ = load_dotenv()

file_path = "../docs/policy/"

vector_store = "../vector_store_local"

file_store_path = "file_store"

model = ChatOpenAI(temperature=0,
                       model="gpt-4o-2024-08-06")

# ingest semi-structured data

retriever = ingest_semi_structured_data(file_path, vector_store)

# Prompt template
template = """Answer the question based only on the following context, which can include text and tables:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# RAG pipeline
chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
)

query = "Whats the cashback amount for dental fees per year? "
# query = "What is the cashback amount for optical fees per year?"

response = chain.invoke(query)
print(response)