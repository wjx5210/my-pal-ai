import { Link } from "react-router-dom";

import type { Source } from "../types";


function PalCardLink({ source }: { source: Source }) {
  return (
    <Link className="source-chip" to={`/pal/${encodeURIComponent(source.name)}`}>
      {source.name}
      {typeof source.score === "number" && (
        <small>{Math.round(source.score * 100)}%</small>
      )}
    </Link>
  );
}


export default PalCardLink;
