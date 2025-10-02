import { Routes, Route, Navigate } from "react-router-dom";
import { useAuthContext } from "./context/AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import TambosList from "./pages/Tambos/TambosList";
import TamboDetail from "./pages/Tambos/TamboDetail";
import ComederoDetail from "./pages/Comederos/ComederoDetail";
import DispositivoDetail from "./pages/Dispositivos/DispositivoDetail";

function App() {
  const { user } = useAuthContext();

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/tamboslist" /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to="/tamboslist" /> : <Register />} />

      <Route path="/tamboslist" element={user ? <TambosList /> : <Navigate to="/login" />} />
      <Route path="/tambos/:id" element={user ? <TamboDetail /> : <Navigate to="/login" />} />
      
      <Route path="/comederos/:id" element={user ? <ComederoDetail /> : <Navigate to="/login" />} />
      <Route path="/dispositivos/:id" element={user ? <DispositivoDetail /> : <Navigate to="/login" />} />

      <Route path="*" element={user ? <Navigate to="/tamboslist" /> : <Navigate to="/login" />} />
    </Routes>
  );
}

export default App;
