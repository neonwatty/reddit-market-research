# Reddit Market Research Tool

Search Reddit for potential users and market opportunities.

## Setup

```bash
cd /Users/jeremywatt/Desktop/reddit-market-research
source venv/bin/activate
```

## Usage

### Search Historical Posts

```bash
python reddit_monitor.py search                              # Default (seating keywords)
python reddit_monitor.py search --json                       # JSON output
python reddit_monitor.py search --output results.csv         # Save to CSV
python reddit_monitor.py search --limit 50                   # More results
python reddit_monitor.py search --time week                  # Last week only
python reddit_monitor.py search --sort top                   # Sort by top
```

### Custom Market Research

```bash
python reddit_monitor.py search \
  --subreddits "SaaS+startups" \
  --keywords "AI tool,automation" \
  --json
```

### Monitor New Posts (real-time)

```bash
python reddit_monitor.py monitor
```

## Options

| Flag | Short | Description |
|------|-------|-------------|
| `--subreddits` | `-s` | Subreddits to search (plus-separated) |
| `--keywords` | `-k` | Keywords to match (comma-separated) |
| `--time` | `-t` | Time filter: hour, day, week, month, year, all |
| `--sort` | | Sort: relevance, hot, top, new, comments |
| `--limit` | `-l` | Max results to display |
| `--json` | `-j` | Output as JSON |
| `--output` | `-o` | Save to file (.csv or .json) |

## Output Fields

Each result includes:
- `title` - Post title
- `subreddit` - Source subreddit
- `score` - Upvotes
- `comments` - Comment count
- `url` - Direct link to post
- `created` - Post timestamp
- `author` - Reddit username

## Development

```bash
# Install dev dependencies
pip install ruff pytest mypy vulture

# Run linting
ruff check reddit_monitor.py

# Run formatter
ruff format reddit_monitor.py

# Run type checking
mypy reddit_monitor.py

# Run dead code detection
vulture reddit_monitor.py tests/

# Run tests
pytest tests/ -v
```
