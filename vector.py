from langchain_ollama import OllamaEmbeddings
from langchain_chroma import  Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_csv('games.csv')
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_db"
add_document = not os.path.exists(db_location)

if add_document:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row['title'] + " " + row['author'],
            metadata={
                "title": row['title'],
                "author": row['author'],
                "year": row['year'],
            },
            ids=str(i)
        )

        ids.append(i)
        documents.append(document)

vectorstore = Chroma(
    collection_name="Games",
    persist_directory=db_location,
    embedding_function=embeddings,
)

if add_document:
    vectorstore.add_documents(documents=documents, ids=ids)

retriver = vectorstore.as_retriever(
    search_kwargs={"k": 2},
)
