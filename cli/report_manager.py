#!/usr/bin/env python3
"""
Report Manager for TradingAgents
Helps you find, list, and manage saved reports
"""

import typer
from pathlib import Path
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
import glob

console = Console()
app = typer.Typer(help="Manage TradingAgents reports")

def get_results_dir():
    """Get the results directory path."""
    return Path("./results")

def find_reports(ticker: str = None, date: str = None):
    """Find reports based on ticker and/or date."""
    results_dir = get_results_dir()
    
    if not results_dir.exists():
        console.print("[red]No results directory found. Run an analysis first.[/red]")
        return []
    
    reports = []
    
    # Find all ticker directories
    ticker_dirs = list(results_dir.glob("*"))
    
    for ticker_dir in ticker_dirs:
        if ticker_dir.is_dir():
            current_ticker = ticker_dir.name
            
            # Filter by ticker if specified
            if ticker and current_ticker.upper() != ticker.upper():
                continue
                
            # Find all date directories
            date_dirs = list(ticker_dir.glob("*"))
            
            for date_dir in date_dirs:
                if date_dir.is_dir():
                    current_date = date_dir.name
                    
                    # Filter by date if specified
                    if date and current_date != date:
                        continue
                    
                    # Find report files
                    report_files = list(date_dir.glob("*.md"))
                    summary_files = list(date_dir.glob("*.json"))
                    log_files = list(date_dir.glob("*.log"))
                    
                    # Check for complete reports
                    complete_reports = list(date_dir.glob("complete_report_*.md"))
                    
                    reports.append({
                        "ticker": current_ticker,
                        "date": current_date,
                        "path": date_dir,
                        "report_files": report_files,
                        "summary_files": summary_files,
                        "log_files": log_files,
                        "complete_reports": complete_reports
                    })
    
    return reports

@app.command()
def list_reports(
    ticker: str = typer.Option(None, "--ticker", "-t", help="Filter by ticker symbol"),
    date: str = typer.Option(None, "--date", "-d", help="Filter by date (YYYY-MM-DD)"),
    show_details: bool = typer.Option(False, "--details", help="Show detailed file information")
):
    """List all saved reports."""
    reports = find_reports(ticker, date)
    
    if not reports:
        console.print("[yellow]No reports found matching your criteria.[/yellow]")
        return
    
    # Create table
    table = Table(title="TradingAgents Reports")
    table.add_column("Ticker", style="cyan")
    table.add_column("Date", style="green")
    table.add_column("Complete Reports", style="blue")
    table.add_column("Individual Reports", style="magenta")
    table.add_column("Path", style="dim")
    
    for report in reports:
        complete_count = len(report["complete_reports"])
        individual_count = len(report["report_files"])
        
        table.add_row(
            report["ticker"],
            report["date"],
            str(complete_count),
            str(individual_count),
            str(report["path"])
        )
    
    console.print(table)
    
    if show_details:
        for report in reports:
            console.print(f"\n[bold]Details for {report['ticker']} on {report['date']}:[/bold]")
            
            if report["complete_reports"]:
                console.print("  [green]Complete Reports:[/green]")
                for file in report["complete_reports"]:
                    console.print(f"    - {file.name}")
            
            if report["report_files"]:
                console.print("  [blue]Individual Reports:[/blue]")
                for file in report["report_files"]:
                    console.print(f"    - {file.name}")
            
            if report["summary_files"]:
                console.print("  [yellow]Summary Files:[/yellow]")
                for file in report["summary_files"]:
                    console.print(f"    - {file.name}")

@app.command()
def show_report(
    ticker: str = typer.Argument(..., help="Ticker symbol"),
    date: str = typer.Argument(..., help="Analysis date (YYYY-MM-DD)"),
    report_type: str = typer.Option("complete", "--type", "-t", help="Report type: complete, market, sentiment, news, fundamentals, investment, trader, final")
):
    """Show a specific report."""
    reports = find_reports(ticker, date)
    
    if not reports:
        console.print(f"[red]No reports found for {ticker} on {date}[/red]")
        return
    
    report = reports[0]  # Take the first match
    
    if report_type == "complete":
        # Find the most recent complete report
        complete_reports = report["complete_reports"]
        if not complete_reports:
            console.print("[red]No complete report found. Run an analysis first.[/red]")
            return
        
        # Sort by modification time and get the most recent
        latest_report = max(complete_reports, key=lambda f: f.stat().st_mtime)
        
        with open(latest_report, "r") as f:
            content = f.read()
        
        console.print(Panel(Markdown(content), title=f"Complete Report - {ticker} ({date})"))
    
    else:
        # Find individual report
        report_file = report["path"] / "reports" / f"{report_type}_report.md"
        
        if not report_file.exists():
            console.print(f"[red]Report {report_type}_report.md not found.[/red]")
            return
        
        with open(report_file, "r") as f:
            content = f.read()
        
        console.print(Panel(Markdown(content), title=f"{report_type.title()} Report - {ticker} ({date})"))

@app.command()
def latest_report(ticker: str = typer.Argument(..., help="Ticker symbol")):
    """Show the latest report for a ticker."""
    reports = find_reports(ticker)
    
    if not reports:
        console.print(f"[red]No reports found for {ticker}[/red]")
        return
    
    # Sort by date and get the latest
    latest_report_data = max(reports, key=lambda r: r["date"])
    
    # Find the most recent complete report
    complete_reports = latest_report_data["complete_reports"]
    if not complete_reports:
        console.print(f"[red]No complete report found for {ticker}[/red]")
        return
    
    latest_report_file = max(complete_reports, key=lambda f: f.stat().st_mtime)
    
    with open(latest_report_file, "r") as f:
        content = f.read()
    
    console.print(Panel(Markdown(content), title=f"Latest Report - {ticker} ({latest_report_data['date']})"))

@app.command()
def export_reports(
    ticker: str = typer.Argument(..., help="Ticker symbol"),
    date: str = typer.Argument(..., help="Analysis date (YYYY-MM-DD)"),
    output_dir: str = typer.Option("./export", "--output", "-o", help="Output directory")
):
    """Export all reports for a ticker and date to a directory."""
    reports = find_reports(ticker, date)
    
    if not reports:
        console.print(f"[red]No reports found for {ticker} on {date}[/red]")
        return
    
    report = reports[0]
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Copy all files
    import shutil
    
    for file in report["path"].rglob("*"):
        if file.is_file():
            relative_path = file.relative_to(report["path"])
            dest_path = output_path / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest_path)
    
    console.print(f"[green]✅ Reports exported to {output_path}[/green]")

if __name__ == "__main__":
    app() 