import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { 
  Bug, 
  Code, 
  Zap, 
  FileText, 
  Video, 
  CheckCircle,
  ArrowRight,
  Play,
  Sparkles
} from 'lucide-react'

interface WelcomeScreenProps {
  onGetStarted: () => void
  onSkip: () => void
}

export function WelcomeScreen({ onGetStarted, onSkip }: WelcomeScreenProps) {
  const [currentStep, setCurrentStep] = useState(0)

  const steps = [
    {
      icon: <FileText className="h-8 w-8 text-blue-500" />,
      title: "Upload Your Project",
      description: "Start by uploading your original specification and codebase files.",
      details: "Supports various file formats including JS, TS, Python, and more."
    },
    {
      icon: <Sparkles className="h-8 w-8 text-purple-500" />,
      title: "AI Analysis",
      description: "Our AI analyzes your code against the specification to identify issues.",
      details: "Advanced pattern recognition finds bugs, performance issues, and inconsistencies."
    },
    {
      icon: <Bug className="h-8 w-8 text-red-500" />,
      title: "Bug Detection",
      description: "Get detailed reports on bugs, security issues, and code quality problems.",
      details: "Each issue includes severity level, location, and detailed explanations."
    },
    {
      icon: <Code className="h-8 w-8 text-green-500" />,
      title: "Auto-Generated Fixes",
      description: "Receive AI-generated code fixes with explanations and confidence scores.",
      details: "Review, apply, or reject fixes with one-click integration."
    }
  ]

  const features = [
    { icon: <Zap className="h-5 w-5" />, text: "Lightning-fast analysis" },
    { icon: <CheckCircle className="h-5 w-5" />, text: "95% accuracy rate" },
    { icon: <Video className="h-5 w-5" />, text: "Screen recording support" },
    { icon: <Code className="h-5 w-5" />, text: "Multi-language support" }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center w-16 h-16 bg-primary rounded-2xl mx-auto mb-6 shadow-lg">
            <Bug className="h-8 w-8 text-primary-foreground" />
          </div>
          <h1 className="text-4xl font-bold text-foreground mb-4">
            Welcome to BugOff AI
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Intelligent debugging for no-code applications. Find bugs, get fixes, and improve your code quality with AI.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {features.map((feature, index) => (
            <Card key={index} className="text-center">
              <CardContent className="p-6">
                <div className="flex items-center justify-center w-12 h-12 bg-primary/10 rounded-lg mx-auto mb-4">
                  {feature.icon}
                </div>
                <p className="text-sm font-medium">{feature.text}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* How It Works */}
        <Card className="mb-8">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">How It Works</CardTitle>
            <CardDescription>
              Get started in 4 simple steps
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {steps.map((step, index) => (
                <div 
                  key={index} 
                  className={`relative p-6 rounded-lg border transition-all cursor-pointer ${
                    currentStep === index 
                      ? 'bg-primary/5 border-primary shadow-md' 
                      : 'bg-card hover:bg-muted/50'
                  }`}
                  onClick={() => setCurrentStep(index)}
                >
                  <div className="flex items-center justify-center w-12 h-12 bg-background rounded-lg mx-auto mb-4 shadow-sm">
                    {step.icon}
                  </div>
                  <h3 className="font-semibold text-center mb-2">{step.title}</h3>
                  <p className="text-sm text-muted-foreground text-center mb-3">
                    {step.description}
                  </p>
                  
                  {currentStep === index && (
                    <div className="mt-4 p-3 bg-muted rounded-lg">
                      <p className="text-xs text-muted-foreground">
                        {step.details}
                      </p>
                    </div>
                  )}
                  
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-bold">
                    {index + 1}
                  </div>
                  
                  {index < steps.length - 1 && (
                    <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2">
                      <ArrowRight className="h-4 w-4 text-muted-foreground" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold text-primary mb-2">10,000+</div>
              <div className="text-sm text-muted-foreground">Projects Analyzed</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">95%</div>
              <div className="text-sm text-muted-foreground">Bug Detection Rate</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">2.3min</div>
              <div className="text-sm text-muted-foreground">Average Analysis Time</div>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <Button 
            onClick={onGetStarted} 
            size="lg" 
            className="px-8 py-3 text-lg"
          >
            <Play className="h-5 w-5 mr-2" />
            Get Started
          </Button>
          <Button 
            onClick={onSkip} 
            variant="outline" 
            size="lg" 
            className="px-8 py-3 text-lg"
          >
            Skip Tour
          </Button>
        </div>

        {/* Pro Tip */}
        <div className="mt-8 text-center">
          <Badge variant="secondary" className="px-4 py-2">
            <Sparkles className="h-4 w-4 mr-2" />
            Pro Tip: Upload screen recordings for better runtime analysis
          </Badge>
        </div>
      </div>
    </div>
  )
}