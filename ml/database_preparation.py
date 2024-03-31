from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import os
import json
import shutil

CHROMA_PATH = "ml/all_data/chroma"
CHROMA_PATH_LINKS = "ml/all_data/chroma_links"
DATA_PATH = "ml/all_data/data_md"

# CHROMA_PATH = "all_data/chroma" # not for main
# DATA_PATH = "all_data/data_md" # not for main

embedding_function = SentenceTransformerEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
loader = DirectoryLoader(DATA_PATH)


def main_generate_data_store():
    CHROMA_PATH = "ml/all_data/chroma"
    DATA_PATH = "ml/all_data/data_md"
    embedding_function = SentenceTransformerEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    loader = DirectoryLoader(DATA_PATH)
    generate_data_store()
    print("Done")


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=712,
        chunk_overlap=356,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    os.mkdir(CHROMA_PATH)
    db = Chroma.from_documents(chunks, embedding_function, persist_directory=CHROMA_PATH)
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def convert_to_chroma_embeddings(json_file):
    chroma_db = Chroma(persist_directory="CHROMA_PATH_LINKS")

    embedding_function = SentenceTransformerEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    with open(json_file, 'r') as file:
        data = json.load(file)
        for line in data:
            embedding = embedding_function.encode(line)
            # Save the embedding with the metadata to the Chroma database
            chroma_db.

    print("All embeddings saved to Chroma database.")


# Usage example
convert_to_chroma_embeddings('ml/all_data/data_prev/links_parsed.json')
