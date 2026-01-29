import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY environment variable")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openai/gpt-oss-20b:free"
CSV_PATH = "students.csv"

SYSTEM_PROMPT = (
    "You are a data analysis agent.\n"
    "The user is inside a student performance CSV dataset.\n"
    "Choose the correct tool based on the question.\n"
    "After tool execution, explain the result in Markdown.\n"
    "Never output raw JSON."
)

