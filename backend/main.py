from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import re
from fractions import Fraction

app = FastAPI(title="AI MathTutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

history = []
feedback_list = []


class SolveRequest(BaseModel):
    question: str
    grade: str = "初中"
    mode: str = "详细讲解"


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    reason: str


def solve_linear_equation(question: str):
    """
    支持类似：
    2x + 3 = 11
    6x + 10 = 50
    3x - 5 = 10
    """
    text = question.replace(" ", "")
    text = text.replace("解方程", "")
    text = text.replace("：", "")
    text = text.replace(":", "")

    pattern = r"^([+-]?\d*)x([+-]\d+)?=([+-]?\d+)$"
    match = re.match(pattern, text)

    if not match:
        return {
            "answer": "暂时只支持形如 ax + b = c 的一元一次方程",
            "steps": [
                "第一步：系统尝试识别题型。",
                "第二步：当前 Demo 只支持 ax + b = c 形式。",
                "第三步：如果是更复杂题目，后续可以接入大模型 API 或符号计算库处理。"
            ],
            "knowledge_points": ["一元一次方程", "表达式解析", "AI 教育 Demo"],
            "common_mistakes": ["输入格式过于复杂", "题目中缺少等号", "暂未接入真实大模型"]
        }

    a_str, b_str, c_str = match.groups()

    if a_str in ["", "+"]:
        a = 1
    elif a_str == "-":
        a = -1
    else:
        a = int(a_str)

    b = int(b_str) if b_str else 0
    c = int(c_str)

    numerator = c - b
    x = Fraction(numerator, a)

    if x.denominator == 1:
        answer = f"x = {x.numerator}"
        x_display = str(x.numerator)
    else:
        answer = f"x = {x.numerator}/{x.denominator}"
        x_display = f"{x.numerator}/{x.denominator}"

    steps = [
        f"第一步：识别题型，这是形如 ax + b = c 的一元一次方程。",
        f"第二步：原方程可理解为 {a}x + ({b}) = {c}。",
        f"第三步：两边同时减去 {b}，得到 {a}x = {c} - ({b}) = {numerator}。",
        f"第四步：两边同时除以 {a}，得到 x = {numerator}/{a} = {x_display}。"
    ]

    return {
        "answer": answer,
        "steps": steps,
        "knowledge_points": ["一元一次方程", "等式性质", "移项", "分数化简"],
        "common_mistakes": [
            "移项时忘记变号",
            "等式两边没有同时进行相同操作",
            "分数结果没有化简",
            "只写答案，没有写推理过程"
        ]
    }


@app.get("/")
def health_check():
    return {"message": "AI MathTutor backend is running"}


@app.post("/api/solve")
def solve_math(req: SolveRequest):
    solve_result = solve_linear_equation(req.question)

    result = {
        "question": req.question,
        "answer": solve_result["answer"],
        "steps": solve_result["steps"],
        "knowledge_points": solve_result["knowledge_points"],
        "common_mistakes": solve_result["common_mistakes"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(result)
    return result


@app.get("/api/history")
def get_history():
    return {"history": history}


@app.post("/api/feedback")
def submit_feedback(req: FeedbackRequest):
    feedback = {
        "question": req.question,
        "answer": req.answer,
        "reason": req.reason,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    feedback_list.append(feedback)

    return {
        "message": "Bad Case 反馈已记录",
        "feedback": feedback
    }
