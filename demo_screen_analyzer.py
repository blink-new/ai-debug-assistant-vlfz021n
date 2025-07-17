#!/usr/bin/env python3
"""
Screen Recording Analyzer Demo Script

This script demonstrates the complete functionality of the ScreenRecordingAnalyzer
module with sample data and comprehensive examples.

Author: AI Debug Assistant
Version: 1.0.0
"""

import os
import json
import tempfile
import cv2
import numpy as np
from pathlib import Path
from screen_recording_analyzer import ScreenRecordingAnalyzer


def create_demo_video(output_path: str, duration_per_frame: int = 2) -> None:
    """
    Create a demonstration video with different UI screens.
    
    Args:
        output_path: Path to save the demo video
        duration_per_frame: Duration in seconds for each frame
    """
    print("🎥 Creating demonstration video...")
    
    # Define demo screens with colors and text
    demo_screens = [
        {
            "color": (240, 240, 255),  # Light blue
            "texts": ["TaskApp Login", "Email: user@example.com", "Password: ********", "[ Login Button ]"],
            "description": "Login Screen"
        },
        {
            "color": (240, 240, 255),  # Same color (simulating stuck screen)
            "texts": ["TaskApp Login", "Email: user@example.com", "Password: ********", "[ Login Button ]"],
            "description": "Login Screen (Stuck)"
        },
        {
            "color": (200, 255, 200),  # Light green
            "texts": ["Dashboard", "Welcome, User!", "Tasks: 5 Active", "[ Add Task ] [ Profile ] [ Settings ]"],
            "description": "Main Dashboard"
        },
        {
            "color": (255, 240, 200),  # Light yellow
            "texts": ["New Task", "Title: [_______________]", "Description: [_______________]", "Due Date: [_______________]", "[ Save ] [ Cancel ]"],
            "description": "Task Creation Form"
        },
        {
            "color": (255, 240, 200),  # Same color (form validation)
            "texts": ["New Task", "Title: [Buy groceries____]", "Description: [Weekly shopping___]", "Due Date: [2024-01-20_____]", "[ Save ] [ Cancel ]"],
            "description": "Form Filled"
        },
        {
            "color": (200, 255, 200),  # Light green
            "texts": ["Success!", "Task 'Buy groceries' created", "[ Continue ] [ Add Another ]"],
            "description": "Success Confirmation"
        },
        {
            "color": (220, 220, 255),  # Light purple
            "texts": ["Task List", "1. Buy groceries (Due: Jan 20)", "2. Team meeting (Due: Jan 18)", "3. Code review (Due: Jan 19)", "[ Edit ] [ Delete ] [ Complete ]"],
            "description": "Task List View"
        },
        {
            "color": (255, 200, 200),  # Light red
            "texts": ["Error", "Network connection failed", "Unable to save changes", "[ Retry ] [ Cancel ]"],
            "description": "Error State"
        }
    ]
    
    # Video settings
    width, height = 800, 600
    fps = 2  # Low FPS for easier analysis
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Create video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for i, screen in enumerate(demo_screens):
        print(f"  📱 Creating screen {i+1}: {screen['description']}")
        
        # Create frame with background color
        frame = np.full((height, width, 3), screen['color'], dtype=np.uint8)
        
        # Add text lines
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2
        text_color = (0, 0, 0)  # Black text
        
        # Calculate starting position for centered text
        line_height = 40
        total_text_height = len(screen['texts']) * line_height
        start_y = (height - total_text_height) // 2
        
        for j, text in enumerate(screen['texts']):
            # Get text size for centering
            (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
            x = (width - text_width) // 2
            y = start_y + (j * line_height) + text_height
            
            # Add text to frame
            cv2.putText(frame, text, (x, y), font, font_scale, text_color, thickness)
        
        # Write frame multiple times to create duration
        frames_to_write = fps * duration_per_frame
        for _ in range(frames_to_write):
            out.write(frame)
    
    out.release()
    print(f"✅ Demo video created: {output_path}")


def create_demo_spec() -> dict:
    """
    Create a demonstration enhanced specification.
    
    Returns:
        Dictionary containing the demo specification
    """
    return {
        "app_name": "TaskApp - Task Management System",
        "version": "1.0.0",
        "user_flows": [
            "User authentication and login",
            "Main dashboard navigation",
            "Task creation workflow",
            "Task list management",
            "Error handling and recovery"
        ],
        "features": [
            {
                "name": "Authentication",
                "flow": "User enters email and password, clicks login button",
                "expected_elements": ["Email", "Password", "Login", "Button"]
            },
            {
                "name": "Dashboard",
                "flow": "User views welcome message, task summary, and navigation options",
                "expected_elements": ["Dashboard", "Welcome", "Tasks", "Add Task", "Profile", "Settings"]
            },
            {
                "name": "Task Creation",
                "flow": "User fills task form with title, description, due date and saves",
                "expected_elements": ["New Task", "Title", "Description", "Due Date", "Save", "Cancel"]
            },
            {
                "name": "Task Management",
                "flow": "User views task list and can edit, delete, or complete tasks",
                "expected_elements": ["Task List", "Edit", "Delete", "Complete"]
            },
            {
                "name": "Error Handling",
                "flow": "System displays error messages and recovery options",
                "expected_elements": ["Error", "Network", "Retry", "Cancel"]
            }
        ],
        "critical_paths": [
            "Login → Dashboard → Add Task → Fill Form → Save → Success → Task List",
            "Dashboard → Task List → Edit Task → Update → Confirmation"
        ],
        "expected_screens": [
            "Login Screen",
            "Main Dashboard", 
            "Task Creation Form",
            "Success Confirmation",
            "Task List View",
            "Error State"
        ],
        "performance_expectations": {
            "page_load_time": "< 3 seconds",
            "form_submission": "< 2 seconds",
            "navigation_transition": "< 1 second"
        },
        "error_scenarios": [
            {
                "scenario": "Network Connection Lost",
                "expected_behavior": "Show error message with retry option"
            },
            {
                "scenario": "Form Validation Error",
                "expected_behavior": "Highlight invalid fields with error messages"
            }
        ]
    }


def run_comprehensive_demo():
    """
    Run a comprehensive demonstration of the Screen Recording Analyzer.
    """
    print("🎬 SCREEN RECORDING ANALYZER - COMPREHENSIVE DEMO")
    print("=" * 60)
    
    # Create temporary directory for demo files
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Demo files will be saved in: {temp_dir}")
    
    try:
        # 1. Create demo video
        video_path = os.path.join(temp_dir, "taskapp_demo.mp4")
        create_demo_video(video_path, duration_per_frame=3)
        
        # 2. Create demo specification
        spec_data = create_demo_spec()
        spec_path = os.path.join(temp_dir, "taskapp_spec.json")
        with open(spec_path, 'w') as f:
            json.dump(spec_data, f, indent=2)
        print(f"📋 Demo specification created: {spec_path}")
        
        # 3. Initialize analyzer
        print("\n🔧 Initializing Screen Recording Analyzer...")
        analyzer = ScreenRecordingAnalyzer(
            output_dir=os.path.join(temp_dir, "analysis_frames"),
            sampling_fps=1.0
        )
        
        # 4. Run analysis
        print("\n🔍 Running comprehensive analysis...")
        print("⏳ This may take a moment...")
        
        results = analyzer.analyze_video(video_path, spec_path)
        
        if "error" in results:
            print(f"❌ Analysis failed: {results['error']}")
            return
        
        # 5. Display detailed results
        print("\n" + "="*60)
        print("📊 ANALYSIS RESULTS")
        print("="*60)
        
        # Video information
        video_info = results["video_info"]
        print(f"\n📹 VIDEO INFORMATION:")
        print(f"   Duration: {video_info['duration']:.1f} seconds")
        print(f"   FPS: {video_info['fps']:.1f}")
        print(f"   Total Frames: {video_info['total_frames']}")
        print(f"   Processed Frames: {video_info['processed_frames']}")
        
        # Analysis summary
        summary = results["analysis_summary"]
        print(f"\n📈 ANALYSIS SUMMARY:")
        print(f"   Key Frames Detected: {summary['key_frames_detected']}")
        print(f"   UI Transitions: {summary['transitions_detected']}")
        print(f"   Journey Steps: {summary['journey_steps']}")
        print(f"   Issues Found: {summary['issues_found']}")
        
        # User journey
        journey = results["user_journey"]
        print(f"\n🗺️  USER JOURNEY ({len(journey['steps'])} steps):")
        for i, step in enumerate(journey["steps"], 1):
            print(f"   {i:2d}. {step}")
        
        # UI Transitions
        if journey["transitions"]:
            print(f"\n🔄 UI TRANSITIONS ({len(journey['transitions'])} detected):")
            for i, transition in enumerate(journey["transitions"], 1):
                print(f"   {i}. {transition['from_timestamp']:.1f}s → {transition['to_timestamp']:.1f}s")
                print(f"      Type: {transition['transition_type']}")
                print(f"      Description: {transition['description']}")
                print(f"      Confidence: {transition['confidence']:.1%}")
                print()
        
        # Specification comparison
        comparison = results["spec_comparison"]
        print(f"📋 SPECIFICATION COMPARISON:")
        print(f"   Coverage: {comparison['spec_coverage']:.1%}")
        print(f"   Overall Score: {comparison['overall_score']:.1%}")
        
        if comparison["missing_flows"]:
            print(f"\n❌ MISSING EXPECTED FLOWS:")
            for flow in comparison["missing_flows"]:
                print(f"   • {flow}")
        
        if comparison["unexpected_flows"]:
            print(f"\n⚠️  UNEXPECTED FLOWS:")
            for flow in comparison["unexpected_flows"]:
                print(f"   • {flow}")
        
        # Issues detected
        if journey["issues"]:
            print(f"\n🚨 ISSUES DETECTED ({len(journey['issues'])}):")
            for issue in journey["issues"]:
                print(f"   • {issue}")
        
        # 6. Generate reports
        print(f"\n📝 GENERATING REPORTS...")
        
        # Markdown report
        report_path = os.path.join(temp_dir, "taskapp_analysis_report.md")
        analyzer.generate_report(results, report_path)
        
        # JSON results
        json_path = os.path.join(temp_dir, "taskapp_analysis_results.json")
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"   📄 Markdown Report: {report_path}")
        print(f"   📊 JSON Results: {json_path}")
        print(f"   🖼️  Key Frames: {analyzer.output_dir}")
        
        # 7. Display key insights
        print(f"\n💡 KEY INSIGHTS:")
        
        # Coverage analysis
        coverage = comparison['spec_coverage']
        if coverage >= 0.8:
            print(f"   ✅ Excellent spec coverage ({coverage:.1%})")
        elif coverage >= 0.6:
            print(f"   ⚠️  Good spec coverage ({coverage:.1%}) - some flows missing")
        else:
            print(f"   ❌ Low spec coverage ({coverage:.1%}) - significant gaps detected")
        
        # Issue analysis
        issue_count = len(journey['issues'])
        if issue_count == 0:
            print(f"   ✅ No issues detected - smooth user experience")
        elif issue_count <= 2:
            print(f"   ⚠️  Minor issues detected ({issue_count}) - review recommended")
        else:
            print(f"   ❌ Multiple issues detected ({issue_count}) - attention required")
        
        # Transition analysis
        transition_count = len(journey['transitions'])
        if transition_count >= 4:
            print(f"   ✅ Rich user interaction detected ({transition_count} transitions)")
        elif transition_count >= 2:
            print(f"   ⚠️  Moderate interaction ({transition_count} transitions)")
        else:
            print(f"   ❌ Limited interaction detected ({transition_count} transitions)")
        
        # 8. Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        
        if coverage < 0.8:
            print(f"   • Review and implement missing user flows")
        
        if issue_count > 0:
            print(f"   • Address detected UI issues and stuck screens")
        
        if comparison['overall_score'] < 0.7:
            print(f"   • Consider UX improvements to enhance user flow")
        
        print(f"   • Test with real users to validate analysis results")
        print(f"   • Monitor performance metrics during actual usage")
        
        # 9. File summary
        print(f"\n📁 GENERATED FILES:")
        print(f"   🎥 Demo Video: {video_path}")
        print(f"   📋 Specification: {spec_path}")
        print(f"   📄 Analysis Report: {report_path}")
        print(f"   📊 Results JSON: {json_path}")
        print(f"   🖼️  Frame Directory: {analyzer.output_dir}")
        
        print(f"\n✅ DEMO COMPLETED SUCCESSFULLY!")
        print(f"🔍 Review the generated files to explore detailed analysis results")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n📁 All demo files saved in: {temp_dir}")
        print(f"💡 You can examine the files to understand the analysis process")


