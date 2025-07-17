#!/usr/bin/env python3
"""
CodeAnalyzer Module for AI-Powered Debugging Assistant

This module recursively analyzes code directories to extract features including:
- Functions and classes
- Imported libraries
- Data models and schemas
- File structure and dependencies

Author: AI-Powered Debugging Assistant
Version: 1.0.0
"""

import os
import ast
import json
import re
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
from dataclasses import dataclass, asdict
import argparse


@dataclass
class FunctionInfo:
    """Information about a function definition."""
    name: str
    args: List[str]
    decorators: List[str]
    docstring: Optional[str]
    line_number: int
    is_async: bool = False


@dataclass
class ClassInfo:
    """Information about a class definition."""
    name: str
    bases: List[str]
    methods: List[FunctionInfo]
    decorators: List[str]
    docstring: Optional[str]
    line_number: int


@dataclass
class ImportInfo:
    """Information about imports in a file."""
    module: str
    names: List[str]
    alias: Optional[str] = None
    is_from_import: bool = False


@dataclass
class DataModelInfo:
    """Information about data models/schemas."""
    name: str
    type: str  # 'dataclass', 'pydantic', 'sqlalchemy', 'interface', 'type'
    fields: List[Dict[str, Any]]
    line_number: int


@dataclass
class FileAnalysis:
    """Analysis results for a single file."""
    file_path: str
    language: str
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: List[ImportInfo]
    data_models: List[DataModelInfo]
    lines_of_code: int
    complexity_score: int


@dataclass
class FeatureMap:
    """Complete feature map of the analyzed codebase."""
    project_name: str
    total_files: int
    total_lines: int
    languages: Dict[str, int]
    files: List[FileAnalysis]
    global_imports: Set[str]
    global_functions: Set[str]
    global_classes: Set[str]
    data_models: List[DataModelInfo]


