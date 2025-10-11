import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .generator import TestGenerator
from .analyzer import CodeAnalyzer
from .models import TestGenerationConfig, TestFramework
from .config import Config

console = Console()

@click.group()
@click.version_option(version='2.0.0')
def cli():
    pass

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output test file path')
@click.option('--framework', '-f', type=click.Choice(['pytest', 'unittest']), 
              default='pytest', help='Test framework to use')
@click.option('--no-ai', is_flag=True, help='Generate tests without AI')
@click.option('--api-key', '-k', envvar='GEMINI_API_KEY', help='Gemini API key')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def generate(file, output, framework, no_ai, api_key, verbose):
    
    # Validate API key if using AI
    if not no_ai and not api_key:
        console.print("[red] Gemini API key required for AI generation.[/red]")
        console.print("[yellow] Use --api-key or set GEMINI_API_KEY environment variable[/yellow]")
        console.print("[yellow] Or use --no-ai for template-based generation[/yellow]")
        console.print("\nGet API key at: https://aistudio.google.com/app/apikey")
        sys.exit(1)
    
    # Create configuration
    config = TestGenerationConfig(
        framework=TestFramework.PYTEST if framework == 'pytest' else TestFramework.UNITTEST,
        use_ai=not no_ai,
        verbose=verbose
    )
    
    # Set API key if provided
    if api_key:
        Config.GEMINI_API_KEY = api_key
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Analyzing Python file...", total=None)
        
        try:
            # Create generator
            generator = TestGenerator(config)
            
            # Generate test file
            progress.update(task, description=" Generating test file...")
            test_file = generator.generate_test_file(file, output)
            
            progress.update(task, description=" Test generation complete!")
        
        except Exception as e:
            console.print(f"[red] Error: {e}[/red]")
            if verbose:
                console.print_exception()
            sys.exit(1)
    
    # Success message
    console.print(f"\n[green] Test file generated:[/green] [cyan]{test_file}[/cyan]")
    console.print(f"\n[yellow]Run tests with:[/yellow] pytest {test_file} -v")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--json', '-j', 'json_output', is_flag=True, help='Output as JSON')
def analyze(file, json_output):
    
    try:
        analyzer = CodeAnalyzer()
        result = analyzer.analyze_file(file)
        
        if json_output:
            import json
            console.print_json(data=result.to_dict())
        else:
            _display_analysis(result)
    
    except Exception as e:
        console.print(f"[red] Error: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for tests')
@click.option('--framework', '-f', type=click.Choice(['pytest', 'unittest']), 
              default='pytest', help='Test framework')
@click.option('--no-ai', is_flag=True, help='Generate without AI')
@click.option('--api-key', '-k', envvar='GEMINI_API_KEY', help='Gemini API key')
@click.option('--exclude', '-e', multiple=True, help='Patterns to exclude')
def batch(directory, output_dir, framework, no_ai, api_key, exclude):
    
    
    if not no_ai and not api_key:
        console.print("[red] API key required for AI generation[/red]")
        sys.exit(1)
    
    # Set API key
    if api_key:
        Config.GEMINI_API_KEY = api_key
    
    # Find Python files
    dir_path = Path(directory)
    python_files = list(dir_path.rglob('*.py'))
    
    # Apply exclusions
    exclude_patterns = set(exclude) if exclude else set()
    exclude_patterns.update(Config.EXCLUDE_PATTERNS)
    
    python_files = [
        f for f in python_files
        if not any(pattern in str(f) for pattern in exclude_patterns)
    ]
    
    if not python_files:
        console.print("[yellow] No Python files found[/yellow]")
        sys.exit(0)
    
    console.print(f"[cyan] Found {len(python_files)} Python files[/cyan]\n")
    
    # Create configuration
    config = TestGenerationConfig(
        framework=TestFramework.PYTEST if framework == 'pytest' else TestFramework.UNITTEST,
        use_ai=not no_ai
    )
    
    generator = TestGenerator(config)
    
    successful = 0
    failed = 0
    
    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Generating tests...", total=len(python_files))
        
        for py_file in python_files:
            try:
                # Determine output path
                if output_dir:
                    rel_path = py_file.relative_to(dir_path)
                    out_file = Path(output_dir) / f"test_{rel_path.name}"
                else:
                    out_file = None
                
                generator.generate_test_file(str(py_file), str(out_file) if out_file else None)
                console.print(f"[green]✓[/green] {py_file.name}")
                successful += 1
                
            except Exception as e:
                console.print(f"[red]✗[/red] {py_file.name}: {e}")
                failed += 1
            
            progress.update(task, advance=1)
    
    # Summary
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"[green]✓ Successful: {successful}[/green]")
    if failed:
        console.print(f"[red]✗ Failed: {failed}[/red]")

def _display_analysis(result):
    """Display analysis results in a formatted table"""
    
    # Summary table
    table = Table(title=" Code Analysis", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")
    
    table.add_row("File", result.file_path)
    table.add_row("Total Functions", str(result.total_functions))
    table.add_row("Total Classes", str(len(result.classes)))
    table.add_row("Average Complexity", str(result.average_complexity))
    table.add_row("Total Complexity", str(result.total_complexity))
    
    console.print(table)
    
    # Functions details
    if result.functions:
        console.print("\n[bold]Functions:[/bold]")
        for func in result.functions:
            panel_content = [
                f"[bold]Parameters:[/bold] {', '.join(func.params) if func.params else 'None'}",
                f"[bold]Return Type:[/bold] {func.return_type or 'Not specified'}",
                f"[bold]Line:[/bold] {func.line_number}",
                f"[bold]Complexity:[/bold] {func.complexity}",
            ]
            
            if func.class_name:
                panel_content.insert(0, f"[bold]Class:[/bold] {func.class_name}")
            
            if func.is_async:
                panel_content.append("[cyan]⚡ Async Function[/cyan]")
            
            console.print(Panel(
                "\n".join(panel_content),
                title=f"🔧 {func.name}",
                border_style="blue"
            ))

if __name__ == '__main__':
    cli()