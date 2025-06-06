# 구구단 MCP Mock 프로젝트

이 프로젝트는 **MCP 구조**를 실습하기 위한 예제로, Python(FastAPI)와 Node.js(Express)로 각각 구현된 구구단 서버와, LLM(대형언어모델) 연동 클라이언트를 포함합니다.

학생, 개발자, 사용자 모두가 쉽게 따라할 수 있도록 전체 폴더 구조, 소스 설명, 동작 원리, 실습 방법, API 예시, 학습 포인트를 정리했습니다.

로컬에 LM Studio를 설치하여 실행하고, llmstudio_client.py를 참고하여 LLM에 질문을 보내는 코드를 작성해보세요.

---

## 1. 전체 폴더/파일 구조

```
backend/
├── app/
│   ├── mcp_gugudan_server.py   # Python 구구단 MCP 서버 (FastAPI)
│   ├── client.py               # MCP 서버/LLM 스마트 라우팅 클라이언트
│   ├── lmstudio_client.py      # LM Studio(로컬 LLM) 연동 모듈
│   └── __init__.py
├── js_mcp_gugudan_server/
│   ├── server.js               # Node.js 구구단 MCP 서버 (Express)
│   ├── package.json            # Node.js 의존성
│   └── README.md               # JS 서버 실행법
├── requirements.txt            # Python 의존성
├── .gitignore                  # 불필요 파일 제외
├── .python-version             # Python 버전 지정
└── README.md                   # (최상위) 전체 프로젝트 설명
```

---

## 2. 소스 설명 및 아키텍처 흐름

### (1) Python MCP 구구단 서버

- **mcp_gugudan_server.py**
  - `/mcp/gugudan` 엔드포인트로 1~9단 구구단을 계산해 반환
  - 예: { "query": "3단 알려줘" } → 3단 결과 반환

### (2) Node.js MCP 구구단 서버

- **server.js**
  - Python 서버와 동일하게 POST `/mcp/gugudan` 제공
  - Express 기반, API 응답 형식도 동일

### (3) 스마트 클라이언트

- **client.py**
  - 질문이 구구단이면 MCP 서버에 먼저 요청, 아니면 LLM(LM Studio)로 자동 fallback
  - 예: "9단 알려줘" → MCP 서버, "대한민국 인구는?" → LLM
- **lmstudio_client.py**
  - LM Studio API와 통신(로컬 LLM 답변)
  - LM Studio는 PC에서 직접 실행하는 무료 LLM 서버로, OpenAI 호환 REST API를 제공합니다.
  - 본 프로젝트는 LM Studio를 로컬에서 띄워(`http://localhost:1234/v1/chat/completions` 등) LLM 응답을 받도록 설계되어 있습니다.

### (4) 기타

- **requirements.txt / package.json** : 각 언어별 의존성
- **.gitignore** : Python, Node.js, 에디터, OS 임시파일 모두 포함

#### 아키텍처 흐름도

```
[사용자 질문]
    ↓
[client.py]
  ├─(구구단 관련)─→ [MCP 서버(Python/JS)]
  └─(기타 질문)───→ [LLM(LM Studio)]
```

---

## 3. 동작 및 실습 방법 (Step by Step)

### (A) Python MCP 구구단 서버 실습

1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 서버 실행
   ```bash
   python -m app.mcp_gugudan_server
   # 또는
   uv run python -m app.mcp_gugudan_server
   ```
3. 클라이언트 실행
   ```bash
   python -m app.client
   ```

### (B) Node.js MCP 구구단 서버 실습

1. 디렉터리 이동 및 의존성 설치
   ```bash
   cd js_mcp_gugudan_server
   npm install
   ```
2. 서버 실행
   ```bash
   npm start
   ```

### (C) API 직접 테스트

```bash
curl -X POST http://localhost:8000/mcp/gugudan -H "Content-Type: application/json" -d '{"query": "3단 알려줘"}'
```

