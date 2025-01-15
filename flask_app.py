
"""
Write a python script which launches a server locally for an html file which has a big text box. When i enter text into that box and press submit, it should send that request to
the {ollama_model api}, take the resulting code, save it to a temporary file on the desktop,  then execute that file in a new python terminal.
A few more details:
. please add some extra prompting into the request to the api to specify that it should only return raw code without any formatting or markdown at all.
. you'll be executing on a Windows PC.


"""


# This script demonstrates how to use the Ollama API to generate Python code based on user instructions.
import json
import requests
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for the text box
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Generator</title>
</head>
<body>
    <h1>Enter your instructions below:</h1>
    <form action="/" method="post">
        <textarea name="code_input" rows="10" cols="80" placeholder="Enter your instructions here..."></textarea><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# Replace with the actual API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Replace with the actual API endpoint

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("code_input", "")
        if not user_input.strip():
            return "Please enter valid instructions.", 400
        
        # Prepare the request to the API
        api_payload = {
            "model": "llama3.1:8b", # Model name
            "prompt": f"Generate raw Python code based on this input:\n{user_input}\n"
                      f"Ensure the output is plain Python code without any formatting or markdown.",
        }
        
        try:
            # Call the API and collect the response chunks
            response = requests.post(OLLAMA_API_URL, json=api_payload, stream=True)
            response.raise_for_status()

            # Reconstruct the full code from the chunks
            full_code = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    try:
                        chunk_data = json.loads(chunk)  # Safely parse JSON
                        if "response" in chunk_data:
                            full_code += chunk_data["response"]
                    except json.JSONDecodeError:
                        return "Failed to decode API response. Please check the API output format.", 500
            

            # Save the reconstructed code to a temporary file
            temp_script_path = "E:\Test\Temp_script.py"  # Replace with the actual path
            with open(temp_script_path, "w", encoding="utf-8") as temp_script:
                # Clean the code to remove unwanted characters like backticks
                clean_code = full_code.strip("`").strip()
                temp_script.write(clean_code)
            
            # Execute the script in a new Python terminal
            subprocess.run(["python", temp_script_path], shell=True)
            
            return f"Code executed successfully. Check {temp_script_path} for 'temp_script.py'."
        
        except Exception as e:
            return f"An error occurred: {e}", 500

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True) # Run the Flask app in debug mode