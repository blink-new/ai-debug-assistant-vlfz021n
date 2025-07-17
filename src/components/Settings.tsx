import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Switch } from './ui/switch'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Separator } from './ui/separator'
import { Badge } from './ui/badge'
import { 
  Settings as SettingsIcon, 
  User, 
  Bell, 
  Shield, 
  Palette, 
  Code, 
  Save,
  RefreshCw,
  Download,
  Trash2,
  Eye,
  EyeOff,
  X
} from 'lucide-react'
import { blink } from '../blink/client'

interface SettingsProps {
  user: any
  onNotification?: (notification: { type: 'success' | 'error' | 'warning' | 'info', title: string, message?: string, duration?: number }) => void
  onClose?: () => void
}

export function Settings({ user, onNotification, onClose }: SettingsProps) {
  const [loading, setLoading] = useState(false)
  const [showApiKey, setShowApiKey] = useState(false)
  
  // User Settings
  const [displayName, setDisplayName] = useState(user?.displayName || '')
  const [email, setEmail] = useState(user?.email || '')
  
  // Notification Settings
  const [emailNotifications, setEmailNotifications] = useState(true)
  const [pushNotifications, setPushNotifications] = useState(true)
  const [analysisComplete, setAnalysisComplete] = useState(true)
  const [bugDetected, setBugDetected] = useState(true)
  const [fixApplied, setFixApplied] = useState(true)
  
  // Analysis Settings
  const [analysisDepth, setAnalysisDepth] = useState('standard')
  const [autoApplyFixes, setAutoApplyFixes] = useState(false)
  const [confidenceThreshold, setConfidenceThreshold] = useState('80')
  const [maxFileSize, setMaxFileSize] = useState('10')
  
  // API Settings
  const [apiKey, setApiKey] = useState('')
  const [webhookUrl, setWebhookUrl] = useState('')
  
  // Theme Settings
  const [theme, setTheme] = useState('system')
  const [compactMode, setCompactMode] = useState(false)
  const [animationsEnabled, setAnimationsEnabled] = useState(true)

  const handleSaveProfile = async () => {
    try {
      setLoading(true)
      
      // In a real app, this would update the user profile
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
      
      onNotification?.({
        type: 'success',
        title: 'Profile Updated',
        message: 'Your profile settings have been saved successfully.',
        duration: 3000
      })
    } catch (error) {
      onNotification?.({
        type: 'error',
        title: 'Update Failed',
        message: 'Failed to update profile. Please try again.',
        duration: 5000
      })
    } finally {
      setLoading(false)
    }
  }

  const handleExportData = async () => {
    try {
      setLoading(true)
      
      // Simulate data export
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const exportData = {
        user: { displayName, email },
        settings: {
          notifications: { emailNotifications, pushNotifications },
          analysis: { analysisDepth, autoApplyFixes, confidenceThreshold }
        },
        exportDate: new Date().toISOString()
      }
      
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'ai-debug-assistant-data.json'
      a.click()
      URL.revokeObjectURL(url)
      
      onNotification?.({
        type: 'success',
        title: 'Data Exported',
        message: 'Your data has been exported successfully.',
        duration: 3000
      })
    } catch (error) {
      onNotification?.({
        type: 'error',
        title: 'Export Failed',
        message: 'Failed to export data. Please try again.',
        duration: 5000
      })
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteAccount = async () => {
    if (!confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return
    }
    
    try {
      setLoading(true)
      
      // In a real app, this would delete the user account
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      onNotification?.({
        type: 'info',
        title: 'Account Deletion Initiated',
        message: 'Your account deletion request has been processed.',
        duration: 5000
      })
    } catch (error) {
      onNotification?.({
        type: 'error',
        title: 'Deletion Failed',
        message: 'Failed to delete account. Please contact support.',
        duration: 5000
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="relative min-h-full">
      <div className="space-y-6 pb-16">
        {/* Header */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-lg">
            <SettingsIcon className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Settings</h1>
            <p className="text-sm text-muted-foreground">Manage your account and application preferences</p>
          </div>
        </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="profile" className="flex items-center space-x-2">
            <User className="h-4 w-4" />
            <span>Profile</span>
          </TabsTrigger>
          <TabsTrigger value="notifications" className="flex items-center space-x-2">
            <Bell className="h-4 w-4" />
            <span>Notifications</span>
          </TabsTrigger>
          <TabsTrigger value="analysis" className="flex items-center space-x-2">
            <Code className="h-4 w-4" />
            <span>Analysis</span>
          </TabsTrigger>
          <TabsTrigger value="api" className="flex items-center space-x-2">
            <Shield className="h-4 w-4" />
            <span>API</span>
          </TabsTrigger>
          <TabsTrigger value="appearance" className="flex items-center space-x-2">
            <Palette className="h-4 w-4" />
            <span>Appearance</span>
          </TabsTrigger>
        </TabsList>

        {/* Profile Settings */}
        <TabsContent value="profile" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
              <CardDescription>
                Update your personal information and account details
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="displayName">Display Name</Label>
                  <Input
                    id="displayName"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    placeholder="Enter your display name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                  />
                </div>
              </div>
              
              <Separator />
              
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Account Status</h4>
                  <p className="text-sm text-muted-foreground">Your account is active and verified</p>
                </div>
                <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
                  Active
                </Badge>
              </div>
              
              <div className="flex space-x-2">
                <Button onClick={handleSaveProfile} disabled={loading}>
                  {loading ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Save className="h-4 w-4 mr-2" />}
                  Save Changes
                </Button>
                <Button variant="outline" onClick={handleExportData} disabled={loading}>
                  <Download className="h-4 w-4 mr-2" />
                  Export Data
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card className="border-red-200 dark:border-red-800">
            <CardHeader>
              <CardTitle className="text-red-600 dark:text-red-400">Danger Zone</CardTitle>
              <CardDescription>
                Irreversible actions that will permanently affect your account
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                variant="destructive" 
                onClick={handleDeleteAccount}
                disabled={loading}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete Account
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notification Settings */}
        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>
                Choose how you want to be notified about analysis results and updates
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Email Notifications</h4>
                    <p className="text-sm text-muted-foreground">Receive notifications via email</p>
                  </div>
                  <Switch
                    checked={emailNotifications}
                    onCheckedChange={setEmailNotifications}
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Push Notifications</h4>
                    <p className="text-sm text-muted-foreground">Receive browser push notifications</p>
                  </div>
                  <Switch
                    checked={pushNotifications}
                    onCheckedChange={setPushNotifications}
                  />
                </div>
              </div>
              
              <Separator />
              
              <div className="space-y-4">
                <h4 className="font-medium">Notification Types</h4>
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-sm font-medium">Analysis Complete</span>
                      <p className="text-xs text-muted-foreground">When code analysis finishes</p>
                    </div>
                    <Switch
                      checked={analysisComplete}
                      onCheckedChange={setAnalysisComplete}
                    />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-sm font-medium">Bug Detected</span>
                      <p className="text-xs text-muted-foreground">When new bugs are found</p>
                    </div>
                    <Switch
                      checked={bugDetected}
                      onCheckedChange={setBugDetected}
                    />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-sm font-medium">Fix Applied</span>
                      <p className="text-xs text-muted-foreground">When fixes are successfully applied</p>
                    </div>
                    <Switch
                      checked={fixApplied}
                      onCheckedChange={setFixApplied}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analysis Settings */}
        <TabsContent value="analysis" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Analysis Configuration</CardTitle>
              <CardDescription>
                Configure how the AI analyzes your code and generates fixes
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="analysisDepth">Analysis Depth</Label>
                  <Select value={analysisDepth} onValueChange={setAnalysisDepth}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select analysis depth" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="quick">Quick - Basic issues only</SelectItem>
                      <SelectItem value="standard">Standard - Comprehensive analysis</SelectItem>
                      <SelectItem value="deep">Deep - Thorough security & performance</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="confidenceThreshold">Confidence Threshold (%)</Label>
                  <Input
                    id="confidenceThreshold"
                    type="number"
                    min="50"
                    max="100"
                    value={confidenceThreshold}
                    onChange={(e) => setConfidenceThreshold(e.target.value)}
                  />
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Auto-Apply Fixes</h4>
                    <p className="text-sm text-muted-foreground">Automatically apply high-confidence fixes</p>
                  </div>
                  <Switch
                    checked={autoApplyFixes}
                    onCheckedChange={setAutoApplyFixes}
                  />
                </div>
              </div>
              
              <Separator />
              
              <div className="space-y-2">
                <Label htmlFor="maxFileSize">Max File Size (MB)</Label>
                <Input
                  id="maxFileSize"
                  type="number"
                  min="1"
                  max="100"
                  value={maxFileSize}
                  onChange={(e) => setMaxFileSize(e.target.value)}
                />
                <p className="text-xs text-muted-foreground">
                  Files larger than this will be skipped during analysis
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* API Settings */}
        <TabsContent value="api" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>API Configuration</CardTitle>
              <CardDescription>
                Manage API keys and webhook settings for integrations
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="apiKey">API Key</Label>
                  <div className="flex space-x-2">
                    <Input
                      id="apiKey"
                      type={showApiKey ? "text" : "password"}
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      placeholder="Enter your API key"
                    />
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setShowApiKey(!showApiKey)}
                    >
                      {showApiKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="webhookUrl">Webhook URL</Label>
                  <Input
                    id="webhookUrl"
                    type="url"
                    value={webhookUrl}
                    onChange={(e) => setWebhookUrl(e.target.value)}
                    placeholder="https://your-app.com/webhook"
                  />
                  <p className="text-xs text-muted-foreground">
                    Receive analysis results and notifications at this URL
                  </p>
                </div>
              </div>
              
              <Separator />
              
              <div className="space-y-4">
                <h4 className="font-medium">API Usage</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-muted rounded-lg">
                    <div className="text-2xl font-bold text-primary">1,247</div>
                    <div className="text-sm text-muted-foreground">Requests This Month</div>
                  </div>
                  <div className="text-center p-4 bg-muted rounded-lg">
                    <div className="text-2xl font-bold text-green-600">99.9%</div>
                    <div className="text-sm text-muted-foreground">Uptime</div>
                  </div>
                  <div className="text-center p-4 bg-muted rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">156ms</div>
                    <div className="text-sm text-muted-foreground">Avg Response</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Appearance Settings */}
        <TabsContent value="appearance" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Appearance & Display</CardTitle>
              <CardDescription>
                Customize the look and feel of the application
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="theme">Theme</Label>
                  <Select value={theme} onValueChange={setTheme}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select theme" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="light">Light</SelectItem>
                      <SelectItem value="dark">Dark</SelectItem>
                      <SelectItem value="system">System</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Compact Mode</h4>
                    <p className="text-sm text-muted-foreground">Use smaller spacing and components</p>
                  </div>
                  <Switch
                    checked={compactMode}
                    onCheckedChange={setCompactMode}
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Animations</h4>
                    <p className="text-sm text-muted-foreground">Enable smooth transitions and animations</p>
                  </div>
                  <Switch
                    checked={animationsEnabled}
                    onCheckedChange={setAnimationsEnabled}
                  />
                </div>
              </div>
              
              <Separator />
              
              <div className="space-y-4">
                <h4 className="font-medium">Preview</h4>
                <div className="p-4 border rounded-lg bg-card">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                      <Code className="h-4 w-4 text-primary-foreground" />
                    </div>
                    <div>
                      <h5 className="font-medium">Sample Bug Report</h5>
                      <p className="text-sm text-muted-foreground">Authentication flow incomplete</p>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Badge variant="destructive">High</Badge>
                    <Badge variant="outline">src/auth.js:45</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
      </div>
      
      {/* Close button positioned at bottom right */}
      {onClose && (
        <div className="fixed bottom-6 right-6">
          <Button
            variant="outline"
            size="sm"
            onClick={onClose}
            className="h-10 px-4 shadow-lg border-2 hover:bg-primary hover:text-primary-foreground transition-colors"
          >
            <X className="h-4 w-4 mr-2" />
            Close
          </Button>
        </div>
      )}
    </div>
  )
}