import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Progress } from './ui/progress'
import { 
  CheckCircle, 
  X, 
  Code, 
  GitBranch,
  Download,
  Eye,
  Zap,
  AlertTriangle,
  Clock,
  TrendingUp,
  FileText,
  Play,
  Pause
} from 'lucide-react'

interface Fix {
  id: string
  bugId: string
  title: string
  description: string
  file: string
  confidence: number
  impact: string
  status: 'pending' | 'applied' | 'rejected'
  originalCode: string
  fixedCode: string
  explanation: string
}

interface CodeDiffViewerProps {
  fixes: Fix[]
  onApplyFix: (fixId: string) => void
  onRejectFix: (fixId: string) => void
}

export function CodeDiffViewer({ fixes, onApplyFix, onRejectFix }: CodeDiffViewerProps) {
  const [selectedFix, setSelectedFix] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<'side-by-side' | 'unified'>('side-by-side')

  // If no fixes provided, show dummy data
  const dummyFixes: Fix[] = [
    {
      id: 'fix-1',
      bugId: 'bug-1',
      title: 'Implement Parameterized Queries',
      description: 'Replace string concatenation with parameterized queries to prevent SQL injection',
      file: 'src/api/users.js',
      confidence: 98,
      impact: 'critical',
      status: 'pending',
      originalCode: `const query = "SELECT * FROM users WHERE email = '" + email + "' AND password = '" + password + "'";
const result = await db.query(query);

if (result.length > 0) {
  return { success: true, user: result[0] };
} else {
  return { success: false, message: 'Invalid credentials' };
}`,
      fixedCode: `const query = "SELECT * FROM users WHERE email = ? AND password = ?";
const hashedPassword = await bcrypt.hash(password, 10);
const result = await db.query(query, [email, hashedPassword]);

if (result.length > 0) {
  return { success: true, user: result[0] };
} else {
  return { success: false, message: 'Invalid credentials' };
}`,
      explanation: 'Uses parameterized queries to safely handle user input and prevents SQL injection attacks. Also includes password hashing for security.'
    },
    {
      id: 'fix-2',
      bugId: 'bug-2',
      title: 'Add JWT Validation Middleware',
      description: 'Implement comprehensive JWT token validation for protected routes',
      file: 'src/middleware/auth.js',
      confidence: 95,
      impact: 'high',
      status: 'pending',
      originalCode: `app.get('/api/protected', (req, res) => {
  // No authentication check
  res.json({ data: 'sensitive information' });
});

app.post('/api/user/update', (req, res) => {
  // Direct database update without auth
  const { userId, data } = req.body;
  updateUser(userId, data);
  res.json({ success: true });
});`,
      fixedCode: `const jwt = require('jsonwebtoken');

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid or expired token' });
    }
    req.user = user;
    next();
  });
};

app.get('/api/protected', authenticateToken, (req, res) => {
  res.json({ data: 'sensitive information', user: req.user });
});

app.post('/api/user/update', authenticateToken, (req, res) => {
  const { data } = req.body;
  const userId = req.user.id; // Use authenticated user ID
  updateUser(userId, data);
  res.json({ success: true });
});`,
      explanation: 'Adds proper JWT validation middleware that checks for valid tokens and handles authentication errors gracefully.'
    },
    {
      id: 'fix-3',
      bugId: 'bug-3',
      title: 'Add Comprehensive Error Handling',
      description: 'Implement error handling for async operations to prevent crashes',
      file: 'src/components/Dashboard.jsx',
      confidence: 92,
      impact: 'medium',
      status: 'applied',
      originalCode: `const fetchUserData = async () => {
  const response = await fetch('/api/user');
  const userData = await response.json();
  setUserData(userData);
};

const handleSubmit = async (formData) => {
  const response = await fetch('/api/submit', {
    method: 'POST',
    body: JSON.stringify(formData)
  });
  const result = await response.json();
  setResult(result);
};

useEffect(() => {
  fetchUserData();
}, []);`,
      fixedCode: `const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

const fetchUserData = async () => {
  try {
    setLoading(true);
    setError(null);
    
    const response = await fetch('/api/user');
    
    if (!response.ok) {
      throw new Error(\`HTTP error! status: \${response.status}\`);
    }
    
    const userData = await response.json();
    setUserData(userData);
  } catch (err) {
    setError(err.message || 'Failed to fetch user data');
    console.error('Error fetching user data:', err);
  } finally {
    setLoading(false);
  }
};

const handleSubmit = async (formData) => {
  try {
    setLoading(true);
    setError(null);
    
    const response = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    
    if (!response.ok) {
      throw new Error(\`Submission failed: \${response.status}\`);
    }
    
    const result = await response.json();
    setResult(result);
  } catch (err) {
    setError(err.message || 'Submission failed');
    console.error('Error submitting form:', err);
  } finally {
    setLoading(false);
  }
};

useEffect(() => {
  fetchUserData();
}, []);`,
      explanation: 'Adds comprehensive error handling with loading states, proper HTTP status checking, and user feedback for better UX.'
    }
  ]

  const displayFixes = fixes.length > 0 ? fixes : dummyFixes
  const selectedFixData = displayFixes.find(fix => fix.id === selectedFix)

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'critical': return 'text-red-600 bg-red-50 border-red-200'
      case 'high': return 'text-orange-600 bg-orange-50 border-orange-200'
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'low': return 'text-blue-600 bg-blue-50 border-blue-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'text-yellow-600 bg-yellow-50'
      case 'applied': return 'text-green-600 bg-green-50'
      case 'rejected': return 'text-red-600 bg-red-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <Clock className="h-4 w-4" />
      case 'applied': return <CheckCircle className="h-4 w-4" />
      case 'rejected': return <X className="h-4 w-4" />
      default: return <Clock className="h-4 w-4" />
    }
  }

  const stats = {
    total: displayFixes.length,
    pending: displayFixes.filter(f => f.status === 'pending').length,
    applied: displayFixes.filter(f => f.status === 'applied').length,
    rejected: displayFixes.filter(f => f.status === 'rejected').length,
    avgConfidence: Math.round(displayFixes.reduce((acc, f) => acc + f.confidence, 0) / displayFixes.length)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-foreground">Code Fixes</h2>
        <p className="text-muted-foreground">
          Review and apply AI-generated fixes for detected issues
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card className="text-center">
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-foreground">{stats.total}</div>
            <div className="text-xs text-muted-foreground">Total Fixes</div>
          </CardContent>
        </Card>
        
        <Card className="text-center border-yellow-200 bg-yellow-50">
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
            <div className="text-xs text-yellow-600">Pending</div>
          </CardContent>
        </Card>
        
        <Card className="text-center border-green-200 bg-green-50">
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">{stats.applied}</div>
            <div className="text-xs text-green-600">Applied</div>
          </CardContent>
        </Card>
        
        <Card className="text-center border-red-200 bg-red-50">
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-red-600">{stats.rejected}</div>
            <div className="text-xs text-red-600">Rejected</div>
          </CardContent>
        </Card>
        
        <Card className="text-center border-blue-200 bg-blue-50">
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">{stats.avgConfidence}%</div>
            <div className="text-xs text-blue-600">Avg Confidence</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Fix List */}
        <div className="lg:col-span-1 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <GitBranch className="h-5 w-5" />
                <span>Available Fixes</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {displayFixes.map((fix) => (
                <div
                  key={fix.id}
                  className={`p-3 rounded-lg border cursor-pointer transition-all hover:shadow-sm ${
                    selectedFix === fix.id ? 'border-primary bg-primary/5' : 'border-border'
                  }`}
                  onClick={() => setSelectedFix(fix.id)}
                >
                  <div className="space-y-2">
                    <div className="flex items-start justify-between">
                      <h4 className="text-sm font-medium line-clamp-2">{fix.title}</h4>
                      <Badge variant="outline" className={`text-xs ml-2 ${getStatusColor(fix.status)}`}>
                        {getStatusIcon(fix.status)}
                        <span className="ml-1">{fix.status}</span>
                      </Badge>
                    </div>
                    
                    <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                      <Code className="h-3 w-3" />
                      <span className="truncate">{fix.file}</span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Badge variant="outline" className={`text-xs ${getImpactColor(fix.impact)}`}>
                        {fix.impact}
                      </Badge>
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <TrendingUp className="h-3 w-3" />
                        <span>{fix.confidence}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Fix Details */}
        <div className="lg:col-span-2">
          {selectedFixData ? (
            <Card>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <CardTitle className="flex items-center space-x-2">
                      <span>{selectedFixData.title}</span>
                      <Badge variant="outline" className={`text-xs ${getImpactColor(selectedFixData.impact)}`}>
                        {selectedFixData.impact}
                      </Badge>
                    </CardTitle>
                    <CardDescription className="flex items-center space-x-4">
                      <span className="flex items-center space-x-1">
                        <Code className="h-3 w-3" />
                        <span>{selectedFixData.file}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <TrendingUp className="h-3 w-3" />
                        <span>{selectedFixData.confidence}% confidence</span>
                      </span>
                    </CardDescription>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setViewMode(viewMode === 'side-by-side' ? 'unified' : 'side-by-side')}
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      {viewMode === 'side-by-side' ? 'Unified' : 'Side by Side'}
                    </Button>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-6">
                {/* Description */}
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h4 className="text-sm font-medium text-blue-800 mb-2">Fix Description</h4>
                  <p className="text-sm text-blue-700">{selectedFixData.description}</p>
                </div>

                {/* Code Diff */}
                <Tabs value={viewMode} onValueChange={(value) => setViewMode(value as any)}>
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="side-by-side">Side by Side</TabsTrigger>
                    <TabsTrigger value="unified">Unified View</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="side-by-side" className="space-y-4">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                      {/* Original Code */}
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                          <span className="text-sm font-medium">Original Code</span>
                        </div>
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4 overflow-x-auto">
                          <pre className="text-sm font-mono whitespace-pre-wrap text-red-800">
                            {selectedFixData.originalCode}
                          </pre>
                        </div>
                      </div>
                      
                      {/* Fixed Code */}
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                          <span className="text-sm font-medium">Fixed Code</span>
                        </div>
                        <div className="bg-green-50 border border-green-200 rounded-lg p-4 overflow-x-auto">
                          <pre className="text-sm font-mono whitespace-pre-wrap text-green-800">
                            {selectedFixData.fixedCode}
                          </pre>
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="unified" className="space-y-4">
                    <div className="bg-muted rounded-lg p-4 overflow-x-auto">
                      <div className="space-y-1 font-mono text-sm">
                        {selectedFixData.originalCode.split('\n').map((line, i) => (
                          <div key={`orig-${i}`} className="flex">
                            <span className="w-8 text-red-600 text-right mr-4">-{i + 1}</span>
                            <span className="bg-red-50 text-red-800 px-2 rounded flex-1">{line}</span>
                          </div>
                        ))}
                        <div className="my-2 border-t border-muted-foreground/20"></div>
                        {selectedFixData.fixedCode.split('\n').map((line, i) => (
                          <div key={`fixed-${i}`} className="flex">
                            <span className="w-8 text-green-600 text-right mr-4">+{i + 1}</span>
                            <span className="bg-green-50 text-green-800 px-2 rounded flex-1">{line}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>

                {/* Explanation */}
                <div className="p-4 bg-muted rounded-lg">
                  <h4 className="text-sm font-medium mb-2 flex items-center space-x-2">
                    <FileText className="h-4 w-4" />
                    <span>Explanation</span>
                  </h4>
                  <p className="text-sm text-muted-foreground">{selectedFixData.explanation}</p>
                </div>

                {/* Confidence Score */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">AI Confidence Score</span>
                    <span className="text-sm text-muted-foreground">{selectedFixData.confidence}%</span>
                  </div>
                  <Progress value={selectedFixData.confidence} className="w-full" />
                </div>

                {/* Actions */}
                {selectedFixData.status === 'pending' && (
                  <div className="flex space-x-3 pt-4 border-t">
                    <Button
                      onClick={() => onApplyFix(selectedFixData.id)}
                      className="flex-1"
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Apply Fix
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => onRejectFix(selectedFixData.id)}
                      className="flex-1"
                    >
                      <X className="h-4 w-4 mr-2" />
                      Reject
                    </Button>
                    <Button variant="outline" size="icon">
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                )}

                {selectedFixData.status === 'applied' && (
                  <div className="flex items-center justify-center p-4 bg-green-50 border border-green-200 rounded-lg">
                    <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                    <span className="text-sm font-medium text-green-800">Fix has been applied successfully</span>
                  </div>
                )}

                {selectedFixData.status === 'rejected' && (
                  <div className="flex items-center justify-center p-4 bg-red-50 border border-red-200 rounded-lg">
                    <X className="h-5 w-5 text-red-600 mr-2" />
                    <span className="text-sm font-medium text-red-800">Fix has been rejected</span>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="text-center py-12">
                <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
                  <Code className="h-8 w-8 text-muted-foreground" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">Select a Fix</h3>
                <p className="text-muted-foreground">
                  Choose a fix from the list to view the code diff and apply changes.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}