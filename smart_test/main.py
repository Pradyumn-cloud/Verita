from __future__ import annotations
import os
import sys
import click
from pathlib import Path
import importlib
from typing import List, Optional, Dict, Any
import pytest

from .analyzer import (
    analyze_project, 
    parse_coverage_xml, 
    map_coverage_to_functions, 
    summarize_coverage,
    generate_test_skeleton, 
    FunctionInfo
)
from .utils import load_config, safe_write_file, create_directory_if_not_exists

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version="0.1.0")
def cli():
    """smart-test - A tool for analyzing and generating tests for Python projects."""
    pass

@cli.command("analyze")
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--coverage", "coverage_path", type=click.Path(exists=True), default=None, 
              help="Path to coverage.py XML file")
@click.option("--output", "-o", type=click.Path(path_type=Path), default=None,
              help="Path to output JSON file with analysis results")
@click.option("--verbose", "-v", is_flag=True, help="Print detailed information")
@click.option("--format", "-f", type=click.Choice(["text", "json", "table"]), default="text",
              help="Output format")
def analyze_cmd(path: Path, coverage_path: Optional[str], output: Optional[Path], 
               verbose: bool, format: str):
    """Analyze a Python project for test coverage."""
    import time
    
    # Start timing
    start_time = time.time()
    
    # Load configuration
    config = load_config(path)
    
    # Use config values as defaults if not provided via CLI
    if not coverage_path and "coverage_path" in config:
        coverage_path = config["coverage_path"]
        
    click.echo(f"Analyzing project at {path}...")
    
    # Show progress for large projects
    with click.progressbar(length=100, label="Scanning files") as bar:
        # Update progress at intervals
        bar.update(30)
        results = analyze_project(path)
        bar.update(70)
    
    # Calculate statistics
    total_functions = len(results)
    with_tests = sum(1 for fi in results if fi.has_tests)
    without_tests = total_functions - with_tests
    
    # Add coverage information if available
    if coverage_path:
        click.echo(f"Including coverage data from {coverage_path}")
        file_coverage = parse_coverage_xml(coverage_path)
        results = map_coverage_to_functions(results, file_coverage)
        stats = summarize_coverage(results)
        
        covered = sum(1 for fi in results if fi.covered)
        
        # Output based on format
        if format == "text":
            click.echo(f"Found {total_functions} functions:")
            click.echo(f"  - {with_tests} have tests ({with_tests/total_functions*100:.1f}%)")
            click.echo(f"  - {covered} are covered by tests ({covered/total_functions*100:.1f}%)")
            click.echo(f"  - {stats['need_tests_count']} need tests")
            
            if stats['priority_functions']:
                click.echo("\nPriority functions to test:")
                for func in stats['priority_functions']:
                    click.echo(f"  - {func}")
        
        elif format == "json":
            import json
            output_data = {
                "total_functions": total_functions,
                "with_tests": with_tests,
                "without_tests": without_tests,
                "covered": covered,
                "need_tests": stats['need_tests_count'],
                "priority_functions": stats['priority_functions']
            }
            click.echo(json.dumps(output_data, indent=2))
        
        elif format == "table":
            from tabulate import tabulate
            headers = ["Metric", "Count", "Percentage"]
            table = [
                ["Total Functions", total_functions, "100.0%"],
                ["With Tests", with_tests, f"{with_tests/total_functions*100:.1f}%"],
                ["Covered by Tests", covered, f"{covered/total_functions*100:.1f}%"],
                ["Need Tests", stats['need_tests_count'], f"{stats['need_tests_count']/total_functions*100:.1f}%"]
            ]
            click.echo(tabulate(table, headers=headers, tablefmt="grid"))
            
            if stats['priority_functions']:
                click.echo("\nPriority functions to test:")
                for func in stats['priority_functions']:
                    click.echo(f"  - {func}")
    else:
        # Output without coverage data
        if format == "text":
            click.echo(f"Found {total_functions} functions, {with_tests} with tests ({with_tests/total_functions*100:.1f}%).")
            
            if verbose:
                # Group by module for better readability
                by_module = {}
                for fi in results:
                    module = str(fi.module_rel)
                    if module not in by_module:
                        by_module[module] = []
                    by_module[module].append(fi)
                
                for module, funcs in sorted(by_module.items()):
                    click.echo(f"\n{module}:")
                    for fi in funcs:
                        status = "✓ Tests exist" if fi.has_tests else "✗ No tests"
                        click.echo(f"  - {fi.qualname}() - {status}")
        
        elif format == "json":
            import json
            output_data = {
                "total_functions": total_functions,
                "with_tests": with_tests,
                "without_tests": without_tests,
                "percentage_with_tests": with_tests/total_functions*100
            }
            click.echo(json.dumps(output_data, indent=2))
        
        elif format == "table":
            from tabulate import tabulate
            headers = ["Metric", "Count", "Percentage"]
            table = [
                ["Total Functions", total_functions, "100.0%"],
                ["With Tests", with_tests, f"{with_tests/total_functions*100:.1f}%"],
                ["Without Tests", without_tests, f"{without_tests/total_functions*100:.1f}%"]
            ]
            click.echo(tabulate(table, headers=headers, tablefmt="grid"))
    
    # Save results to file if requested
    if output:
        import json
        # Convert to serializable format
        serializable_results = [
            {
                "file": str(fi.file),
                "module_rel": str(fi.module_rel),
                "qualname": fi.qualname,
                "lineno": fi.lineno,
                "has_tests": fi.has_tests,
                "covered": fi.covered if hasattr(fi, "covered") else False
            }
            for fi in results
        ]
        
        with safe_write_file(output) as f:
            json.dump(serializable_results, f, indent=2)
            
        click.echo(f"Analysis results saved to {output}")
    
    # Show timing
    elapsed = time.time() - start_time
    click.echo(f"\nAnalysis completed in {elapsed:.2f} seconds.")

