import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from pathlib import Path

from zero_agent.config import load_config, save_config, DEFAULT_CAPABILITIES
from zero_agent.rust_builder import build_rust_scraper, get_scraper_path
from zero_agent.core import run_agent  # ✅ IMPORT THE AGENT

app = typer.Typer(help="Zero AI Agent - Autonomous Web Scraping & Research")
console = Console()

BANNER = r"""
  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ╚══███╔╝██╔═══██╗██╔══██╗██╔═══██╗██╔════╝
    ███╔╝ ██║   ██║██████╔╝██║   ██║███████╗
   ███╔╝  ██║   ██║██╔══██╗██║   ██║╚════██║
  ███████╗╚██████╔╝██║  ██║██████╔╝███████║
  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
         [bold cyan]Autonomous AI Agent v1.0[/bold cyan]
"""

@app.command()
def setup():
    """Interactive setup wizard to configure your AI Agent."""
    console.print(Panel(BANNER, border_style="cyan", expand=False))
    console.print("[bold yellow]🚀 Welcome to the Zero AI Agent Setup Wizard![/bold yellow]\n")

    # 1. Model Configuration
    console.print("[bold]Step 1: Configure Ollama Model[/bold]")
    model_type = Prompt.ask("Are you using [green]local[/green] or [blue]cloud[/blue] Ollama?", choices=["local", "cloud"], default="local")
    
    if model_type == "local":
        base_url = "http://localhost:11434"
    else:
        base_url = Prompt.ask("Enter your Cloud Ollama API Base URL", default="http://localhost:11434")

    model_name = Prompt.ask("Enter the model name (e.g., llama3, gemma2, mistral)", default="llama3")

    # 2. Update Capabilities JSON
    config = DEFAULT_CAPABILITIES.copy()
    config["model_info"]["name"] = model_name
    config["model_info"]["type"] = model_type
    config["model_info"]["base_url"] = base_url

    # 3. Rust Scraper Setup
    console.print("\n[bold]Step 2: Build High-Performance Rust Scraper[/bold]")
    
    project_dir = Path.cwd() / "web_scraper"

    if get_scraper_path().exists() and Confirm.ask("Scraper already exists. Rebuild it?", default=False):
        if project_dir.exists():
            build_rust_scraper(project_dir)
        else:
            console.print(f"[yellow]⚠️ web_scraper folder not found in {Path.cwd()}. Skipping rebuild.[/yellow]")
    elif not get_scraper_path().exists():
        if project_dir.exists():
            build_rust_scraper(project_dir)
        else:
            console.print(f"[yellow]⚠️ web_scraper folder not found in {Path.cwd()}. Skipping Rust build.[/yellow]")

    # 4. Save
    save_config(config)
    
    console.print(Panel(
        f"[green]✅ Setup Complete![/green]\n\n"
        f"Model: [bold]{model_name}[/bold]\n"
        f"Type: [bold]{model_type}[/bold]\n"
        f"Scraper: [bold]Ready[/bold]\n\n"
        f"Run [bold cyan]zero-ai-agent run[/bold cyan] to start chatting!",
        title="Success", border_style="green"
    ))

@app.command()
def run():
    """Start the interactive AI Agent chat."""
    config = load_config()
    if not config:
        console.print("[bold red]❌ Setup not complete. Please run 'zero-ai-agent setup' first.[/bold red]")
        raise typer.Exit(code=1)

    console.print(Panel(BANNER, border_style="cyan", expand=False))
    
    # Display capabilities table
    table = Table(title="Agent Capabilities Loaded")
    table.add_column("Tool", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    for cap in config["agent_capabilities"]:
        name, desc = cap.split(": ", 1)
        table.add_row(name, desc)
    console.print(table)

    console.print(f"\n[bold]🧠 Brain:[/bold] {config['model_info']['name']} ({config['model_info']['type']})")
    
    # ✅ RUN THE AGENT
    run_agent(config)

@app.command()
def status():
    """Check the current configuration and status."""
    config = load_config()
    if not config:
        console.print("[red]No configuration found. Run setup first.[/red]")
        return
    
    table = Table(title="Zero AI Agent Status")
    table.add_column("Setting", style="bold")
    table.add_column("Value", style="green")
    
    table.add_row("Model", config["model_info"]["name"])
    table.add_row("Type", config["model_info"]["type"])
    table.add_row("Base URL", config["model_info"]["base_url"])
    table.add_row("Scraper", "Installed" if get_scraper_path().exists() else "Missing")
    
    console.print(table)

if __name__ == "__main__":
    app()