import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Home from './pages/Home'
import Game from './pages/Game'
import Profile from './pages/Profile'
import Ranking from './pages/Ranking'
import Auth from './pages/Auth'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-700">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/game/:gameId" element={<Game />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/ranking" element={<Ranking />} />
            <Route path="/auth" element={<Auth />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
