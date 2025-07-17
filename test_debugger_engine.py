#!/usr/bin/env python3
"""
Test script for DebuggerEngine module

This script demonstrates the functionality of the DebuggerEngine
by running it with sample data and showing the generated fixes.
"""

import json
import os
import sys
from debugger_engine import DebuggerEngine, BugSeverity


def create_sample_comparison_report():
    """Create a comprehensive sample comparison report for testing"""
    sample_report = {
        "analysis_metadata": {
            "timestamp": "2024-01-15T10:30:00Z",
            "spec_file": "enhanced_spec.json",
            "codebase_path": "src/",
            "analyzer_version": "1.0"
        },
        "missing_features": [
            {
                "name": "User Authentication",
                "description": "Complete login and registration system with JWT tokens",
                "expected_file": "src/components/Auth.tsx",
                "expected_behavior": "Users should be able to sign in, register, and maintain session",
                "priority": "high",
                "estimated_effort": "4 hours"
            },
            {
                "name": "Real-time Notifications",
                "description": "WebSocket-based notification system",
                "expected_file": "src/services/notifications.ts",
                "expected_behavior": "Show real-time updates to users",
                "priority": "medium",
                "estimated_effort": "6 hours"
            },
            {
                "name": "Data Export Functionality",
                "description": "Export analysis results to PDF/CSV",
                "expected_file": "src/utils/export.ts",
                "expected_behavior": "Allow users to download reports",
                "priority": "low",
                "estimated_effort": "2 hours"
            }
        ],
        "implementation_gaps": [
            {
                "component": "Dashboard",
                "file": "src/components/Dashboard.tsx",
                "line": 45,
                "issue": "Missing data fetching logic",
                "current_code": "// TODO: Fetch dashboard data\nconst data = null;",
                "suggested_fix": "const [data, setData] = useState(null);\nconst [loading, setLoading] = useState(true);\n\nuseEffect(() => {\n  fetchDashboardData().then(setData).finally(() => setLoading(false));\n}, []);",
                "explanation": "Dashboard component doesn't load actual data from API",
                "impact": "high"
            },
            {
                "component": "BugReports",
                "file": "src/components/BugReports.tsx",
                "line": 78,
                "issue": "Incomplete error handling",
                "current_code": "fetch('/api/bugs').then(res => res.json())",
                "suggested_fix": "fetch('/api/bugs')\n  .then(res => {\n    if (!res.ok) throw new Error('Failed to fetch bugs');\n    return res.json();\n  })\n  .catch(error => {\n    console.error('Bug fetch error:', error);\n    setError(error.message);\n  })",
                "explanation": "API calls lack proper error handling",
                "impact": "medium"
            },
            {
                "component": "CodeDiffViewer",
                "file": "src/components/CodeDiffViewer.tsx",
                "line": 123,
                "issue": "Performance issue with large diffs",
                "current_code": "diffs.map((diff, index) => <DiffLine key={index} diff={diff} />)",
                "suggested_fix": "import { FixedSizeList as List } from 'react-window';\n\n<List\n  height={400}\n  itemCount={diffs.length}\n  itemSize={25}\n  itemData={diffs}\n>\n  {({ index, style, data }) => (\n    <div style={style}>\n      <DiffLine diff={data[index]} />\n    </div>\n  )}\n</List>",
                "explanation": "Large diff files cause performance issues",
                "impact": "medium"
            }
        ],
        "code_quality_issues": [
            {
                "type": "Security",
                "file": "src/api/auth.ts",
                "line": 23,
                "description": "Hardcoded API endpoint",
                "code": "const API_URL = 'http://localhost:3000';",
                "explanation": "Should use environment variable for API URL",
                "severity": "high",
                "fix_suggestion": "const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';"
            },
            {
                "type": "Performance",
                "file": "src/components/AnalysisResults.tsx",
                "line": 67,
                "description": "Unnecessary re-renders",
                "code": "const processedData = expensiveCalculation(rawData);",
                "explanation": "Expensive calculation runs on every render",
                "severity": "medium",
                "fix_suggestion": "const processedData = useMemo(() => expensiveCalculation(rawData), [rawData]);"
            },
            {
                "type": "Code Quality",
                "file": "src/utils/helpers.ts",
                "line": 34,
                "description": "Unused import",
                "code": "import { debounce, throttle } from 'lodash';",
                "explanation": "throttle is imported but never used",
                "severity": "low",
                "fix_suggestion": "import { debounce } from 'lodash';"
            },
            {
                "type": "Accessibility",
                "file": "src/components/ProjectUpload.tsx",
                "line": 89,
                "description": "Missing accessibility attributes",
                "code": "<button onClick={handleUpload}>Upload</button>",
                "explanation": "Button lacks proper accessibility attributes",
                "severity": "medium",
                "fix_suggestion": "<button onClick={handleUpload} aria-label='Upload project files' disabled={isUploading}>{isUploading ? 'Uploading...' : 'Upload'}</button>"
            },
            {
                "type": "Error Handling",
                "file": "src/services/api.ts",
                "line": 156,
                "description": "Unhandled promise rejection",
                "code": "apiCall().then(handleSuccess);",
                "explanation": "Promise rejection not handled",
                "severity": "high",
                "fix_suggestion": "apiCall().then(handleSuccess).catch(handleError);"
            }
        ],
        "architectural_issues": [
            {
                "issue": "Missing state management",
                "description": "Complex state is passed through props instead of using context or state management",
                "affected_files": ["src/App.tsx", "src/components/Dashboard.tsx"],
                "recommendation": "Implement React Context or Redux for global state"
            },
            {
                "issue": "No error boundaries",
                "description": "Application lacks error boundaries for graceful error handling",
                "affected_files": ["src/App.tsx"],
                "recommendation": "Add React Error Boundaries to catch and handle component errors"
            }
        ],
        "summary": {
            "total_issues": 11,
            "critical_issues": 0,
            "major_issues": 5,
            "minor_issues": 6,
            "estimated_fix_time": "16 hours",
            "code_coverage": "65%",
            "technical_debt_score": 7.2
        }
    }
    
    return sample_report


