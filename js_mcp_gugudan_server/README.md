# JS MCP Gugudan Server

Node.js/Express 기반의 구구단 MCP 서버입니다.

## 실행 방법

1. 의존성 설치

```bash
npm install
```

2. 서버 실행

```bash
npm start
```

3. 테스트 예시

```bash
curl -X POST http://localhost:8000/mcp/gugudan -H "Content-Type: application/json" -d '{"query": "3단 알려줘"}'
```
