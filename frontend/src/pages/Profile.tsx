import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { users, rankings } from '../services/api'

const Profile: React.FC = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [profile, setProfile] = useState<any>(null)
  const [rankingData, setRankingData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) {
      navigate('/auth')
      return
    }

    loadProfile()
  }, [user])

  const loadProfile = async () => {
    try {
      const [profileRes, rankingRes] = await Promise.all([
        users.getProfile(),
        rankings.getUserRanking(user!.id),
      ])
      setProfile(profileRes.data)
      setRankingData(rankingRes.data)
    } catch (error) {
      console.error('Error loading profile:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-2xl">Loading profile...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="mb-6 bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
        >
          ← Back
        </button>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">{profile?.username}</h1>
              <p className="text-white/70">{profile?.email}</p>
              {profile?.full_name && (
                <p className="text-white/70">{profile.full_name}</p>
              )}
            </div>
            <button
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-6 rounded-lg transition-colors"
            >
              Logout
            </button>
          </div>

          {rankingData && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white mb-4">Rankings</h2>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <h3 className="text-xl font-bold text-yellow-400 mb-2">⚡ Blitz</h3>
                  <p className="text-4xl font-bold text-white mb-2">
                    {rankingData.blitz?.rating || 1200}
                  </p>
                  <p className="text-white/70 text-sm">
                    Peak: {rankingData.blitz?.peak || 1200}
                  </p>
                  <p className="text-white/70 text-sm">
                    Games: {rankingData.blitz?.games || 0}
                  </p>
                </div>

                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <h3 className="text-xl font-bold text-blue-400 mb-2">⏱️ Rapid</h3>
                  <p className="text-4xl font-bold text-white mb-2">
                    {rankingData.rapid?.rating || 1200}
                  </p>
                  <p className="text-white/70 text-sm">
                    Peak: {rankingData.rapid?.peak || 1200}
                  </p>
                  <p className="text-white/70 text-sm">
                    Games: {rankingData.rapid?.games || 0}
                  </p>
                </div>

                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <h3 className="text-xl font-bold text-green-400 mb-2">🏛️ Classical</h3>
                  <p className="text-4xl font-bold text-white mb-2">
                    {rankingData.classical?.rating || 1200}
                  </p>
                  <p className="text-white/70 text-sm">
                    Peak: {rankingData.classical?.peak || 1200}
                  </p>
                  <p className="text-white/70 text-sm">
                    Games: {rankingData.classical?.games || 0}
                  </p>
                </div>
              </div>

              <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                <h3 className="text-xl font-bold text-white mb-4">Overall Statistics</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-white/70 text-sm">Total Games</p>
                    <p className="text-2xl font-bold text-white">
                      {rankingData.overall?.total_games || 0}
                    </p>
                  </div>
                  <div>
                    <p className="text-white/70 text-sm">Wins</p>
                    <p className="text-2xl font-bold text-green-400">
                      {rankingData.overall?.wins || 0}
                    </p>
                  </div>
                  <div>
                    <p className="text-white/70 text-sm">Losses</p>
                    <p className="text-2xl font-bold text-red-400">
                      {rankingData.overall?.losses || 0}
                    </p>
                  </div>
                  <div>
                    <p className="text-white/70 text-sm">Draws</p>
                    <p className="text-2xl font-bold text-yellow-400">
                      {rankingData.overall?.draws || 0}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Profile
