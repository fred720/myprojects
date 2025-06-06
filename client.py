
from ollama import chat
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Run chat with command-line input.')
    parser.add_argument('--model', type=str, help="Model to use for answering the questions.", required=True)
    
    return parser.parse_args()

arg = parse_args()
llm = arg.model

import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = llm
def generate(prompt, context):
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': model,
                          'prompt': prompt,
                          'context': context,
                      },
                      stream=True)
    r.raise_for_status()

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        # the response streams one token at a time, print that as we receive it
        print(response_part, end='', flush=True)

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return body['context']

def main():
    context = [] # the context stores a conversation history, you can use this to make the model more context aware
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        if user_input.strip() == "":
            continue
        print()
        context = generate(user_input, context)
        print()

if __name__ == "__main__":
    main()