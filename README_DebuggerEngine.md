# DebuggerEngine Module

## Overview

The DebuggerEngine is a comprehensive Python module that analyzes comparison reports from the spec_comparer and generates specific code fixes for identified bugs. It categorizes issues by severity and creates patch files with proposed solutions.

## Features

### 🔍 Bug Analysis
- **Multi-source Analysis**: Processes comparison reports, runtime logs, and UI flow data
- **Severity Classification**: Categorizes bugs as Critical, Major, Minor, or Info
- **Pattern Recognition**: Uses regex patterns to identify common code issues
- **Confidence Scoring**: Assigns confidence levels to bug detections

### 🔧 Fix Generation
- **Automated Code Fixes**: Generates specific code solutions for identified bugs
- **Patch File Creation**: Creates unified diff patches for easy application
- **Multiple Fix Formats**: Supports various fix types (implementation, quality, security)
- **Contextual Solutions**: Provides fixes tailored to specific bug types

### 📊 Reporting
- **Comprehensive Summaries**: Detailed analysis reports with statistics
- **JSON Export**: Machine-readable fix summaries
- **Severity Breakdown**: Bug counts by severity level
- **Fix Success Tracking**: Monitors which fixes can be automatically generated

## Architecture

```
DebuggerEngine
├── Bug Detection
│   ├── Comparison Report Analysis
│   ├── Runtime Log Analysis
│   └── UI Flow Analysis
├── Fix Generation
│   ├── Pattern-based Fixes
│   ├── Template Solutions
│   └── Contextual Repairs
└── Output Generation
    ├── Patch Files (.patch)
    ├── Summary Reports (JSON)
    └── Console Summaries
```

## Usage

### Basic Usage

```python
from debugger_engine import DebuggerEngine

# Initialize engine
engine = DebuggerEngine(fixes_dir="fixes")

# Load comparison report
engine.load_comparison_report("spec_comparison_report.json")

# Optional: Load additional data
engine.load_logs("runtime_logs.json")
engine.load_ui_flows("ui_flows.json")

# Analyze bugs
bugs = engine.analyze_bugs()

# Generate fixes
fixes = engine.generate_fixes()

# Save fixes to files
engine.save_fixes()

# Print summary
engine.print_summary()
```

### Advanced Usage

```python
# Custom fixes directory
engine = DebuggerEngine(fixes_dir="custom_fixes")

# Access individual bugs
for bug in engine.bugs:
    print(f"Bug: {bug.title}")
    print(f"Severity: {bug.severity.value}")
    print(f"File: {bug.file_path}")
    print(f"Fix: {bug.proposed_fix}")

# Access generated fixes
for fix in engine.fixes:
    print(f"Fix for {fix.bug_id}")
    print(f"File: {fix.file_path}")
    print(f"Lines: {fix.start_line}-{fix.end_line}")
    print(fix.unified_diff)
```

## Bug Categories

### 1. Missing Implementation
- **Pattern**: `TODO`, `FIXME`, `NotImplemented`, `placeholder`
- **Severity**: Major
- **Fix**: Provides implementation templates

### 2. Code Quality Issues
- **Unused Imports**: Identifies and removes unused imports
- **Console Logs**: Removes debug console statements
- **Hardcoded Values**: Replaces with environment variables

### 3. Security Issues
- **Hardcoded Credentials**: Detects hardcoded API keys or URLs
- **Missing Input Validation**: Identifies unvalidated inputs
- **Severity**: Critical/Major

### 4. Performance Issues
- **Missing Error Handling**: Detects unhandled promises/API calls
- **Inefficient Rendering**: Identifies performance bottlenecks
- **Memory Leaks**: Detects potential memory issues

### 5. Accessibility Issues
- **Missing ARIA Labels**: Detects buttons/inputs without accessibility attributes
- **Keyboard Navigation**: Identifies keyboard accessibility issues
- **Severity**: Major

## Input Formats

### Comparison Report (Required)
```json
{
  "missing_features": [
    {
      "name": "Feature Name",
      "description": "Feature description",
      "expected_file": "src/component.tsx",
      "expected_behavior": "Expected behavior"
    }
  ],
  "implementation_gaps": [
    {
      "component": "ComponentName",
      "file": "src/component.tsx",
      "line": 45,
      "issue": "Issue description",
      "current_code": "current code",
      "suggested_fix": "suggested fix"
    }
  ],
  "code_quality_issues": [
    {
      "type": "Security",
      "file": "src/file.ts",
      "line": 23,
      "description": "Issue description",
      "code": "problematic code"
    }
  ]
}
```