@cli.command("generate")
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), default=None,
              help="Directory to write test files (defaults to tests/)")
@click.option("--function", "-f", multiple=True, help="Generate tests only for specific functions")
@click.option("--module", "-m", multiple=True, help="Generate tests only for specific modules")
@click.option("--force", is_flag=True, help="Overwrite existing test files")
@click.option("--update", is_flag=True, help="Update existing test files by adding missing tests")
@click.option("--preview", is_flag=True, help="Show what would be generated without writing files")
def generate_cmd(path: Path, output_dir: Optional[Path], function: List[str], 
                module: List[str], force: bool, update: bool, preview: bool):
    """Generate test skeletons for functions without tests."""
    # Load configuration
    config = load_config(path)
    
    # Use config values as defaults if not provided via CLI
    if not output_dir:
        output_dir = config.get("test_output_dir", path / "tests")
    
    # Ensure output_dir is a Path
    output_dir = Path(output_dir)
    
    # Analyze the project
    click.echo(f"Analyzing project at {path}...")
    functions = analyze_project(path)
    
    # Filter functions that need tests
    functions_needing_tests = [fi for fi in functions if not fi.has_tests]
    
    # Apply filters if specified
    if function:
        functions_needing_tests = [
            fi for fi in functions_needing_tests 
            if any(f in fi.qualname for f in function)
        ]
    
    if module:
        functions_needing_tests = [
            fi for fi in functions_needing_tests 
            if any(m in str(fi.module_rel) for m in module)
        ]
    
    if not functions_needing_tests:
        click.echo("No functions found that need tests.")
        return
    
    click.echo(f"Generating test skeletons for {len(functions_needing_tests)} functions...")
    
    if preview:
        # Just show what would be generated
        for fi in functions_needing_tests:
            skeleton = generate_test_skeleton(fi, path)
            if skeleton:
                click.echo(f"\nTest for {fi.module_rel}::{fi.qualname}:")
                click.echo("=" * 60)
                click.echo(skeleton)
                click.echo("=" * 60)
        click.echo("\nPreview mode - no files were written.")
        return
    
    # Create the output directory if it doesn't exist
    create_directory_if_not_exists(output_dir)
    
    # Group functions by module for better organization
    module_functions: Dict[Path, List[FunctionInfo]] = {}
    for fi in functions_needing_tests:
        module_path = fi.module_rel
        if module_path not in module_functions:
            module_functions[module_path] = []
        module_functions[module_path].append(fi)
    
    # Generate test files
    test_files_created = 0
    test_files_updated = 0
    
    for module_path, funcs in module_functions.items():
        # Determine the test file path
        test_filename = f"test_{module_path.stem}.py"
        test_file_path = output_dir / test_filename
        
        # Check if file exists
        if test_file_path.exists():
            if force:
                # Generate from scratch
                test_content = [
                    "# Generated by smart-test",
                    f"# Test file for {module_path}",
                    "",
                    "import pytest",
                    f"from {module_path.stem} import *  # Import the module under test",
                    ""
                ]
                
                for fi in funcs:
                    skeleton = generate_test_skeleton(fi, path)
                    if skeleton:
                        test_content.append(skeleton)
                        test_content.append("")  # Add a blank line
                
                with safe_write_file(test_file_path) as f:
                    f.write("\n".join(test_content))
                
                test_files_created += 1
                click.echo(f"Overwrote test file: {test_file_path}")
            
            elif update:
                # Read existing file
                existing_content = test_file_path.read_text(encoding="utf-8")
                
                # Check which functions already have tests
                new_tests = []
                for fi in funcs:
                    test_name = f"test_{fi.qualname.replace('.', '_')}"
                    if test_name not in existing_content:
                        skeleton = generate_test_skeleton(fi, path)
                        if skeleton:
                            new_tests.append(skeleton)
                
                if new_tests:
                    # Append new tests to the file
                    with open(test_file_path, "a", encoding="utf-8") as f:
                        f.write("\n\n")  # Add spacing
                        f.write("\n\n".join(new_tests))
                    
                    test_files_updated += 1
                    click.echo(f"Updated test file with {len(new_tests)} new tests: {test_file_path}")
                else:
                    click.echo(f"No new tests to add to {test_file_path}")
            else:
                click.echo(f"Test file {test_file_path} already exists. Use --force to overwrite or --update to add missing tests.")
        else:
            # Create new test file
            test_content = [
                "# Generated by smart-test",
                f"# Test file for {module_path}",
                "",
                "import pytest",
                f"from {module_path.stem} import *  # Import the module under test",
                ""
            ]
            
            for fi in funcs:
                skeleton = generate_test_skeleton(fi, path)
                if skeleton:
                    test_content.append(skeleton)
                    test_content.append("")  # Add a blank line
            
            with safe_write_file(test_file_path) as f:
                f.write("\n".join(test_content))
            
            test_files_created += 1
            click.echo(f"Created test file: {test_file_path}")
    
    # Summary
    if test_files_created > 0 or test_files_updated > 0:
        if test_files_created > 0:
            click.echo(f"Successfully created {test_files_created} test files.")
        if test_files_updated > 0:
            click.echo(f"Successfully updated {test_files_updated} test files.")
    else:
        click.echo("No test files were created or updated. Use --force to overwrite existing files or --update to add tests to existing files.")
        
@cli.command("cleanup")
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--all", is_flag=True, help="Remove all generated files, including .pytest_cache")
def cleanup_cmd(path: Path, all: bool):
    """Clean up generated files from the project."""
    import shutil
    
    # Files to always clean
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
    ]
    
    # Files to clean if --all is specified
    if all:
        patterns.extend([
            "**/.pytest_cache",
            "**/.coverage",
            "**/htmlcov",
            "build",
            "dist",
            "*.egg-info",
        ])
    
    files_removed = 0
    dirs_removed = 0
    
    click.echo(f"Cleaning up generated files in {path}...")
    
    for pattern in patterns:
        for item in path.glob(pattern):
            if item.is_file():
                item.unlink()
                files_removed += 1
                click.echo(f"Removed file: {item}")
            elif item.is_dir():
                shutil.rmtree(item)
                dirs_removed += 1
                click.echo(f"Removed directory: {item}")
    
    click.echo(f"Cleanup complete. Removed {files_removed} files and {dirs_removed} directories.")

def main():
    """Entry point for the smart-test CLI."""
    cli()

if __name__ == "__main__":
    main()