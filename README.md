# AI MathTutor 智能数学辅导助手

AI MathTutor 是一个用于 AI 全栈工程师面试展示的教育场景 Demo。项目模拟数学辅导助手的核心流程：学生输入数学题，React 前端调用 FastAPI 后端接口，后端返回结构化解题结果，前端展示答案、解题步骤、知识点和易错点，并支持提交 Bad Case 反馈。

这个项目重点展示前后端联调、结构化 JSON 数据流、数学解题结果展示，以及 AI 教育产品中常见的反馈闭环。

## 项目背景

在 AI+教育场景中，数学辅导类产品通常需要把模型输出转成可解释、可展示、可评估的结构化内容，而不是只返回一段纯文本答案。

本 Demo 以一元一次方程为例，展示一个最小可运行的 AI 教育产品原型：

- 前端负责题目输入、请求发送、结果展示和 Bad Case 反馈
- 后端负责接收 JSON 请求、解析题目、生成结构化解题结果
- 反馈接口用于模拟后续 Prompt 优化、模型评测和质量改进流程

## 技术栈

- 前端：React + Vite
- 后端：Python + FastAPI
- 前后端通信：fetch + JSON
- 跨域处理：FastAPI CORSMiddleware
- 数学处理：正则解析 + Python Fraction 分数化简
- 前端地址：http://localhost:5173
- 后端地址：http://127.0.0.1:8000

## 核心功能

- 输入数学题并生成解题步骤
- 支持简单一元一次方程 `ax + b = c`
- 返回结构化结果：`answer`、`steps`、`knowledge_points`、`common_mistakes`
- 前端用卡片展示题目、答案、步骤、知识点和易错点
- 自定义列表行结构展示编号和圆点，避免默认列表缩进过大
- 支持提交 Bad Case 反馈
- 后端保存历史提问记录和反馈记录

## 项目结构

```text
ai-mathtutor-demo/
├── backend/
│   ├── main.py
│   └── .venv/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
└── README.md
```

## 后端接口说明

### GET `/`

健康检查接口，用于确认后端是否正常运行。

返回示例：

```json
{
  "message": "AI MathTutor backend is running"
}
```

### POST `/api/solve`

提交数学题，返回结构化解题结果。

请求示例：

```json
{
  "question": "2x+3=11",
  "grade": "初中",
  "mode": "详细讲解"
}
```

返回示例：

```json
{
  "question": "2x+3=11",
  "answer": "x = 4",
  "steps": [
    "第一步：识别题型，这是形如 ax + b = c 的一元一次方程。",
    "第二步：原方程可理解为 2x + (3) = 11。",
    "第三步：两边同时减去 3，得到 2x = 11 - (3) = 8。",
    "第四步：两边同时除以 2，得到 x = 8/2 = 4。"
  ],
  "knowledge_points": ["一元一次方程", "等式性质", "移项", "分数化简"],
  "common_mistakes": [
    "移项时忘记变号",
    "等式两边没有同时进行相同操作",
    "分数结果没有化简",
    "只写答案，没有写推理过程"
  ],
  "created_at": "2026-06-12 21:39:17"
}
```

当前支持示例：

- 输入 `2x+3=11`，返回 `x = 4`
- 输入 `6x+10=50`，返回 `x = 20/3`
- 输入 `3x-5=10`，返回 `x = 5`

如果输入不符合当前支持格式，后端会返回“暂时只支持形如 ax + b = c 的一元一次方程”的提示。

### GET `/api/history`

获取历史提问记录。

返回格式：

```json
{
  "history": []
}
```

### POST `/api/feedback`

提交 Bad Case 反馈。

请求示例：

```json
{
  "question": "2x+3=11",
  "answer": "x = 4",
  "reason": "步骤不够详细"
}
```

返回示例：

```json
{
  "message": "Bad Case 反馈已记录",
  "feedback": {
    "question": "2x+3=11",
    "answer": "x = 4",
    "reason": "步骤不够详细",
    "created_at": "2026-06-12 21:40:00"
  }
}
```

## 本地运行方法

### 1. 启动后端

```bash
cd ~/Desktop/ai-mathtutor-demo/backend
source .venv/bin/activate
python -m uvicorn main:app --reload
```

后端默认运行在：

```text
http://127.0.0.1:8000
```

### 2. 启动前端

```bash
cd ~/Desktop/ai-mathtutor-demo/frontend
npm install
npm run dev
```

前端默认运行在：

```text
http://localhost:5173
```

### 3. 页面联调测试

打开前端页面后，输入：

```text
2x+3=11
```

预期答案：

```text
x = 4
```

再输入：

```text
6x+10=50
```

预期答案：

```text
x = 20/3
```

## 前后端数据流

```text
用户输入数学题
    ↓
React 使用 fetch 请求 /api/solve
    ↓
FastAPI 接收 question、grade、mode
    ↓
后端解析一元一次方程并生成结构化 JSON
    ↓
React 渲染答案、解题步骤、知识点、易错点
    ↓
用户可通过 /api/feedback 提交 Bad Case
```

## 面试介绍话术

我做了一个 AI MathTutor Demo，用 React 作为前端，FastAPI 作为后端。前端页面包含题目输入框、生成按钮、答案展示区和 Bad Case 反馈输入框。用户输入数学题后，React 通过 fetch 向 FastAPI 的 `/api/solve` 接口发送 POST 请求。后端接收 `question`、`grade`、`mode` 参数，然后返回结构化 JSON，包括 `answer`、`steps`、`knowledge_points` 和 `common_mistakes`。前端拿到 JSON 后，把解题结果渲染到页面上。用户如果觉得答案有问题，也可以通过 `/api/feedback` 提交 Bad Case，后续可以用于 Prompt 优化和模型质量改进。

这个 Demo 虽然没有接入真实大模型，但保留了 AI 教育产品的核心工程结构：输入问题、后端处理、结构化输出、前端展示和反馈闭环。后续可以把当前规则解析模块替换成大模型 API 或符号计算引擎。

## 后续优化方向

- 接入真实大模型 API，支持更复杂的数学题和自然语言应用题
- 引入 SymPy 等符号计算库，提高数学解析能力
- 增加年级、难度、讲解风格等可配置参数
- 将历史记录和 Bad Case 反馈保存到数据库
- 增加反馈类型统计和 Bad Case 管理页面
- 增加接口错误处理、空状态和更完整的加载状态
- 增加后端单元测试和前端端到端测试
