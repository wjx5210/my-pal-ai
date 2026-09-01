import { useEffect, useMemo, useState } from "react";

import { api } from "../api";
import ChatBox from "../components/ChatBox";
import PalCard from "../components/PalCard";
import type { ChatMessage, Pal } from "../types";


type Props = {
  messages: ChatMessage[];
  setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  sessionId: string | null;
  setSessionId: (value: string | null) => void;
};


const elements = ["全部", "无属性", "火属性", "水属性", "草属性", "雷属性", "冰属性", "地属性", "暗属性", "龙属性"];


function Home(props: Props) {
  const [pals, setPals] = useState<Pal[]>([]);
  const [search, setSearch] = useState("");
  const [element, setElement] = useState("全部");
  const [work, setWork] = useState("全部");
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    api.get<Pal[]>("/pals")
      .then((response) => setPals(response.data))
      .catch(() => setLoadError("无法加载图鉴，请确认 FastAPI 服务已启动。"))
      .finally(() => setLoading(false));
  }, []);

  const workTypes = useMemo(
    () => ["全部", ...Array.from(new Set(pals.flatMap((pal) => Object.keys(pal.work_suitability))))],
    [pals],
  );

  const filteredPals = useMemo(() => {
    const keyword = search.trim().toLowerCase();
    return pals.filter((pal) => {
      const matchesSearch = !keyword || pal.name.toLowerCase().includes(keyword) || pal.summary.toLowerCase().includes(keyword);
      const matchesElement = element === "全部" || pal.element.includes(element);
      const matchesWork = work === "全部" || work in pal.work_suitability;
      return matchesSearch && matchesElement && matchesWork;
    });
  }, [element, pals, search, work]);

  return (
    <div className="site-shell">
      <header className="site-header">
        <a className="brand" href="#top" aria-label="我的帕鲁首页">
          <span className="brand-mark">帕</span>
          <span><strong>我的帕鲁</strong><small>野外调查手册</small></span>
        </a>
        <nav>
          <a href="#paldex">帕鲁图鉴</a>
          <a href="#assistant">AI 问答</a>
        </nav>
        <span className="knowledge-status"><i />资料库已载入 · {pals.length || 100} 条</span>
      </header>

      <main id="top">
        <section className="hero-section">
          <div className="hero-copy">
            <span className="eyebrow">帕洛斯群岛 · 调查记录 001</span>
            <h1>查图鉴，配队伍，<br /><em>少走一点弯路。</em></h1>
            <p>按属性和工作能力筛选帕鲁，或者把具体问题交给攻略助手。资料来自本地图鉴，回答会附上参考对象。</p>
            <div className="hero-actions">
              <a className="primary-link" href="#paldex">开始查图鉴</a>
              <a className="secondary-link" href="#assistant">直接提问</a>
            </div>
            <div className="hero-stats">
              <div><strong>{pals.length || 100}</strong><span>图鉴记录</span></div>
              <div><strong>9</strong><span>属性分类</span></div>
              <div><strong>12</strong><span>工作类型</span></div>
            </div>
          </div>
          <div id="assistant" className="hero-chat">
            <ChatBox {...props} />
          </div>
        </section>

        <section className="paldex-section" id="paldex">
          <div className="section-heading">
            <div>
              <span className="eyebrow">调查目录</span>
              <h2>帕鲁图鉴</h2>
              <p>搜索名称，或按照属性与基地工作快速缩小范围。</p>
            </div>
            <strong>当前显示 {filteredPals.length} / {pals.length}</strong>
          </div>

          <div className="filter-panel">
            <label className="search-box">
              <span>⌕</span>
              <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="搜索帕鲁名称或简介…" />
            </label>

            <div className="filter-group">
              <span>属性</span>
              <div className="filter-chips">
                {elements.map((item) => (
                  <button className={element === item ? "active" : ""} onClick={() => setElement(item)} key={item}>{item.replace("属性", "")}</button>
                ))}
              </div>
            </div>

            <div className="filter-group">
              <span>工作</span>
              <div className="filter-chips compact">
                {workTypes.map((item) => (
                  <button className={work === item ? "active" : ""} onClick={() => setWork(item)} key={item}>{item}</button>
                ))}
              </div>
            </div>
          </div>

          {loading ? (
            <div className="state-panel">正在载入帕鲁图鉴…</div>
          ) : loadError ? (
            <div className="state-panel error">{loadError}</div>
          ) : filteredPals.length ? (
            <div className="paldex-grid">
              {filteredPals.map((pal) => (
                <PalCard pal={pal} index={pals.indexOf(pal)} key={pal.name} />
              ))}
            </div>
          ) : (
            <div className="state-panel">没有符合当前筛选条件的帕鲁。</div>
          )}
        </section>
      </main>

      <footer>
        <span>我的帕鲁 · 非官方调查手册</span>
        <span className="footer-meta">
          <span>资料来自本地知识库，AI 回答仅供参考</span>
          <a href="https://beian.miit.gov.cn/" target="_blank" rel="noreferrer">
            皖ICP备2026027122号
          </a>
          <a
            className="public-security-record"
            href="https://beian.mps.gov.cn/#/query/webSearch?code=34130202000906"
            target="_blank"
            rel="noreferrer"
          >
            <img src="/beian-icon.png" alt="公安备案图标" />
            <span>皖公网安备34130202000906号</span>
          </a>
        </span>
      </footer>
    </div>
  );
}


export default Home;
