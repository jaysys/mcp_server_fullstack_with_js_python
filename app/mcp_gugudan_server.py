from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class MCPRequest(BaseModel):
    query: str  # 예: "3단 알려줘", "5단 계산해줘"

def extract_number_from_query(query: str) -> int:
    match = re.search(r'([1-9])\s*단', query)
    if match:
        return int(match.group(1))
    raise ValueError("1~9 사이의 단을 찾을 수 없습니다.")

def calculate_gugudan(n: int) -> str:
    print(f"[Python MCP 구구단 서버!]계산 실행: {n}단")
    return "\n".join([f"{n} x {i} = {n*i}" for i in range(1, 10)])

@app.post("/mcp/gugudan")
def handle_mcp_gugudan(req: MCPRequest):
    try:
        number = extract_number_from_query(req.query)
        result = calculate_gugudan(number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "task": "gugudan",
        "number": number,
        "result": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.mcp_gugudan_server:app", host="0.0.0.0", port=8000, reload=True)
