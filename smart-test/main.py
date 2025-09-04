from __future__ import annotations
import click
from pathlib import Path
from .analyzer import analyze_project

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """smart-test CLI"""

@cli.command("analyze")
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
def analyze_cmd(path: Path):

    results = analyze_project(path)
    for fi in results:
        status = "Tests exist" if fi.has_tests else "No tests found"
        print(f"- {fi.module_rel}::{fi.qualname}() - {status}")

@cli.command("generate")
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
def generate_cmd(path: Path):
    click.echo("Generate command not implemented in Phase 1.")
    
@click.option("--coverage", "coverage_path", type=click.Path(exists=True), default=None, help="coverage.py XML file")
def analyze_cmd(path: Path, coverage_path: str | None):
    results = analyze_project(path)
    if coverage_path:
        file_coverage = parse_coverage_xml(coverage_path)
        results = map_coverage_to_functions(results, file_coverage)
        stats = summarize_coverage(results)
        print(f"Functions needing tests: {stats['need_tests_count']}")
        print(f"Functions with low coverage: {stats['low_coverage_count']}")
        print(f"Priority functions: {', '.join(stats['priority_functions'])}")
    else:
        # Original output (Phase 1)
        for fi in results:
            status = "Tests exist" if fi.has_tests else "No tests found"
            print(f"- {fi.module_rel}::{fi.qualname}() - {status}")

def main():
    cli()

if __name__ == "__main__":
    main()
