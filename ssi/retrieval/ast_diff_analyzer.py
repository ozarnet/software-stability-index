"""
AST Diff Analyzer - A reusable utility for detecting breaking changes between code versions.

This module provides a unified interface for analyzing differences between
Abstract Syntax Trees (ASTs) of code files to detect breaking changes.
It supports multiple programming languages and can be easily integrated
into other projects.

Supported Languages:
- Python (using ast module)
- JavaScript/TypeScript (planned)
- Go (planned)
- Rust (planned)

Usage:
    analyzer = ASTDiffAnalyzer()
    changes = analyzer.analyze_breaking_changes("old_file.py", "new_file.py")
    
    for change in changes:
        print(f"{change.severity}: {change.description}")
"""

import ast
import difflib
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Set, Tuple
import importlib.util


class ChangeType(Enum):
    """Types of changes that can be detected in code."""
    FUNCTION_REMOVED = "function_removed"
    FUNCTION_SIGNATURE_CHANGED = "function_signature_changed"
    FUNCTION_ADDED = "function_added"
    CLASS_REMOVED = "class_removed"
    CLASS_INHERITANCE_CHANGED = "class_inheritance_changed"
    CLASS_ADDED = "class_added"
    METHOD_REMOVED = "method_removed"
    METHOD_SIGNATURE_CHANGED = "method_signature_changed"
    METHOD_ADDED = "method_added"
    VARIABLE_REMOVED = "variable_removed"
    VARIABLE_TYPE_CHANGED = "variable_type_changed"
    VARIABLE_ADDED = "variable_added"
    IMPORT_REMOVED = "import_removed"
    IMPORT_ADDED = "import_added"
    CONSTANT_VALUE_CHANGED = "constant_value_changed"
    DECORATOR_REMOVED = "decorator_removed"
    DECORATOR_ADDED = "decorator_added"


class SeverityLevel(Enum):
    """Severity levels for detected changes."""
    BREAKING = "breaking"      # Major version bump required
    COMPATIBLE = "compatible"  # Minor version bump required
    PATCH = "patch"           # Patch version bump sufficient
    INTERNAL = "internal"     # No public API impact


@dataclass
class CodeChange:
    """Represents a single change detected between two code versions."""
    change_type: ChangeType
    severity: SeverityLevel
    description: str
    old_location: Optional[str] = None
    new_location: Optional[str] = None
    old_signature: Optional[str] = None
    new_signature: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'change_type': self.change_type.value,
            'severity': self.severity.value,
            'description': self.description,
            'old_location': self.old_location,
            'new_location': self.new_location,
            'old_signature': self.old_signature,
            'new_signature': self.new_signature,
            'additional_info': self.additional_info
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CodeChange':
        """Create from dictionary."""
        return cls(
            change_type=ChangeType(data['change_type']),
            severity=SeverityLevel(data['severity']),
            description=data['description'],
            old_location=data.get('old_location'),
            new_location=data.get('new_location'),
            old_signature=data.get('old_signature'),
            new_signature=data.get('new_signature'),
            additional_info=data.get('additional_info')
        )


class LanguageAnalyzer(ABC):
    """Abstract base class for language-specific AST analyzers."""
    
    @abstractmethod
    def parse_file(self, file_path: Union[str, Path]) -> Any:
        """Parse a file and return its AST."""
        pass
    
    @abstractmethod
    def extract_public_api(self, ast_node: Any) -> Dict[str, Any]:
        """Extract public API elements from an AST."""
        pass
    
    @abstractmethod
    def compare_apis(self, old_api: Dict[str, Any], new_api: Dict[str, Any]) -> List[CodeChange]:
        """Compare two API dictionaries and return detected changes."""
        pass


