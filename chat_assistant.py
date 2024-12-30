import ollama
import sys_msgs
import chromadb
from colorama import Fore

MODEL = 'phi3:latest'

client = chromadb.PersistentClient(path="E:/Chroma_DB/chroma_collections")

message_history = sys_msgs.message_history
###########################################################################################################
convo = [sys_msgs.system_message_2]
###########################################################################################################
def stream_response(prompt):
    convo.append({'role':'user','content': prompt})
    response = ''
    stream = ollama.chat(model=MODEL,messages=convo, stream=True)
    print(f'\n{MODEL}: \n')

    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(Fore.LIGHTWHITE_EX + content, end='',flush=True)

    print('\n')
    convo.append({'role':'assistant','content': response})
############################################################################
def create_vectordb(conversations):
    vectordb_name = 'conversations'

    try:
        client.delete_collection(name=vectordb_name)
    except ValueError:
        pass

    vectordb = client.create_collection(name=vectordb_name)

    for c in conversations:
        serialized_convo = f'prompt: {c['prompt']} response:{c['response']}'
        response = ollama.embeddings(model='nomic-embed-text:latest',prompt=serialized_convo)
        embedding = response['embedding']

        vectordb.add(ids=[str(c['id'])],
                     embeddings=[embedding],
                     documents=[serialized_convo])
############################################################################        
def retrieve_embeddings(prompt):
    response =  ollama.embeddings(model='nomic-embed-text:latest', prompt=prompt)
    prompt_embedding = response['embedding']

    vectordb = client.get_collection(name='conversations')
    results = vectordb.query(query_embeddings=[prompt_embedding],n_results=1)
    best_embedding = results['documents'][0][0]

    return best_embedding
############################################################################
create_vectordb(conversations=message_history)
############################################################################
while True:
    prompt = input(Fore.LIGHTGREEN_EX + 'USER: \n')
    if prompt.lower() == 'exit':
        break
    context = retrieve_embeddings(prompt=prompt)
    prompt =  f'USER PROMPT: {prompt} \nCONTEXT FROM EMBEDDINGS: {context}'
    stream_response(prompt=prompt)
############################################################################