### (D) client.py로 기능 테스트하기

#### 1. client.py 실행

```bash
python -m app.client
   # 또는
uv run python -m app.client
```

#### 2. 동작 예시 (출력)

```
질문: 3단 알려줘
[MCP 서버 응답]
3 x 1 = 3
3 x 2 = 6
...
3 x 9 = 27

질문: 대한민국의 인구는 얼마야?
 -> 질문내용운 제공하는 MCP서버와 관련 없음. LLM으로 답변하겠습니다.
[LLM 직접 응답]
2023년 12월 31일 기준으로, 대한민국의 인구는 약 51,814,000명입니다.

질문: 80단 알려줘
 -> 질문내용운 제공하는 MCP서버와 관련 없음. LLM으로 답변하겠습니다.
[LLM 직접 응답]
80 x 1 = 80
80 x 2 = 160
...
80 x 9 = 720
```

- MCP 서버가 처리 가능한 구구단(1~9단) 질문은 직접 계산해서 반환합니다.
- 그 외의 질문(상식, 80단 등)은 LLM(LM Studio)로 자동 fallback되어 답변합니다.
- client.py를 통해 실제 라우팅/응답 동작을 쉽게 테스트할 수 있습니다.

---

## 4. 학습 포인트 & 실전 팁

- **MCP 구조** : 여러 처리 컴포넌트(서버/LLM)를 상황에 따라 스마트하게 라우팅하는 방법 실습
- **API 설계** : Python/Node.js 두 언어에서 동일한 REST API 설계 실습
- **에러 핸들링** : 잘못된 요청(예: "80단 알려줘")시 graceful하게 에러 반환
- **확장성** : 구구단 이외의 수학 연산, 기타 AI 기능도 동일 구조로 쉽게 확장 가능
- **실전 연동** : curl, 클라이언트 코드 등 실제 API 활용법까지 포함

---

## 5. 참고/추가 자료

- `.gitignore`는 Python/Node.js/에디터/OS 임시파일을 모두 포함
- LM Studio(Llama3 등) API 연동 예제는 `app/lmstudio_client.py` 참고
- Node.js 버전은 `js_mcp_gugudan_server/README.md` 참고

---

## [부록] LLM(LM Studio) 구성 및 활용 안내

### LM Studio란?

- **LM Studio**는 PC에서 직접 실행할 수 있는 무료 LLM(대형언어모델) 서버입니다.
- OpenAI API와 호환되는 REST API(`http://localhost:1234/v1/chat/completions` 등)를 제공합니다.
- GPT-3, Llama3 등 다양한 모델을 다운로드하여 로컬에서 프라이빗하게 사용할 수 있습니다.

### 본 프로젝트에서의 활용

- `app/lmstudio_client.py`에서 LM Studio API로 질문을 보내고, LLM이 답변을 생성합니다.
- 클라이언트(client.py)는 구구단 등 MCP 서버가 처리하지 못하는 질문을 자동으로 LM Studio로 라우팅합니다.
- LM Studio는 반드시 PC에서 실행 중이어야 하며, 기본 포트는 1234입니다.

### LM Studio 설정 예시

1. [LM Studio 공식 사이트](https://lmstudio.ai/)에서 다운로드 및 설치
2. LM Studio 실행 후, 원하는 모델(예: Llama3) 선택 및 다운로드
3. "OpenAI Compatible API" 기능 활성화 (설정에서 토글)
4. 서버가 켜지면 `http://localhost:1234/v1/chat/completions` 주소로 API 요청 가능

### 예시 코드 (app/lmstudio_client.py)

```python
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
# ... 이하 생략 ...
```

---

이 자료는 MCP 구조와 서버-클라이언트-LLM 연동을 처음 배우는 학생/개발자/사용자 모두에게 실전적으로 도움이 되도록 작성되었습니다. 궁금한 점이나 확장 아이디어가 있으면 언제든 질문하세요!
