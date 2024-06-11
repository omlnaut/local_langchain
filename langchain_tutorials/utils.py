import os


def load_openai_key():
    with open("openai.key", "r") as f:
        os.environ["OPENAI_API_KEY"] = f.read().strip()
