import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { games } from '../services/api'

const Home: React.FC = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const startGame = async (mode: string, aiDifficulty?: number) => {
    try {
      const response = await games.create({
        mode,
        ai_difficulty: aiDifficulty,
        time_control: 'rapid',
        is_ranked: mode === 'online',
      })
      navigate(`/game/${response.data.game_id}`)
    } catch (error) {
      console.error('Error creating game:', error)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold text-white mb-4">♔ Chess AI Solver</h1>
          <p className="text-xl text-white/80">
            Play chess against AI or friends online
          </p>
        </div>

        {user ? (
          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-6">Welcome, {user.username}!</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={() => startGame('local')}
                  className="bg-green-500 hover:bg-green-600 text-white font-bold py-6 px-8 rounded-xl transition-colors"
                >
                  <div className="text-3xl mb-2">👥</div>
                  <div className="text-xl">Local 2 Players</div>
                </button>

                <button
                  onClick={() => startGame('ai', 3)}
                  className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-6 px-8 rounded-xl transition-colors"
                >
                  <div className="text-3xl mb-2">🤖</div>
                  <div className="text-xl">Play vs AI</div>
                </button>

                <button
                  onClick={() => navigate('/ranking')}
                  className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-6 px-8 rounded-xl transition-colors"
                >
                  <div className="text-3xl mb-2">🏆</div>
                  <div className="text-xl">Leaderboard</div>
                </button>

                <button
                  onClick={() => navigate('/profile')}
                  className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-6 px-8 rounded-xl transition-colors"
                >
                  <div className="text-3xl mb-2">👤</div>
                  <div className="text-xl">Profile</div>
                </button>
              </div>

              <div className="mt-6">
                <button
                  onClick={logout}
                  className="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-xl transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 text-center">
            <p className="text-white text-xl mb-6">Please login to start playing</p>
            <button
              onClick={() => navigate('/auth')}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-8 rounded-xl transition-colors"
            >
              Login / Register
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Home
