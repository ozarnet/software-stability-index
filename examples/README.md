# AST Diff Analyzer

A reusable utility for detecting breaking changes between code versions using Abstract Syntax Tree (AST) analysis.

## Overview

The AST Diff Analyzer provides a language-agnostic framework for detecting breaking changes in code by comparing the Abstract Syntax Trees of different versions. This is much more accurate than text-based diffs as it understands the semantic structure of code.

## Features

- **Language Support**: Currently supports Python, with extensible architecture for other languages
- **Breaking Change Detection**: Identifies function removals, signature changes, class modifications, etc.
- **Severity Classification**: Categorizes changes as BREAKING, COMPATIBLE, PATCH, or INTERNAL
- **Semantic Versioning Guidance**: Recommends appropriate version bumps based on detected changes
- **Multiple Output Formats**: Human-readable reports and JSON export
- **Reusable Design**: Can be easily integrated into other projects

## Supported Change Types

### Python
- Function removal/addition/signature changes
- Class removal/addition/inheritance changes  
- Method removal/addition/signature changes
- Variable removal/addition
- Import changes
- Decorator changes

## Installation

The analyzer is part of the SSI (Software Stability Index) project. To use it:

```bash
# From the project root
python -m pip install -e .
```

## Usage

### Basic Usage

```python
from ssi.retrieval.ast_diff_analyzer import ASTDiffAnalyzer

analyzer = ASTDiffAnalyzer()
changes = analyzer.analyze_breaking_changes("old_file.py", "new_file.py")

for change in changes:
    print(f"{change.severity.value}: {change.description}")
```

### Command Line Usage

```bash
# Analyze two files
python ssi/retrieval/ast_diff_analyzer.py old_file.py new_file.py

# Export results to JSON
python ssi/retrieval/ast_diff_analyzer.py old_file.py new_file.py results.json
```

### Directory Analysis

```python
analyzer = ASTDiffAnalyzer()
results = analyzer.analyze_directory_changes("old_version/", "new_version/", ["*.py"])

for file_path, changes in results.items():
    print(f"Changes in {file_path}:")
    for change in changes:
        print(f"  - {change.description}")
```

## Example

See the demonstration in `examples/demo_ast_diff.py`:

```bash
cd examples
python demo_ast_diff.py
```

This will analyze the differences between `test_old.py` and `test_new.py`, showing:

- Function signature changes
- Removed functions and methods
- New classes and methods
- Severity classification
- Recommended version bump

## Output Example

```
Breaking Changes Analysis Report
========================================

BREAKING CHANGES:
--------------------
• Function 'process_data' was removed
  Old: line 10

• Method in class 'DataProcessor' 'batch_transform' was removed
  Old: line 23

• Function '__init__' signature changed
  Old: line 16
  New: line 17
  Old signature: __init__(self, multiplier)
  New signature: __init__(self, multiplier, offset)

COMPATIBLE CHANGES:
--------------------
• Function 'process_items' was added
  New: line 10

• Class 'AdvancedProcessor' was added
  New: line 30
```

## Integration with Other Projects

The AST Diff Analyzer is designed to be reusable. To integrate it into your project:

1. Copy the `ast_diff_analyzer.py` file to your project
2. Install dependencies: `ast`, `dataclasses`, `pathlib` (all standard library)
3. Use the `ASTDiffAnalyzer` class in your code

### Example Integration

```python
from your_project.ast_diff_analyzer import ASTDiffAnalyzer, SeverityLevel

def check_api_compatibility(old_version_path, new_version_path):
    analyzer = ASTDiffAnalyzer()
    changes = analyzer.analyze_breaking_changes(old_version_path, new_version_path)
    
    # Check if there are breaking changes
    breaking_changes = [c for c in changes if c.severity == SeverityLevel.BREAKING]
    
    if breaking_changes:
        print("❌ Breaking changes detected!")
        return False
    else:
        print("✅ No breaking changes detected")
        return True
```

## Extending to Other Languages

To add support for a new language, implement the `LanguageAnalyzer` interface:

```python
class JavaScriptAnalyzer(LanguageAnalyzer):
    def parse_file(self, file_path):
        # Parse JavaScript/TypeScript file
        pass
    
    def extract_public_api(self, ast_node):
        # Extract public API elements
        pass
    
    def compare_apis(self, old_api, new_api):
        # Compare APIs and return changes
        pass

# Register the analyzer
analyzer = ASTDiffAnalyzer()
analyzer.analyzers['.js'] = JavaScriptAnalyzer()
```

## Configuration

The analyzer can be configured for different use cases:

- **Severity Mapping**: Customize which changes are considered breaking
- **API Filtering**: Control which elements are considered part of the public API
- **Output Formatting**: Customize report generation

## Limitations

- Currently only supports Python (extensible to other languages)
- Focuses on structural changes, not semantic/behavioral changes
- Does not detect changes in docstrings or comments
- Requires valid, parseable code

## Contributing

This utility is part of the larger SSI project. Contributions are welcome:

1. Add support for new languages
2. Improve change detection accuracy
3. Add new change types
4. Enhance reporting capabilities

## License

This utility is part of the Software Stability Index project and follows the same license terms. 