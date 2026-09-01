import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Link, useParams } from "react-router-dom";

import { api } from "../api";
import type { Pal } from "../types";


function PalDetail() {
  const { name } = useParams();
  const [pal, setPal] = useState<Pal | null>(null);
  const [error, setError] = useState("");
  const [summary, setSummary] = useState("");
  const [summaryLoading, setSummaryLoading] = useState(false);

  useEffect(() => {
    if (!name) return;
    api.get<Pal>(`/pal/${encodeURIComponent(name)}`)
      .then((response) => setPal(response.data))
      .catch(() => setError("没有找到这只帕鲁，或者后端服务暂时不可用。"));
  }, [name]);

  async function generateSummary() {
    if (!pal || summaryLoading) return;
    setSummaryLoading(true);
    try {
      const response = await api.post(`/pal/${encodeURIComponent(pal.name)}/summary`);
      setSummary(response.data.summary);
    } catch {
      setSummary("AI 总结暂时不可用，请稍后再试。");
    } finally {
      setSummaryLoading(false);
    }
  }

  if (error) {
    return <div className="detail-state"><p>{error}</p><Link to="/">返回图鉴</Link></div>;
  }
  if (!pal) return <div className="detail-state">正在载入帕鲁资料…</div>;

  return (
    <div className="detail-page">
      <header className="detail-nav">
        <Link to="/">← 返回帕鲁图鉴</Link>
        <span>帕洛斯野外调查手册</span>
      </header>

      <main className="detail-content">
        <section className="detail-hero">
          <div className="detail-emblem">{pal.element[0] === "火属性" ? "🔥" : pal.element[0] === "水属性" ? "💧" : pal.element[0] === "草属性" ? "🍃" : pal.element[0] === "雷属性" ? "⚡" : pal.element[0] === "冰属性" ? "❄" : "✦"}</div>
          <div>
            <span className="eyebrow">帕鲁档案</span>
            <h1>{pal.name}</h1>
            <div className="element-row large">
              {pal.element.map((item) => <span className="element-pill" key={item}>{item}</span>)}
              <span className="stage-pill">推荐：{pal.recommended_stage}</span>
            </div>
            <p>{pal.summary}</p>
          </div>
        </section>

        <div className="detail-grid">
          <section className="detail-card">
            <span className="eyebrow">基地记录</span><h2>工作适应性</h2>
            <div className="work-grid">
              {Object.entries(pal.work_suitability).map(([work, level]) => (
                <div key={work}><span>{work}</span><strong>Lv.{level}</strong></div>
              ))}
            </div>
          </section>

          <section className="detail-card">
            <span className="eyebrow">战斗记录</span><h2>战斗定位</h2>
            <p className="positioning">{pal.combat.positioning}</p>
            <div className="pros-cons">
              <div><h3>优势</h3>{pal.combat.strengths.map((item) => <p key={item}>＋ {item}</p>)}</div>
              <div><h3>弱点</h3>{pal.combat.weaknesses.map((item) => <p key={item}>－ {item}</p>)}</div>
            </div>
          </section>

          <section className="detail-card">
            <span className="eyebrow">野外记录</span><h2>地点与掉落</h2>
            <h3>出现地点</h3>{pal.locations.map((item) => <span className="data-tag" key={item}>{item}</span>)}
            <h3>掉落物</h3>{pal.drops.map((item) => <span className="data-tag" key={item}>{item}</span>)}
          </section>

          <section className="detail-card recommendation-card">
            <span className="eyebrow">调查员笔记</span><h2>培养建议</h2>
            <p>{pal.recommendation}</p>
            <blockquote>{pal.tips}</blockquote>
          </section>
        </div>

        <section className="ai-summary-card">
          <div>
            <span className="assistant-orb">析</span>
            <div><span className="eyebrow">资料分析</span><h2>生成一份培养摘要</h2><p>根据当前图鉴资料，整理培养和使用重点。</p></div>
          </div>
          {!summary && <button onClick={generateSummary} disabled={summaryLoading}>{summaryLoading ? "正在分析…" : "生成 AI 总结"}</button>}
          {summary && <div className="ai-summary-answer"><ReactMarkdown>{summary}</ReactMarkdown></div>}
        </section>
      </main>
    </div>
  );
}


export default PalDetail;
