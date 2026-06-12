import { useState } from "react";
import "./App.css";

function ListBlock({ items = [], type = "number" }) {
  return (
    <div className="list-block">
      {items.map((item, index) => (
        <div className="list-row" key={`${type}-${index}`}>
          <span className="list-index">
            {type === "number" ? `${index + 1}.` : "•"}
          </span>
          <span className="list-text">{item}</span>
        </div>
      ))}
    </div>
  );
}

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [feedbackReason, setFeedbackReason] = useState("");

  async function handleSolve() {
    if (!question.trim()) {
      alert("请输入数学题");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/solve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question: question,
          grade: "初中",
          mode: "详细讲解"
        })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("请求后端失败，请检查 FastAPI 是否正在运行");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function handleFeedback() {
    if (!result) {
      alert("请先生成答案");
      return;
    }

    await fetch("http://127.0.0.1:8000/api/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: result.question,
        answer: result.answer,
        reason: feedbackReason || "答案不够准确"
      })
    });

    alert("Bad Case 已记录");
    setFeedbackReason("");
  }

  return (
    <main className="page">
      <section className="intro">
        <h1>AI MathTutor 智能数学辅导助手</h1>
        <p>
          这是一个 React + FastAPI 的 AI 教育 Demo，用于模拟学生输入数学题后，
          系统返回答案、解题步骤、知识点和易错点。
        </p>
      </section>

      <section className="card input-card">
        <label className="field-label" htmlFor="question">
          数学题
        </label>
        <textarea
          id="question"
          rows="5"
          placeholder="请输入一道数学题，例如：解方程 2x + 3 = 11"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button className="primary-button" onClick={handleSolve} disabled={loading}>
          {loading ? "生成中..." : "生成解题步骤"}
        </button>
      </section>

      {result && (
        <section className="card result-card">
          <h2>解答结果</h2>

          <div className="result-summary">
            <p>
              <strong>题目：</strong>
              {result.question}
            </p>
            <p>
              <strong>答案：</strong>
              <span className="answer-text">{result.answer}</span>
            </p>
          </div>

          <div className="result-section">
            <h3>解题步骤</h3>
            <ListBlock items={result.steps} type="number" />
          </div>

          <div className="result-section">
            <h3>知识点</h3>
            <ListBlock items={result.knowledge_points} type="bullet" />
          </div>

          <div className="result-section">
            <h3>易错点</h3>
            <ListBlock items={result.common_mistakes} type="bullet" />
          </div>

          <div className="feedback-box">
            <h3>Bad Case 反馈</h3>
            <input
              placeholder="例如：步骤不够详细 / 答案错误 / 知识点不准确"
              value={feedbackReason}
              onChange={(e) => setFeedbackReason(e.target.value)}
            />

            <button className="secondary-button" onClick={handleFeedback}>
              答案有问题，提交反馈
            </button>
          </div>
        </section>
      )}
    </main>
  );
}

export default App;
