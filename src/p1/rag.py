
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

embedding=HuggingFaceEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
)
docs=Document(
    page_content=open("./src/p1/simple_source.py").read(),
    metadata={
        "file_name":"simple_source.py"
    }   
)
spliters=RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
docs_split=spliters.split_documents([docs])
vector=Chroma.from_documents(
    documents=docs_split,
    embedding=embedding
)

retriever=vector.as_retriever(search_kwargs={"k":2})
