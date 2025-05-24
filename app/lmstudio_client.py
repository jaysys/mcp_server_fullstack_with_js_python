import requests

LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

def ask_llm_general_question(question: str = "대한민국의 수도는 무엇이야?") -> str:
    response = requests.post(LMSTUDIO_API_URL, json={
        "model": "llama3",  # LM Studio에서 선택한 모델 이름
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.2,
        "max_tokens": 200
    })
    if response.status_code != 200:
        raise RuntimeError(f"LLM 요청 실패: {response.text}")
        
    return response.json()["choices"][0]["message"]["content"].strip()

