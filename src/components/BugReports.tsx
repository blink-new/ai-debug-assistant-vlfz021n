import { useState, useEffect, useCallback } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Input } from './ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { ScrollArea } from './ui/scroll-area'
import { Separator } from './ui/separator'
import { 
  Bug, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Search,
  Filter,
  Download,
  Eye,
  Code,
  ExternalLink,
  Calendar,
  User,
  FileText
} from 'lucide-react'
import { blink } from '../blink/client'

interface BugReport {
  id: string
  title: string
  severity: 'high' | 'medium' | 'low'
  status: 'open' | 'in-progress' | 'resolved'
  description: string
  file: string
  line: number
  createdAt: string
  projectName: string
  suggestion: string
}

export function BugReports() {
  const [reports, setReports] = useState<BugReport[]>([])
  const [filteredReports, setFilteredReports] = useState<BugReport[]>([])
  const [selectedReport, setSelectedReport] = useState<BugReport | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [severityFilter, setSeverityFilter] = useState<string>('all')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadBugReports()
  }, [])

  useEffect(() => {
    filterReports()
  }, [filterReports, reports, searchTerm, severityFilter, statusFilter])

  const loadBugReports = async () => {
    try {
      setLoading(true)
      const user = await blink.auth.me()
      
      // Mock data for demonstration - in real app, this would come from database
      const mockReports: BugReport[] = [
        {
          id: 'bug-1',
          title: 'Authentication Flow Incomplete',
          severity: 'high',
          status: 'open',
          description: 'The login component is missing proper error handling and validation. Users can submit empty forms and receive unclear error messages.',
          file: 'src/components/Login.tsx',
          line: 45,
          createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
          projectName: 'E-commerce Dashboard',
          suggestion: 'Add form validation, loading states, and comprehensive error handling'
        },
        {
          id: 'bug-2',
          title: 'API Response Not Handled',
          severity: 'medium',
          status: 'in-progress',
          description: 'Missing error handling for API responses in user dashboard. Network failures cause the app to crash.',
          file: 'src/pages/Dashboard.tsx',
          line: 23,
          createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          projectName: 'User Management System',
          suggestion: 'Implement try-catch blocks, loading states, and retry mechanisms'
        },
        {
          id: 'bug-3',
          title: 'Memory Leak in Component',
          severity: 'high',
          status: 'open',
          description: 'useEffect cleanup not properly implemented, causing memory leaks when components unmount.',
          file: 'src/components/DataTable.tsx',
          line: 78,
          createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
          projectName: 'Analytics Platform',
          suggestion: 'Add cleanup functions to useEffect hooks and cancel pending requests'
        },
        {
          id: 'bug-4',
          title: 'Accessibility Issues',
          severity: 'low',
          status: 'resolved',
          description: 'Missing ARIA labels and keyboard navigation support in navigation component.',
          file: 'src/components/Navigation.tsx',
          line: 12,
          createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
          projectName: 'Corporate Website',
          suggestion: 'Add proper ARIA attributes and keyboard event handlers'
        },
        {
          id: 'bug-5',
          title: 'Race Condition in State Updates',
          severity: 'medium',
          status: 'open',
          description: 'Multiple async operations updating the same state simultaneously, causing inconsistent UI state.',
          file: 'src/hooks/useUserData.ts',
          line: 34,
          createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
          projectName: 'Social Media App',
          suggestion: 'Implement proper state management with reducers or use libraries like Zustand'
        }
      ]
      
      setReports(mockReports)
    } catch (error) {
      console.error('Failed to load bug reports:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterReports = useCallback(() => {
    let filtered = reports

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(report =>
        report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.file.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.projectName.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Severity filter
    if (severityFilter !== 'all') {
      filtered = filtered.filter(report => report.severity === severityFilter)
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(report => report.status === statusFilter)
    }

    setFilteredReports(filtered)
  }, [reports, searchTerm, severityFilter, statusFilter])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'destructive'
      case 'medium': return 'default'
      case 'low': return 'secondary'
      default: return 'outline'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'destructive'
      case 'in-progress': return 'default'
      case 'resolved': return 'secondary'
      default: return 'outline'
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high': return <AlertTriangle className="h-4 w-4" />
      case 'medium': return <Clock className="h-4 w-4" />
      case 'low': return <CheckCircle className="h-4 w-4" />
      default: return <AlertTriangle className="h-4 w-4" />
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open': return <Bug className="h-4 w-4" />
      case 'in-progress': return <Clock className="h-4 w-4" />
      case 'resolved': return <CheckCircle className="h-4 w-4" />
      default: return <Bug className="h-4 w-4" />
    }
  }

  const exportReports = () => {
    const csvContent = [
      ['ID', 'Title', 'Severity', 'Status', 'File', 'Line', 'Project', 'Created'],
      ...filteredReports.map(report => [
        report.id,
        report.title,
        report.severity,
        report.status,
        report.file,
        report.line.toString(),
        report.projectName,
        new Date(report.createdAt).toLocaleDateString()
      ])
    ].map(row => row.join(',')).join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'bug-reports.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <Bug className="h-8 w-8 animate-pulse text-muted-foreground mx-auto mb-2" />
            <p className="text-muted-foreground">Loading bug reports...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Bug className="h-5 w-5 text-destructive" />
              <div>
                <div className="text-2xl font-bold">{reports.filter(r => r.status === 'open').length}</div>
                <div className="text-sm text-muted-foreground">Open Issues</div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Clock className="h-5 w-5 text-yellow-500" />
              <div>
                <div className="text-2xl font-bold">{reports.filter(r => r.status === 'in-progress').length}</div>
                <div className="text-sm text-muted-foreground">In Progress</div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <div>
                <div className="text-2xl font-bold">{reports.filter(r => r.status === 'resolved').length}</div>
                <div className="text-sm text-muted-foreground">Resolved</div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5 text-destructive" />
              <div>
                <div className="text-2xl font-bold">{reports.filter(r => r.severity === 'high').length}</div>
                <div className="text-sm text-muted-foreground">High Priority</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Bug Reports</CardTitle>
              <CardDescription>
                {filteredReports.length} of {reports.length} reports
              </CardDescription>
            </div>
            <Button onClick={exportReports} variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export CSV
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search reports..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <Select value={severityFilter} onValueChange={setSeverityFilter}>
              <SelectTrigger className="w-[140px]">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Severity" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Severities</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[140px]">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                <SelectItem value="open">Open</SelectItem>
                <SelectItem value="in-progress">In Progress</SelectItem>
                <SelectItem value="resolved">Resolved</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Reports List */}
            <div className="space-y-3">
              <h3 className="font-medium text-sm text-muted-foreground">Reports ({filteredReports.length})</h3>
              <ScrollArea className="h-[500px]">
                <div className="space-y-3">
                  {filteredReports.map((report) => (
                    <div
                      key={report.id}
                      className={`p-4 rounded-lg border cursor-pointer transition-colors ${
                        selectedReport?.id === report.id 
                          ? 'bg-primary/10 border-primary' 
                          : 'bg-card hover:bg-muted/50'
                      }`}
                      onClick={() => setSelectedReport(report)}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <Badge variant={getSeverityColor(report.severity)} className="text-xs">
                            {getSeverityIcon(report.severity)}
                            <span className="ml-1">{report.severity}</span>
                          </Badge>
                          <Badge variant={getStatusColor(report.status)} className="text-xs">
                            {getStatusIcon(report.status)}
                            <span className="ml-1">{report.status}</span>
                          </Badge>
                        </div>
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      </div>
                      
                      <h4 className="font-medium text-sm mb-1">{report.title}</h4>
                      <p className="text-xs text-muted-foreground mb-2 line-clamp-2">
                        {report.description}
                      </p>
                      
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span>{report.file}:{report.line}</span>
                        <span>{new Date(report.createdAt).toLocaleDateString()}</span>
                      </div>
                    </div>
                  ))}
                  
                  {filteredReports.length === 0 && (
                    <div className="text-center py-8">
                      <Bug className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                      <p className="text-sm text-muted-foreground">
                        No bug reports match your filters
                      </p>
                    </div>
                  )}
                </div>
              </ScrollArea>
            </div>

            {/* Report Details */}
            <div>
              <h3 className="font-medium text-sm text-muted-foreground mb-3">Report Details</h3>
              <Card>
                <CardContent className="p-6">
                  {selectedReport ? (
                    <div className="space-y-4">
                      <div>
                        <div className="flex items-center space-x-2 mb-2">
                          <Badge variant={getSeverityColor(selectedReport.severity)}>
                            {getSeverityIcon(selectedReport.severity)}
                            <span className="ml-1">{selectedReport.severity}</span>
                          </Badge>
                          <Badge variant={getStatusColor(selectedReport.status)}>
                            {getStatusIcon(selectedReport.status)}
                            <span className="ml-1">{selectedReport.status}</span>
                          </Badge>
                        </div>
                        <h4 className="font-semibold text-lg">{selectedReport.title}</h4>
                      </div>

                      <Separator />

                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div className="flex items-center space-x-2">
                          <User className="h-4 w-4 text-muted-foreground" />
                          <span className="text-muted-foreground">Project:</span>
                          <span>{selectedReport.projectName}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Calendar className="h-4 w-4 text-muted-foreground" />
                          <span className="text-muted-foreground">Created:</span>
                          <span>{new Date(selectedReport.createdAt).toLocaleDateString()}</span>
                        </div>
                      </div>

                      <div>
                        <h5 className="font-medium text-sm mb-2 flex items-center">
                          <FileText className="h-4 w-4 mr-1" />
                          Description
                        </h5>
                        <p className="text-sm text-muted-foreground bg-muted p-3 rounded">
                          {selectedReport.description}
                        </p>
                      </div>

                      <div>
                        <h5 className="font-medium text-sm mb-2 flex items-center">
                          <Code className="h-4 w-4 mr-1" />
                          Location
                        </h5>
                        <div className="bg-muted p-3 rounded font-mono text-sm">
                          <div className="flex items-center justify-between">
                            <span>{selectedReport.file}:{selectedReport.line}</span>
                            <Button variant="ghost" size="sm">
                              <ExternalLink className="h-3 w-3" />
                            </Button>
                          </div>
                        </div>
                      </div>

                      <div>
                        <h5 className="font-medium text-sm mb-2">AI Suggestion</h5>
                        <div className="bg-green-50 dark:bg-green-950/20 p-3 rounded border border-green-200 dark:border-green-800">
                          <p className="text-sm text-green-800 dark:text-green-200">
                            {selectedReport.suggestion}
                          </p>
                        </div>
                      </div>

                      <div className="flex space-x-2 pt-2">
                        <Button size="sm">
                          View Fix
                        </Button>
                        <Button size="sm" variant="outline">
                          Mark Resolved
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <Bug className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <p className="text-muted-foreground">
                        Select a bug report to view detailed information
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}