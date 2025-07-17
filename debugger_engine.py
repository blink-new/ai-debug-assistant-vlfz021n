#!/usr/bin/env python3
"""
DebuggerEngine Module

This module analyzes comparison reports from spec_comparer.py and generates
specific code fixes for identified bugs. It categorizes issues by severity
and creates patch files with proposed solutions.

Author: AI Debugging Assistant
Version: 1.0
"""

import json
import os
import re
import difflib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class BugSeverity(Enum):
    """Bug severity levels"""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


@dataclass
class Bug:
    """Represents a detected bug with fix information"""
    id: str
    title: str
    description: str
    severity: BugSeverity
    file_path: str
    line_number: Optional[int]
    category: str
    original_code: Optional[str]
    proposed_fix: Optional[str]
    explanation: str
    confidence: float  # 0.0 to 1.0


@dataclass
class CodeFix:
    """Represents a code fix with diff information"""
    bug_id: str
    file_path: str
    original_lines: List[str]
    fixed_lines: List[str]
    start_line: int
    end_line: int
    unified_diff: str


class DebuggerEngine:
    """
    Main debugging engine that analyzes comparison reports and generates fixes
    """
    
    def __init__(self, fixes_dir: str = "fixes"):
        """
        Initialize the debugger engine
        
        Args:
            fixes_dir: Directory to save generated fixes
        """
        self.fixes_dir = fixes_dir
        self.bugs: List[Bug] = []
        self.fixes: List[CodeFix] = []
        self.comparison_report: Optional[Dict] = None
        self.logs_data: Optional[Dict] = None
        self.ui_flows: Optional[Dict] = None
        
        # Create fixes directory if it doesn't exist
        os.makedirs(self.fixes_dir, exist_ok=True)
        
        # Bug detection patterns
        self.bug_patterns = self._initialize_bug_patterns()
        
    def _initialize_bug_patterns(self) -> Dict[str, Dict]:
        """Initialize bug detection patterns and their fixes"""
        return {
            "missing_implementation": {
                "pattern": r"(TODO|FIXME|NotImplemented|placeholder)",
                "severity": BugSeverity.MAJOR,
                "category": "Implementation",
                "fix_template": "// Implement actual functionality here"
            },
            "unused_imports": {
                "pattern": r"import\s+.*\s+from\s+['\"].*['\"];?\s*$",
                "severity": BugSeverity.MINOR,
                "category": "Code Quality",
                "fix_template": "// Remove unused import"
            },
            "console_logs": {
                "pattern": r"console\.(log|debug|info|warn|error)",
                "severity": BugSeverity.MINOR,
                "category": "Code Quality",
                "fix_template": "// Remove debug console statement"
            },
            "hardcoded_values": {
                "pattern": r"(http://localhost|127\.0\.0\.1|hardcoded)",
                "severity": BugSeverity.MAJOR,
                "category": "Configuration",
                "fix_template": "// Use environment variable or config"
            },
            "missing_error_handling": {
                "pattern": r"(fetch|axios|api)\s*\([^)]*\)\s*(?!\.catch)",
                "severity": BugSeverity.MAJOR,
                "category": "Error Handling",
                "fix_template": ".catch(error => console.error('API Error:', error))"
            },
            "accessibility_issues": {
                "pattern": r"<(button|input|img)(?![^>]*alt=)(?![^>]*aria-)",
                "severity": BugSeverity.MAJOR,
                "category": "Accessibility",
                "fix_template": "// Add accessibility attributes"
            }
        }
    
    def load_comparison_report(self, report_path: str) -> bool:
        """
        Load comparison report from spec_comparer
        
        Args:
            report_path: Path to the comparison report JSON file
            
        Returns:
            bool: True if loaded successfully
        """
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                self.comparison_report = json.load(f)
            print(f"✅ Loaded comparison report from {report_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading comparison report: {e}")
            return False
    
    def load_logs(self, logs_path: str) -> bool:
        """
        Load runtime logs (stubbed for now)
        
        Args:
            logs_path: Path to logs file
            
        Returns:
            bool: True if loaded successfully
        """
        # Stubbed implementation - would parse actual log files
        self.logs_data = {
            "errors": [
                {"timestamp": "2024-01-15T10:30:00Z", "level": "error", "message": "API call failed"},
                {"timestamp": "2024-01-15T10:31:00Z", "level": "warning", "message": "Deprecated function used"}
            ],
            "performance": {
                "slow_queries": ["getUserData", "loadDashboard"],
                "memory_leaks": ["EventListener not cleaned up"]
            }
        }
        print(f"📋 Loaded logs data (stubbed)")
        return True
    
    def load_ui_flows(self, flows_path: str) -> bool:
        """
        Load extracted UI flows from screen recordings (stubbed for now)
        
        Args:
            flows_path: Path to UI flows file
            
        Returns:
            bool: True if loaded successfully
        """
        # Stubbed implementation - would analyze screen recording data
        self.ui_flows = {
            "user_actions": [
                {"action": "click", "element": "login-button", "timestamp": 1.5},
                {"action": "type", "element": "username-input", "timestamp": 2.0},
                {"action": "click", "element": "submit-button", "timestamp": 3.0}
            ],
            "ui_issues": [
                {"issue": "Button not responding", "severity": "major", "timestamp": 3.1},
                {"issue": "Loading spinner stuck", "severity": "critical", "timestamp": 5.0}
            ]
        }
        print(f"🎬 Loaded UI flows data (stubbed)")
        return True
    
    def analyze_bugs(self) -> List[Bug]:
        """
        Analyze loaded data to identify bugs
        
        Returns:
            List[Bug]: List of identified bugs
        """
        self.bugs = []
        
        if self.comparison_report:
            self._analyze_comparison_report()
        
        if self.logs_data:
            self._analyze_logs()
        
        if self.ui_flows:
            self._analyze_ui_flows()
        
        # Sort bugs by severity
        severity_order = {
            BugSeverity.CRITICAL: 0,
            BugSeverity.MAJOR: 1,
            BugSeverity.MINOR: 2,
            BugSeverity.INFO: 3
        }
        self.bugs.sort(key=lambda bug: severity_order[bug.severity])
        
        return self.bugs
    
    def _analyze_comparison_report(self):
        """Analyze comparison report for bugs"""
        if not self.comparison_report:
            return
        
        # Analyze missing features
        missing_features = self.comparison_report.get('missing_features', [])
        for feature in missing_features:
            bug = Bug(
                id=f"missing_{len(self.bugs)}",
                title=f"Missing Feature: {feature.get('name', 'Unknown')}",
                description=feature.get('description', 'Feature not implemented'),
                severity=BugSeverity.MAJOR,
                file_path=feature.get('expected_file', 'unknown'),
                line_number=None,
                category="Missing Implementation",
                original_code=None,
                proposed_fix=self._generate_feature_fix(feature),
                explanation=f"This feature was specified but not found in the codebase",
                confidence=0.8
            )
            self.bugs.append(bug)
        
        # Analyze implementation gaps
        gaps = self.comparison_report.get('implementation_gaps', [])
        for gap in gaps:
            bug = Bug(
                id=f"gap_{len(self.bugs)}",
                title=f"Implementation Gap: {gap.get('component', 'Unknown')}",
                description=gap.get('issue', 'Implementation incomplete'),
                severity=BugSeverity.MAJOR,
                file_path=gap.get('file', 'unknown'),
                line_number=gap.get('line', None),
                category="Implementation Gap",
                original_code=gap.get('current_code', None),
                proposed_fix=gap.get('suggested_fix', 'TODO: Implement missing functionality'),
                explanation=gap.get('explanation', 'Code does not match specification'),
                confidence=0.7
            )
            self.bugs.append(bug)
        
        # Analyze code quality issues
        quality_issues = self.comparison_report.get('code_quality_issues', [])
        for issue in quality_issues:
            severity = BugSeverity.MINOR
            if 'security' in issue.get('type', '').lower():
                severity = BugSeverity.CRITICAL
            elif 'performance' in issue.get('type', '').lower():
                severity = BugSeverity.MAJOR
            
            bug = Bug(
                id=f"quality_{len(self.bugs)}",
                title=f"Code Quality: {issue.get('type', 'Unknown')}",
                description=issue.get('description', 'Code quality issue detected'),
                severity=severity,
                file_path=issue.get('file', 'unknown'),
                line_number=issue.get('line', None),
                category="Code Quality",
                original_code=issue.get('code', None),
                proposed_fix=self._generate_quality_fix(issue),
                explanation=issue.get('explanation', 'Code quality can be improved'),
                confidence=0.6
            )
            self.bugs.append(bug)
    
    def _analyze_logs(self):
        """Analyze runtime logs for bugs"""
        if not self.logs_data:
            return
        
        # Analyze errors from logs
        errors = self.logs_data.get('errors', [])
        for error in errors:
            severity = BugSeverity.CRITICAL if error['level'] == 'error' else BugSeverity.MAJOR
            
            bug = Bug(
                id=f"log_error_{len(self.bugs)}",
                title=f"Runtime Error: {error['message'][:50]}...",
                description=error['message'],
                severity=severity,
                file_path="runtime",
                line_number=None,
                category="Runtime Error",
                original_code=None,
                proposed_fix=self._generate_error_fix(error),
                explanation=f"Error occurred at {error['timestamp']}",
                confidence=0.9
            )
            self.bugs.append(bug)
        
        # Analyze performance issues
        performance = self.logs_data.get('performance', {})
        slow_queries = performance.get('slow_queries', [])
        for query in slow_queries:
            bug = Bug(
                id=f"perf_{len(self.bugs)}",
                title=f"Performance Issue: Slow {query}",
                description=f"Function {query} is performing slowly",
                severity=BugSeverity.MAJOR,
                file_path="performance",
                line_number=None,
                category="Performance",
                original_code=None,
                proposed_fix=f"// Optimize {query} function with caching or better algorithm",
                explanation="Function execution time exceeds acceptable limits",
                confidence=0.7
            )
            self.bugs.append(bug)
    
    def _analyze_ui_flows(self):
        """Analyze UI flows for bugs"""
        if not self.ui_flows:
            return
        
        # Analyze UI issues from flows
        ui_issues = self.ui_flows.get('ui_issues', [])
        for issue in ui_issues:
            severity_map = {
                'critical': BugSeverity.CRITICAL,
                'major': BugSeverity.MAJOR,
                'minor': BugSeverity.MINOR
            }
            severity = severity_map.get(issue.get('severity', 'minor'), BugSeverity.MINOR)
            
            bug = Bug(
                id=f"ui_{len(self.bugs)}",
                title=f"UI Issue: {issue['issue']}",
                description=f"UI problem detected at {issue['timestamp']}s",
                severity=severity,
                file_path="ui_component",
                line_number=None,
                category="User Interface",
                original_code=None,
                proposed_fix=self._generate_ui_fix(issue),
                explanation="Issue detected during user interaction flow",
                confidence=0.8
            )
            self.bugs.append(bug)
    
    def _generate_feature_fix(self, feature: Dict) -> str:
        """Generate fix for missing feature"""
        feature_name = feature.get('name', 'Unknown')
        return f"""
// TODO: Implement {feature_name}
// Description: {feature.get('description', 'No description')}
// Expected behavior: {feature.get('expected_behavior', 'Not specified')}

function implement{feature_name.replace(' ', '')}() {{
    // Add implementation here
    throw new Error('Feature not implemented: {feature_name}');
}}
"""
    
    def _generate_quality_fix(self, issue: Dict) -> str:
        """Generate fix for code quality issue"""
        issue_type = issue.get('type', 'unknown')
        
        if 'unused' in issue_type.lower():
            return "// Remove unused code"
        elif 'security' in issue_type.lower():
            return "// Add input validation and sanitization"
        elif 'performance' in issue_type.lower():
            return "// Optimize for better performance"
        else:
            return f"// Fix {issue_type} issue"
    
    def _generate_error_fix(self, error: Dict) -> str:
        """Generate fix for runtime error"""
        message = error['message']
        
        if 'api' in message.lower():
            return """
try {
    // API call here
} catch (error) {
    console.error('API Error:', error);
    // Handle error appropriately
}
"""
        elif 'undefined' in message.lower():
            return "// Add null/undefined checks before accessing properties"
        else:
            return f"// Handle error: {message}"
    
    def _generate_ui_fix(self, issue: Dict) -> str:
        """Generate fix for UI issue"""
        issue_text = issue['issue']
        
        if 'button' in issue_text.lower():
            return """
// Ensure button has proper event handlers
<button 
    onClick={handleClick}
    disabled={isLoading}
    aria-label="Action button"
>
    {isLoading ? 'Loading...' : 'Click me'}
</button>
"""
        elif 'loading' in issue_text.lower():
            return """
// Add proper loading state management
const [isLoading, setIsLoading] = useState(false);

// Show loading indicator
{isLoading && <LoadingSpinner />}
"""
        else:
            return f"// Fix UI issue: {issue_text}"
    
    def generate_fixes(self) -> List[CodeFix]:
        """
        Generate code fixes for identified bugs
        
        Returns:
            List[CodeFix]: List of generated fixes
        """
        self.fixes = []
        
        for bug in self.bugs:
            if bug.proposed_fix and bug.file_path != 'unknown':
                fix = self._create_code_fix(bug)
                if fix:
                    self.fixes.append(fix)
        
        return self.fixes
    
    def _create_code_fix(self, bug: Bug) -> Optional[CodeFix]:
        """Create a code fix from a bug"""
        if not bug.original_code or not bug.proposed_fix:
            return None
        
        original_lines = bug.original_code.split('\n')
        fixed_lines = bug.proposed_fix.split('\n')
        
        # Generate unified diff
        diff = difflib.unified_diff(
            original_lines,
            fixed_lines,
            fromfile=f"a/{bug.file_path}",
            tofile=f"b/{bug.file_path}",
            lineterm=''
        )
        unified_diff = '\n'.join(diff)
        
        return CodeFix(
            bug_id=bug.id,
            file_path=bug.file_path,
            original_lines=original_lines,
            fixed_lines=fixed_lines,
            start_line=bug.line_number or 1,
            end_line=(bug.line_number or 1) + len(original_lines),
            unified_diff=unified_diff
        )
    
    def save_fixes(self) -> bool:
        """
        Save generated fixes to patch files
        
        Returns:
            bool: True if saved successfully
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save individual patch files
            for fix in self.fixes:
                patch_filename = f"{fix.bug_id}_{timestamp}.patch"
                patch_path = os.path.join(self.fixes_dir, patch_filename)
                
                with open(patch_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Bug Fix: {fix.bug_id}\n")
                    f.write(f"# File: {fix.file_path}\n")
                    f.write(f"# Lines: {fix.start_line}-{fix.end_line}\n\n")
                    f.write(fix.unified_diff)
            
            # Save summary report
            summary_path = os.path.join(self.fixes_dir, f"fixes_summary_{timestamp}.json")
            summary = {
                "timestamp": timestamp,
                "total_bugs": len(self.bugs),
                "total_fixes": len(self.fixes),
                "bugs_by_severity": self._get_bugs_by_severity(),
                "bugs": [self._bug_to_dict(bug) for bug in self.bugs],
                "fixes": [self._fix_to_dict(fix) for fix in self.fixes]
            }
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, default=str)
            
            print(f"💾 Saved {len(self.fixes)} fixes to {self.fixes_dir}/")
            return True
            
        except Exception as e:
            print(f"❌ Error saving fixes: {e}")
            return False
    
    def _get_bugs_by_severity(self) -> Dict[str, int]:
        """Get bug count by severity"""
        counts = {severity.value: 0 for severity in BugSeverity}
        for bug in self.bugs:
            counts[bug.severity.value] += 1
        return counts
    
    def _bug_to_dict(self, bug: Bug) -> Dict:
        """Convert Bug to dictionary"""
        return {
            "id": bug.id,
            "title": bug.title,
            "description": bug.description,
            "severity": bug.severity.value,
            "file_path": bug.file_path,
            "line_number": bug.line_number,
            "category": bug.category,
            "confidence": bug.confidence,
            "has_fix": bug.proposed_fix is not None
        }
    
    def _fix_to_dict(self, fix: CodeFix) -> Dict:
        """Convert CodeFix to dictionary"""
        return {
            "bug_id": fix.bug_id,
            "file_path": fix.file_path,
            "start_line": fix.start_line,
            "end_line": fix.end_line,
            "lines_changed": len(fix.fixed_lines)
        }
    
    def print_summary(self):
        """Print summary of analysis and fixes"""
        print("\n" + "="*60)
        print("🔍 DEBUGGER ENGINE ANALYSIS SUMMARY")
        print("="*60)
        
        if not self.bugs:
            print("✅ No bugs detected!")
            return
        
        # Bug summary by severity
        severity_counts = self._get_bugs_by_severity()
        print(f"\n📊 BUGS BY SEVERITY:")
        for severity, count in severity_counts.items():
            if count > 0:
                emoji = {"critical": "🔴", "major": "🟠", "minor": "🟡", "info": "🔵"}
                print(f"   {emoji.get(severity, '⚪')} {severity.upper()}: {count}")
        
        print(f"\n📋 DETAILED BUG REPORT:")
        for i, bug in enumerate(self.bugs[:10], 1):  # Show top 10
            print(f"\n{i}. [{bug.severity.value.upper()}] {bug.title}")
            print(f"   📁 File: {bug.file_path}")
            if bug.line_number:
                print(f"   📍 Line: {bug.line_number}")
            print(f"   📝 {bug.description}")
            print(f"   🎯 Confidence: {bug.confidence:.1%}")
            if bug.proposed_fix:
                print(f"   ✅ Fix available")
        
        if len(self.bugs) > 10:
            print(f"\n... and {len(self.bugs) - 10} more bugs")
        
        print(f"\n🔧 FIXES GENERATED: {len(self.fixes)}")
        print(f"💾 Fixes saved to: {self.fixes_dir}/")
        
        print("\n" + "="*60)


def main():
    """Main function for testing the debugger engine"""
    print("🚀 Starting Debugger Engine...")
    
    # Initialize engine
    engine = DebuggerEngine()
    
    # Load comparison report
    if os.path.exists("spec_comparison_report.json"):
        engine.load_comparison_report("spec_comparison_report.json")
    else:
        print("⚠️  No comparison report found, creating sample data...")
        # Create sample data for testing
        sample_report = {
            "missing_features": [
                {
                    "name": "User Authentication",
                    "description": "Login and registration functionality",
                    "expected_file": "src/components/Auth.tsx",
                    "expected_behavior": "Allow users to sign in and register"
                }
            ],
            "implementation_gaps": [
                {
                    "component": "Dashboard",
                    "file": "src/components/Dashboard.tsx",
                    "line": 45,
                    "issue": "Missing data fetching logic",
                    "current_code": "// TODO: Fetch dashboard data",
                    "suggested_fix": "const data = await fetchDashboardData();",
                    "explanation": "Dashboard component doesn't load actual data"
                }
            ],
            "code_quality_issues": [
                {
                    "type": "Security",
                    "file": "src/api/auth.ts",
                    "line": 23,
                    "description": "Hardcoded API endpoint",
                    "code": "const API_URL = 'http://localhost:3000';",
                    "explanation": "Should use environment variable"
                }
            ]
        }
        
        with open("spec_comparison_report.json", 'w') as f:
            json.dump(sample_report, f, indent=2)
        
        engine.load_comparison_report("spec_comparison_report.json")
    
    # Load optional data (stubbed)
    engine.load_logs("logs.json")  # Stubbed
    engine.load_ui_flows("ui_flows.json")  # Stubbed
    
    # Analyze bugs
    bugs = engine.analyze_bugs()
    
    # Generate fixes
    fixes = engine.generate_fixes()
    
    # Save fixes
    engine.save_fixes()
    
    # Print summary
    engine.print_summary()


if __name__ == "__main__":
    main()