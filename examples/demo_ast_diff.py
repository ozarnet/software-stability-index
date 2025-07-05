#!/usr/bin/env python3
"""
Demonstration of the AST Diff Analyzer utility.

This script shows how to use the reusable AST diff analyzer to detect
breaking changes between two versions of a Python file.
"""

import sys
import os

# Add the parent directory to sys.path so we can import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ssi.retrieval.ast_diff_analyzer import ASTDiffAnalyzer, SeverityLevel

def main():
    """Demonstrate the AST diff analyzer."""
    print("🔍 AST Diff Analyzer Demonstration")
    print("=" * 50)
    
    # Initialize the analyzer
    analyzer = ASTDiffAnalyzer()
    
    # Analyze changes between the example files
    old_file = "test_old.py"
    new_file = "test_new.py"
    
    print(f"📁 Analyzing changes between:")
    print(f"   Old: {old_file}")
    print(f"   New: {new_file}")
    print()
    
    try:
        # Perform the analysis
        changes = analyzer.analyze_breaking_changes(old_file, new_file)
        
        # Generate and display the report
        report = analyzer.generate_report(changes)
        print(report)
        
        # Show summary statistics
        print("\n📊 Summary Statistics:")
        print("-" * 20)
        
        severity_counts = {}
        for change in changes:
            severity = change.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        for severity in [SeverityLevel.BREAKING, SeverityLevel.COMPATIBLE, SeverityLevel.PATCH, SeverityLevel.INTERNAL]:
            count = severity_counts.get(severity, 0)
            if count > 0:
                print(f"{severity.value.capitalize()}: {count} changes")
        
        print(f"Total changes detected: {len(changes)}")
        
        # Export results to JSON
        output_file = "analysis_results.json"
        analyzer.export_results(changes, output_file)
        print(f"\n💾 Results exported to: {output_file}")
        
        # Determine recommended version bump
        has_breaking = any(c.severity == SeverityLevel.BREAKING for c in changes)
        has_compatible = any(c.severity == SeverityLevel.COMPATIBLE for c in changes)
        
        print(f"\n🎯 Recommended Version Bump:")
        if has_breaking:
            print("   MAJOR version bump required (breaking changes detected)")
        elif has_compatible:
            print("   MINOR version bump required (compatible changes detected)")
        else:
            print("   PATCH version bump sufficient (no API changes)")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 