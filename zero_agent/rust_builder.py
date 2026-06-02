import os
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def get_scraper_path() -> Path:
    bin_name = "rust_scraper.exe" if os.name == "nt" else "rust_scraper"
    return Path.home() / ".zero_agent" / bin_name

def build_rust_scraper(project_dir: Path):
    console.print("\n[bold blue]🦀 Checking Rust environment...[/bold blue]")
    
    try:
        subprocess.run(["cargo", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        console.print("[bold red]❌ Rust (Cargo) is not installed![/bold red]")
        if os.environ.get("TERMUX_VERSION"):
            console.print("👉 Since you are on Termux, run: [bold]pkg install rust[/bold]")
        elif os.name == "nt":
            console.print("👉 Download and install Rust from: https://rustup.rs/")
        else:
            console.print("👉 Run: [bold]curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh[/bold]")
        raise SystemExit(1)

    console.print("[green]✅ Rust detected. Compiling high-performance scraper...[/green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Building rust_scraper (this may take a minute)...", total=None)
        
        try:
            subprocess.run(
                ["cargo", "build", "--release"],
                cwd=project_dir,
                capture_output=True,
                check=True
            )
            
            bin_name = "rust_scraper.exe" if os.name == "nt" else "rust_scraper"
            src_bin = project_dir / "target" / "release" / bin_name
            dest_bin = get_scraper_path()
            
            # Create the destination folder if it doesn't exist
            dest_bin.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy(src_bin, dest_bin)
            console.print(f"[bold green]✅ Scraper compiled and saved to {dest_bin}[/bold green]")
            
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]❌ Compilation failed:\n{e.stderr.decode()}[/bold red]")
            raise SystemExit(1)