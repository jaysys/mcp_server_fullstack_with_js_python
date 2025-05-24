// js_mcp_gugudan_server/server.js
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

function extractNumberFromQuery(query) {
  const match = query.match(/([1-9])\s*단/);
  if (match) {
    return parseInt(match[1], 10);
  }
  throw new Error('1~9 사이의 단을 찾을 수 없습니다.');
}

function calculateGugudan(n) {
  console.log(`[JS MCP 구구단 서버] 계산 실행: ${n}단`);
  let result = [];
  for (let i = 1; i <= 9; i++) {
    result.push(`${n} x ${i} = ${n * i}`);
  }
  return result.join('\n');
}

app.post('/mcp/gugudan', (req, res) => {
  try {
    const { query } = req.body;
    const number = extractNumberFromQuery(query);
    const result = calculateGugudan(number);
    res.json({
      task: 'gugudan',
      number,
      result
    });
  } catch (error) {
    res.status(400).json({ detail: error.message });
  }
});

const PORT = 8000;
app.listen(PORT, () => {
  console.log(`JS MCP Gugudan Server listening on port ${PORT}`);
});
