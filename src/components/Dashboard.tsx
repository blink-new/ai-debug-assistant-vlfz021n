import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { 
  Upload, 
  FileText, 
  Code, 
  Play, 
  Bug, 
  CheckCircle, 
  AlertCircle,
  Zap,
  Brain,
  Settings
} from 'lucide-react'
import { ProjectUpload } from './ProjectUpload'
import { AnalysisResults } from './AnalysisResults'
import { BugReports } from './BugReports'
import { CodeDiffViewer } from './CodeDiffViewer'
import { NotificationSystem } from './NotificationSystem'
import { Settings } from './Settings'
import { useNotifications } from '../hooks/useNotifications'
import { WelcomeScreen } from './WelcomeScreen'

interface DashboardProps {
  user: any
}

export function Dashboard({ user }: DashboardProps) {
  const [activeTab, setActiveTab] = useState('upload')
  const [analysisData, setAnalysisData] = useState(null)
  const [showWelcome, setShowWelcome] = useState(() => {
    // Check if user has seen welcome screen before
    return !localStorage.getItem('ai-debug-welcome-seen')
  })
  const { notifications, addNotification, removeNotification } = useNotifications()

  const handleApplyFix = async (fixId: string) => {
    try {
      console.log('Applying fix:', fixId)
      // In a real app, this would apply the fix to the codebase
      // For now, we'll simulate the process
      
      // Update analysis data to mark fix as applied
      if (analysisData?.fixes) {
        const updatedFixes = analysisData.fixes.map((fix: any) => 
          fix.id === fixId ? { ...fix, status: 'applied' } : fix
        )
        setAnalysisData({ ...analysisData, fixes: updatedFixes })
        
        addNotification({
          type: 'success',
          title: 'Fix Applied Successfully',
          message: 'The code fix has been applied to your project.',
          duration: 4000
        })
      }
    } catch (error) {
      console.error('Failed to apply fix:', error)
      addNotification({
        type: 'error',
        title: 'Failed to Apply Fix',
        message: 'There was an error applying the fix. Please try again.',
        duration: 5000
      })
    }
  }

  const handleRejectFix = async (fixId: string) => {
    try {
      console.log('Rejecting fix:', fixId)
      // In a real app, this would mark the fix as rejected
      
      // Update analysis data to mark fix as rejected
      if (analysisData?.fixes) {
        const updatedFixes = analysisData.fixes.map((fix: any) => 
          fix.id === fixId ? { ...fix, status: 'rejected' } : fix
        )
        setAnalysisData({ ...analysisData, fixes: updatedFixes })
        
        addNotification({
          type: 'info',
          title: 'Fix Rejected',
          message: 'The code fix has been marked as rejected.',
          duration: 3000
        })
      }
    } catch (error) {
      console.error('Failed to reject fix:', error)
      addNotification({
        type: 'error',
        title: 'Failed to Reject Fix',
        message: 'There was an error rejecting the fix. Please try again.',
        duration: 5000
      })
    }
  }

  const handleWelcomeComplete = () => {
    localStorage.setItem('ai-debug-welcome-seen', 'true')
    setShowWelcome(false)
    addNotification({
      type: 'success',
      title: 'Welcome to BugOff AI!',
      message: 'Ready to start analyzing your projects.',
      duration: 4000
    })
  }

  const handleSkipWelcome = () => {
    localStorage.setItem('ai-debug-welcome-seen', 'true')
    setShowWelcome(false)
  }

  // Show welcome screen for new users
  if (showWelcome) {
    return (
      <WelcomeScreen 
        onGetStarted={handleWelcomeComplete}
        onSkip={handleSkipWelcome}
      />
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-lg">
                <Bug className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-foreground">BugOff AI</h1>
                <p className="text-sm text-muted-foreground">Intelligent debugging for no-code apps</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="secondary" className="hidden sm:flex">
                <Zap className="h-3 w-3 mr-1" />
                Pro Plan
              </Badge>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setActiveTab('settings')}
              >
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-primary-foreground">
                    {user.email?.[0]?.toUpperCase() || 'U'}
                  </span>
                </div>
                <span className="text-sm text-muted-foreground hidden sm:block">
                  {user.email}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Projects Analyzed</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-muted-foreground">+2 from last week</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Bugs Detected</CardTitle>
              <Bug className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">47</div>
              <p className="text-xs text-muted-foreground">+12 from last week</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Fixes Applied</CardTitle>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">38</div>
              <p className="text-xs text-muted-foreground">81% success rate</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">AI Analysis Time</CardTitle>
              <Brain className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">2.3m</div>
              <p className="text-xs text-muted-foreground">Average per project</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="upload" className="flex items-center space-x-2">
              <Upload className="h-4 w-4" />
              <span>Upload Project</span>
            </TabsTrigger>
            <TabsTrigger value="analysis" className="flex items-center space-x-2">
              <Code className="h-4 w-4" />
              <span>Analysis</span>
            </TabsTrigger>
            <TabsTrigger value="bugs" className="flex items-center space-x-2">
              <AlertCircle className="h-4 w-4" />
              <span>Bug Reports</span>
            </TabsTrigger>
            <TabsTrigger value="fixes" className="flex items-center space-x-2">
              <Play className="h-4 w-4" />
              <span>Apply Fixes</span>
            </TabsTrigger>
            <TabsTrigger value="settings" className="flex items-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>Settings</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upload" className="space-y-6">
            <ProjectUpload 
              onAnalysisComplete={setAnalysisData} 
              onNotification={addNotification}
            />
          </TabsContent>

          <TabsContent value="analysis" className="space-y-6">
            <AnalysisResults data={analysisData} />
          </TabsContent>

          <TabsContent value="bugs" className="space-y-6">
            <BugReports />
          </TabsContent>

          <TabsContent value="fixes" className="space-y-6">
            <CodeDiffViewer 
              fixes={analysisData?.fixes || []}
              onApplyFix={handleApplyFix}
              onRejectFix={handleRejectFix}
            />
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Settings 
              user={user} 
              onNotification={addNotification}
              onClose={() => setActiveTab('upload')}
            />
          </TabsContent>
        </Tabs>
      </main>
      
      {/* Notification System */}
      <NotificationSystem 
        notifications={notifications} 
        onRemove={removeNotification} 
      />
    </div>
  )
}