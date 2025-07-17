#!/usr/bin/env python3
"""
Screen Recording Analyzer Module

This module analyzes screen recordings of applications to extract user journey flows,
compare them against expected specifications, and identify UI/UX issues.

Author: AI Debug Assistant
Version: 1.0.0
"""

import cv2
import json
import os
import numpy as np
import pytesseract
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import re
from pathlib import Path


@dataclass
class FrameInfo:
    """Information about a video frame"""
    frame_number: int
    timestamp: float
    frame_hash: str
    extracted_text: str
    is_key_frame: bool
    change_score: float
    ui_elements: List[str]


@dataclass
class UITransition:
    """Represents a transition between UI states"""
    from_frame: int
    to_frame: int
    from_timestamp: float
    to_timestamp: float
    transition_type: str
    description: str
    confidence: float


@dataclass
class UserJourney:
    """Complete user journey extracted from screen recording"""
    steps: List[str]
    transitions: List[UITransition]
    total_duration: float
    key_frames: List[FrameInfo]
    issues: List[str]


class ScreenRecordingAnalyzer:
    """
    Analyzes screen recordings to extract user flows and compare against specifications.
    
    This class processes video files frame by frame, detects UI changes, extracts text,
    and reconstructs user journey flows for comparison with expected specifications.
    """
    
    def __init__(self, output_dir: str = "output_frames", sampling_fps: float = 1.0):
        """
        Initialize the Screen Recording Analyzer.
        
        Args:
            output_dir: Directory to save extracted key frames
            sampling_fps: Frames per second to sample (default: 1.0)
        """
        self.output_dir = Path(output_dir)
        self.sampling_fps = sampling_fps
        self.change_threshold = 0.15  # Threshold for detecting significant frame changes
        self.text_similarity_threshold = 0.8  # Threshold for text similarity
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize frame storage
        self.frames: List[FrameInfo] = []
        self.transitions: List[UITransition] = []
        
        print(f"🎬 Screen Recording Analyzer initialized")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"⚡ Sampling rate: {sampling_fps} FPS")
    
    def calculate_frame_hash(self, frame: np.ndarray) -> str:
        """
        Calculate a hash for frame comparison.
        
        Args:
            frame: OpenCV frame (numpy array)
            
        Returns:
            MD5 hash string of the frame
        """
        # Convert to grayscale and resize for consistent hashing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64, 64))
        
        # Calculate hash
        frame_bytes = resized.tobytes()
        return hashlib.md5(frame_bytes).hexdigest()
    
    def calculate_frame_difference(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """
        Calculate the difference between two frames.
        
        Args:
            frame1: First frame
            frame2: Second frame
            
        Returns:
            Difference score (0.0 = identical, 1.0 = completely different)
        """
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Resize for consistent comparison
        gray1 = cv2.resize(gray1, (640, 480))
        gray2 = cv2.resize(gray2, (640, 480))
        
        # Calculate structural similarity
        diff = cv2.absdiff(gray1, gray2)
        non_zero_count = np.count_nonzero(diff)
        total_pixels = diff.shape[0] * diff.shape[1]
        
        return non_zero_count / total_pixels
    
    def extract_text_from_frame(self, frame: np.ndarray) -> Tuple[str, List[str]]:
        """
        Extract text from a frame using OCR.
        
        Args:
            frame: OpenCV frame
            
        Returns:
            Tuple of (full_text, ui_elements_list)
        """
        try:
            # Preprocess frame for better OCR
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get better text recognition
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(thresh, config='--psm 6')
            
            # Clean and process text
            cleaned_text = ' '.join(text.split())
            
            # Extract potential UI elements (buttons, labels, etc.)
            ui_elements = self.extract_ui_elements(cleaned_text)
            
            return cleaned_text, ui_elements
            
        except Exception as e:
            print(f"⚠️  OCR Error: {e}")
            return "", []
    
    def extract_ui_elements(self, text: str) -> List[str]:
        """
        Extract UI elements from OCR text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            List of identified UI elements
        """
        ui_elements = []
        
        # Common UI element patterns
        button_patterns = [
            r'\b(Submit|Save|Cancel|Delete|Edit|Create|Login|Logout|Sign Up|Sign In)\b',
            r'\b(Continue|Next|Previous|Back|Finish|Start|Stop)\b',
            r'\b(Add|Remove|Update|Refresh|Search|Filter|Sort)\b'
        ]
        
        form_patterns = [
            r'\b(Email|Password|Username|Name|Address|Phone)\b',
            r'\b(First Name|Last Name|Company|Title|Description)\b'
        ]
        
        navigation_patterns = [
            r'\b(Home|Dashboard|Settings|Profile|Help|About)\b',
            r'\b(Menu|Navigation|Sidebar|Header|Footer)\b'
        ]
        
        all_patterns = button_patterns + form_patterns + navigation_patterns
        
        for pattern in all_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            ui_elements.extend(matches)
        
        # Remove duplicates and return
        return list(set(ui_elements))
    
    def detect_ui_transitions(self, frames: List[FrameInfo]) -> List[UITransition]:
        """
        Detect UI transitions between frames.
        
        Args:
            frames: List of analyzed frames
            
        Returns:
            List of detected UI transitions
        """
        transitions = []
        
        for i in range(1, len(frames)):
            prev_frame = frames[i-1]
            curr_frame = frames[i]
            
            # Check if this is a significant transition
            if curr_frame.change_score > self.change_threshold:
                
                # Determine transition type
                transition_type = self.classify_transition(prev_frame, curr_frame)
                
                # Create transition description
                description = self.generate_transition_description(prev_frame, curr_frame, transition_type)
                
                # Calculate confidence based on change score and text differences
                confidence = min(curr_frame.change_score * 2, 1.0)
                
                transition = UITransition(
                    from_frame=prev_frame.frame_number,
                    to_frame=curr_frame.frame_number,
                    from_timestamp=prev_frame.timestamp,
                    to_timestamp=curr_frame.timestamp,
                    transition_type=transition_type,
                    description=description,
                    confidence=confidence
                )
                
                transitions.append(transition)
                print(f"🔄 Detected transition: {description} (confidence: {confidence:.2f})")
        
        return transitions
    
    def classify_transition(self, prev_frame: FrameInfo, curr_frame: FrameInfo) -> str:
        """
        Classify the type of UI transition.
        
        Args:
            prev_frame: Previous frame info
            curr_frame: Current frame info
            
        Returns:
            Transition type string
        """
        prev_elements = set(prev_frame.ui_elements)
        curr_elements = set(curr_frame.ui_elements)
        
        # Check for specific transition types
        if "Login" in curr_elements or "Sign In" in curr_elements:
            return "authentication"
        elif "Submit" in prev_elements and "Success" in curr_frame.extracted_text:
            return "form_submission"
        elif "Menu" in curr_elements or "Navigation" in curr_elements:
            return "navigation"
        elif len(curr_elements) > len(prev_elements):
            return "modal_open"
        elif len(curr_elements) < len(prev_elements):
            return "modal_close"
        elif "Error" in curr_frame.extracted_text or "Failed" in curr_frame.extracted_text:
            return "error_state"
        else:
            return "page_change"
    
    def generate_transition_description(self, prev_frame: FrameInfo, curr_frame: FrameInfo, transition_type: str) -> str:
        """
        Generate a human-readable description of the transition.
        
        Args:
            prev_frame: Previous frame info
            curr_frame: Current frame info
            transition_type: Type of transition
            
        Returns:
            Human-readable description
        """
        descriptions = {
            "authentication": "User navigated to login/authentication screen",
            "form_submission": "Form was submitted successfully",
            "navigation": "User navigated to different section",
            "modal_open": "Modal or popup window opened",
            "modal_close": "Modal or popup window closed",
            "error_state": "Error or failure state displayed",
            "page_change": "Page or screen changed"
        }
        
        base_description = descriptions.get(transition_type, "UI state changed")
        
        # Add specific elements if available
        if curr_frame.ui_elements:
            elements = ", ".join(curr_frame.ui_elements[:3])  # Show first 3 elements
            base_description += f" (elements: {elements})"
        
        return base_description
    
    def reconstruct_user_journey(self, frames: List[FrameInfo], transitions: List[UITransition]) -> UserJourney:
        """
        Reconstruct the complete user journey from frames and transitions.
        
        Args:
            frames: List of analyzed frames
            transitions: List of detected transitions
            
        Returns:
            UserJourney object with complete flow information
        """
        print("🗺️  Reconstructing user journey...")
        
        # Extract journey steps from transitions
        steps = []
        issues = []
        
        # Add initial state
        if frames:
            initial_elements = frames[0].ui_elements
            if initial_elements:
                steps.append(f"Started at: {', '.join(initial_elements[:2])}")
            else:
                steps.append("Started at: Unknown screen")
        
        # Process each transition
        for transition in transitions:
            step_description = f"{transition.description} at {transition.to_timestamp:.1f}s"
            steps.append(step_description)
            
            # Check for potential issues
            if transition.confidence < 0.3:
                issues.append(f"Low confidence transition at {transition.to_timestamp:.1f}s")
            
            if transition.transition_type == "error_state":
                issues.append(f"Error state detected at {transition.to_timestamp:.1f}s")
        
        # Detect stuck screens (same frame repeated)
        self.detect_stuck_screens(frames, issues)
        
        # Calculate total duration
        total_duration = frames[-1].timestamp if frames else 0.0
        
        # Get key frames (frames with significant changes)
        key_frames = [f for f in frames if f.is_key_frame]
        
        journey = UserJourney(
            steps=steps,
            transitions=transitions,
            total_duration=total_duration,
            key_frames=key_frames,
            issues=issues
        )
        
        print(f"✅ Journey reconstructed: {len(steps)} steps, {len(issues)} issues found")
        return journey
    
    def detect_stuck_screens(self, frames: List[FrameInfo], issues: List[str]) -> None:
        """
        Detect screens that appear to be stuck (same content for extended periods).
        
        Args:
            frames: List of analyzed frames
            issues: List to append detected issues to
        """
        stuck_threshold = 10.0  # seconds
        current_hash = None
        stuck_start = None
        
        for frame in frames:
            if current_hash == frame.frame_hash:
                if stuck_start is None:
                    stuck_start = frame.timestamp
                elif frame.timestamp - stuck_start > stuck_threshold:
                    issues.append(f"Screen appears stuck from {stuck_start:.1f}s to {frame.timestamp:.1f}s")
                    stuck_start = None  # Reset to avoid duplicate reports
            else:
                current_hash = frame.frame_hash
                stuck_start = None
    
    def compare_with_spec(self, journey: UserJourney, enhanced_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare the observed journey with the enhanced specification.
        
        Args:
            journey: Reconstructed user journey
            enhanced_spec: Enhanced specification JSON
            
        Returns:
            Comparison results dictionary
        """
        print("🔍 Comparing journey with enhanced specification...")
        
        comparison_results = {
            "spec_coverage": 0.0,
            "missing_flows": [],
            "unexpected_flows": [],
            "timing_issues": [],
            "ui_deviations": [],
            "overall_score": 0.0
        }
        
        # Extract expected flows from spec
        expected_flows = self.extract_expected_flows(enhanced_spec)
        observed_steps = [step.lower() for step in journey.steps]
        
        # Check spec coverage
        covered_flows = 0
        for expected_flow in expected_flows:
            flow_found = any(expected_flow.lower() in step for step in observed_steps)
            if flow_found:
                covered_flows += 1
            else:
                comparison_results["missing_flows"].append(expected_flow)
        
        if expected_flows:
            comparison_results["spec_coverage"] = covered_flows / len(expected_flows)
        
        # Check for unexpected flows (basic implementation)
        common_flows = ["login", "submit", "navigation", "error"]
        for step in journey.steps:
            step_lower = step.lower()
            if not any(flow in step_lower for flow in common_flows + expected_flows):
                comparison_results["unexpected_flows"].append(step)
        
        # Check timing issues
        for transition in journey.transitions:
            if transition.transition_type == "error_state":
                comparison_results["timing_issues"].append(f"Error at {transition.to_timestamp:.1f}s")
        
        # Add journey issues as UI deviations
        comparison_results["ui_deviations"] = journey.issues
        
        # Calculate overall score
        coverage_score = comparison_results["spec_coverage"]
        issue_penalty = min(len(journey.issues) * 0.1, 0.5)
        comparison_results["overall_score"] = max(0.0, coverage_score - issue_penalty)
        
        print(f"📊 Spec coverage: {coverage_score:.1%}")
        print(f"🎯 Overall score: {comparison_results['overall_score']:.1%}")
        
        return comparison_results
    
    def extract_expected_flows(self, enhanced_spec: Dict[str, Any]) -> List[str]:
        """
        Extract expected user flows from the enhanced specification.
        
        Args:
            enhanced_spec: Enhanced specification dictionary
            
        Returns:
            List of expected flow descriptions
        """
        expected_flows = []
        
        # Look for user flows in various spec formats
        if "user_flows" in enhanced_spec:
            expected_flows.extend(enhanced_spec["user_flows"])
        
        if "features" in enhanced_spec:
            for feature in enhanced_spec["features"]:
                if isinstance(feature, dict) and "flow" in feature:
                    expected_flows.append(feature["flow"])
                elif isinstance(feature, str):
                    expected_flows.append(feature)
        
        if "workflows" in enhanced_spec:
            expected_flows.extend(enhanced_spec["workflows"])
        
        # Default flows if none specified
        if not expected_flows:
            expected_flows = ["user authentication", "main navigation", "form submission", "data display"]
        
        return expected_flows
    
    def save_key_frame(self, frame: np.ndarray, frame_info: FrameInfo) -> str:
        """
        Save a key frame to the output directory.
        
        Args:
            frame: OpenCV frame to save
            frame_info: Frame information
            
        Returns:
            Path to saved frame file
        """
        filename = f"frame_{frame_info.frame_number:06d}_{frame_info.timestamp:.1f}s.jpg"
        filepath = self.output_dir / filename
        
        cv2.imwrite(str(filepath), frame)
        return str(filepath)
    
    def analyze_video(self, video_path: str, enhanced_spec_path: str) -> Dict[str, Any]:
        """
        Main method to analyze a screen recording video.
        
        Args:
            video_path: Path to the video file
            enhanced_spec_path: Path to the enhanced specification JSON
            
        Returns:
            Complete analysis results dictionary
        """
        print(f"🎬 Starting analysis of: {video_path}")
        print(f"📋 Using spec: {enhanced_spec_path}")
        
        # Load enhanced specification
        try:
            with open(enhanced_spec_path, 'r') as f:
                enhanced_spec = json.load(f)
        except Exception as e:
            print(f"❌ Error loading spec: {e}")
            return {"error": f"Failed to load specification: {e}"}
        
        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {"error": f"Failed to open video file: {video_path}"}
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"📹 Video info: {total_frames} frames, {fps:.1f} FPS, {duration:.1f}s duration")
        
        # Calculate frame sampling interval
        frame_interval = int(fps / self.sampling_fps) if fps > 0 else 1
        
        # Process frames
        frame_count = 0
        processed_frames = 0
        prev_frame = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frames at specified rate
            if frame_count % frame_interval == 0:
                timestamp = frame_count / fps if fps > 0 else frame_count
                
                # Calculate frame hash and difference
                frame_hash = self.calculate_frame_hash(frame)
                change_score = 0.0
                is_key_frame = processed_frames == 0  # First frame is always key
                
                if prev_frame is not None:
                    change_score = self.calculate_frame_difference(prev_frame, frame)
                    is_key_frame = change_score > self.change_threshold
                
                # Extract text and UI elements
                extracted_text, ui_elements = self.extract_text_from_frame(frame)
                
                # Create frame info
                frame_info = FrameInfo(
                    frame_number=frame_count,
                    timestamp=timestamp,
                    frame_hash=frame_hash,
                    extracted_text=extracted_text,
                    is_key_frame=is_key_frame,
                    change_score=change_score,
                    ui_elements=ui_elements
                )
                
                self.frames.append(frame_info)
                
                # Save key frames
                if is_key_frame:
                    saved_path = self.save_key_frame(frame, frame_info)
                    print(f"🖼️  Key frame saved: {saved_path} (change: {change_score:.3f})")
                
                prev_frame = frame.copy()
                processed_frames += 1
                
                # Progress indicator
                if processed_frames % 10 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"⏳ Progress: {progress:.1f}% ({processed_frames} frames processed)")
            
            frame_count += 1
        
        cap.release()
        
        print(f"✅ Video processing complete: {processed_frames} frames analyzed")
        
        # Detect transitions
        self.transitions = self.detect_ui_transitions(self.frames)
        
        # Reconstruct user journey
        journey = self.reconstruct_user_journey(self.frames, self.transitions)
        
        # Compare with specification
        comparison = self.compare_with_spec(journey, enhanced_spec)
        
        # Compile final results
        results = {
            "video_info": {
                "path": video_path,
                "duration": duration,
                "fps": fps,
                "total_frames": total_frames,
                "processed_frames": processed_frames
            },
            "analysis_summary": {
                "key_frames_detected": len([f for f in self.frames if f.is_key_frame]),
                "transitions_detected": len(self.transitions),
                "journey_steps": len(journey.steps),
                "issues_found": len(journey.issues)
            },
            "user_journey": asdict(journey),
            "spec_comparison": comparison,
            "frames": [asdict(f) for f in self.frames],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return results
    
    def generate_report(self, results: Dict[str, Any], output_path: str = "screen_analysis_report.md") -> None:
        """
        Generate a comprehensive Markdown report.
        
        Args:
            results: Analysis results dictionary
            output_path: Path to save the report
        """
        print(f"📝 Generating report: {output_path}")
        
        report_lines = [
            "# Screen Recording Analysis Report",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "## 📹 Video Information",
            f"- **File**: {results['video_info']['path']}",
            f"- **Duration**: {results['video_info']['duration']:.1f} seconds",
            f"- **FPS**: {results['video_info']['fps']:.1f}",
            f"- **Frames Processed**: {results['video_info']['processed_frames']}",
            "",
            "## 📊 Analysis Summary",
            f"- **Key Frames Detected**: {results['analysis_summary']['key_frames_detected']}",
            f"- **UI Transitions**: {results['analysis_summary']['transitions_detected']}",
            f"- **Journey Steps**: {results['analysis_summary']['journey_steps']}",
            f"- **Issues Found**: {results['analysis_summary']['issues_found']}",
            "",
            "## 🗺️ User Journey Flow"
        ]
        
        # Add journey steps
        journey = results['user_journey']
        for i, step in enumerate(journey['steps'], 1):
            report_lines.append(f"{i}. {step}")
        
        report_lines.extend([
            "",
            "## 🔄 UI Transitions",
            ""
        ])
        
        # Add transitions
        for transition in journey['transitions']:
            report_lines.extend([
                f"### {transition['transition_type'].title()} Transition",
                f"- **Time**: {transition['from_timestamp']:.1f}s → {transition['to_timestamp']:.1f}s",
                f"- **Description**: {transition['description']}",
                f"- **Confidence**: {transition['confidence']:.1%}",
                ""
            ])
        
        # Add spec comparison
        comparison = results['spec_comparison']
        report_lines.extend([
            "## 📋 Specification Comparison",
            f"- **Coverage**: {comparison['spec_coverage']:.1%}",
            f"- **Overall Score**: {comparison['overall_score']:.1%}",
            ""
        ])
        
        if comparison['missing_flows']:
            report_lines.extend([
                "### ❌ Missing Expected Flows",
                ""
            ])
            for flow in comparison['missing_flows']:
                report_lines.append(f"- {flow}")
            report_lines.append("")
        
        if comparison['unexpected_flows']:
            report_lines.extend([
                "### ⚠️ Unexpected Flows",
                ""
            ])
            for flow in comparison['unexpected_flows']:
                report_lines.append(f"- {flow}")
            report_lines.append("")
        
        # Add issues
        if journey['issues']:
            report_lines.extend([
                "## 🚨 Issues Detected",
                ""
            ])
            for issue in journey['issues']:
                report_lines.append(f"- {issue}")
            report_lines.append("")
        
        # Add recommendations
        report_lines.extend([
            "## 💡 Recommendations",
            ""
        ])
        
        if comparison['spec_coverage'] < 0.8:
            report_lines.append("- Review missing flows and ensure all expected functionality is implemented")
        
        if len(journey['issues']) > 0:
            report_lines.append("- Address detected UI issues and stuck screens")
        
        if comparison['overall_score'] < 0.7:
            report_lines.append("- Consider UX improvements to enhance user flow")
        
        report_lines.append("- Test the application with real users to validate the analysis")
        
        # Write report to file
        with open(output_path, 'w') as f:
            f.write('\n'.join(report_lines))
        
        print(f"✅ Report saved to: {output_path}")


def main():
    """
    Main function to demonstrate the Screen Recording Analyzer.
    """
    print("🎬 Screen Recording Analyzer - Demo")
    print("=" * 50)
    
    # Example usage
    analyzer = ScreenRecordingAnalyzer(
        output_dir="output_frames",
        sampling_fps=1.0
    )
    
    # Note: These would be actual file paths in real usage
    video_path = "sample_screen_recording.mp4"
    spec_path = "sample_enhanced_spec.json"
    
    print(f"📁 Expected video file: {video_path}")
    print(f"📋 Expected spec file: {spec_path}")
    print("\n⚠️  To run analysis, provide actual video and spec files")
    print("💡 Example usage:")
    print("   results = analyzer.analyze_video('your_video.mp4', 'your_spec.json')")
    print("   analyzer.generate_report(results)")
    
    # Create sample enhanced spec for testing
    sample_spec = {
        "user_flows": [
            "User authentication flow",
            "Main dashboard navigation",
            "Form submission process",
            "Data visualization display"
        ],
        "features": [
            {"name": "Login", "flow": "User enters credentials and submits"},
            {"name": "Dashboard", "flow": "User views main dashboard"},
            {"name": "Forms", "flow": "User fills and submits forms"}
        ],
        "expected_screens": [
            "Login Screen",
            "Dashboard",
            "Form Page",
            "Success Page"
        ]
    }
    
    # Save sample spec
    with open("sample_enhanced_spec.json", 'w') as f:
        json.dump(sample_spec, f, indent=2)
    
    print(f"📄 Sample spec created: sample_enhanced_spec.json")


if __name__ == "__main__":
    main()