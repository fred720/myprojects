import ollama



embedding = ollama.embeddings(model='nomic-embed-text:latest',prompt='why is the sky blue?')
embedding1 = ollama.embed(model='nomic-embed-text:latest',input='why is the sky blue?')
embedding = ollama.embeddings(model='nomic-embed-text:latest',prompt='why is the sky blue?')['embedding']
embedding1 = ollama.embed(model='nomic-embed-text:latest',input='why is the sky blue?')['embeddings']
print(f"ollama.embedding: {embedding} \n")
print(f"ollama.embed: {embedding1} \n")



