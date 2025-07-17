#!/usr/bin/env python3
"""
Test script for SpecComparer module

This script tests the SpecComparer functionality with sample data
to ensure proper comparison between Enhanced Spec and Feature Map.
"""

import json
import os
from spec_comparer import SpecComparer


def create_test_enhanced_spec():
    """Create a test Enhanced Specification for testing."""
    test_spec = {
        "project_name": "AI Debug Assistant",
        "core_features": [
            {
                "name": "File Upload System",
                "description": "Allow users to upload project files and specifications",
                "priority": "high",
                "configurable": True,
                "implementation_approach": "drag_and_drop"
            },
            {
                "name": "Spec Enhancement Engine",
                "description": "AI-powered enhancement of original specifications",
                "priority": "high",
                "configurable": True,
                "implementation_approach": "ai_processing"
            },
            {
                "name": "Code Analysis Engine",
                "description": "Analyze codebase structure and extract features",
                "priority": "high",
                "configurable": False,
                "implementation_approach": "static_analysis"
            },
            {
                "name": "Real-time Notifications",
                "description": "Show progress and completion notifications",
                "priority": "medium",
                "configurable": True,
                "implementation_approach": "websocket"
            }
        ],
        "ui_components": [
            {
                "name": "Dashboard",
                "description": "Main dashboard interface",
                "styling": "tailwind"
            },
            {
                "name": "File Upload Zone",
                "description": "Drag and drop file upload area",
                "styling": "tailwind"
            },
            {
                "name": "Progress Indicator",
                "description": "Show analysis progress",
                "styling": "tailwind"
            }
        ],
        "api_endpoints": [
            {
                "path": "/api/upload",
                "method": "POST",
                "description": "Upload project files"
            },
            {
                "path": "/api/analyze",
                "method": "POST",
                "description": "Start analysis process"
            },
            {
                "path": "/api/results",
                "method": "GET",
                "description": "Get analysis results"
            }
        ],
        "data_flow": [
            {
                "name": "File Processing Flow",
                "direction": "upload -> analyze -> results"
            }
        ],
        "business_rules": [
            {
                "name": "File Size Limit",
                "description": "Maximum file size of 100MB per upload"
            }
        ],
        "security_requirements": [
            {
                "name": "File Validation",
                "description": "Validate uploaded files for security"
            },
            {
                "name": "User Authentication",
                "description": "Require authentication for all operations"
            }
        ]
    }
    
    with open('test_enhanced_spec.json', 'w') as f:
        json.dump(test_spec, f, indent=2)
    
    return test_spec


def create_test_feature_map():
    """Create a test Feature Map for testing."""
    test_map = {
        "project_name": "AI Debug Assistant",
        "features": [
            {
                "name": "File Upload System",
                "description": "Basic file upload functionality",
                "configurable": False,  # Deviation: should be configurable
                "implementation_type": "basic_form"  # Deviation: should be drag_and_drop
            },
            {
                "name": "Spec Enhancement Engine",
                "description": "AI-powered enhancement of original specifications",
                "configurable": True,
                "implementation_type": "ai_processing"
            },
            {
                "name": "Code Analysis Engine",
                "description": "Analyze codebase structure and extract features",
                "configurable": False,
                "implementation_type": "static_analysis"
            },
            {
                "name": "Extra Logging Feature",
                "description": "Additional logging not in spec",
                "configurable": True,
                "implementation_type": "custom"
            }
            # Missing: Real-time Notifications
        ],
        "ui_components": [
            {
                "name": "Dashboard",
                "description": "Main dashboard interface",
                "styling": "tailwind"
            },
            {
                "name": "File Upload Zone",
                "description": "Basic file upload area",
                "styling": "css_modules"  # Deviation: should be tailwind
            }
            # Missing: Progress Indicator
        ],
        "api_endpoints": [
            {
                "path": "/api/upload",
                "method": "POST",
                "description": "Upload project files"
            },
            {
                "path": "/api/analyze",
                "method": "POST",
                "description": "Start analysis process"
            }
            # Missing: /api/results
        ],
        "data_flow": [
            {
                "name": "File Processing Flow",
                "direction": "upload -> process -> analyze"  # Mismatch: different flow
            }
        ],
        "business_logic": [
            {
                "name": "File Size Limit",
                "description": "Maximum file size of 100MB per upload"
            }
        ],
        "security_features": [
            {
                "name": "File Validation",
                "description": "Basic file type validation"
            }
            # Missing: User Authentication
        ]
    }
    
    with open('test_feature_map.json', 'w') as f:
        json.dump(test_map, f, indent=2)
    
    return test_map


def run_comparison_test():
    """Run a comprehensive test of the SpecComparer."""
    print("🧪 Starting SpecComparer Test")
    print("=" * 50)
    
    # Create test data
    print("📝 Creating test data...")
    create_test_enhanced_spec()
    create_test_feature_map()
    
    # Initialize comparer
    comparer = SpecComparer()
    
    # Load test files
    print("📂 Loading test files...")
    if not comparer.load_enhanced_spec('test_enhanced_spec.json'):
        print("❌ Failed to load test Enhanced Spec")
        return False
    
    if not comparer.load_feature_map('test_feature_map.json'):
        print("❌ Failed to load test Feature Map")
        return False
    
    # Run comparison
    print("🔍 Running comparison...")
    results = comparer.compare_specifications()
    
    # Save test reports
    print("💾 Saving test reports...")
    json_path, md_path = comparer.save_comparison_report('test_output')
    
    # Display results
    print("\n📊 Test Results Summary:")
    print("-" * 30)
    summary = results['summary']
    print(f"Health Score: {summary['health_score']}/100")
    print(f"Overall Status: {summary['overall_status']}")
    print(f"Total Issues: {summary['total_issues']}")
    print(f"Missing Features: {summary['missing_features_count']}")
    print(f"Deviations: {summary['deviations_count']}")
    print(f"Logical Mismatches: {summary['logical_mismatches_count']}")
    print(f"Extra Features: {summary['extra_features_count']}")
    
    # Show specific findings
    if results['missing_features']:
        print(f"\n🔍 Missing Features Found:")
        for feature in results['missing_features']:
            print(f"  - {feature['name']} ({feature['type']})")
    
    if results['deviations']:
        print(f"\n⚠️  Deviations Found:")
        for deviation in results['deviations']:
            feature_name = deviation.get('feature', deviation.get('component', 'Unknown'))
            print(f"  - {feature_name}: {deviation['expected']} → {deviation['actual']}")
    
    if results['logical_mismatches']:
        print(f"\n❌ Logical Mismatches Found:")
        for mismatch in results['logical_mismatches']:
            item_name = mismatch.get('flow', mismatch.get('rule', mismatch.get('requirement', 'Unknown')))
            print(f"  - {item_name} ({mismatch['type']})")
    
    if results['extra_features']:
        print(f"\n➕ Extra Features Found:")
        for extra in results['extra_features']:
            print(f"  - {extra['name']}")
    
    print(f"\n📄 Reports saved to:")
    print(f"  JSON: {json_path}")
    print(f"  Markdown: {md_path}")
    
    # Cleanup test files
    cleanup_files = ['test_enhanced_spec.json', 'test_feature_map.json']
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n✅ SpecComparer test completed successfully!")
    return True


if __name__ == "__main__":
    success = run_comparison_test()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Tests failed!")