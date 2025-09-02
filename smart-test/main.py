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

def main():
    cli()

if __name__ == "__main__":
    main()
