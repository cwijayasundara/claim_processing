import warnings
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain.chains import RetrievalQA

warnings.filterwarnings('ignore')
_ = load_dotenv()

documents = TextLoader("docs/state_of_the_union.txt").load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

texts = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(documents=texts,
                                    embedding=OpenAIEmbeddings(model="text-embedding-3-small"))

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

query = "What did the president say about Ketanji Brown Jackson?"

llm = ChatOpenAI(model="gpt-4o-2024-08-06",
                 temperature=0.1)

compressor = CohereRerank(model="rerank-english-v3.0")

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

chain = RetrievalQA.from_chain_type(
    llm=llm, retriever=compression_retriever
)

response = chain.invoke({"query": query})

# extract the result from the response
print(response["result"])
