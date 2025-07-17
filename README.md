# AI-Powered Debugging Assistant

An intelligent debugging platform that analyzes AI-generated and no-code applications by comparing original specifications with actual codebases, processing runtime behavior through screen recordings and logs, and generating comprehensive bug reports with automated code fixes.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  Python Backend │    │   AI Services   │
│                 │    │                 │    │                 │
│  • Dashboard    │◄──►│  • API Server   │◄──►│  • OpenAI GPT   │
│  • File Upload  │    │  • PromptRefiner│    │  • Code Analysis│
│  • Code Viewer  │    │  • CodeAnalyzer │    │  • Bug Detection│
│  • Bug Reports  │    │  • SpecComparer │    │                 │
│                 │    │  • DebugEngine  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API key (for AI analysis features)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-debug-assistant
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run with Docker Compose

**Development Mode (with hot reload):**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

**Production Mode:**
```bash
docker-compose --profile production up --build
```

**Standard Mode (development frontend + production backend):**
```bash
docker-compose up --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000 (development) or http://localhost (production)
- **Backend API**: http://localhost:8000
- **API Health Check**: http://localhost:8000/health

## 📦 Manual Installation

### Backend Setup

1. **Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install System Dependencies (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng libgl1-mesa-glx
```

3. **Install System Dependencies (macOS):**
```bash
brew install tesseract
```

4. **Set Environment Variables:**
```bash
export OPENAI_API_KEY=your_api_key_here
```

5. **Start Backend Server:**
```bash
python api_server.py
```

### Frontend Setup

1. **Install Node.js Dependencies:**
```bash
npm install
```

2. **Start Development Server:**
```bash
npm run dev
```

3. **Build for Production:**
```bash
npm run build
npm run preview
```

## 🧪 Testing Individual Modules

### 1. PromptRefiner Module

```bash
# Test prompt refinement
python test_prompt_refiner.py

# Manual testing
python -c "
from prompt_refiner import PromptRefiner
refiner = PromptRefiner()
result = refiner.refine_prompt('Build a todo app')
print(result)
"
```

### 2. CodeAnalyzer Module

```bash
# Test code analysis
python test_code_analyzer.py

# Analyze specific directory
python -c "
from code_analyzer import CodeAnalyzer
analyzer = CodeAnalyzer()
result = analyzer.analyze_codebase('src/')
print(result)
"
```

### 3. SpecComparer Module

```bash
# Test spec comparison
python test_spec_comparer.py

# Manual comparison
python -c "
from spec_comparer import SpecComparer
comparer = SpecComparer()
result = comparer.compare_spec_to_codebase('sample_enhanced_spec.json', 'src/')
print(result)
"
```

### 4. DebuggerEngine Module

```bash
# Test debugging engine
python test_debugger_engine.py

# Manual debugging
python -c "
from debugger_engine import DebuggerEngine
engine = DebuggerEngine()
engine.load_comparison_report('spec_comparison_report.json')
bugs = engine.analyze_bugs()
fixes = engine.generate_fixes()
print(f'Found {len(bugs)} bugs, generated {len(fixes)} fixes')
"
```

### 5. Full Analysis Pipeline

```bash
# Run complete analysis
python run_full_analysis.py

# With custom parameters
python -c "
from run_full_analysis import run_full_analysis
success = run_full_analysis('Build a todo app with React', 'src/')
print(f'Analysis completed: {success}')
"
```

## 🔧 API Endpoints

### Backend API (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/modules` | Available modules |
| POST | `/refine-prompt` | Enhance original prompt |
| POST | `/analyze-code` | Analyze codebase |
| POST | `/compare-spec` | Compare spec to code |
| POST | `/debug-analysis` | Generate bug reports |
| POST | `/full-analysis` | Run complete pipeline |

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Refine prompt
curl -X POST http://localhost:8000/refine-prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Build a todo app with React"}'

# Analyze codebase
curl -X POST http://localhost:8000/analyze-code \
  -H "Content-Type: application/json" \
  -d '{"codebase_path": "src/"}'

# Full analysis
curl -X POST http://localhost:8000/full-analysis \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Build a todo app", "codebase_path": "src/"}'
```

## 📋 Example Usage Flow

### 1. Basic Workflow

```bash
# 1. Start the services
docker-compose up --build

# 2. Open browser to http://localhost:3000

# 3. Upload your project files:
#    - Original prompt/specification
#    - Codebase (ZIP file or individual files)
#    - Optional: Screen recordings, logs

# 4. Click "Start Analysis" to begin the process

# 5. Review results:
#    - Enhanced specification
#    - Code analysis report
#    - Bug reports with severity levels
#    - Suggested fixes with code diffs

# 6. Apply fixes directly through the UI
```

### 2. Command Line Workflow

```bash
# Step 1: Refine the original prompt
python -c "
from prompt_refiner import PromptRefiner
refiner = PromptRefiner()
enhanced = refiner.refine_prompt('Build a todo app')
print('Enhanced spec created')
"

# Step 2: Analyze the codebase
python -c "
from code_analyzer import CodeAnalyzer
analyzer = CodeAnalyzer()
analysis = analyzer.analyze_codebase('src/')
print(f'Found {len(analysis.get(\"files\", []))} files')
"

