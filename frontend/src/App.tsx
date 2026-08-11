import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";


import Home from "./pages/Home";
import PalDetail from "./pages/PalDetail";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
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