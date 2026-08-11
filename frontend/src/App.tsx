import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import { useState } from "react";


import Home from "./pages/Home";
import PalDetail from "./pages/PalDetail";

function App() {

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [sources, setSources] = useState([]);

  const [loading, setLoading] = useState(false);

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={
            <Home
              question={question}
              setQuestion={setQuestion}
              answer={answer}
              setAnswer={setAnswer}
              sources={sources}
              setSources={setSources}
              loading={loading}
              setLoading={setLoading}
            />
          }
        />

        <Route
          path="/pal/:name"
          element={<PalDetail />}
        />


      </Routes>

    </BrowserRouter>

  )

}


export default App;