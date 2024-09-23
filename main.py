import logging
import os
from pydantic import BaseModel
from fastapi import FastAPI
from typing import Annotated
from fastapi import File, Form, UploadFile
from langchain_helper import save_pdf, query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/upload")
async def upload_file(
        file: Annotated[UploadFile, File()],
        index_name: Annotated[str, Form()]
):
    file_upload_target_path = os.path.join(os.getcwd(), file.filename)
    with open(file_upload_target_path, "wb+") as f:
        f.write(file.file.read())
    save_pdf(file_upload_target_path, index_name)
    return {"message": f"File uploaded successfully", "file_name": file.filename, "index_name": index_name}


class Query(BaseModel):
    index_name: str
    query_question: str


@app.post("/search")
def query_index(request: Query):
    logging.info("--------------------------------------")
    index_name = request.index_name
    query_question = request.query_question
    logging.info(f"index_name: {index_name}, question: {query_question}")
    return query(index_name, query_question)
