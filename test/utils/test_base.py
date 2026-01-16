"""
Base test class with common utilities for all tests
"""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, List

class TestBase:
    """Base class for all tests providing common utilities"""

    def __init__(self):
        self.test_dir = None
        self.original_cwd = os.getcwd()
        self.project_root = Path(__file__).parent.parent.parent

    def setup(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix='claude_test_')
        os.chdir(self.test_dir)

    def teardown(self):
        """Cleanup test environment"""
        os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_file(self, path: str, content: str = "") -> Path:
        """Create a test file"""
        file_path = Path(self.test_dir) / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path

    def create_json(self, path: str, data: Dict[str, Any]) -> Path:
        """Create a JSON test file"""
        file_path = Path(self.test_dir) / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return file_path

    def read_file(self, path: str) -> str:
        """Read a test file"""
        file_path = Path(self.test_dir) / path
        return file_path.read_text()

    def read_json(self, path: str) -> Dict[str, Any]:
        """Read a JSON test file"""
        file_path = Path(self.test_dir) / path
        with open(file_path) as f:
            return json.load(f)

    def assert_file_exists(self, path: str):
        """Assert that a file exists"""
        file_path = Path(self.test_dir) / path
        assert file_path.exists(), f"File {path} does not exist"

    def assert_file_contains(self, path: str, content: str):
        """Assert that a file contains specific content"""
        actual = self.read_file(path)
        assert content in actual, f"File {path} does not contain '{content}'"

    def assert_json_has_keys(self, path: str, keys: List[str]):
        """Assert that a JSON file has specific keys"""
        data = self.read_json(path)
        for key in keys:
            assert key in data, f"JSON file {path} missing key '{key}'"

    def assert_directory_structure(self, expected_structure: Dict[str, Any], base_path: str = ""):
        """Assert that a directory structure matches expectations"""
        base = Path(self.test_dir) / base_path

        for name, item in expected_structure.items():
            path = base / name

            if isinstance(item, dict):
                # Directory
                assert path.is_dir(), f"Expected directory {path} not found"
                self.assert_directory_structure(item, str(path.relative_to(self.test_dir)))
            elif isinstance(item, str):
                # File with content check
                assert path.is_file(), f"Expected file {path} not found"
                if item:  # If content specified, check it
                    actual = path.read_text()
                    assert item in actual, f"File {path} doesn't contain expected content"
            elif item is None:
                # File existence check only
                assert path.is_file(), f"Expected file {path} not found"

    def create_mock_specification(self, spec_type: str = "base") -> str:
        """Create a mock project specification for testing"""
        specs = {
            "base": """
# Project Specification

## Overview
Basic project for testing

## Requirements
- Feature A
- Feature B
- Feature C

## Technical Stack
- Python
- SQLite
            """,
            "power-query": """
# Power BI Dashboard Project

## Overview
Power Query based data transformation

## Requirements
- Import data from Excel
- Transform using Power Query
- Create DAX measures
- Build Power BI reports

## Data Sources
- Sales.xlsx
- Customers.csv
            """,
            "research": """
# Research Analysis Project

## Overview
Statistical analysis and research study

## Requirements
- Literature review
- Data collection
- Statistical analysis
- Report generation

## Methodology
- Quantitative analysis
- Regression models
            """,
            "life-projects": """
# Home Renovation Project

## Overview
Personal life project for home renovation

## Requirements
- Kitchen remodel
- Budget tracking
- Vendor coordination
- Timeline management

## Budget
- Total: $50,000
- Contingency: 10%
            """,
            "documentation": """
# API Documentation Project

## Overview
Documentation for REST API

## Requirements
- API endpoint documentation
- Code examples
- Tutorial guides
- Reference documentation

## Structure
- Getting Started
- API Reference
- Examples
            """
        }
        return specs.get(spec_type, specs["base"])