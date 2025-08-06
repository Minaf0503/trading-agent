# TradingAgents Report Management

This guide explains how to always save and manage your TradingAgents analysis reports.

## How Reports Are Saved

TradingAgents automatically saves reports in the following structure:

```
results/
└── {TICKER}/
    └── {DATE}/
        ├── complete_report_YYYYMMDD_HHMMSS.md    # Complete analysis report
        ├── analysis_summary_YYYYMMDD_HHMMSS.json # Analysis metadata
        ├── message_tool.log                      # Detailed execution log
        └── reports/
            ├── market_report.md                   # Market analyst report
            ├── sentiment_report.md                # Social media analyst report
            ├── news_report.md                     # News analyst report
            ├── fundamentals_report.md             # Fundamentals analyst report
            ├── investment_plan.md                 # Research team decision
            ├── trader_investment_plan.md          # Trading team plan
            └── final_trade_decision.md           # Portfolio management decision
```

## What Gets Saved Automatically

### 1. **Complete Report** (`complete_report_*.md`)
- **Always saved** with timestamp
- Contains all analysis sections in one file
- Includes metadata (ticker, date, analysts used, etc.)
- Most comprehensive report format

### 2. **Individual Reports** (`reports/*.md`)
- Each analyst's report saved separately
- Updated in real-time as analysis progresses
- Useful for detailed review of specific components

### 3. **Analysis Summary** (`analysis_summary_*.json`)
- Metadata about the analysis
- Configuration used (LLM models, research depth, etc.)
- File paths to all generated reports
- Final trading decision

### 4. **Execution Log** (`message_tool.log`)
- Detailed log of all tool calls and messages
- Useful for debugging and understanding the analysis process

## Managing Your Reports

### Using the Report Manager

The system includes a report management tool to help you find and access your saved reports:

```bash
# List all reports
python cli/report_manager.py list-reports

# List reports for a specific ticker
python cli/report_manager.py list-reports --ticker AAPL

# List reports for a specific date
python cli/report_manager.py list-reports --date 2025-01-15

# Show detailed file information
python cli/report_manager.py list-reports --details

# Show the latest complete report for a ticker
python cli/report_manager.py latest-report AAPL

# Show a specific report
python cli/report_manager.py show-report AAPL 2025-01-15 --type complete
python cli/report_manager.py show-report AAPL 2025-01-15 --type market
python cli/report_manager.py show-report AAPL 2025-01-15 --type sentiment

# Export all reports for a ticker/date
python cli/report_manager.py export-reports AAPL 2025-01-15 --output ./my_reports
```

### Report Types Available

- `complete` - Full analysis report (default)
- `market` - Market analyst report
- `sentiment` - Social media analyst report
- `news` - News analyst report
- `fundamentals` - Fundamentals analyst report
- `investment` - Research team decision
- `trader` - Trading team plan
- `final` - Portfolio management decision

## Configuration Options

You can control report saving behavior by modifying the configuration in `tradingagents/default_config.py`:

```python
# Report saving settings
"always_save_reports": True,        # Always save reports (default: True)
"save_complete_report": True,        # Save complete report (default: True)
"save_individual_reports": True,     # Save individual reports (default: True)
"save_analysis_summary": True,       # Save analysis summary (default: True)
```

## Manual Report Access

You can also directly access your reports in the file system:

```bash
# Navigate to results directory
cd results

# Find reports for a specific ticker
ls -la AAPL/

# View a complete report
cat AAPL/2025-01-15/complete_report_20250115_143022.md

# View individual reports
cat AAPL/2025-01-15/reports/market_report.md
cat AAPL/2025-01-15/reports/sentiment_report.md
```

## Report Content Structure

### Complete Report Format
```markdown
# TradingAgents Complete Analysis Report

**Ticker:** AAPL
**Analysis Date:** 2025-01-15
**Generated:** 2025-01-15 14:30:22
**Analysts:** market, social, news, fundamentals
**Research Depth:** 5
**LLM Provider:** openai

---

## Analyst Team Reports

### Market Analysis
[Market analyst content...]

### Social Sentiment
[Social media analyst content...]

### News Analysis
[News analyst content...]

### Fundamentals Analysis
[Fundamentals analyst content...]

## Research Team Decision
[Research team content...]

## Trading Team Plan
[Trading team content...]

## Portfolio Management Decision
[Portfolio management content...]
```

## Tips for Report Management

1. **Always check the complete report first** - It contains the most comprehensive analysis
2. **Use timestamps** - Reports are saved with timestamps to avoid overwrites
3. **Export for sharing** - Use the export function to share reports with others
4. **Review individual reports** - Check specific analyst reports for detailed insights
5. **Check the summary** - The JSON summary contains metadata and file locations

## Troubleshooting

### Reports Not Saving
- Check that the `results` directory exists and is writable
- Verify that `always_save_reports` is set to `True` in the configuration
- Check the console output for any error messages during analysis

### Missing Reports
- Reports are saved in `./results/{TICKER}/{DATE}/`
- Complete reports have timestamps: `complete_report_YYYYMMDD_HHMMSS.md`
- Individual reports are in the `reports/` subdirectory

### Access Issues
- Use the report manager tool for easy access
- Check file permissions if you can't read saved reports
- Verify the analysis completed successfully before looking for reports 