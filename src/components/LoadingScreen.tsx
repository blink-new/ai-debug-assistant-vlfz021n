import { useState, useEffect } from 'react'
import { Loader2, Bug, Code, Zap } from 'lucide-react'

export function LoadingScreen() {
  const [loadingText, setLoadingText] = useState('Initializing AI Debug Assistant...')
  
  useEffect(() => {
    const messages = [
      'Initializing AI Debug Assistant...',
      'Loading analysis engines...',
      'Preparing code intelligence...',
      'Almost ready...'
    ]
    
    let index = 0
    const interval = setInterval(() => {
      index = (index + 1) % messages.length
      setLoadingText(messages[index])
    }, 1500)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center">
      <div className="text-center space-y-8 max-w-md">
        {/* Animated Logo */}
        <div className="relative">
          <div className="flex items-center justify-center w-20 h-20 bg-primary rounded-2xl mx-auto mb-4 shadow-lg">
            <Bug className="h-10 w-10 text-primary-foreground" />
          </div>
          
          {/* Floating Icons */}
          <div className="absolute -top-2 -right-2 w-8 h-8 bg-accent rounded-lg flex items-center justify-center animate-bounce">
            <Code className="h-4 w-4 text-accent-foreground" />
          </div>
          <div className="absolute -bottom-2 -left-2 w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center animate-bounce" style={{ animationDelay: '0.5s' }}>
            <Zap className="h-4 w-4 text-white" />
          </div>
        </div>

        {/* Title */}
        <div>
          <h1 className="text-2xl font-bold text-foreground mb-2">AI Debug Assistant</h1>
          <p className="text-muted-foreground text-sm">Intelligent debugging for no-code applications</p>
        </div>

        {/* Loading Animation */}
        <div className="space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <Loader2 className="h-5 w-5 animate-spin text-primary" />
            <span className="text-sm text-muted-foreground">{loadingText}</span>
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-muted rounded-full h-1">
            <div className="bg-primary h-1 rounded-full animate-pulse" style={{ width: '60%' }}></div>
          </div>
        </div>

        {/* Features Preview */}
        <div className="grid grid-cols-3 gap-4 text-center">
          <div className="space-y-2">
            <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center mx-auto">
              <Code className="h-4 w-4 text-blue-600 dark:text-blue-400" />
            </div>
            <p className="text-xs text-muted-foreground">Code Analysis</p>
          </div>
          <div className="space-y-2">
            <div className="w-8 h-8 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center mx-auto">
              <Bug className="h-4 w-4 text-green-600 dark:text-green-400" />
            </div>
            <p className="text-xs text-muted-foreground">Bug Detection</p>
          </div>
          <div className="space-y-2">
            <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center mx-auto">
              <Zap className="h-4 w-4 text-purple-600 dark:text-purple-400" />
            </div>
            <p className="text-xs text-muted-foreground">Auto Fixes</p>
          </div>
        </div>
      </div>
    </div>
  )
}