import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { ScrollArea } from './ui/scroll-area'
import { Separator } from './ui/separator'
import { 
  FileText, 
  Code, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Eye,
  Download,
  Copy,
  ExternalLink
} from 'lucide-react'

interface AnalysisResultsProps {
  data: any
}

export function AnalysisResults({ data }: AnalysisResultsProps) {
  const [selectedBug, setSelectedBug] = useState<string | null>(null)

  if (!data) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Analysis Results</CardTitle>
          <CardDescription>
            Upload a project and run analysis to see results here
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">
              No analysis data available. Start by uploading your project files.
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'destructive'
      case 'medium': return 'default'
      case 'low': return 'secondary'
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

  return (
    <div className="space-y-6">
      {/* Analysis Overview */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Analysis Overview</CardTitle>
              <CardDescription>
                Completed on {new Date(data.timestamp).toLocaleString()}
              </CardDescription>
            </div>
            <Badge variant="outline" className="flex items-center space-x-1">
              <CheckCircle className="h-3 w-3" />
              <span>Complete</span>
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold text-destructive">{data.bugs?.length || 0}</div>
              <div className="text-sm text-muted-foreground">Bugs Found</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold text-primary">{data.files?.code?.length || 0}</div>
              <div className="text-sm text-muted-foreground">Files Analyzed</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold text-green-600">{data.fixes?.length || 0}</div>
              <div className="text-sm text-muted-foreground">Fixes Available</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Analysis Tabs */}
      <Tabs defaultValue="specs" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="specs">Specifications</TabsTrigger>
          <TabsTrigger value="bugs">Bug Analysis</TabsTrigger>
          <TabsTrigger value="code">Code Review</TabsTrigger>
          <TabsTrigger value="runtime">Runtime Data</TabsTrigger>
        </TabsList>

        {/* Specifications Tab */}
        <TabsContent value="specs" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="h-5 w-5" />
                  <span>Original Specification</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[300px]">
                  <pre className="text-sm whitespace-pre-wrap font-mono bg-muted p-4 rounded">
                    {data.originalSpec}
                  </pre>
                </ScrollArea>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Code className="h-5 w-5" />
                  <span>Enhanced Specification</span>
                </CardTitle>
                <CardDescription>AI-enhanced version with detailed requirements</CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[300px]">
                  <pre className="text-sm whitespace-pre-wrap font-mono bg-muted p-4 rounded">
                    {data.enhancedSpec}
                  </pre>
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Bug Analysis Tab */}
        <TabsContent value="bugs" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Bug List */}
            <Card>
              <CardHeader>
                <CardTitle>Detected Issues</CardTitle>
                <CardDescription>
                  {data.bugs?.length || 0} issues found in your codebase
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[400px]">
                  <div className="space-y-3">
                    {data.bugs?.map((bug: any) => (
                      <div
                        key={bug.id}
                        className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                          selectedBug === bug.id 
                            ? 'bg-primary/10 border-primary' 
                            : 'bg-muted hover:bg-muted/80'
                        }`}
                        onClick={() => setSelectedBug(bug.id)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-1">
                              <Badge variant={getSeverityColor(bug.severity)} className="text-xs">
                                {getSeverityIcon(bug.severity)}
                                <span className="ml-1">{bug.severity}</span>
                              </Badge>
                            </div>
                            <h4 className="font-medium text-sm">{bug.title}</h4>
                            <p className="text-xs text-muted-foreground mt-1">
                              {bug.file}:{bug.line}
                            </p>
                          </div>
                          <Eye className="h-4 w-4 text-muted-foreground" />
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>

            {/* Bug Details */}
            <Card>
              <CardHeader>
                <CardTitle>Issue Details</CardTitle>
                <CardDescription>
                  {selectedBug ? 'Detailed analysis and suggestions' : 'Select an issue to view details'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {selectedBug ? (
                  <div className="space-y-4">
                    {(() => {
                      const bug = data.bugs?.find((b: any) => b.id === selectedBug)
                      if (!bug) return null
                      
                      return (
                        <>
                          <div>
                            <div className="flex items-center space-x-2 mb-2">
                              <Badge variant={getSeverityColor(bug.severity)}>
                                {getSeverityIcon(bug.severity)}
                                <span className="ml-1">{bug.severity}</span>
                              </Badge>
                              <span className="text-sm font-medium">{bug.title}</span>
                            </div>
                            <p className="text-sm text-muted-foreground mb-3">
                              {bug.description}
                            </p>
                          </div>

                          <Separator />

                          <div>
                            <h5 className="font-medium text-sm mb-2">Location</h5>
                            <div className="bg-muted p-3 rounded font-mono text-sm">
                              <div className="flex items-center justify-between">
                                <span>{bug.file}:{bug.line}</span>
                                <Button variant="ghost" size="sm">
                                  <ExternalLink className="h-3 w-3" />
                                </Button>
                              </div>
                            </div>
                          </div>

                          <div>
                            <h5 className="font-medium text-sm mb-2">Suggested Fix</h5>
                            <div className="bg-muted p-3 rounded">
                              <p className="text-sm">{bug.suggestion}</p>
                            </div>
                          </div>

                          <div className="flex space-x-2">
                            <Button size="sm" variant="outline">
                              <Copy className="h-3 w-3 mr-1" />
                              Copy Details
                            </Button>
                            <Button size="sm" variant="outline">
                              <Download className="h-3 w-3 mr-1" />
                              Export
                            </Button>
                          </div>
                        </>
                      )
                    })()}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <AlertTriangle className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                    <p className="text-sm text-muted-foreground">
                      Select an issue from the list to view detailed analysis
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Code Review Tab */}
        <TabsContent value="code" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Code Analysis Summary</CardTitle>
              <CardDescription>
                Analysis of {data.files?.code?.length || 0} code files
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {data.files?.code?.map((file: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <Code className="h-4 w-4" />
                        <span className="font-medium text-sm">{file.name}</span>
                      </div>
                      <Badge variant="outline">Analyzed</Badge>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Size: {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                ))}
                
                {(!data.files?.code || data.files.code.length === 0) && (
                  <div className="text-center py-8">
                    <Code className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                    <p className="text-sm text-muted-foreground">
                      No code files were uploaded for analysis
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Runtime Data Tab */}
        <TabsContent value="runtime" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Screen Recordings</CardTitle>
                <CardDescription>
                  {data.files?.video?.length || 0} video files analyzed
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.files?.video?.map((file: any, index: number) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-muted rounded">
                      <div className="flex items-center space-x-2">
                        <Eye className="h-4 w-4" />
                        <span className="text-sm">{file.name}</span>
                      </div>
                      <Button variant="ghost" size="sm">
                        <ExternalLink className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                  
                  {(!data.files?.video || data.files.video.length === 0) && (
                    <div className="text-center py-8">
                      <Eye className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                      <p className="text-sm text-muted-foreground">
                        No video files uploaded
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Log Files</CardTitle>
                <CardDescription>
                  {data.files?.logs?.length || 0} log files processed
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.files?.logs?.map((file: any, index: number) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-muted rounded">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-4 w-4" />
                        <span className="text-sm">{file.name}</span>
                      </div>
                      <Button variant="ghost" size="sm">
                        <ExternalLink className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                  
                  {(!data.files?.logs || data.files.logs.length === 0) && (
                    <div className="text-center py-8">
                      <FileText className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                      <p className="text-sm text-muted-foreground">
                        No log files uploaded
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}