class PythonAnalyzer(LanguageAnalyzer):
    """Python-specific AST analyzer."""
    
    def parse_file(self, file_path: Union[str, Path]) -> ast.AST:
        """Parse a Python file and return its AST."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ast.parse(content, filename=str(file_path))
    
    def extract_public_api(self, ast_node: ast.AST) -> Dict[str, Any]:
        """Extract public API elements from a Python AST."""
        api = {
            'functions': {},
            'classes': {},
            'variables': {},
            'imports': {},
            'constants': {}
        }
        
        for node in ast.walk(ast_node):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                api['functions'][node.name] = self._extract_function_info(node)
            elif isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                api['classes'][node.name] = self._extract_class_info(node)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith('_'):
                        api['variables'][target.id] = self._extract_variable_info(node)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = self._extract_import_info(node)
                api['imports'][import_info['name']] = import_info
        
        return api
    
    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Extract information about a function."""
        return {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'defaults': len(node.args.defaults),
            'vararg': node.args.vararg.arg if node.args.vararg else None,
            'kwarg': node.args.kwarg.arg if node.args.kwarg else None,
            'decorators': [self._ast_to_string(dec) for dec in node.decorator_list],
            'lineno': node.lineno,
            'returns': self._ast_to_string(node.returns) if node.returns else None,
            'docstring': ast.get_docstring(node)
        }
    
    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Extract information about a class."""
        methods = {}
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                methods[item.name] = self._extract_function_info(item)
        
        return {
            'name': node.name,
            'bases': [self._ast_to_string(base) for base in node.bases],
            'decorators': [self._ast_to_string(dec) for dec in node.decorator_list],
            'methods': methods,
            'lineno': node.lineno,
            'docstring': ast.get_docstring(node)
        }
    
    def _extract_variable_info(self, node: ast.Assign) -> Dict[str, Any]:
        """Extract information about a variable assignment."""
        return {
            'value_type': type(node.value).__name__,
            'lineno': node.lineno,
            'value': self._ast_to_string(node.value) if hasattr(node.value, 'n') or hasattr(node.value, 's') else None
        }
    
    def _extract_import_info(self, node: Union[ast.Import, ast.ImportFrom]) -> Dict[str, Any]:
        """Extract information about an import."""
        if isinstance(node, ast.Import):
            name = node.names[0].name
            return {
                'name': name,
                'type': 'import',
                'module': name,
                'lineno': node.lineno
            }
        else:  # ast.ImportFrom
            name = f"{node.module}.{node.names[0].name}" if node.module else node.names[0].name
            return {
                'name': name,
                'type': 'from_import',
                'module': node.module,
                'imported': [alias.name for alias in node.names],
                'lineno': node.lineno
            }
    
    def _ast_to_string(self, node: ast.AST) -> str:
        """Convert an AST node to a string representation."""
        try:
            return ast.unparse(node)
        except:
            return str(node)
    
    def compare_apis(self, old_api: Dict[str, Any], new_api: Dict[str, Any]) -> List[CodeChange]:
        """Compare two Python API dictionaries and return detected changes."""
        changes = []
        
        # Compare functions
        changes.extend(self._compare_functions(old_api.get('functions', {}), new_api.get('functions', {})))
        
        # Compare classes
        changes.extend(self._compare_classes(old_api.get('classes', {}), new_api.get('classes', {})))
        
        # Compare variables
        changes.extend(self._compare_variables(old_api.get('variables', {}), new_api.get('variables', {})))
        
        # Compare imports
        changes.extend(self._compare_imports(old_api.get('imports', {}), new_api.get('imports', {})))
        
        return changes
    
    def _compare_functions(self, old_funcs: Dict[str, Any], new_funcs: Dict[str, Any]) -> List[CodeChange]:
        """Compare function definitions between old and new APIs."""
        changes = []
        
        # Check for removed functions
        for func_name in old_funcs:
            if func_name not in new_funcs:
                changes.append(CodeChange(
                    change_type=ChangeType.FUNCTION_REMOVED,
                    severity=SeverityLevel.BREAKING,
                    description=f"Function '{func_name}' was removed",
                    old_location=f"line {old_funcs[func_name]['lineno']}",
                    old_signature=self._format_function_signature(old_funcs[func_name])
                ))
        
        # Check for added functions
        for func_name in new_funcs:
            if func_name not in old_funcs:
                changes.append(CodeChange(
                    change_type=ChangeType.FUNCTION_ADDED,
                    severity=SeverityLevel.COMPATIBLE,
                    description=f"Function '{func_name}' was added",
                    new_location=f"line {new_funcs[func_name]['lineno']}",
                    new_signature=self._format_function_signature(new_funcs[func_name])
                ))
        
        # Check for signature changes
        for func_name in old_funcs:
            if func_name in new_funcs:
                old_sig = self._format_function_signature(old_funcs[func_name])
                new_sig = self._format_function_signature(new_funcs[func_name])
                if old_sig != new_sig:
                    changes.append(CodeChange(
                        change_type=ChangeType.FUNCTION_SIGNATURE_CHANGED,
                        severity=SeverityLevel.BREAKING,
                        description=f"Function '{func_name}' signature changed",
                        old_location=f"line {old_funcs[func_name]['lineno']}",
                        new_location=f"line {new_funcs[func_name]['lineno']}",
                        old_signature=old_sig,
                        new_signature=new_sig
                    ))
        
        return changes
    
    def _compare_classes(self, old_classes: Dict[str, Any], new_classes: Dict[str, Any]) -> List[CodeChange]:
        """Compare class definitions between old and new APIs."""
        changes = []
        
        # Check for removed classes
        for class_name in old_classes:
            if class_name not in new_classes:
                changes.append(CodeChange(
                    change_type=ChangeType.CLASS_REMOVED,
                    severity=SeverityLevel.BREAKING,
                    description=f"Class '{class_name}' was removed",
                    old_location=f"line {old_classes[class_name]['lineno']}"
                ))
        
        # Check for added classes
        for class_name in new_classes:
            if class_name not in old_classes:
                changes.append(CodeChange(
                    change_type=ChangeType.CLASS_ADDED,
                    severity=SeverityLevel.COMPATIBLE,
                    description=f"Class '{class_name}' was added",
                    new_location=f"line {new_classes[class_name]['lineno']}"
                ))
        
        # Check for inheritance changes and method changes
        for class_name in old_classes:
            if class_name in new_classes:
                old_class = old_classes[class_name]
                new_class = new_classes[class_name]
                
                # Check inheritance changes
                if old_class['bases'] != new_class['bases']:
                    changes.append(CodeChange(
                        change_type=ChangeType.CLASS_INHERITANCE_CHANGED,
                        severity=SeverityLevel.BREAKING,
                        description=f"Class '{class_name}' inheritance changed",
                        old_location=f"line {old_class['lineno']}",
                        new_location=f"line {new_class['lineno']}",
                        additional_info={
                            'old_bases': old_class['bases'],
                            'new_bases': new_class['bases']
                        }
                    ))
                
                # Check method changes
                method_changes = self._compare_functions(old_class['methods'], new_class['methods'])
                for change in method_changes:
                    # Convert function changes to method changes
                    if change.change_type == ChangeType.FUNCTION_REMOVED:
                        change.change_type = ChangeType.METHOD_REMOVED
                    elif change.change_type == ChangeType.FUNCTION_ADDED:
                        change.change_type = ChangeType.METHOD_ADDED
                    elif change.change_type == ChangeType.FUNCTION_SIGNATURE_CHANGED:
                        change.change_type = ChangeType.METHOD_SIGNATURE_CHANGED
                    
                    change.description = change.description.replace("Function", f"Method in class '{class_name}'")
                    changes.append(change)
        
        return changes
    
    def _compare_variables(self, old_vars: Dict[str, Any], new_vars: Dict[str, Any]) -> List[CodeChange]:
        """Compare variable definitions between old and new APIs."""
        changes = []
        
        # Check for removed variables
        for var_name in old_vars:
            if var_name not in new_vars:
                changes.append(CodeChange(
                    change_type=ChangeType.VARIABLE_REMOVED,
                    severity=SeverityLevel.BREAKING,
                    description=f"Variable '{var_name}' was removed",
                    old_location=f"line {old_vars[var_name]['lineno']}"
                ))
        
        # Check for added variables
        for var_name in new_vars:
            if var_name not in old_vars:
                changes.append(CodeChange(
                    change_type=ChangeType.VARIABLE_ADDED,
                    severity=SeverityLevel.COMPATIBLE,
                    description=f"Variable '{var_name}' was added",
                    new_location=f"line {new_vars[var_name]['lineno']}"
                ))
        
        return changes
    
    def _compare_imports(self, old_imports: Dict[str, Any], new_imports: Dict[str, Any]) -> List[CodeChange]:
        """Compare import statements between old and new APIs."""
        changes = []
        
        # Check for removed imports
        for import_name in old_imports:
            if import_name not in new_imports:
                changes.append(CodeChange(
                    change_type=ChangeType.IMPORT_REMOVED,
                    severity=SeverityLevel.INTERNAL,
                    description=f"Import '{import_name}' was removed",
                    old_location=f"line {old_imports[import_name]['lineno']}"
                ))
        
        # Check for added imports
        for import_name in new_imports:
            if import_name not in old_imports:
                changes.append(CodeChange(
                    change_type=ChangeType.IMPORT_ADDED,
                    severity=SeverityLevel.INTERNAL,
                    description=f"Import '{import_name}' was added",
                    new_location=f"line {new_imports[import_name]['lineno']}"
                ))
        
        return changes
    
    def _format_function_signature(self, func_info: Dict[str, Any]) -> str:
        """Format a function signature string."""
        args = func_info['args']
        if func_info['vararg']:
            args.append(f"*{func_info['vararg']}")
        if func_info['kwarg']:
            args.append(f"**{func_info['kwarg']}")
        
        signature = f"{func_info['name']}({', '.join(args)})"
        if func_info['returns']:
            signature += f" -> {func_info['returns']}"
        
        return signature


class ASTDiffAnalyzer:
    """Main analyzer class that coordinates language-specific analyzers."""
    
    def __init__(self):
        self.analyzers = {
            '.py': PythonAnalyzer(),
            # Future: Add more language analyzers here
            # '.js': JavaScriptAnalyzer(),
            # '.ts': TypeScriptAnalyzer(),
            # '.go': GoAnalyzer(),
            # '.rs': RustAnalyzer(),
        }
    
    def analyze_breaking_changes(
        self, 
        old_file: Union[str, Path], 
        new_file: Union[str, Path],
        language: Optional[str] = None
    ) -> List[CodeChange]:
        """
        Analyze breaking changes between two code files.
        
        Args:
            old_file: Path to the old version of the file
            new_file: Path to the new version of the file
            language: Language override (auto-detected from file extension if not provided)
        
        Returns:
            List of detected changes
        """
        old_path = Path(old_file)
        new_path = Path(new_file)
        
        # Determine language
        if language is None:
            language = old_path.suffix.lower()
        
        if language not in self.analyzers:
            raise ValueError(f"Unsupported language: {language}")
        
        analyzer = self.analyzers[language]
        
        # Parse both files
        old_ast = analyzer.parse_file(old_path)
        new_ast = analyzer.parse_file(new_path)
        
        # Extract APIs
        old_api = analyzer.extract_public_api(old_ast)
        new_api = analyzer.extract_public_api(new_ast)
        
        # Compare and detect changes
        changes = analyzer.compare_apis(old_api, new_api)
        
        return changes
    
    def analyze_directory_changes(
        self, 
        old_dir: Union[str, Path], 
        new_dir: Union[str, Path],
        file_patterns: Optional[List[str]] = None
    ) -> Dict[str, List[CodeChange]]:
        """
        Analyze breaking changes across all files in two directories.
        
        Args:
            old_dir: Path to the old version directory
            new_dir: Path to the new version directory
            file_patterns: List of file patterns to include (e.g., ['*.py', '*.js'])
        
        Returns:
            Dictionary mapping file paths to their detected changes
        """
        old_path = Path(old_dir)
        new_path = Path(new_dir)
        
        if file_patterns is None:
            file_patterns = ['*.py']  # Default to Python files
        
        results = {}
        
        # Find all matching files in old directory
        for pattern in file_patterns:
            for old_file in old_path.rglob(pattern):
                relative_path = old_file.relative_to(old_path)
                new_file = new_path / relative_path
                
                if new_file.exists():
                    try:
                        changes = self.analyze_breaking_changes(old_file, new_file)
                        if changes:  # Only include files with changes
                            results[str(relative_path)] = changes
                    except Exception as e:
                        # Log error but continue processing other files
                        print(f"Error analyzing {relative_path}: {e}")
        
        return results
    
    def export_results(self, changes: Union[List[CodeChange], Dict[str, List[CodeChange]]], output_file: Union[str, Path]):
        """Export analysis results to a JSON file."""
        output_path = Path(output_file)
        
        if isinstance(changes, list):
            # Single file results
            data = [change.to_dict() for change in changes]
        else:
            # Directory results
            data = {
                file_path: [change.to_dict() for change in file_changes]
                for file_path, file_changes in changes.items()
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def generate_report(self, changes: List[CodeChange]) -> str:
        """Generate a human-readable report of detected changes."""
        if not changes:
            return "No breaking changes detected."
        
        report_lines = ["Breaking Changes Analysis Report", "=" * 40, ""]
        
        # Group by severity
        by_severity = {}
        for change in changes:
            if change.severity not in by_severity:
                by_severity[change.severity] = []
            by_severity[change.severity].append(change)
        
        for severity in [SeverityLevel.BREAKING, SeverityLevel.COMPATIBLE, SeverityLevel.PATCH, SeverityLevel.INTERNAL]:
            if severity in by_severity:
                report_lines.append(f"{severity.value.upper()} CHANGES:")
                report_lines.append("-" * 20)
                
                for change in by_severity[severity]:
                    report_lines.append(f"• {change.description}")
                    if change.old_location:
                        report_lines.append(f"  Old: {change.old_location}")
                    if change.new_location:
                        report_lines.append(f"  New: {change.new_location}")
                    if change.old_signature and change.new_signature:
                        report_lines.append(f"  Old signature: {change.old_signature}")
                        report_lines.append(f"  New signature: {change.new_signature}")
                    report_lines.append("")
                
                report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """Example usage of the AST Diff Analyzer."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python ast_diff_analyzer.py <old_file> <new_file>")
        sys.exit(1)
    
    old_file = sys.argv[1]
    new_file = sys.argv[2]
    
    analyzer = ASTDiffAnalyzer()
    
    try:
        changes = analyzer.analyze_breaking_changes(old_file, new_file)
        report = analyzer.generate_report(changes)
        print(report)
        
        # Export to JSON if requested
        if len(sys.argv) > 3:
            output_file = sys.argv[3]
            analyzer.export_results(changes, output_file)
            print(f"\nResults exported to {output_file}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 