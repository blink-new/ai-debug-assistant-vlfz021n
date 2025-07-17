# 🎬 Screen Recording Analyzer

A comprehensive Python module for analyzing screen recordings of applications to extract user journey flows, detect UI issues, and compare actual behavior against expected specifications.

## 🎯 Overview

The Screen Recording Analyzer processes video files of application usage to:

- **Extract User Flows**: Automatically detect UI transitions and reconstruct user journey steps
- **Identify Issues**: Find stuck screens, errors, and unexpected behaviors
- **Compare Specifications**: Validate actual usage against expected user flows
- **Generate Reports**: Create detailed Markdown and JSON reports with actionable insights

## 🚀 Features

### 📥 Input Processing
- **Video Files**: Supports MP4, WebM, and other OpenCV-compatible formats
- **Enhanced Specifications**: JSON files with expected user flows and UI elements
- **Flexible Sampling**: Configurable frame sampling rate (default: 1 FPS)

### 🔍 Analysis Capabilities
- **Frame Comparison**: Detects significant visual changes between frames
- **OCR Text Extraction**: Uses Tesseract to extract text from UI elements
- **UI Element Recognition**: Identifies buttons, forms, navigation elements
- **Transition Classification**: Categorizes UI changes (authentication, navigation, errors, etc.)
- **Journey Reconstruction**: Builds complete user flow from detected transitions

### 📊 Output & Reporting
- **Markdown Reports**: Human-readable analysis summaries
- **JSON Results**: Structured data for programmatic processing
- **Key Frame Extraction**: Saves important transition frames for debugging
- **Issue Detection**: Identifies stuck screens, errors, and deviations

## 📦 Installation

### Prerequisites

```bash
# Install Python dependencies
pip install opencv-python pytesseract numpy

# Install Tesseract OCR (system dependency)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# Windows:
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Required Python Packages

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
opencv-python>=4.5.0
pytesseract>=0.3.8
numpy>=1.21.0
```

## 🛠️ Usage

### Basic Usage

```python
from screen_recording_analyzer import ScreenRecordingAnalyzer

# Initialize analyzer
analyzer = ScreenRecordingAnalyzer(
    output_dir="analysis_frames",
    sampling_fps=1.0
)

# Analyze video
results = analyzer.analyze_video(
    video_path="app_recording.mp4",
    enhanced_spec_path="app_specification.json"
)

# Generate report
analyzer.generate_report(results, "analysis_report.md")
```

### Enhanced Specification Format

Create a JSON file describing expected user flows:

```json
{
  "app_name": "Task Management App",
  "user_flows": [
    "User authentication and login",
    "Main dashboard navigation",
    "Task creation and management",
    "Task completion workflow"
  ],
  "features": [
    {
      "name": "Authentication",
      "flow": "User enters email/password and logs in",
      "expected_elements": ["Email", "Password", "Login", "Submit"]
    },
    {
      "name": "Dashboard",
      "flow": "User views task overview and navigation menu",
      "expected_elements": ["Dashboard", "Tasks", "Profile", "Settings"]
    }
  ],
  "critical_paths": [
    "Login → Dashboard → Add Task → Save → Task List",
    "Dashboard → Task Details → Edit → Update → Confirmation"
  ],
  "expected_screens": [
    "Login Screen",
    "Main Dashboard",
    "Task Creation Form",
    "Task List View"
  ]
}
```

### Advanced Configuration

```python
# Custom analyzer settings
analyzer = ScreenRecordingAnalyzer(
    output_dir="custom_frames",
    sampling_fps=2.0,  # Higher sampling rate
)

# Adjust detection thresholds
analyzer.change_threshold = 0.2  # More sensitive change detection
analyzer.text_similarity_threshold = 0.9  # Stricter text matching
```

## 📋 API Reference

### ScreenRecordingAnalyzer Class

#### Constructor
```python
ScreenRecordingAnalyzer(output_dir="output_frames", sampling_fps=1.0)
```

**Parameters:**
- `output_dir` (str): Directory to save extracted key frames
- `sampling_fps` (float): Frames per second to sample from video

#### Main Methods

##### analyze_video()
```python
analyze_video(video_path: str, enhanced_spec_path: str) -> Dict[str, Any]
```

Analyzes a screen recording video against specifications.

**Returns:** Complete analysis results dictionary with:
- `video_info`: Video metadata and processing stats
- `analysis_summary`: Key metrics and counts
- `user_journey`: Reconstructed user flow with steps and transitions
- `spec_comparison`: Comparison against expected specifications
- `frames`: Detailed frame analysis data

##### generate_report()
```python
generate_report(results: Dict[str, Any], output_path: str = "screen_analysis_report.md")
```

Generates a comprehensive Markdown report from analysis results.

#### Utility Methods

##### calculate_frame_difference()
```python
calculate_frame_difference(frame1: np.ndarray, frame2: np.ndarray) -> float
```

Calculates visual difference between two frames (0.0 = identical, 1.0 = completely different).

##### extract_text_from_frame()
```python
extract_text_from_frame(frame: np.ndarray) -> Tuple[str, List[str]]
```

Extracts text and UI elements from a video frame using OCR.

##### detect_ui_transitions()
```python
detect_ui_transitions(frames: List[FrameInfo]) -> List[UITransition]
```

Detects significant UI transitions between analyzed frames.

### Data Classes

#### FrameInfo
```python
@dataclass
class FrameInfo:
    frame_number: int
    timestamp: float
    frame_hash: str
    extracted_text: str
    is_key_frame: bool
    change_score: float
    ui_elements: List[str]
```

