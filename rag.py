import ollama
import argparse
import chromadb
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, WebBaseLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import sys_msgs
from colorama import init, Fore, Style
import os
from tqdm import tqdm
import time
from dotenv import load_dotenv

# Load environment variables
init(autoreset=True)
load_dotenv()
####################################################################################################################################
start_time = time.time()
####################################################################################################################################
# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Run chat with command-line input.')
    parser.add_argument('--model', type=str, help="Model to use for answering the questions.", required=True)
    parser.add_argument('--doc_path', type=str, help="Path to document.", required=True)
    return parser.parse_args()
####################################################################################################################################
# Parse arguments
arg = parse_args()
model = arg.model
doc_path = arg.doc_path
EMBED = "nomic-embed-text:latest"

####################################################################################################################################
# Load and process the document
def load_and_process_document(doc_path):
    data = ""

    if doc_path.endswith('.txt'):
        print(f"{Fore.LIGHTRED_EX}LOADING TEXT FILE...{Style.RESET_ALL}")
        txt_loader = TextLoader(doc_path)
        documents = txt_loader.load()
        data = "\n".join([doc.page_content for doc in documents])

    elif doc_path.endswith('.pdf'):
        print(f"{Fore.LIGHTRED_EX}LOADING PDF FILE...{Style.RESET_ALL}")
        pdf_loader = PyMuPDFLoader(doc_path)
        documents = pdf_loader.load()
        data = "\n".join([doc.page_content for doc in documents])

    elif doc_path.startswith('https'):
        print(f"{Fore.LIGHTRED_EX}LOADING LOADING URL...{Style.RESET_ALL}")
        url_loader = WebBaseLoader(doc_path)
        documents = url_loader.load()
        data = "\n".join([doc.page_content for doc in documents])

    elif os.path.isdir(doc_path):  # Check if the path is a directory
        txt_files = any(file.endswith(".txt") for file in os.listdir(doc_path))
        pdf_files = any(file.endswith(".pdf") for file in os.listdir(doc_path))

        if txt_files:
            print(f"{Fore.LIGHTRED_EX}LOADING DIRECTORY (text)...{Style.RESET_ALL}")
            glob = "**/*.txt"
            loader_cls = TextLoader
            exclude = "*.pdf"
        elif pdf_files:
            print(f"{Fore.LIGHTRED_EX}LOADING DIRECTORY (pdf)...{Style.RESET_ALL}")
            glob = "**/*.pdf"
            loader_cls = PyMuPDFLoader
            exclude = "*.txt"
        else:
            raise ValueError(f"No supported files found in directory: {doc_path}")

        dir_loader = DirectoryLoader(path=doc_path, glob=glob, loader_cls=loader_cls, show_progress=True, exclude=exclude)
        documents = dir_loader.load()
        data = "\n".join([doc.page_content for doc in documents])

    else:
        print("No Document was loaded")

    return data
####################################################################################################################################
data = load_and_process_document(doc_path)
####################################################################################################################################
# Split documents into chunks
if data:
    # Process documents
    print(f"{Fore.LIGHTRED_EX}SPLITTING DOCUMENTS INTO CHUNKS...{Style.RESET_ALL}")
    chunk_size = 1024
    chunk_overlap = 0
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_chunks = text_splitter.split_text(data)

else:
    print("No Document was loaded")
####################################################################################################################################
# Initialize and process collection
def initialize_and_process_collection(collectionname, persist_directory, text_chunks, doc_path, embed_model):
    print(f'{Fore.LIGHTRED_EX}INITIALIZING VECTORDB...{Style.RESET_ALL}')
    vector_client = chromadb.PersistentClient(path=persist_directory)

    if any(collection.name == collectionname for collection in vector_client.list_collections()):
        print(F'{Fore.LIGHTRED_EX}DELETING COLLECTION{Style.RESET_ALL}')
        vector_client.delete_collection(collectionname)

    print(f'{Fore.LIGHTRED_EX}CREATING NEW COLLECTION: {collectionname}')
    collection = vector_client.create_collection(name=collectionname, metadata={"hnsw:space": "cosine"})

    with tqdm(text_chunks, desc=f"{Fore.LIGHTYELLOW_EX}PROCESSING CHUNKS: {doc_path}") as progress_bar:
        for index, chunk in enumerate(progress_bar):
            embeddings = ollama.embed(model=embed_model, input=chunk)['embeddings']
            collection.add(ids=[doc_path + str(index)], embeddings=embeddings, documents=['search_document: ' + chunk], metadatas=[{'source': doc_path}])

    return collection
####################################################################################################################################
# Initialize collection before starting chat
collectionname = 'rag_collection'
persist_directory = "E:/Chroma_DB/chroma"
collection = initialize_and_process_collection(collectionname, persist_directory, text_chunks, doc_path, EMBED)
####################################################################################################################################
# Initialize conversation
conversation = []
####################################################################################################################################
# Stream response
def stream_response(query):
    # Generate the embeddings for the query
    queryembed = ollama.embed(model=EMBED, input=query)['embeddings']
    relevantdocs = collection.query(query_embeddings=queryembed, n_results=5)["documents"][0]
    docs = "\n\n".join(relevantdocs)

    # Create the system message and conversation context
    system_message = {'role': 'system', 'content': f"You are a helpful AI assistant. Here is a document: {docs}."}
    conversation_with_context = [system_message] + conversation + [{'role': 'user', 'content': query}]

    # Stream the response
    response = ''
    stream = ollama.chat(model=model, messages=conversation_with_context, stream=True, options={"num_ctx": 4096})
    print(f'\n{model}: \n')

    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(Fore.LIGHTWHITE_EX + content + Style.RESET_ALL, end='', flush=True)
    print('\n')

    # Update the conversation history
    conversation.append({'role': 'user', 'content': query})
    conversation.append({'role': 'assistant', 'content': response})
#####################################################################################################################################
# Start chat
while True:
    print(Fore.LIGHTCYAN_EX + '\nCHAT WITH DOCUMENTS! type exit to quit' + Style.RESET_ALL)
    query = input(f'{Fore.LIGHTGREEN_EX}\nUSER: \n')
    if not query:
        print('Ask a question. \n')
        continue

    if query.lower() == 'exit':
        break
    stream_response(query=query)
# ####################################################################################################################################
elapsed_time = time.time() - start_time
print(f"{Fore.CYAN}\nTotal runtime: {elapsed_time:.2f} seconds\n{Style.RESET_ALL}")