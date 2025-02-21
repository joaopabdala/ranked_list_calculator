import os

def load_env(filepath="../.env"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo {filepath} não encontrado.")

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value

load_env()
