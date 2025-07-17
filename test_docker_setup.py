#!/usr/bin/env python3
"""
Test script to verify Docker setup and module functionality
"""

import json
import os
import sys
import time
import requests
from datetime import datetime

def test_environment():
    """Test environment setup"""
    print("🔧 Testing Environment Setup...")
    
    # Check Python version
    print(f"   Python version: {sys.version}")
    
    # Check required environment variables
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print(f"   ✅ OPENAI_API_KEY: Set (length: {len(openai_key)})")
    else:
        print("   ❌ OPENAI_API_KEY: Not set")
    
    # Check working directory
    print(f"   Working directory: {os.getcwd()}")
    
    # Check required files
    required_files = [
        'prompt_refiner.py',
        'code_analyzer.py', 
        'spec_comparer.py',
        'debugger_engine.py',
        'api_server.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}: Found")
        else:
            print(f"   ❌ {file}: Missing")
    
    print()

def test_module_imports():
    """Test module imports"""
    print("📦 Testing Module Imports...")
    
    modules = [
        ('prompt_refiner', 'PromptRefiner'),
        ('code_analyzer', 'CodeAnalyzer'),
        ('spec_comparer', 'SpecComparer'),
        ('debugger_engine', 'DebuggerEngine')
    ]
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            instance = cls()
            print(f"   ✅ {module_name}.{class_name}: OK")
        except Exception as e:
            print(f"   ❌ {module_name}.{class_name}: {e}")
    
    print()

def test_api_server():
    """Test API server endpoints"""
    print("🌐 Testing API Server...")
    
    base_url = "http://localhost:8000"
    
    # Test endpoints
    endpoints = [
        ('GET', '/'),
        ('GET', '/health'),
        ('GET', '/modules')
    ]
    
    for method, endpoint in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ {method} {endpoint}: {response.status_code}")
            else:
                print(f"   ❌ {method} {endpoint}: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {method} {endpoint}: Connection failed (server not running?)")
        except Exception as e:
            print(f"   ❌ {method} {endpoint}: {e}")
    
    print()

def test_basic_functionality():
    """Test basic module functionality"""
    print("⚙️  Testing Basic Functionality...")
    
    # Test PromptRefiner
    try:
        from prompt_refiner import PromptRefiner
        refiner = PromptRefiner()
        result = refiner.refine_prompt("Build a simple todo app")
        if result and 'enhanced_requirements' in result:
            print("   ✅ PromptRefiner: Working")
        else:
            print("   ❌ PromptRefiner: Invalid output")
    except Exception as e:
        print(f"   ❌ PromptRefiner: {e}")
    
    # Test CodeAnalyzer (without OpenAI)
    try:
        from code_analyzer import CodeAnalyzer
        analyzer = CodeAnalyzer()
        # Test with current directory
        if os.path.exists('src'):
            result = analyzer.analyze_codebase('src')
            print("   ✅ CodeAnalyzer: Working")
        else:
            print("   ⚠️  CodeAnalyzer: No src directory to test")
    except Exception as e:
        print(f"   ❌ CodeAnalyzer: {e}")
    
    # Test SpecComparer
    try:
        from spec_comparer import SpecComparer
        comparer = SpecComparer()
        print("   ✅ SpecComparer: Initialized")
    except Exception as e:
        print(f"   ❌ SpecComparer: {e}")
    
    # Test DebuggerEngine
    try:
        from debugger_engine import DebuggerEngine
        engine = DebuggerEngine()
        print("   ✅ DebuggerEngine: Initialized")
    except Exception as e:
        print(f"   ❌ DebuggerEngine: {e}")
    
    print()

def test_docker_health():
    """Test Docker container health"""
    print("🐳 Testing Docker Health...")
    
    # Check if running in Docker
    if os.path.exists('/.dockerenv'):
        print("   ✅ Running inside Docker container")
    else:
        print("   ⚠️  Not running in Docker container")
    
    # Check mounted volumes
    upload_dir = '/app/uploads'
    output_dir = '/app/output'
    
    for directory in [upload_dir, output_dir]:
        if os.path.exists(directory):
            print(f"   ✅ Directory {directory}: Exists")
        else:
            print(f"   ❌ Directory {directory}: Missing")
    
    # Check system dependencies
    import subprocess
    
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"   ✅ Tesseract: {version}")
        else:
            print("   ❌ Tesseract: Not working")
    except Exception as e:
        print(f"   ❌ Tesseract: {e}")
    
    print()

def main():
    """Run all tests"""
    print("🧪 AI Debug Assistant - Docker Setup Test")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    test_environment()
    test_module_imports()
    test_basic_functionality()
    test_docker_health()
    
    # Only test API server if it might be running
    if os.getenv('TEST_API_SERVER', '').lower() == 'true':
        test_api_server()
    
    print("🎉 Test completed!")
    print()
    print("Next steps:")
    print("1. If running in Docker: docker-compose up --build")
    print("2. If running locally: python api_server.py")
    print("3. Open http://localhost:3000 for frontend")
    print("4. Open http://localhost:8000 for API")

if __name__ == '__main__':
    main()