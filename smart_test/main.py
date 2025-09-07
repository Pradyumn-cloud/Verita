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
def analyze_cmd(path: Path, coverage_path: Optional[str], output: Optional[Path], verbose: bool):
    """Analyze a Python project for test coverage."""
    # Load configuration
    config = load_config(path)
    
    # Use config values as defaults if not provided via CLI
    if not coverage_path and "coverage_path" in config:
        coverage_path = config["coverage_path"]
        
    click.echo(f"Analyzing project at {path}...")
    results = analyze_project(path)
    
    # Add coverage information if available
    if coverage_path:
        click.echo(f"Including coverage data from {coverage_path}")
        file_coverage = parse_coverage_xml(coverage_path)
        results = map_coverage_to_functions(results, file_coverage)
        stats = summarize_coverage(results)
        
        click.echo(f"Functions needing tests: {stats['need_tests_count']}")
        click.echo(f"Files with low coverage: {stats['low_coverage_count']}")
        
        if stats['priority_functions']:
            click.echo("Priority functions to test:")
            for func in stats['priority_functions']:
                click.echo(f"  - {func}")
    else:
        # Original output (without coverage)
        with_tests = sum(1 for fi in results if fi.has_tests)
        click.echo(f"Found {len(results)} functions, {with_tests} with tests.")
        
        if verbose:
            for fi in results:
                status = "Tests exist" if fi.has_tests else "No tests found"
                click.echo(f"- {fi.module_rel}::{fi.qualname}() - {status}")
    
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
                "covered": fi.covered
            }
            for fi in results
        ]
        
        with safe_write_file(output) as f:
            json.dump(serializable_results, f, indent=2)
            
        click.echo(f"Analysis results saved to {output}")

@cli.command("generate")
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), default=None,
              help="Directory to write test files (defaults to tests/)")
@click.option("--function", "-f", multiple=True, help="Generate tests only for specific functions")
@click.option("--module", "-m", multiple=True, help="Generate tests only for specific modules")
@click.option("--force", is_flag=True, help="Overwrite existing test files")
def generate_cmd(path: Path, output_dir: Optional[Path], function: List[str], 
                module: List[str], force: bool):
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
    for module_path, funcs in module_functions.items():
        # Determine the test file path
        test_filename = f"test_{module_path.stem}.py"
        test_file_path = output_dir / test_filename
        
        # Check if file exists and we're not forcing overwrite
        if test_file_path.exists() and not force:
            click.echo(f"Test file {test_file_path} already exists. Use --force to overwrite.")
            continue
        
        # Generate test skeletons for all functions in this module
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
        
        # Write the test file
        with safe_write_file(test_file_path) as f:
            f.write("\n".join(test_content))
        
        test_files_created += 1
        click.echo(f"Created test file: {test_file_path}")
    
    if test_files_created > 0:
        click.echo(f"Successfully created {test_files_created} test files.")
    else:
        click.echo("No test files were created.")

@cli.command("run")
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--generate", "-g", is_flag=True, help="Generate missing tests before running")
@click.argument("pytest_args", nargs=-1)
def run_cmd(path: Path, generate: bool, pytest_args):
    """Run tests for the project using pytest."""
    # Load configuration
    config = load_config(path)
    
    # Generate tests if requested
    if generate:
        click.echo("Generating missing tests...")
        ctx = click.Context(generate_cmd)
        click.invoke(generate_cmd, ctx, path=path)
    
    # Run pytest
    click.echo("Running tests...")
    
    # Construct pytest arguments
    pytest_options = list(pytest_args)
    
    # Add default arguments from config
    default_args = config.get("pytest_args", [])
    for arg in default_args:
        if arg not in pytest_options:
            pytest_options.append(arg)
    
    # Change to the project directory
    original_dir = os.getcwd()
    os.chdir(path)
    
    try:
        # Run pytest with collected arguments
        exit_code = pytest.main(pytest_options)
        sys.exit(exit_code)
    finally:
        # Restore original directory
        os.chdir(original_dir)

def main():
    """Entry point for the smart-test CLI."""
    cli()

if __name__ == "__main__":
    main()