def run_quick_demo():
    """
    Run a quick demonstration with minimal output.
    """
    print("🚀 QUICK DEMO - Screen Recording Analyzer")
    print("-" * 40)
    
    # Create minimal demo
    temp_dir = tempfile.mkdtemp()
    
    # Simple 3-screen demo
    video_path = os.path.join(temp_dir, "quick_demo.mp4")
    
    # Create simple video
    width, height = 640, 480
    fps = 1
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    
    screens = [
        ((255, 255, 255), "Login Screen"),
        ((200, 255, 200), "Dashboard"),
        ((255, 200, 200), "Error Page")
    ]
    
    for color, text in screens:
        frame = np.full((height, width, 3), color, dtype=np.uint8)
        cv2.putText(frame, text, (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Write 2 seconds of frames
        for _ in range(2):
            out.write(frame)
    
    out.release()
    
    # Simple spec
    spec = {"user_flows": ["login", "dashboard", "error handling"]}
    spec_path = os.path.join(temp_dir, "quick_spec.json")
    with open(spec_path, 'w') as f:
        json.dump(spec, f)
    
    # Analyze
    analyzer = ScreenRecordingAnalyzer(os.path.join(temp_dir, "frames"))
    results = analyzer.analyze_video(video_path, spec_path)
    
    if "error" not in results:
        print(f"✅ Analysis completed!")
        print(f"   Frames processed: {results['video_info']['processed_frames']}")
        print(f"   Transitions: {results['analysis_summary']['transitions_detected']}")
        print(f"   Coverage: {results['spec_comparison']['spec_coverage']:.1%}")
    else:
        print(f"❌ Error: {results['error']}")
    
    print(f"📁 Files in: {temp_dir}")


if __name__ == "__main__":
    import sys
    
    print("🎬 Screen Recording Analyzer - Demo Options")
    print("=" * 50)
    print("1. Comprehensive Demo (detailed analysis)")
    print("2. Quick Demo (fast overview)")
    print("3. Exit")
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        run_comprehensive_demo()
    elif choice == "2":
        run_quick_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Running comprehensive demo...")
        run_comprehensive_demo()