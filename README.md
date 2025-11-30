# Reddit Market Research Tool

Search Reddit for potential users, pain points, and market opportunities for your projects.

## Setup

```bash
cd /Users/jeremywatt/Desktop/reddit-market-research
source venv/bin/activate
```

## Usage

### Search Historical Posts

```bash
# Basic search (keywords and subreddits required)
python reddit_monitor.py search -s "startups+SaaS" -k "AI tool,help,recommendation"

# JSON output for programmatic use
python reddit_monitor.py search -s "webdev" -k "bug,issue" --json

# Save to CSV
python reddit_monitor.py search -s "programming" -k "help,looking for" --output results.csv

# Time filters and limits
python reddit_monitor.py search -s "fitness" -k "app,tracking" --time year --limit 50

# Load keywords from file
python reddit_monitor.py search -s "startups" --keywords-file keywords.txt --json
```

### Monitor New Posts (real-time)

```bash
python reddit_monitor.py monitor -s "startups+SaaS" -k "looking for,need help"
```

## Options

| Flag | Short | Description |
|------|-------|-------------|
| `--subreddits` | `-s` | Subreddits to search (plus-separated) **required** |
| `--keywords` | `-k` | Keywords to match (comma-separated) |
| `--keywords-file` | | Load keywords from file (one per line) |
| `--time` | `-t` | Time filter: hour, day, week, month, year, all |
| `--sort` | | Sort: relevance, hot, top, new, comments |
| `--limit` | `-l` | Max results to display |
| `--json` | `-j` | Output as JSON |
| `--output` | `-o` | Save to file (.csv or .json) |

## Output Fields

Each result includes:
- `title` - Post title
- `body` - First 200 chars of post body (where pain points often live)
- `subreddit` - Source subreddit
- `score` - Upvotes
- `comments` - Comment count
- `url` - Direct link to post
- `created` - Post timestamp
- `author` - Reddit username

## Claude Code Workflow

This tool is designed to be used with Claude Code for market research on GitHub repos:

```
User: "Research market opportunities for https://github.com/neonwatty/seating-arrangement"

Claude Code:
  1. Fetches repo README via WebFetch
  2. Analyzes project → generates keywords + subreddits
  3. Runs: python reddit_monitor.py search -s "..." -k "..." --json
  4. Parses JSON results
  5. Summarizes opportunities for user
```

Example prompts:
- "Find Reddit discussions about problems my seating-arrangement tool could solve"
- "Search for potential users of my meme-search project"
- "What pain points do people have that my youtube-tools repo addresses?"

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