### Runtime Logs (Optional)
```json
{
  "errors": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "level": "error",
      "message": "Error message"
    }
  ],
  "performance": {
    "slow_queries": ["functionName1", "functionName2"],
    "memory_leaks": ["EventListener not cleaned up"]
  }
}
```

### UI Flows (Optional)
```json
{
  "user_actions": [
    {
      "action": "click",
      "element": "button-id",
      "timestamp": 1.5
    }
  ],
  "ui_issues": [
    {
      "issue": "Button not responding",
      "severity": "major",
      "timestamp": 3.1
    }
  ]
}
```

## Output Formats

### Patch Files
- **Format**: Unified diff format
- **Naming**: `{bug_id}_{timestamp}.patch`
- **Application**: Can be applied with `git apply` or `patch` command

### Summary Report
```json
{
  "timestamp": "20240115_103000",
  "total_bugs": 15,
  "total_fixes": 12,
  "bugs_by_severity": {
    "critical": 2,
    "major": 8,
    "minor": 5,
    "info": 0
  },
  "bugs": [...],
  "fixes": [...]
}
```

## Bug Severity Levels

| Severity | Description | Examples |
|----------|-------------|----------|
| **Critical** | Security vulnerabilities, app-breaking issues | Hardcoded API keys, unhandled errors |
| **Major** | Functionality issues, missing features | Missing implementations, API errors |
| **Minor** | Code quality, performance issues | Unused imports, console logs |
| **Info** | Suggestions, best practices | Code style, documentation |

## Fix Types

### 1. Template Fixes
- Pre-defined solutions for common patterns
- Quick fixes for standard issues
- High confidence level

### 2. Contextual Fixes
- Analyzed based on surrounding code
- Tailored to specific implementation
- Medium confidence level

### 3. Suggested Fixes
- General recommendations
- Require manual review
- Lower confidence level

## Testing

Run the test suite to verify functionality:

```bash
python test_debugger_engine.py
```

The test creates sample data and demonstrates:
- Bug detection from comparison reports
- Fix generation for various bug types
- Patch file creation
- Summary report generation

## Integration

### With spec_comparer.py
```python
# Generate comparison report first
from spec_comparer import SpecComparer
comparer = SpecComparer()
comparer.compare_spec_to_codebase("enhanced_spec.json", "src/")

# Then analyze with debugger engine
from debugger_engine import DebuggerEngine
engine = DebuggerEngine()
engine.load_comparison_report("spec_comparison_report.json")
engine.analyze_bugs()
```

### With CI/CD Pipeline
```yaml
# Example GitHub Actions integration
- name: Run Bug Analysis
  run: |
    python spec_comparer.py
    python debugger_engine.py
    
- name: Create PR with Fixes
  run: |
    git apply fixes/*.patch
    git commit -m "Auto-fix: Apply generated bug fixes"
```

## Configuration

### Custom Bug Patterns
```python
engine = DebuggerEngine()
engine.bug_patterns["custom_pattern"] = {
    "pattern": r"your_regex_pattern",
    "severity": BugSeverity.MAJOR,
    "category": "Custom Category",
    "fix_template": "Your fix template"
}
```

### Custom Fix Templates
```python
def custom_fix_generator(bug):
    if "custom_condition" in bug.description:
        return "custom fix code"
    return None

engine._generate_custom_fix = custom_fix_generator
```

## Limitations

1. **Static Analysis Only**: Cannot detect runtime-specific issues without logs
2. **Pattern-based Detection**: May miss complex logical errors
3. **Language Specific**: Currently optimized for JavaScript/TypeScript/React
4. **Manual Review Required**: Generated fixes should be reviewed before application

## Future Enhancements

- [ ] Support for more programming languages
- [ ] Machine learning-based bug detection
- [ ] Integration with popular IDEs
- [ ] Real-time analysis during development
- [ ] Automated fix testing and validation
- [ ] Custom rule configuration UI

## Dependencies

```
- Python 3.7+
- json (built-in)
- os (built-in)
- re (built-in)
- difflib (built-in)
- dataclasses (built-in)
- enum (built-in)
- datetime (built-in)
```

## Contributing

1. Add new bug patterns to `_initialize_bug_patterns()`
2. Implement fix generators for new bug types
3. Add test cases in `test_debugger_engine.py`
4. Update documentation for new features

## License

This module is part of the AI-Powered Debugging Assistant project.