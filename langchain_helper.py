from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import QianfanEmbeddingsEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
embeddings_model = QianfanEmbeddingsEndpoint()
embedding = QianfanEmbeddingsEndpoint()
persist_directory = f'C:\\Users\\Downloads\\chroma\\'


def save_pdf(file_path, file_name):
    # file_path = f"C:\\Users\\Downloads\\{file_name}.pdf"
    # file_name = file_path.split("\\")[-1].rstrip(".pdf")
    loader = PyPDFLoader(file_path)
    # 分割
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=5,  # 每个块之间的重叠长度
        length_function=len,
    )
    pages = loader.load_and_split(text_spliter)
    persist_path = persist_directory + file_name
    # 持久化到本地
    Chroma.from_documents(
        documents=pages,
        embedding=embedding,
        persist_directory=persist_path
        )


def load_index(file_name):
    persist_path = persist_directory + file_name
    print(persist_path)
    index = Chroma(persist_directory=persist_path, embedding_function=embedding)
    return index


def query(index, question):
    idx = load_index(index)
    return len(idx.similarity_search(question))

