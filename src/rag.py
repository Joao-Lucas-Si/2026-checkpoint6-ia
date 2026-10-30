import os

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

def rag_load():
    
    prefixo = "data/documents"
    
    docs = [i for i in os.listdir(prefixo) if i.endswith(".md")]
    
    markdowns = [(doc, open(f"{prefixo}/{doc}", "r").read()) for doc in docs]
    return markdowns



def split(paginas: list[tuple[str, str]]):
    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1024,
    #     chunk_overlap=15,
    #     separators=["\n\n", "\n", ". ", " ", ""],
    # )
    splitter = MarkdownHeaderTextSplitter([
        ("#", "principal"),
        ("##", "seção"),
        ("###", "subseção")
    ], strip_headers=False)
    # Dividir as páginas em chunks menores
    chunks: list[Document] = []
    for pagina in paginas:
        splitted = splitter.split_text(pagina[1])
        for doc in splitted:
            doc.metadata["document"] = pagina[0]
        chunks.extend(splitted)
    # all_chunks = [splitter.split_text(pagina) for pagina in paginas]
    # all_chunks[0][0].metadata["document"] = 
    # chunks = flat splitter.split_text(paginas)
    # tamanhos = [len(c.page_content) for c in chunks]
    # chunks = [j for i in all_chunks for j in i]

    return chunks


def embed():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    return embeddings

persist_directory = "./content"
collection_name = "assistente_escrita"

def obter_salvo(embeddings: Embeddings):
    if os.path.exists("./content/chroma.sqlite3"):
        return Chroma(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embeddings)
    return 
def store(chunks: list[Document], embeddings: Embeddings):
    db: Chroma
    
    
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    db.persist()
    # db._collection.delete(
        #     where = { "": "" }
        # )
    return db

db: Chroma|None = None


def atualizar_rag(documento: str):
    if db:
        db._collection.delete(where={
            "document": documento
        })
        
        conteudo = open(f"data/documents/{documento}").read()
        
        chunks = split([(documento, conteudo)])
        
        db.add_documents(chunks)
        # db.persist()

def rag_indexar():
    global db
    embedding = embed()
    if not db:
        db = obter_salvo(embedding)
        if not db:
            paginas = rag_load()
            chunks = split(paginas)
            
            db = store(chunks, embedding)
    

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},  
    )
    
    # for i in db.similarity_search_with_relevance_scores("4. Robert Malthus", 3):
    #     print(i)
    #     print(f"score: {i[1]}")
    # print()
    return retriever