import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { rankings } from '../services/api'

const Ranking: React.FC = () => {
  const navigate = useNavigate()
  const [leaderboard, setLeaderboard] = useState<any[]>([])
  const [timeControl, setTimeControl] = useState('rapid')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadLeaderboard()
  }, [timeControl])

  const loadLeaderboard = async () => {
    setLoading(true)
    try {
      const response = await rankings.leaderboard(timeControl, 50)
      setLeaderboard(response.data)
    } catch (error) {
      console.error('Error loading leaderboard:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="mb-6 bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
        >
          ← Back
        </button>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <h1 className="text-4xl font-bold text-white mb-6">🏆 Leaderboard</h1>

          <div className="flex gap-4 mb-6">
            <button
              onClick={() => setTimeControl('blitz')}
              className={`px-6 py-2 rounded-lg font-bold transition-colors ${
                timeControl === 'blitz'
                  ? 'bg-yellow-500 text-white'
                  : 'bg-white/10 text-white hover:bg-white/20'
              }`}
            >
              ⚡ Blitz
            </button>
            <button
              onClick={() => setTimeControl('rapid')}
              className={`px-6 py-2 rounded-lg font-bold transition-colors ${
                timeControl === 'rapid'
                  ? 'bg-blue-500 text-white'
                  : 'bg-white/10 text-white hover:bg-white/20'
              }`}
            >
              ⏱️ Rapid
            </button>
            <button
              onClick={() => setTimeControl('classical')}
              className={`px-6 py-2 rounded-lg font-bold transition-colors ${
                timeControl === 'classical'
                  ? 'bg-green-500 text-white'
                  : 'bg-white/10 text-white hover:bg-white/20'
              }`}
            >
              🏛️ Classical
            </button>
          </div>

          {loading ? (
            <div className="text-white text-center py-8">Loading...</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/20">
                    <th className="text-left text-white py-3 px-4">Rank</th>
                    <th className="text-left text-white py-3 px-4">Player</th>
                    <th className="text-right text-white py-3 px-4">Rating</th>
                    <th className="text-right text-white py-3 px-4">Games</th>
                    <th className="text-right text-white py-3 px-4">Wins</th>
                    <th className="text-right text-white py-3 px-4">Losses</th>
                    <th className="text-right text-white py-3 px-4">Draws</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry) => (
                    <tr
                      key={entry.user_id}
                      className="border-b border-white/10 hover:bg-white/5 transition-colors"
                    >
                      <td className="py-3 px-4">
                        <span className="text-white font-bold">
                          {entry.rank <= 3 && (
                            <span className="mr-2">
                              {entry.rank === 1 && '🥇'}
                              {entry.rank === 2 && '🥈'}
                              {entry.rank === 3 && '🥉'}
                            </span>
                          )}
                          #{entry.rank}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-white">{entry.username}</td>
                      <td className="py-3 px-4 text-right text-white font-bold">
                        {entry.rating}
                      </td>
                      <td className="py-3 px-4 text-right text-white/70">
                        {entry.games}
                      </td>
                      <td className="py-3 px-4 text-right text-green-400">
                        {entry.wins}
                      </td>
                      <td className="py-3 px-4 text-right text-red-400">
                        {entry.losses}
                      </td>
                      <td className="py-3 px-4 text-right text-yellow-400">
                        {entry.draws}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {leaderboard.length === 0 && (
                <div className="text-white text-center py-8">
                  No players yet. Be the first!
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Ranking
