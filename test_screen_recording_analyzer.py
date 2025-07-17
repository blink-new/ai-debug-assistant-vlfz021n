#!/usr/bin/env python3
"""
Test Suite for Screen Recording Analyzer

This module contains comprehensive tests for the ScreenRecordingAnalyzer class,
including unit tests and integration tests with sample data.

Author: AI Debug Assistant
Version: 1.0.0
"""

import unittest
import json
import os
import tempfile
import numpy as np
import cv2
from pathlib import Path
from screen_recording_analyzer import ScreenRecordingAnalyzer, FrameInfo, UITransition, UserJourney


class TestScreenRecordingAnalyzer(unittest.TestCase):
    """Test cases for the ScreenRecordingAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = ScreenRecordingAnalyzer(
            output_dir=os.path.join(self.temp_dir, "test_frames"),
            sampling_fps=2.0
        )
        
        # Create sample enhanced spec
        self.sample_spec = {
            "user_flows": [
                "User login authentication",
                "Dashboard navigation",
                "Form submission process",
                "Data display and interaction"
            ],
            "features": [
                {"name": "Authentication", "flow": "User enters credentials and logs in"},
                {"name": "Navigation", "flow": "User navigates through main sections"},
                {"name": "Forms", "flow": "User fills out and submits forms"},
                {"name": "Data View", "flow": "User views and interacts with data"}
            ],
            "expected_screens": [
                "Login Screen",
                "Main Dashboard",
                "Form Page",
                "Data View",
                "Success/Confirmation Page"
            ],
            "critical_paths": [
                "Login → Dashboard → Form → Submit → Success",
                "Dashboard → Data View → Filter → Results"
            ]
        }
        
        self.spec_path = os.path.join(self.temp_dir, "test_spec.json")
        with open(self.spec_path, 'w') as f:
            json.dump(self.sample_spec, f, indent=2)
    
    def tearDown(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_frame(self, width=640, height=480, color=(255, 255, 255), text=""):
        """
        Create a test frame with optional text overlay.
        
        Args:
            width: Frame width
            height: Frame height
            color: Background color (BGR)
            text: Text to overlay on frame
            
        Returns:
            OpenCV frame (numpy array)
        """
        frame = np.full((height, width, 3), color, dtype=np.uint8)
        
        if text:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            text_color = (0, 0, 0)  # Black text
            
            # Get text size and center it
            (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
            x = (width - text_width) // 2
            y = (height + text_height) // 2
            
            cv2.putText(frame, text, (x, y), font, font_scale, text_color, thickness)
        
        return frame
    
    def create_test_video(self, frames_data, output_path, fps=30):
        """
        Create a test video file from frame data.
        
        Args:
            frames_data: List of (color, text) tuples for each frame
            output_path: Path to save the video
            fps: Frames per second
        """
        if not frames_data:
            return
        
        # Create first frame to get dimensions
        first_frame = self.create_test_frame(color=frames_data[0][0], text=frames_data[0][1])
        height, width, _ = first_frame.shape
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Write frames
        for color, text in frames_data:
            frame = self.create_test_frame(color=color, text=text)
            # Write each frame multiple times to create duration
            for _ in range(fps):  # 1 second per frame
                out.write(frame)
        
        out.release()
    
    def test_frame_hash_calculation(self):
        """Test frame hash calculation functionality."""
        frame1 = self.create_test_frame(color=(255, 0, 0), text="Test Frame 1")
        frame2 = self.create_test_frame(color=(255, 0, 0), text="Test Frame 1")
        frame3 = self.create_test_frame(color=(0, 255, 0), text="Test Frame 2")
        
        hash1 = self.analyzer.calculate_frame_hash(frame1)
        hash2 = self.analyzer.calculate_frame_hash(frame2)
        hash3 = self.analyzer.calculate_frame_hash(frame3)
        
        # Same frames should have same hash
        self.assertEqual(hash1, hash2)
        
        # Different frames should have different hashes
        self.assertNotEqual(hash1, hash3)
        
        # Hash should be a valid MD5 string
        self.assertEqual(len(hash1), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash1))
    
    def test_frame_difference_calculation(self):
        """Test frame difference calculation."""
        frame1 = self.create_test_frame(color=(255, 255, 255), text="Same")
        frame2 = self.create_test_frame(color=(255, 255, 255), text="Same")
        frame3 = self.create_test_frame(color=(0, 0, 0), text="Different")
        
        # Same frames should have low difference
        diff_same = self.analyzer.calculate_frame_difference(frame1, frame2)
        self.assertLess(diff_same, 0.1)
        
        # Different frames should have high difference
        diff_different = self.analyzer.calculate_frame_difference(frame1, frame3)
        self.assertGreater(diff_different, 0.3)
        
        # Difference should be between 0 and 1
        self.assertGreaterEqual(diff_same, 0.0)
        self.assertLessEqual(diff_same, 1.0)
        self.assertGreaterEqual(diff_different, 0.0)
        self.assertLessEqual(diff_different, 1.0)
    
    def test_ui_element_extraction(self):
        """Test UI element extraction from text."""
        test_cases = [
            ("Click Submit to continue", ["Submit"]),
            ("Login with your Email and Password", ["Login", "Email", "Password"]),
            ("Navigate to Dashboard or Settings", ["Dashboard", "Settings"]),
            ("Add new item or Delete existing", ["Add", "Delete"]),
            ("No UI elements here", [])
        ]
        
        for text, expected_elements in test_cases:
            extracted = self.analyzer.extract_ui_elements(text)
            
            # Check that all expected elements are found (case insensitive)
            for element in expected_elements:
                self.assertTrue(
                    any(element.lower() == extracted_element.lower() for extracted_element in extracted),
                    f"Expected '{element}' not found in {extracted} for text: '{text}'"
                )
    
    def test_transition_classification(self):
        """Test UI transition classification."""
        # Create test frames with different UI elements
        frame_login = FrameInfo(
            frame_number=1, timestamp=1.0, frame_hash="hash1",
            extracted_text="Please Login to continue", is_key_frame=True,
            change_score=0.5, ui_elements=["Login"]
        )
        
        frame_dashboard = FrameInfo(
            frame_number=2, timestamp=2.0, frame_hash="hash2",
            extracted_text="Welcome to Dashboard", is_key_frame=True,
            change_score=0.6, ui_elements=["Dashboard", "Menu"]
        )
        
        frame_error = FrameInfo(
            frame_number=3, timestamp=3.0, frame_hash="hash3",
            extracted_text="Error: Login failed", is_key_frame=True,
            change_score=0.4, ui_elements=["Error"]
        )
        
        # Test different transition types
        auth_transition = self.analyzer.classify_transition(frame_login, frame_dashboard)
        error_transition = self.analyzer.classify_transition(frame_login, frame_error)
        
        # Should classify authentication and error transitions
        self.assertIn(auth_transition, ["authentication", "page_change", "navigation"])
        self.assertEqual(error_transition, "error_state")
    
    def test_stuck_screen_detection(self):
        """Test detection of stuck screens."""
        # Create frames with repeated content
        frames = []
        for i in range(15):  # 15 frames over 15 seconds
            frame = FrameInfo(
                frame_number=i, timestamp=float(i), frame_hash="same_hash",
                extracted_text="Same content", is_key_frame=i==0,
                change_score=0.0, ui_elements=["Button"]
            )
            frames.append(frame)
        
        issues = []
        self.analyzer.detect_stuck_screens(frames, issues)
        
        # Should detect stuck screen
        self.assertTrue(len(issues) > 0)
        self.assertTrue(any("stuck" in issue.lower() for issue in issues))
    
    def test_expected_flows_extraction(self):
        """Test extraction of expected flows from specification."""
        flows = self.analyzer.extract_expected_flows(self.sample_spec)
        
        # Should extract flows from user_flows
        self.assertIn("User login authentication", flows)
        self.assertIn("Dashboard navigation", flows)
        
        # Should handle empty spec
        empty_flows = self.analyzer.extract_expected_flows({})
        self.assertTrue(len(empty_flows) > 0)  # Should have default flows
    
    def test_journey_reconstruction(self):
        """Test user journey reconstruction."""
        # Create sample frames and transitions
        frames = [
            FrameInfo(1, 1.0, "hash1", "Login Screen", True, 0.0, ["Login"]),
            FrameInfo(2, 2.0, "hash2", "Dashboard", True, 0.5, ["Dashboard"]),
            FrameInfo(3, 3.0, "hash3", "Form Page", True, 0.6, ["Submit"])
        ]
        
        transitions = [
            UITransition(1, 2, 1.0, 2.0, "authentication", "User logged in", 0.8),
            UITransition(2, 3, 2.0, 3.0, "navigation", "Navigated to form", 0.7)
        ]
        
        journey = self.analyzer.reconstruct_user_journey(frames, transitions)
        
        # Check journey structure
        self.assertIsInstance(journey, UserJourney)
        self.assertTrue(len(journey.steps) > 0)
        self.assertEqual(len(journey.transitions), 2)
        self.assertEqual(journey.total_duration, 3.0)
        self.assertEqual(len(journey.key_frames), 3)
    
    def test_spec_comparison(self):
        """Test comparison with specification."""
        # Create a journey with some expected flows
        journey = UserJourney(
            steps=["Started at: Login", "User login authentication at 1.0s", "Dashboard navigation at 2.0s"],
            transitions=[],
            total_duration=3.0,
            key_frames=[],
            issues=["Test issue"]
        )
        
        comparison = self.analyzer.compare_with_spec(journey, self.sample_spec)
        
        # Check comparison structure
        self.assertIn("spec_coverage", comparison)
        self.assertIn("missing_flows", comparison)
        self.assertIn("overall_score", comparison)
        
        # Coverage should be reasonable since we included expected flows
        self.assertGreater(comparison["spec_coverage"], 0.0)
        self.assertLessEqual(comparison["spec_coverage"], 1.0)
    
    def test_full_video_analysis_integration(self):
        """Integration test with a complete video analysis."""
        # Create test video with different screens
        video_path = os.path.join(self.temp_dir, "test_video.mp4")
        
        frames_data = [
            ((255, 255, 255), "Login Screen"),      # White background, login text
            ((200, 200, 255), "Dashboard"),         # Light blue, dashboard
            ((255, 200, 200), "Form Submit"),       # Light red, form
            ((200, 255, 200), "Success Page")       # Light green, success
        ]
        
        self.create_test_video(frames_data, video_path, fps=2)
        
        # Run analysis
        results = self.analyzer.analyze_video(video_path, self.spec_path)
        
        # Check results structure
        self.assertNotIn("error", results)
        self.assertIn("video_info", results)
        self.assertIn("analysis_summary", results)
        self.assertIn("user_journey", results)
        self.assertIn("spec_comparison", results)
        
        # Check video info
        video_info = results["video_info"]
        self.assertEqual(video_info["path"], video_path)
        self.assertGreater(video_info["duration"], 0)
        
        # Check analysis summary
        summary = results["analysis_summary"]
        self.assertGreaterEqual(summary["key_frames_detected"], 1)
        self.assertGreaterEqual(summary["processed_frames"], 1)
    
    def test_report_generation(self):
        """Test Markdown report generation."""
        # Create sample results
        sample_results = {
            "video_info": {
                "path": "test_video.mp4",
                "duration": 10.0,
                "fps": 30.0,
                "total_frames": 300,
                "processed_frames": 10
            },
            "analysis_summary": {
                "key_frames_detected": 4,
                "transitions_detected": 3,
                "journey_steps": 5,
                "issues_found": 1
            },
            "user_journey": {
                "steps": ["Started at: Login", "Authentication completed", "Dashboard loaded"],
                "transitions": [
                    {
                        "from_timestamp": 1.0,
                        "to_timestamp": 2.0,
                        "transition_type": "authentication",
                        "description": "User logged in",
                        "confidence": 0.8
                    }
                ],
                "issues": ["Screen stuck at 5.0s"]
            },
            "spec_comparison": {
                "spec_coverage": 0.75,
                "overall_score": 0.65,
                "missing_flows": ["Data export"],
                "unexpected_flows": [],
                "ui_deviations": []
            }
        }
        
        report_path = os.path.join(self.temp_dir, "test_report.md")
        self.analyzer.generate_report(sample_results, report_path)
        
        # Check that report was created
        self.assertTrue(os.path.exists(report_path))
        
        # Check report content
        with open(report_path, 'r') as f:
            content = f.read()
        
        self.assertIn("Screen Recording Analysis Report", content)
        self.assertIn("Video Information", content)
        self.assertIn("User Journey Flow", content)
        self.assertIn("Specification Comparison", content)
        self.assertIn("test_video.mp4", content)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test with non-existent video file
        results = self.analyzer.analyze_video("nonexistent.mp4", self.spec_path)
        self.assertIn("error", results)
        
        # Test with invalid spec file
        results = self.analyzer.analyze_video("test.mp4", "nonexistent_spec.json")
        self.assertIn("error", results)


class TestFrameInfoDataClass(unittest.TestCase):
    """Test the FrameInfo dataclass."""
    
    def test_frame_info_creation(self):
        """Test FrameInfo object creation and serialization."""
        frame_info = FrameInfo(
            frame_number=1,
            timestamp=1.5,
            frame_hash="abc123",
            extracted_text="Test text",
            is_key_frame=True,
            change_score=0.75,
            ui_elements=["Button", "Link"]
        )
        
        # Test basic properties
        self.assertEqual(frame_info.frame_number, 1)
        self.assertEqual(frame_info.timestamp, 1.5)
        self.assertTrue(frame_info.is_key_frame)
        self.assertEqual(len(frame_info.ui_elements), 2)
        
        # Test serialization
        frame_dict = frame_info.__dict__
        self.assertIn("frame_number", frame_dict)
        self.assertIn("ui_elements", frame_dict)


class TestUITransitionDataClass(unittest.TestCase):
    """Test the UITransition dataclass."""
    
    def test_ui_transition_creation(self):
        """Test UITransition object creation."""
        transition = UITransition(
            from_frame=1,
            to_frame=2,
            from_timestamp=1.0,
            to_timestamp=2.0,
            transition_type="authentication",
            description="User logged in",
            confidence=0.85
        )
        
        # Test properties
        self.assertEqual(transition.from_frame, 1)
        self.assertEqual(transition.to_frame, 2)
        self.assertEqual(transition.transition_type, "authentication")
        self.assertAlmostEqual(transition.confidence, 0.85)


def run_demo_analysis():
    """
    Run a demonstration of the Screen Recording Analyzer with sample data.
    """
    print("\n" + "="*60)
    print("🎬 SCREEN RECORDING ANALYZER - DEMO ANALYSIS")
    print("="*60)
    
    # Create temporary directory for demo
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize analyzer
        analyzer = ScreenRecordingAnalyzer(
            output_dir=os.path.join(temp_dir, "demo_frames"),
            sampling_fps=1.0
        )
        
        # Create sample enhanced spec
        demo_spec = {
            "app_name": "Task Management App",
            "user_flows": [
                "User authentication and login",
                "Main dashboard navigation",
                "Task creation and management",
                "Task completion workflow",
                "User profile management"
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
                },
                {
                    "name": "Task Management",
                    "flow": "User creates, edits, and completes tasks",
                    "expected_elements": ["Add Task", "Edit", "Delete", "Complete"]
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
                "Task List View",
                "Task Details",
                "User Profile"
            ]
        }
        
        # Save demo spec
        spec_path = os.path.join(temp_dir, "demo_spec.json")
        with open(spec_path, 'w') as f:
            json.dump(demo_spec, f, indent=2)
        
        print(f"📋 Demo spec created: {spec_path}")
        
        # Create sample video frames data
        demo_frames = [
            ((240, 240, 255), "Login Screen - Enter Credentials"),
            ((240, 240, 255), "Login Screen - Enter Credentials"),  # Same frame (stuck)
            ((200, 255, 200), "Dashboard - Welcome User"),
            ((255, 240, 200), "Add New Task Form"),
            ((255, 240, 200), "Add New Task Form - Validation"),
            ((200, 255, 200), "Task Added Successfully"),
            ((220, 220, 255), "Task List View"),
            ((255, 200, 200), "Error - Network Connection Failed")
        ]
        
        # Create demo video
        video_path = os.path.join(temp_dir, "demo_recording.mp4")
        
        print("🎥 Creating demo video...")
        
        # Create video writer
        height, width = 480, 640
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, 2.0, (width, height))
        
        for i, (color, text) in enumerate(demo_frames):
            # Create frame
            frame = np.full((height, width, 3), color, dtype=np.uint8)
            
            # Add text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            text_color = (0, 0, 0)
            
            # Multi-line text support
            lines = text.split(' - ')
            y_offset = height // 2 - len(lines) * 15
            
            for line in lines:
                (text_width, text_height), _ = cv2.getTextSize(line, font, font_scale, thickness)
                x = (width - text_width) // 2
                y = y_offset + text_height
                cv2.putText(frame, line, (x, y), font, font_scale, text_color, thickness)
                y_offset += 40
            
            # Write frame multiple times (2 seconds each)
            for _ in range(4):  # 2 seconds at 2 FPS
                out.write(frame)
        
        out.release()
        print(f"✅ Demo video created: {video_path}")
        
        # Run analysis
        print("\n🔍 Running screen recording analysis...")
        results = analyzer.analyze_video(video_path, spec_path)
        
        if "error" in results:
            print(f"❌ Analysis failed: {results['error']}")
            return
        
        # Display results summary
        print("\n📊 ANALYSIS RESULTS SUMMARY")
        print("-" * 40)
        
        video_info = results["video_info"]
        print(f"📹 Video Duration: {video_info['duration']:.1f} seconds")
        print(f"🖼️  Frames Processed: {video_info['processed_frames']}")
        
        summary = results["analysis_summary"]
        print(f"🔑 Key Frames: {summary['key_frames_detected']}")
        print(f"🔄 Transitions: {summary['transitions_detected']}")
        print(f"📝 Journey Steps: {summary['journey_steps']}")
        print(f"⚠️  Issues Found: {summary['issues_found']}")
        
        # Display user journey
        journey = results["user_journey"]
        print(f"\n🗺️  USER JOURNEY ({len(journey['steps'])} steps)")
        print("-" * 40)
        for i, step in enumerate(journey["steps"], 1):
            print(f"{i:2d}. {step}")
        
        # Display transitions
        if journey["transitions"]:
            print(f"\n🔄 UI TRANSITIONS ({len(journey['transitions'])} detected)")
            print("-" * 40)
            for transition in journey["transitions"]:
                print(f"⏱️  {transition['from_timestamp']:.1f}s → {transition['to_timestamp']:.1f}s")
                print(f"   Type: {transition['transition_type']}")
                print(f"   Description: {transition['description']}")
                print(f"   Confidence: {transition['confidence']:.1%}")
                print()
        
        # Display spec comparison
        comparison = results["spec_comparison"]
        print(f"📋 SPECIFICATION COMPARISON")
        print("-" * 40)
        print(f"Coverage: {comparison['spec_coverage']:.1%}")
        print(f"Overall Score: {comparison['overall_score']:.1%}")
        
        if comparison["missing_flows"]:
            print(f"\n❌ Missing Expected Flows:")
            for flow in comparison["missing_flows"]:
                print(f"   • {flow}")
        
        # Display issues
        if journey["issues"]:
            print(f"\n🚨 ISSUES DETECTED ({len(journey['issues'])})")
            print("-" * 40)
            for issue in journey["issues"]:
                print(f"   • {issue}")
        
        # Generate report
        report_path = os.path.join(temp_dir, "demo_analysis_report.md")
        analyzer.generate_report(results, report_path)
        
        # Save results JSON
        results_path = os.path.join(temp_dir, "demo_analysis_results.json")
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Full report saved: {report_path}")
        print(f"📊 Results JSON saved: {results_path}")
        print(f"🖼️  Key frames saved in: {analyzer.output_dir}")
        
        print(f"\n✅ Demo analysis completed successfully!")
        print(f"📁 All files saved in: {temp_dir}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Note: In a real scenario, you might want to clean up temp_dir
        # For demo purposes, we'll leave it so users can examine the files
        pass


if __name__ == "__main__":
    print("🧪 Screen Recording Analyzer - Test Suite")
    print("=" * 50)
    
    # Run unit tests
    print("\n1️⃣  Running Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run demo analysis
    print("\n2️⃣  Running Demo Analysis...")
    run_demo_analysis()
    
    print("\n🎉 All tests and demo completed!")