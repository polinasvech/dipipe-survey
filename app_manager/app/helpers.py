import json
import random
from typing import Dict


def load_json(filename: str) -> Dict:
    try:
        with open(f"data/{filename}", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")


def colors3():
    return ["#fbfbfa", "#828583", "#e7d49b"]

def colors10():
    return ["#e8a675", "#ec6608", "#887b73", "#ffc000", "#adadad"]

def generate_random_hex_color():
    hex_chars = "0123456789ABCDEF"
    hex_color = "#"
    for _ in range(6):
        hex_color += random.choice(hex_chars)
    return hex_color