#### UITransition
```python
@dataclass
class UITransition:
    from_frame: int
    to_frame: int
    from_timestamp: float
    to_timestamp: float
    transition_type: str
    description: str
    confidence: float
```

#### UserJourney
```python
@dataclass
class UserJourney:
    steps: List[str]
    transitions: List[UITransition]
    total_duration: float
    key_frames: List[FrameInfo]
    issues: List[str]
```

## 📊 Output Examples

### Analysis Results Structure

```json
{
  "video_info": {
    "path": "app_recording.mp4",
    "duration": 45.2,
    "fps": 30.0,
    "total_frames": 1356,
    "processed_frames": 45
  },
  "analysis_summary": {
    "key_frames_detected": 8,
    "transitions_detected": 6,
    "journey_steps": 7,
    "issues_found": 2
  },
  "user_journey": {
    "steps": [
      "Started at: Login Screen",
      "User authentication at 2.1s",
      "Dashboard navigation at 5.3s",
      "Form submission at 12.7s"
    ],
    "transitions": [...],
    "issues": [
      "Screen appears stuck from 8.0s to 11.2s",
      "Error state detected at 15.5s"
    ]
  },
  "spec_comparison": {
    "spec_coverage": 0.85,
    "overall_score": 0.72,
    "missing_flows": ["User profile management"],
    "unexpected_flows": [],
    "ui_deviations": [...]
  }
}
```

### Sample Markdown Report

```markdown
# Screen Recording Analysis Report
*Generated on 2024-01-15 14:30:22*

## 📹 Video Information
- **File**: app_recording.mp4
- **Duration**: 45.2 seconds
- **FPS**: 30.0
- **Frames Processed**: 45

## 📊 Analysis Summary
- **Key Frames Detected**: 8
- **UI Transitions**: 6
- **Journey Steps**: 7
- **Issues Found**: 2

## 🗺️ User Journey Flow
1. Started at: Login Screen
2. User authentication at 2.1s
3. Dashboard navigation at 5.3s
4. Form submission at 12.7s

## 🔄 UI Transitions

### Authentication Transition
- **Time**: 1.5s → 2.1s
- **Description**: User logged in successfully
- **Confidence**: 85%

## 📋 Specification Comparison
- **Coverage**: 85%
- **Overall Score**: 72%

### ❌ Missing Expected Flows
- User profile management
- Advanced search functionality

## 🚨 Issues Detected
- Screen appears stuck from 8.0s to 11.2s
- Error state detected at 15.5s

## 💡 Recommendations
- Address detected UI issues and stuck screens
- Review missing flows and ensure all expected functionality is implemented
```

## 🧪 Testing

### Run Unit Tests

```bash
python test_screen_recording_analyzer.py
```

### Run Demo Analysis

The test file includes a comprehensive demo that creates sample video data and runs a complete analysis:

```python
# Run demo with sample data
python -c "from test_screen_recording_analyzer import run_demo_analysis; run_demo_analysis()"
```

### Test Coverage

The test suite includes:
- ✅ Frame hash calculation and comparison
- ✅ UI element extraction from OCR text
- ✅ Transition classification and detection
- ✅ Stuck screen detection
- ✅ Journey reconstruction
- ✅ Specification comparison
- ✅ Report generation
- ✅ Error handling
- ✅ Full integration test with sample video

## 🔧 Configuration

### OCR Settings

Adjust Tesseract OCR configuration for better text recognition:

```python
# In extract_text_from_frame method
text = pytesseract.image_to_string(
    thresh, 
    config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '
)
```

### Detection Thresholds

Fine-tune detection sensitivity:

```python
analyzer.change_threshold = 0.15        # Frame change detection
analyzer.text_similarity_threshold = 0.8  # Text similarity matching
```

### UI Element Patterns

Customize UI element recognition patterns:

```python
# Add custom patterns in extract_ui_elements method
custom_patterns = [
    r'\\b(Custom|Button|Pattern)\\b',
    r'\\b(App|Specific|Elements)\\b'
]
```

## 🚨 Troubleshooting

### Common Issues

**1. Tesseract Not Found**
```bash
# Install Tesseract OCR system dependency
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
brew install tesseract              # macOS
```

**2. Video File Not Opening**
```python
# Check supported formats
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Cannot open video file")
```

**3. Poor OCR Results**
- Ensure video has sufficient resolution (minimum 640x480)
- Check that text is clearly visible and not too small
- Consider preprocessing frames for better contrast

**4. Memory Issues with Large Videos**
- Reduce sampling_fps for longer videos
- Process videos in chunks if needed
- Monitor memory usage during analysis

### Performance Optimization

**For Large Videos:**
```python
# Reduce sampling rate
analyzer = ScreenRecordingAnalyzer(sampling_fps=0.5)

# Process in batches
# (implement custom batching logic if needed)
```

**For Better Accuracy:**
```python
# Increase sampling rate for detailed analysis
analyzer = ScreenRecordingAnalyzer(sampling_fps=2.0)

# Lower change threshold for subtle transitions
analyzer.change_threshold = 0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest test_screen_recording_analyzer.py -v

# Run linting
flake8 screen_recording_analyzer.py
black screen_recording_analyzer.py
```

## 📄 License

This module is part of the AI-Powered Debugging Assistant project.

## 🔗 Related Modules

- **PromptRefiner**: Enhances original specifications
- **CodeAnalyzer**: Analyzes codebase structure and quality
- **BugReportGenerator**: Creates comprehensive bug reports

---

*Built with ❤️ for the AI Debug Assistant platform*