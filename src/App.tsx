import { useState, useEffect } from 'react'
import { blink } from './blink/client'
import { Dashboard } from './components/Dashboard'
import { LoadingScreen } from './components/LoadingScreen'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = blink.auth.onAuthStateChanged((state) => {
      setUser(state.user)
      setLoading(state.isLoading)
    })
    return unsubscribe
  }, [])

  if (loading) {
    return <LoadingScreen />
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <h1 className="text-2xl font-semibold text-foreground">Please sign in to continue</h1>
          <p className="text-muted-foreground">You'll be redirected to authenticate</p>
        </div>
      </div>
    )
  }

  return <Dashboard user={user} />
}

export default App