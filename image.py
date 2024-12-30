from ollama import chat
import argparse
import time
import sys_msgs
from colorama import init,Fore,Style
init(autoreset=True)

start_time = time.time()
def parse_args():
    parser = argparse.ArgumentParser(description='Run chat with command-line input.')
    parser.add_argument('--model', type=str, help="Model to use for answering the questions.", required=True)
    parser.add_argument('--img', type=str, help="Path to image", required=True)
    return parser.parse_args()

# Parse arguments
args = parse_args()
model = args.model
img = args.img
start_time = time.time()
#########################################################################################
#########################################################################################

conversation = [sys_msgs.system_message]

def stream_response(prompt):
    conversation.append({'role': 'user', 'content': f'Hello, my name is Fredrick: {prompt}','images': [img]})
    response = ''
    stream = chat(model=model, messages=conversation, stream=True, options={"num_ctx": 4096})
    print(f'\n{model}: ')

    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(content, end='', flush=True)
    print('\n')
    conversation.append({'role': 'assistant', 'content': response})
    elapsed_time = time.time() - start_time
    print(f"Total runtime: {elapsed_time:.2f} seconds")

#########################################################################################
#########################################################################################     

while True:
    print('Welcome to Ollama! Type "exit" to quit:')
    prompt = input('\nUSER:\n').strip()  # Removes leading/trailing spaces
    if not prompt:  # Check if the input is empty
        print("Input cannot be empty. Please type something.\n")
        continue  # Restart the loop
    if prompt.lower() == 'exit':
        break
    stream_response(prompt=prompt)




