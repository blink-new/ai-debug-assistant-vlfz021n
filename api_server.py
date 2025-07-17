#!/usr/bin/env python3
"""
Simple API Server for AI Debug Assistant

Provides REST endpoints for the Python backend modules.
"""

import json
import os
import tempfile
import zipfile
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# Import our modules
from prompt_refiner import PromptRefiner
from code_analyzer import CodeAnalyzer
from spec_comparer import SpecComparer
from debugger_engine import DebuggerEngine
from run_full_analysis import run_full_analysis


class APIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the API"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.send_json_response({'message': 'AI Debug Assistant API', 'version': '1.0.0'})
        elif path == '/health':
            self.send_json_response({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
        elif path == '/modules':
            self.send_json_response({
                'modules': [
                    'prompt_refiner',
                    'code_analyzer', 
                    'spec_comparer',
                    'debugger_engine',
                    'full_analysis'
                ]
            })
        else:
            self.send_error(404, 'Endpoint not found')
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if path == '/refine-prompt':
                self.handle_refine_prompt(data)
            elif path == '/analyze-code':
                self.handle_analyze_code(data)
            elif path == '/compare-spec':
                self.handle_compare_spec(data)
            elif path == '/debug-analysis':
                self.handle_debug_analysis(data)
            elif path == '/full-analysis':
                self.handle_full_analysis(data)
            else:
                self.send_error(404, 'Endpoint not found')
                
        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON')
        except Exception as e:
            self.send_error(500, f'Internal server error: {str(e)}')
    
    def handle_refine_prompt(self, data):
        """Handle prompt refinement requests"""
        original_prompt = data.get('prompt', '')
        if not original_prompt:
            self.send_error(400, 'Missing prompt field')
            return
        
        refiner = PromptRefiner()
        enhanced_spec = refiner.refine_prompt(original_prompt)
        
        self.send_json_response({
            'success': True,
            'enhanced_spec': enhanced_spec,
            'timestamp': datetime.now().isoformat()
        })
    
    def handle_analyze_code(self, data):
        """Handle code analysis requests"""
        codebase_path = data.get('codebase_path', 'src/')
        
        analyzer = CodeAnalyzer()
        try:
            analysis_result = analyzer.analyze_codebase(codebase_path)
            self.send_json_response({
                'success': True,
                'analysis': analysis_result,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    def handle_compare_spec(self, data):
        """Handle spec comparison requests"""
        enhanced_spec = data.get('enhanced_spec')
        codebase_path = data.get('codebase_path', 'src/')
        
        if not enhanced_spec:
            self.send_error(400, 'Missing enhanced_spec field')
            return
        
        # Save enhanced spec to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(enhanced_spec, f, indent=2)
            spec_file = f.name
        
        try:
            comparer = SpecComparer()
            comparison_result = comparer.compare_spec_to_codebase(spec_file, codebase_path)
            
            self.send_json_response({
                'success': True,
                'comparison': comparison_result,
                'timestamp': datetime.now().isoformat()
            })
        finally:
            # Clean up temporary file
            os.unlink(spec_file)
    
    def handle_debug_analysis(self, data):
        """Handle debug analysis requests"""
        comparison_report = data.get('comparison_report')
        
        if not comparison_report:
            self.send_error(400, 'Missing comparison_report field')
            return
        
        # Save comparison report to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(comparison_report, f, indent=2)
            report_file = f.name
        
        try:
            engine = DebuggerEngine()
            if not engine.load_comparison_report(report_file):
                self.send_json_response({
                    'success': False,
                    'error': 'Failed to load comparison report'
                })
                return
            
            bugs = engine.analyze_bugs()
            fixes = engine.generate_fixes()
            
            self.send_json_response({
                'success': True,
                'bugs': [engine._bug_to_dict(bug) for bug in bugs],
                'fixes': [engine._fix_to_dict(fix) for fix in fixes],
                'summary': {
                    'total_bugs': len(bugs),
                    'total_fixes': len(fixes),
                    'bugs_by_severity': engine._get_bugs_by_severity()
                },
                'timestamp': datetime.now().isoformat()
            })
        finally:
            # Clean up temporary file
            os.unlink(report_file)
    
    def handle_full_analysis(self, data):
        """Handle full analysis pipeline requests"""
        original_prompt = data.get('prompt', '')
        codebase_path = data.get('codebase_path', 'src/')
        
        if not original_prompt:
            self.send_error(400, 'Missing prompt field')
            return
        
        # Run analysis in background thread to avoid timeout
        def run_analysis():
            try:
                success = run_full_analysis(original_prompt, codebase_path)
                # Store result for later retrieval
                # In a real implementation, you'd use a database or cache
                print(f"Analysis completed: {'Success' if success else 'Failed'}")
            except Exception as e:
                print(f"Analysis failed: {e}")
        
        analysis_thread = threading.Thread(target=run_analysis)
        analysis_thread.start()
        
        self.send_json_response({
            'success': True,
            'message': 'Full analysis started in background',
            'status': 'processing',
            'timestamp': datetime.now().isoformat()
        })
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def main():
    """Start the API server"""
    port = int(os.environ.get('PORT', 8000))
    
    print(f"🚀 Starting AI Debug Assistant API Server on port {port}")
    print(f"📡 Available endpoints:")
    print(f"   GET  / - API info")
    print(f"   GET  /health - Health check")
    print(f"   GET  /modules - Available modules")
    print(f"   POST /refine-prompt - Refine original prompt")
    print(f"   POST /analyze-code - Analyze codebase")
    print(f"   POST /compare-spec - Compare spec to code")
    print(f"   POST /debug-analysis - Generate bug reports")
    print(f"   POST /full-analysis - Run complete pipeline")
    print(f"")
    print(f"🔧 CORS enabled for all origins")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🔑 OpenAI API Key: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print("=" * 60)
    
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n🛑 Server stopped by user")
        server.shutdown()


if __name__ == '__main__':
    main()