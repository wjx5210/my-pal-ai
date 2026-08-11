import { Link } from "react-router-dom";

import type { Pal } from "../types";


const elementIcon: Record<string, string> = {
  无属性: "✦",
  火属性: "🔥",
  水属性: "💧",
  草属性: "🍃",
  雷属性: "⚡",
  冰属性: "❄",
  地属性: "◆",
  暗属性: "☾",
  龙属性: "◇",
};


type Props = {
  pal: Pal;
  index: number;
};


function PalCard({ pal, index }: Props) {
  const primaryElement = pal.element[0] ?? "无属性";

  return (
    <Link to={`/pal/${encodeURIComponent(pal.name)}`} className="paldex-card-link">
      <article className="paldex-card" data-element={primaryElement}>
        <div className="paldex-card-topline">
          <span className="paldex-number">#{String(index + 1).padStart(3, "0")}</span>
          <span className="stage-pill">{pal.recommended_stage}</span>
        </div>

        <div className="pal-emblem" aria-hidden="true">
          <span>{elementIcon[primaryElement] ?? "✦"}</span>
        </div>

        <div className="paldex-card-body">
          <h3>{pal.name}</h3>
          <div className="element-row">
            {pal.element.map((element) => (
              <span className="element-pill" key={element}>
                {elementIcon[element]} {element.replace("属性", "")}
              </span>
            ))}
          </div>
          <p>{pal.summary}</p>
          <div className="work-preview">
            {Object.entries(pal.work_suitability)
              .slice(0, 3)
              .map(([work, level]) => (
                <span key={work}>{work} Lv.{level}</span>
              ))}
          </div>
        </div>
      </article>
    </Link>
  );
}


export default PalCard;