def test_debugger_engine():
    """Test the DebuggerEngine with comprehensive sample data"""
    print("🧪 Testing DebuggerEngine Module")
    print("=" * 50)
    
    # Create sample comparison report
    sample_report = create_sample_comparison_report()
    
    # Save sample report to file
    with open("test_comparison_report.json", 'w', encoding='utf-8') as f:
        json.dump(sample_report, f, indent=2)
    
    # Initialize debugger engine
    engine = DebuggerEngine(fixes_dir="test_fixes")
    
    # Load the sample report
    success = engine.load_comparison_report("test_comparison_report.json")
    if not success:
        print("❌ Failed to load comparison report")
        return False
    
    # Load optional data (stubbed)
    engine.load_logs("sample_logs.json")
    engine.load_ui_flows("sample_ui_flows.json")
    
    # Analyze bugs
    print("\n🔍 Analyzing bugs...")
    bugs = engine.analyze_bugs()
    
    print(f"✅ Found {len(bugs)} bugs")
    
    # Show some example bugs
    print("\n📋 Sample Bug Details:")
    for i, bug in enumerate(bugs[:3], 1):
        print(f"\n{i}. {bug.title}")
        print(f"   Severity: {bug.severity.value}")
        print(f"   File: {bug.file_path}")
        print(f"   Category: {bug.category}")
        print(f"   Description: {bug.description}")
        if bug.proposed_fix:
            print(f"   Has Fix: ✅")
        else:
            print(f"   Has Fix: ❌")
    
    # Generate fixes
    print("\n🔧 Generating fixes...")
    fixes = engine.generate_fixes()
    
    print(f"✅ Generated {len(fixes)} fixes")
    
    # Save fixes
    print("\n💾 Saving fixes...")
    save_success = engine.save_fixes()
    
    if save_success:
        print("✅ Fixes saved successfully")
    else:
        print("❌ Failed to save fixes")
    
    # Print comprehensive summary
    engine.print_summary()
    
    # Show generated files
    print(f"\n📁 Generated Files:")
    if os.path.exists("test_fixes"):
        files = os.listdir("test_fixes")
        for file in files:
            print(f"   📄 {file}")
    
    # Cleanup test files
    cleanup_files = ["test_comparison_report.json"]
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Cleaned up {file}")
    
    return True


def demonstrate_fix_application():
    """Demonstrate how fixes would be applied"""
    print("\n" + "=" * 60)
    print("🔧 FIX APPLICATION DEMONSTRATION")
    print("=" * 60)
    
    print("""
The DebuggerEngine generates fixes in multiple formats:

1. 📄 Individual Patch Files (.patch)
   - Each bug gets its own patch file
   - Contains unified diff format
   - Can be applied with 'git apply' or 'patch' command

2. 📊 Summary Report (JSON)
   - Complete analysis results
   - Bug categorization and severity
   - Fix success rates and statistics

3. 🔍 Detailed Bug Reports
   - Root cause analysis
   - Step-by-step fix instructions
   - Code examples and explanations

Example patch file content:
```
# Bug Fix: missing_0
# File: src/components/Auth.tsx
# Lines: 1-10

--- a/src/components/Auth.tsx
+++ b/src/components/Auth.tsx
@@ -1,3 +1,15 @@
-// TODO: Implement User Authentication
+import React, { useState } from 'react';
+import { login, register } from '../services/auth';
+
+function Auth() {
+  const [isLogin, setIsLogin] = useState(true);
+  
+  const handleSubmit = async (credentials) => {
+    try {
+      const result = isLogin ? await login(credentials) : await register(credentials);
+      // Handle successful authentication
+    } catch (error) {
+      // Handle authentication error
+    }
+  };
```

To apply fixes:
1. Review generated patch files in fixes/ directory
2. Apply individual patches: `git apply fixes/bug_id.patch`
3. Or use the summary report to manually implement fixes
4. Test each fix before applying the next one
""")


if __name__ == "__main__":
    try:
        # Run the test
        success = test_debugger_engine()
        
        if success:
            # Show fix application demo
            demonstrate_fix_application()
            print("\n✅ DebuggerEngine test completed successfully!")
        else:
            print("\n❌ DebuggerEngine test failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)