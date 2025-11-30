"""Tests for reddit_monitor.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from reddit_monitor import check_relevance, output_results


class TestCheckRelevance:
    """Tests for check_relevance function."""

    def test_exact_match(self) -> None:
        """Test exact keyword match."""
        assert check_relevance("Help with seating chart", ["seating chart"]) is True

    def test_case_insensitive(self) -> None:
        """Test case insensitive matching."""
        assert check_relevance("SEATING CHART help", ["seating chart"]) is True
        assert check_relevance("Seating Chart Help", ["seating chart"]) is True

    def test_no_match(self) -> None:
        """Test no keyword match."""
        assert check_relevance("Wedding dress ideas", ["seating chart"]) is False

    def test_multiple_keywords(self) -> None:
        """Test multiple keywords."""
        keywords = ["seating chart", "table layout", "guest seating"]
        assert check_relevance("Need help with table layout", keywords) is True
        assert check_relevance("Wedding venue ideas", keywords) is False

    def test_partial_match_in_word(self) -> None:
        """Test that partial matches within words work."""
        assert check_relevance("My seating chart is ready", ["seating"]) is True

    def test_empty_text(self) -> None:
        """Test empty text."""
        assert check_relevance("", ["seating chart"]) is False

    def test_empty_keywords(self) -> None:
        """Test empty keywords list."""
        assert check_relevance("seating chart help", []) is False


class TestOutputResults:
    """Tests for output_results function."""

    @pytest.fixture
    def sample_results(self) -> list[dict[str, str | int]]:
        """Sample results for testing."""
        return [
            {
                "title": "Test Post 1",
                "subreddit": "weddingplanning",
                "score": 100,
                "comments": 50,
                "url": "https://reddit.com/r/weddingplanning/test1",
                "created": "2025-01-01T12:00:00",
                "author": "testuser1",
            },
            {
                "title": "Test Post 2",
                "subreddit": "eventplanning",
                "score": 200,
                "comments": 75,
                "url": "https://reddit.com/r/eventplanning/test2",
                "created": "2025-01-02T12:00:00",
                "author": "testuser2",
            },
        ]

    def test_json_output(
        self, sample_results: list[dict[str, str | int]], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test JSON output format."""
        output_results(sample_results, output_format="json")
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert len(parsed) == 2
        assert parsed[0]["title"] == "Test Post 1"

    def test_limit_results(
        self, sample_results: list[dict[str, str | int]], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test limiting results."""
        output_results(sample_results, output_format="json", limit=1)
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert len(parsed) == 1

    def test_csv_output_to_file(
        self, sample_results: list[dict[str, str | int]], tmp_path: Path
    ) -> None:
        """Test CSV file output."""
        output_file = tmp_path / "test_results.csv"
        output_results(sample_results, output_format="csv", output_file=str(output_file))
        assert output_file.exists()
        content = output_file.read_text()
        assert "title,subreddit,score,comments,url,created,author" in content
        assert "Test Post 1" in content

    def test_json_output_to_file(
        self, sample_results: list[dict[str, str | int]], tmp_path: Path
    ) -> None:
        """Test JSON file output."""
        output_file = tmp_path / "test_results.json"
        output_results(sample_results, output_format="json", output_file=str(output_file))
        assert output_file.exists()
        content = json.loads(output_file.read_text())
        assert len(content) == 2

    def test_text_output(
        self, sample_results: list[dict[str, str | int]], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test text output format."""
        output_results(sample_results, output_format="text")
        captured = capsys.readouterr()
        assert "Found 2 relevant posts" in captured.out
        assert "Test Post 1" in captured.out
        assert "https://reddit.com/r/weddingplanning/test1" in captured.out
