import { useEffect } from 'react'
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react'
import { Button } from './ui/button'
import type { Notification } from '../hooks/useNotifications'

interface NotificationSystemProps {
  notifications: Notification[]
  onRemove: (id: string) => void
}

export function NotificationSystem({ notifications, onRemove }: NotificationSystemProps) {
  useEffect(() => {
    notifications.forEach((notification) => {
      if (notification.duration !== 0) {
        const timer = setTimeout(() => {
          onRemove(notification.id)
        }, notification.duration || 5000)
        
        return () => clearTimeout(timer)
      }
    })
  }, [notifications, onRemove])

  const getIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success': return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'error': return <AlertCircle className="h-5 w-5 text-red-500" />
      case 'warning': return <AlertTriangle className="h-5 w-5 text-yellow-500" />
      case 'info': return <Info className="h-5 w-5 text-blue-500" />
    }
  }

  const getBorderColor = (type: Notification['type']) => {
    switch (type) {
      case 'success': return 'border-green-200 dark:border-green-800'
      case 'error': return 'border-red-200 dark:border-red-800'
      case 'warning': return 'border-yellow-200 dark:border-yellow-800'
      case 'info': return 'border-blue-200 dark:border-blue-800'
    }
  }

  const getBackgroundColor = (type: Notification['type']) => {
    switch (type) {
      case 'success': return 'bg-green-50 dark:bg-green-950/20'
      case 'error': return 'bg-red-50 dark:bg-red-950/20'
      case 'warning': return 'bg-yellow-50 dark:bg-yellow-950/20'
      case 'info': return 'bg-blue-50 dark:bg-blue-950/20'
    }
  }

  if (notifications.length === 0) return null

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`
            p-4 rounded-lg border shadow-lg backdrop-blur-sm
            ${getBorderColor(notification.type)}
            ${getBackgroundColor(notification.type)}
            animate-in slide-in-from-right duration-300
          `}
        >
          <div className="flex items-start space-x-3">
            {getIcon(notification.type)}
            <div className="flex-1 min-w-0">
              <h4 className="text-sm font-medium text-foreground">
                {notification.title}
              </h4>
              {notification.message && (
                <p className="text-sm text-muted-foreground mt-1">
                  {notification.message}
                </p>
              )}
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onRemove(notification.id)}
              className="h-6 w-6 p-0 hover:bg-transparent"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      ))}
    </div>
  )
}