# Step 3: Compare spec to code
python -c "
from spec_comparer import SpecComparer
comparer = SpecComparer()
comparison = comparer.compare_spec_to_codebase('sample_enhanced_spec.json', 'src/')
print('Comparison completed')
"

# Step 4: Generate bug reports and fixes
python -c "
from debugger_engine import DebuggerEngine
engine = DebuggerEngine()
engine.load_comparison_report('spec_comparison_report.json')
bugs = engine.analyze_bugs()
fixes = engine.generate_fixes()
print(f'Generated {len(fixes)} fixes for {len(bugs)} bugs')
"
```

### 3. API Integration Example

```javascript
// Frontend integration example
const analyzeProject = async (prompt, codebase) => {
  try {
    // Step 1: Refine prompt
    const refineResponse = await fetch('http://localhost:8000/refine-prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });
    const { enhanced_spec } = await refineResponse.json();

    // Step 2: Analyze code
    const analyzeResponse = await fetch('http://localhost:8000/analyze-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codebase_path: codebase })
    });
    const { analysis } = await analyzeResponse.json();

    // Step 3: Compare and debug
    const debugResponse = await fetch('http://localhost:8000/debug-analysis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        comparison_report: { enhanced_spec, analysis }
      })
    });
    const { bugs, fixes } = await debugResponse.json();

    return { bugs, fixes };
  } catch (error) {
    console.error('Analysis failed:', error);
  }
};
```

## 🐳 Docker Commands Reference

### Development

```bash
# Build and start development environment
docker-compose -f docker-compose.dev.yml up --build

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down

# Rebuild specific service
docker-compose -f docker-compose.dev.yml up --build backend
```

### Production

```bash
# Build and start production environment
docker-compose --profile production up --build

# Run in background
docker-compose --profile production up -d

# Scale services
docker-compose --profile production up --scale backend=2

# View production logs
docker-compose --profile production logs -f
```

### Maintenance

```bash
# Remove all containers and volumes
docker-compose down -v

# Clean up Docker system
docker system prune -a

# View container status
docker-compose ps

# Execute commands in running container
docker-compose exec backend python -c "print('Backend is running')"
docker-compose exec frontend npm run lint
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Missing**
   ```bash
   # Check if environment variable is set
   echo $OPENAI_API_KEY
   
   # Set in current session
   export OPENAI_API_KEY=your_key_here
   
   # Or add to .env file
   echo "OPENAI_API_KEY=your_key_here" >> .env
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 3000 or 8000
   lsof -i :3000
   lsof -i :8000
   
   # Kill process
   kill -9 <PID>
   
   # Or use different ports in docker-compose.yml
   ```

3. **Docker Build Fails**
   ```bash
   # Clean Docker cache
   docker builder prune -a
   
   # Rebuild without cache
   docker-compose build --no-cache
   
   # Check Docker logs
   docker-compose logs backend
   ```

4. **Frontend Can't Connect to Backend**
   ```bash
   # Check backend health
   curl http://localhost:8000/health
   
   # Verify CORS settings in api_server.py
   # Check VITE_API_URL in frontend environment
   ```

5. **Tesseract OCR Issues**
   ```bash
   # Install Tesseract in container
   docker-compose exec backend apt-get update
   docker-compose exec backend apt-get install tesseract-ocr
   
   # Test Tesseract
   docker-compose exec backend tesseract --version
   ```

### Performance Optimization

1. **Backend Performance**
   - Use Redis for caching analysis results
   - Implement async processing for large codebases
   - Add request queuing for concurrent analyses

2. **Frontend Performance**
   - Enable code splitting in Vite
   - Implement virtual scrolling for large file lists
   - Use React.memo for expensive components

3. **Docker Performance**
   - Use multi-stage builds to reduce image size
   - Implement health checks for better orchestration
   - Use Docker volumes for persistent data

## 📚 Module Documentation

### PromptRefiner
- **Purpose**: Enhances original prompts into comprehensive specifications
- **Input**: Original prompt string
- **Output**: Enhanced specification with detailed requirements
- **Dependencies**: Python standard library only

### CodeAnalyzer
- **Purpose**: Analyzes codebase structure and extracts features
- **Input**: Codebase directory path
- **Output**: Structured analysis of files, functions, and components
- **Dependencies**: OpenAI API, file system access

### SpecComparer
- **Purpose**: Compares enhanced specifications with actual code
- **Input**: Enhanced spec JSON and codebase path
- **Output**: Gap analysis and compliance report
- **Dependencies**: JSON processing, file analysis

### DebuggerEngine
- **Purpose**: Generates bug reports and automated fixes
- **Input**: Comparison report from SpecComparer
- **Output**: Bug reports with severity levels and code fixes
- **Dependencies**: OpenAI API for fix generation

### ScreenRecordingAnalyzer
- **Purpose**: Analyzes runtime behavior from screen recordings
- **Input**: Video files or screen recording data
- **Output**: UI interaction analysis and behavior patterns
- **Dependencies**: OpenCV, Tesseract OCR

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Run linting: `npm run lint` and `python -m flake8`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the `/docs` directory
- **API Reference**: Visit http://localhost:8000 when running
- **Discord**: Join our community server

---

**Built with ❤️ using React, Python, Docker, and OpenAI**