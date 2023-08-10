from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load values from .env
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('openai_key')


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def translate():
    if request.method == "POST":
        source_language = request.form.get("source")
        target_language = request.form.get("target")
        code = request.form.get("code")

        #prompt = f"Translate this function from {source_language} into {target_language} ### {source_language} \n\n {code} \n\n ### {target_language}"
        prompt = f"Translate this code from {source_language} into {target_language} ### {source_language} \n\n {code} \n\n ### {target_language}  give me an explantion of the translation "
        messages = [{"role": "system", "content": "You are a intelligent assistant."}]
        # messages = []
        messages.append(
            {"role": "user", "content": prompt},
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )

        output = response.choices[0].message.content
        return render_template("translate.html", output=output)

if __name__ == '__main__':
    app.run(port=5001)
