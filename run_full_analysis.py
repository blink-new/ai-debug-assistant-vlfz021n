#!/usr/bin/env python3
"""
Full Analysis Pipeline Runner

This script runs the complete AI-Powered Debugging Assistant analysis pipeline:
1. PromptRefiner - Enhance the original prompt
2. CodeAnalyzer - Analyze the codebase
3. SpecComparer - Compare spec with implementation
4. DebuggerEngine - Generate bug reports and fixes

Usage:
    python run_full_analysis.py [prompt] [codebase_path]
    
Example:
    python run_full_analysis.py "Create a todo app" "./src"
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Import our modules
from prompt_refiner import PromptRefiner
from code_analyzer import CodeAnalyzer
from spec_comparer import SpecComparer
from debugger_engine import DebuggerEngine


def main():
    """Run the complete analysis pipeline"""
    parser = argparse.ArgumentParser(description='Run complete AI debugging analysis pipeline')
    parser.add_argument('prompt', nargs='?', 
                       default="Create a simple e-commerce app where users can buy and sell products",
                       help='Original app prompt/specification')
    parser.add_argument('codebase_path', nargs='?', 
                       default="./src",
                       help='Path to the codebase to analyze')
    parser.add_argument('--output-dir', '-o', 
                       default="./test_output",
                       help='Output directory for results')
    parser.add_argument('--fixes-dir', '-f',
                       default="./fixes", 
                       help='Directory for generated fixes')
    
    args = parser.parse_args()
    
    # Create output directories
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.fixes_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🚀 Starting AI-Powered Debugging Assistant Analysis Pipeline")
    print("=" * 70)
    print(f"📝 Prompt: {args.prompt}")
    print(f"📁 Codebase: {args.codebase_path}")
    print(f"📊 Output: {args.output_dir}")
    print(f"🔧 Fixes: {args.fixes_dir}")
    print("=" * 70)
    
    try:
        # Step 1: Enhance the prompt
        print("\\n🔍 Step 1: Enhancing Prompt Specification...")
        refiner = PromptRefiner()
        enhanced_spec = refiner.refine_prompt(args.prompt)
        
        spec_file = os.path.join(args.output_dir, f"enhanced_spec_{timestamp}.json")
        refiner.save_enhanced_spec(enhanced_spec, spec_file)
        print(f"✅ Enhanced specification saved to: {spec_file}")
        
        # Step 2: Analyze the codebase
        print("\\n🔍 Step 2: Analyzing Codebase...")
        if not os.path.exists(args.codebase_path):
            print(f"⚠️  Codebase path not found: {args.codebase_path}")
            print("📁 Using current directory for analysis...")
            args.codebase_path = "."
        
        analyzer = CodeAnalyzer(args.codebase_path)
        feature_map = analyzer.analyze_project()
        
        feature_map_file = os.path.join(args.output_dir, f"feature_map_{timestamp}.json")
        analyzer.save_feature_map(feature_map_file)
        print(f"✅ Feature map saved to: {feature_map_file}")
        
        # Step 3: Compare specifications
        print("\\n🔍 Step 3: Comparing Specifications with Implementation...")
        comparer = SpecComparer()
        
        # Load the generated files
        comparer.load_enhanced_spec(spec_file)
        comparer.load_feature_map(feature_map_file)
        
        # Perform comparison
        comparison_results = comparer.compare_specifications()
        
        # Save comparison report
        comparison_dir = os.path.join(args.output_dir, f"comparison_{timestamp}")
        json_path, md_path = comparer.save_comparison_report(comparison_dir)
        print(f"✅ Comparison report saved to: {comparison_dir}")
        
        # Step 4: Generate bug reports and fixes
        print("\\n🔍 Step 4: Generating Bug Reports and Fixes...")
        engine = DebuggerEngine(args.fixes_dir)
        
        # Load comparison report
        engine.load_comparison_report(json_path)
        
        # Optional: Load logs and UI flows (stubbed for now)
        engine.load_logs("logs.json")  # Stubbed
        engine.load_ui_flows("ui_flows.json")  # Stubbed
        
        # Analyze bugs and generate fixes
        bugs = engine.analyze_bugs()
        fixes = engine.generate_fixes()
        engine.save_fixes()
        
        print(f"✅ Generated {len(fixes)} fixes for {len(bugs)} bugs")
        
        # Step 5: Generate final summary report
        print("\\n🔍 Step 5: Generating Final Analysis Report...")
        final_report = {
            "analysis_timestamp": timestamp,
            "input": {
                "original_prompt": args.prompt,
                "codebase_path": args.codebase_path
            },
            "results": {
                "enhanced_spec_file": spec_file,
                "feature_map_file": feature_map_file,
                "comparison_report": json_path,
                "comparison_markdown": md_path,
                "fixes_directory": args.fixes_dir
            },
            "summary": {
                "total_features_specified": len(enhanced_spec.features),
                "total_files_analyzed": feature_map.total_files,
                "total_lines_analyzed": feature_map.total_lines,
                "languages_detected": list(feature_map.languages.keys()),
                "bugs_found": len(bugs),
                "fixes_generated": len(fixes),
                "health_score": comparison_results['summary']['health_score'],
                "overall_status": comparison_results['summary']['overall_status']
            },
            "recommendations": comparison_results['summary']['recommendations']
        }
        
        final_report_file = os.path.join(args.output_dir, f"final_analysis_report_{timestamp}.json")
        with open(final_report_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Final analysis report saved to: {final_report_file}")
        
        # Print final summary
        print("\\n" + "=" * 70)
        print("🎉 ANALYSIS PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"📊 Health Score: {final_report['summary']['health_score']}/100")
        print(f"📈 Status: {final_report['summary']['overall_status']}")
        print(f"🐛 Bugs Found: {final_report['summary']['bugs_found']}")
        print(f"🔧 Fixes Generated: {final_report['summary']['fixes_generated']}")
        print(f"📁 Files Analyzed: {final_report['summary']['total_files_analyzed']}")
        print(f"📝 Lines of Code: {final_report['summary']['total_lines_analyzed']:,}")
        print(f"🔤 Languages: {', '.join(final_report['summary']['languages_detected'])}")
        
        print("\\n📋 Key Recommendations:")
        for i, rec in enumerate(final_report['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print("\\n📁 Generated Files:")
        print(f"   • Enhanced Spec: {spec_file}")
        print(f"   • Feature Map: {feature_map_file}")
        print(f"   • Comparison Report: {json_path}")
        print(f"   • Markdown Report: {md_path}")
        print(f"   • Final Report: {final_report_file}")
        print(f"   • Fixes Directory: {args.fixes_dir}")
        
        print("\\n🚀 Next Steps:")
        print("   1. Review the generated reports")
        print("   2. Examine the bug fixes in the fixes directory")
        print("   3. Apply fixes using: git apply fixes/*.patch")
        print("   4. Use the web interface for interactive review")
        
        print("\\n" + "=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\\n❌ Error during analysis pipeline: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())