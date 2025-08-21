from app.lmstudio_client import ask_llm_general_question
import requests

def try_mcp_server(query: str):
    # MCP 구구단 서버(gugudan 기능 담당) 엔드포인트
    url = "http://localhost:8000/mcp/gugudan"
    try:
        response = requests.post(url, json={"query": query}, timeout=3)
        response.raise_for_status()
        return response.json()["result"]
    except requests.RequestException:
        return None

def smart_query(query: str):
    mcp_result = try_mcp_server(query)
    if mcp_result is not None:
        return f" -> MCP 서버가 응답합니다\n{mcp_result}"
    else:
        print(" -> 질의하신 내용은 MCP기능과 관련이 없는것 같습니다. 오픈소스 LLM이 답변드리겠습니다.")
    return f"{ask_llm_general_question(query)}"

if __name__ == "__main__":
    questions = ["9단 알려줘", 
                "대한민국의 인구는 얼마야?",
                "80단 알려줘봐"]
    for q in questions:
        print(f"\nQuestion💬 '{q}'")
        print(smart_query(q))
        