class CodeAnalyzer:
    """
    Main code analyzer class that processes code directories and extracts features.
    """
    
    SUPPORTED_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.jsx': 'javascript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust'
    }
    
    IGNORE_DIRS = {
        'node_modules', '.git', '__pycache__', '.venv', 'venv', 
        'env', 'build', 'dist', '.next', 'coverage', '.pytest_cache'
    }
    
    def __init__(self, project_path: str):
        """
        Initialize the CodeAnalyzer.
        
        Args:
            project_path: Path to the project directory to analyze
        """
        self.project_path = Path(project_path)
        self.feature_map = None
        
    def analyze_project(self) -> FeatureMap:
        """
        Analyze the entire project and generate a feature map.
        
        Returns:
            FeatureMap: Complete analysis of the project
        """
        print(f"🔍 Analyzing project: {self.project_path}")
        
        files_analysis = []
        languages = {}
        total_lines = 0
        global_imports = set()
        global_functions = set()
        global_classes = set()
        all_data_models = []
        
        # Walk through all files in the project
        for file_path in self._get_code_files():
            try:
                analysis = self._analyze_file(file_path)
                if analysis:
                    files_analysis.append(analysis)
                    
                    # Update global statistics
                    languages[analysis.language] = languages.get(analysis.language, 0) + 1
                    total_lines += analysis.lines_of_code
                    
                    # Collect global imports, functions, classes
                    for imp in analysis.imports:
                        global_imports.add(imp.module)
                    for func in analysis.functions:
                        global_functions.add(func.name)
                    for cls in analysis.classes:
                        global_classes.add(cls.name)
                    
                    # Collect data models
                    all_data_models.extend(analysis.data_models)
                    
            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")
                continue
        
        # Create feature map
        self.feature_map = FeatureMap(
            project_name=self.project_path.name,
            total_files=len(files_analysis),
            total_lines=total_lines,
            languages=languages,
            files=files_analysis,
            global_imports=global_imports,
            global_functions=global_functions,
            global_classes=global_classes,
            data_models=all_data_models
        )
        
        return self.feature_map
    
    def _get_code_files(self) -> List[Path]:
        """
        Get all code files in the project directory.
        
        Returns:
            List of Path objects for code files
        """
        code_files = []
        
        for root, dirs, files in os.walk(self.project_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    code_files.append(file_path)
        
        return code_files
    
    def _analyze_file(self, file_path: Path) -> Optional[FileAnalysis]:
        """
        Analyze a single code file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            FileAnalysis object or None if analysis failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            language = self.SUPPORTED_EXTENSIONS.get(file_path.suffix.lower(), 'unknown')
            lines_of_code = len([line for line in content.split('\n') if line.strip()])
            
            # Analyze based on language
            if language == 'python':
                return self._analyze_python_file(file_path, content, lines_of_code)
            elif language in ['javascript', 'typescript']:
                return self._analyze_js_ts_file(file_path, content, lines_of_code, language)
            else:
                # Basic analysis for other languages
                return FileAnalysis(
                    file_path=str(file_path.relative_to(self.project_path)),
                    language=language,
                    functions=[],
                    classes=[],
                    imports=[],
                    data_models=[],
                    lines_of_code=lines_of_code,
                    complexity_score=self._calculate_basic_complexity(content)
                )
                
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    def _analyze_python_file(self, file_path: Path, content: str, lines_of_code: int) -> FileAnalysis:
        """
        Analyze a Python file using AST.
        
        Args:
            file_path: Path to the Python file
            content: File content
            lines_of_code: Number of lines of code
            
        Returns:
            FileAnalysis object
        """
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return FileAnalysis(
                file_path=str(file_path.relative_to(self.project_path)),
                language='python',
                functions=[],
                classes=[],
                imports=[],
                data_models=[],
                lines_of_code=lines_of_code,
                complexity_score=0
            )
        
        functions = []
        classes = []
        imports = []
        data_models = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                func_info = FunctionInfo(
                    name=node.name,
                    args=[arg.arg for arg in node.args.args],
                    decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
                    docstring=ast.get_docstring(node),
                    line_number=node.lineno,
                    is_async=isinstance(node, ast.AsyncFunctionDef)
                )
                functions.append(func_info)
                
            elif isinstance(node, ast.ClassDef):
                class_methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_info = FunctionInfo(
                            name=item.name,
                            args=[arg.arg for arg in item.args.args],
                            decorators=[self._get_decorator_name(dec) for dec in item.decorator_list],
                            docstring=ast.get_docstring(item),
                            line_number=item.lineno,
                            is_async=isinstance(item, ast.AsyncFunctionDef)
                        )
                        class_methods.append(method_info)
                
                class_info = ClassInfo(
                    name=node.name,
                    bases=[self._get_base_name(base) for base in node.bases],
                    methods=class_methods,
                    decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
                    docstring=ast.get_docstring(node),
                    line_number=node.lineno
                )
                classes.append(class_info)
                
                # Check if it's a data model
                if self._is_data_model(node):
                    data_model = self._extract_data_model(node)
                    if data_model:
                        data_models.append(data_model)
                        
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_info = ImportInfo(
                        module=alias.name,
                        names=[alias.name],
                        alias=alias.asname,
                        is_from_import=False
                    )
                    imports.append(import_info)
                    
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names = [alias.name for alias in node.names]
                    import_info = ImportInfo(
                        module=node.module,
                        names=names,
                        is_from_import=True
                    )
                    imports.append(import_info)
        
        return FileAnalysis(
            file_path=str(file_path.relative_to(self.project_path)),
            language='python',
            functions=functions,
            classes=classes,
            imports=imports,
            data_models=data_models,
            lines_of_code=lines_of_code,
            complexity_score=self._calculate_python_complexity(tree)
        )
    
    def _analyze_js_ts_file(self, file_path: Path, content: str, lines_of_code: int, language: str) -> FileAnalysis:
        """
        Analyze JavaScript/TypeScript files using regex patterns.
        
        Args:
            file_path: Path to the JS/TS file
            content: File content
            lines_of_code: Number of lines of code
            language: 'javascript' or 'typescript'
            
        Returns:
            FileAnalysis object
        """
        functions = []
        classes = []
        imports = []
        data_models = []
        
        # Extract functions
        func_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*\([^)]*\)\s*=>',
            r'async\s+function\s+(\w+)\s*\([^)]*\)'
        ]
        
        for pattern in func_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                func_name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                
                func_info = FunctionInfo(
                    name=func_name,
                    args=[],  # Would need more complex parsing for args
                    decorators=[],
                    docstring=None,
                    line_number=line_num,
                    is_async='async' in match.group(0)
                )
                functions.append(func_info)
        
        # Extract classes
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
        class_matches = re.finditer(class_pattern, content, re.MULTILINE)
        for match in class_matches:
            class_name = match.group(1)
            base_class = match.group(2) if match.group(2) else None
            line_num = content[:match.start()].count('\n') + 1
            
            class_info = ClassInfo(
                name=class_name,
                bases=[base_class] if base_class else [],
                methods=[],  # Would need more complex parsing
                decorators=[],
                docstring=None,
                line_number=line_num
            )
            classes.append(class_info)
        
        # Extract imports
        import_patterns = [
            r'import\s+(.+?)\s+from\s+[\'"](.+?)[\'"]',
            r'import\s+[\'"](.+?)[\'"]',
            r'const\s+(.+?)\s+=\s+require\([\'"](.+?)[\'"]\)'
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                if len(match.groups()) == 2:
                    names = [match.group(1).strip()]
                    module = match.group(2)
                else:
                    names = []
                    module = match.group(1)
                
                import_info = ImportInfo(
                    module=module,
                    names=names,
                    is_from_import=True
                )
                imports.append(import_info)
        
        # Extract TypeScript interfaces and types
        if language == 'typescript':
            interface_pattern = r'interface\s+(\w+)'
            type_pattern = r'type\s+(\w+)\s*='
            
            for pattern, model_type in [(interface_pattern, 'interface'), (type_pattern, 'type')]:
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    name = match.group(1)
                    line_num = content[:match.start()].count('\n') + 1
                    
                    data_model = DataModelInfo(
                        name=name,
                        type=model_type,
                        fields=[],  # Would need more complex parsing
                        line_number=line_num
                    )
                    data_models.append(data_model)
        
        return FileAnalysis(
            file_path=str(file_path.relative_to(self.project_path)),
            language=language,
            functions=functions,
            classes=classes,
            imports=imports,
            data_models=data_models,
            lines_of_code=lines_of_code,
            complexity_score=self._calculate_basic_complexity(content)
        )
    
    def _get_decorator_name(self, decorator) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{decorator.value.id}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return f"{decorator.func.value.id}.{decorator.func.attr}"
        return str(decorator)
    
    def _get_base_name(self, base) -> str:
        """Extract base class name from AST node."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id}.{base.attr}"
        return str(base)
    
    def _is_data_model(self, node: ast.ClassDef) -> bool:
        """Check if a class is a data model."""
        decorators = [self._get_decorator_name(dec) for dec in node.decorator_list]
        bases = [self._get_base_name(base) for base in node.bases]
        
        data_model_indicators = [
            'dataclass', 'dataclasses.dataclass',
            'BaseModel', 'pydantic.BaseModel',
            'Model', 'django.db.models.Model',
            'SQLModel', 'sqlalchemy'
        ]
        
        return any(indicator in decorators + bases for indicator in data_model_indicators)
    
    def _extract_data_model(self, node: ast.ClassDef) -> Optional[DataModelInfo]:
        """Extract data model information from a class."""
        fields = []
        
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                field_name = item.target.id
                field_type = ast.unparse(item.annotation) if item.annotation else 'Any'
                
                fields.append({
                    'name': field_name,
                    'type': field_type,
                    'default': ast.unparse(item.value) if item.value else None
                })
        
        model_type = 'dataclass'
        decorators = [self._get_decorator_name(dec) for dec in node.decorator_list]
        if 'BaseModel' in [self._get_base_name(base) for base in node.bases]:
            model_type = 'pydantic'
        elif any('Model' in dec for dec in decorators):
            model_type = 'sqlalchemy'
        
        return DataModelInfo(
            name=node.name,
            type=model_type,
            fields=fields,
            line_number=node.lineno
        )
    
    def _calculate_python_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for Python code."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _calculate_basic_complexity(self, content: str) -> int:
        """Calculate basic complexity based on control flow keywords."""
        keywords = ['if', 'else', 'elif', 'while', 'for', 'switch', 'case', 'try', 'catch']
        complexity = 1
        
        for keyword in keywords:
            complexity += content.count(keyword)
        
        return complexity
    
    def print_summary(self):
        """Print a summary of the analysis results."""
        if not self.feature_map:
            print("❌ No analysis results available. Run analyze_project() first.")
            return
        
        fm = self.feature_map
        
        print("\n" + "="*60)
        print(f"📊 CODE ANALYSIS SUMMARY: {fm.project_name}")
        print("="*60)
        
        print(f"📁 Total Files: {fm.total_files}")
        print(f"📝 Total Lines: {fm.total_lines:,}")
        
        print(f"\n🔤 Languages:")
        for lang, count in fm.languages.items():
            print(f"   • {lang.title()}: {count} files")
        
        print(f"\n📦 Global Imports: {len(fm.global_imports)}")
        if fm.global_imports:
            popular_imports = sorted(fm.global_imports)[:10]
            print(f"   Top imports: {', '.join(popular_imports)}")
        
        print(f"\n🔧 Global Functions: {len(fm.global_functions)}")
        print(f"🏗️  Global Classes: {len(fm.global_classes)}")
        print(f"📋 Data Models: {len(fm.data_models)}")
        
        if fm.data_models:
            print(f"\n📋 Data Models Found:")
            for model in fm.data_models[:5]:  # Show first 5
                print(f"   • {model.name} ({model.type}) - {len(model.fields)} fields")
        
        print(f"\n🔍 Most Complex Files:")
        sorted_files = sorted(fm.files, key=lambda x: x.complexity_score, reverse=True)
        for file_analysis in sorted_files[:5]:
            print(f"   • {file_analysis.file_path} (complexity: {file_analysis.complexity_score})")
        
        print("\n" + "="*60)
    
    def save_feature_map(self, output_path: str = "feature_map.json"):
        """
        Save the feature map to a JSON file.
        
        Args:
            output_path: Path to save the JSON file
        """
        if not self.feature_map:
            print("❌ No analysis results available. Run analyze_project() first.")
            return
        
        # Convert to dictionary for JSON serialization
        feature_map_dict = asdict(self.feature_map)
        
        # Convert sets to lists for JSON serialization
        feature_map_dict['global_imports'] = list(self.feature_map.global_imports)
        feature_map_dict['global_functions'] = list(self.feature_map.global_functions)
        feature_map_dict['global_classes'] = list(self.feature_map.global_classes)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(feature_map_dict, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Feature map saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ Error saving feature map: {e}")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Analyze code directory and extract features')
    parser.add_argument('project_path', help='Path to the project directory to analyze')
    parser.add_argument('-o', '--output', default='feature_map.json', 
                       help='Output JSON file path (default: feature_map.json)')
    parser.add_argument('--no-summary', action='store_true', 
                       help='Skip printing summary to console')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project_path):
        print(f"❌ Error: Project path '{args.project_path}' does not exist.")
        return
    
    # Initialize and run analyzer
    analyzer = CodeAnalyzer(args.project_path)
    
    print("🚀 Starting code analysis...")
    feature_map = analyzer.analyze_project()
    
    if not args.no_summary:
        analyzer.print_summary()
    
    analyzer.save_feature_map(args.output)
    
    print(f"\n✨ Analysis complete! Results saved to {args.output}")


if __name__ == "__main__":
    main()