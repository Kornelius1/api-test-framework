import json 
import os
import requests
from dotenv import load_dotenv

load_dotenv

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

def _generate(prompt: str)-> str:
    """Kirim prompt ke ollama, return teks hasil"""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except Exception as e:
        return  None

def generate_payload(field_name: str, hint: str = "") -> str:
    """
    Minta AI menghasilkan nilai untuk field tertentu.
    contoh:  field_name="email" -> "user_123456@test.com"
    """
    prompt = (
        f"Generate one realistic value for field '{field_name}' "
        f"for API testing. {hint} Return only the value, no extra text."
    )
    result = _generate(prompt)
    if result:
        return result

    import time
    if "email" in field_name.lower():
        return f"test_{int(time.time())}@example.com"
    if "name" in field_name.lower():
        return f"TestName_{int(time.time())}"
    if "description" in field_name.lower():
        return "Automated test description"
    if "password" in field_name.lower():
        return "Password123!"
    if "slug" in field_name.lower():
        return f"test-business-{int(time.time())}"
    if "phone" in field_name.lower():
        return "08123456789"
    return f"value_{int(time.time())}"


def explain_failure(request_data: dict, response_data: dict, expected: dict) -> str:
    """
    Kirim request/response/expected ke AI, return 1-2 kalimat penjelasan.
    """
    prompt = (
        f"API test failed. Request: {json.dumps(request_data)}. "
        f"Response: {json.dumps(response_data)}. Expected: {json.dumps(expected)}. "
        "Explain the most likely cause in one sentence (Indonesian or English)."
    )
    result = _generate(prompt)
    return result if result else "No detailed explanation (AI unavailable)."