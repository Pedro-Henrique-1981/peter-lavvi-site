"""
Test Helpers and Fixtures for Lavvi Media Agency E2E Test Suite.
Provides resilient DOM inspection, CSS analysis, asset validation,
and compliance checking without third-party dependencies.
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser
from typing import List, Dict, Optional, Tuple, Any

# Root directory of the repository
ROOT_DIR = Path(__file__).resolve().parent.parent

def get_root_dir() -> Path:
    return ROOT_DIR

def read_text(rel_path: str) -> Optional[str]:
    """Reads a file relative to project root with UTF-8 encoding."""
    target = ROOT_DIR / rel_path
    if not target.exists() or not target.is_file():
        return None
    try:
        return target.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

def file_exists(rel_path: str) -> bool:
    """Checks if a file exists relative to project root."""
    return (ROOT_DIR / rel_path).exists()

def get_file_size(rel_path: str) -> int:
    """Returns the size of a file in bytes, or -1 if missing."""
    target = ROOT_DIR / rel_path
    if not target.exists() or not target.is_file():
        return -1
    return target.stat().st_size

def is_jpeg_valid(rel_path: str) -> bool:
    """Checks if the file has valid JPEG magic bytes (FF D8 FF)."""
    target = ROOT_DIR / rel_path
    if not target.exists() or not target.is_file():
        return False
    try:
        with open(target, "rb") as f:
            header = f.read(3)
            return header == b"\xff\xd8\xff"
    except Exception:
        return False

class DOMNode:
    """Representation of an HTML element node in parsed DOM tree."""
    def __init__(self, tag: str, attrs: Dict[str, str], parent: Optional['DOMNode'] = None):
        self.tag = tag.lower()
        self.attrs = attrs
        self.parent = parent
        self.children: List['DOMNode'] = []
        self.text_content: str = ""

    @property
    def id(self) -> Optional[str]:
        return self.attrs.get("id")

    @property
    def classes(self) -> List[str]:
        c = self.attrs.get("class", "")
        return [cls.strip() for cls in c.split() if cls.strip()]

    def has_class(self, cls_name: str) -> bool:
        return cls_name in self.classes

    def get_attr(self, name: str) -> Optional[str]:
        return self.attrs.get(name)

    def find_all(self, tag: Optional[str] = None, class_name: Optional[str] = None, attr: Optional[Tuple[str, str]] = None) -> List['DOMNode']:
        matches = []
        if (tag is None or self.tag == tag.lower()) and \
           (class_name is None or self.has_class(class_name)) and \
           (attr is None or self.attrs.get(attr[0]) == attr[1]):
            matches.append(self)
        for child in self.children:
            matches.extend(child.find_all(tag=tag, class_name=class_name, attr=attr))
        return matches

    def find_first(self, tag: Optional[str] = None, class_name: Optional[str] = None, attr: Optional[Tuple[str, str]] = None) -> Optional['DOMNode']:
        res = self.find_all(tag=tag, class_name=class_name, attr=attr)
        return res[0] if res else None

class HTMLDOMInspector(HTMLParser):
    """Resilient HTML parser for structural DOM, landmark, and ID validation."""
    def __init__(self):
        super().__init__()
        self.root = DOMNode("root", {})
        self.current_node = self.root
        self.all_nodes: List[DOMNode] = []
        self.ids_map: Dict[str, List[DOMNode]] = {}
        self.comments: List[str] = []
        self.landmarks: Dict[str, List[DOMNode]] = {
            "header": [],
            "nav": [],
            "search": [],
            "main": [],
            "footer": [],
            "dialog": []
        }

    def handle_starttag(self, tag, attrs):
        attr_dict = {k.lower(): v for k, v in attrs if v is not None}
        node = DOMNode(tag, attr_dict, parent=self.current_node)
        self.current_node.children.append(node)
        self.all_nodes.append(node)

        tag_lower = tag.lower()
        if tag_lower in self.landmarks:
            self.landmarks[tag_lower].append(node)

        # Track role="search" or role="navigation" as semantic landmarks
        role = attr_dict.get("role", "").lower()
        if role == "search" and tag_lower != "search":
            self.landmarks["search"].append(node)
        elif role == "navigation" and tag_lower != "nav":
            self.landmarks["nav"].append(node)

        node_id = attr_dict.get("id")
        if node_id:
            if node_id not in self.ids_map:
                self.ids_map[node_id] = []
            self.ids_map[node_id].append(node)

        # Void elements in HTML
        if tag_lower not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.current_node = node

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        node = self.current_node
        while node is not None and node.tag != tag_lower:
            node = node.parent
        if node is not None and node.parent is not None:
            self.current_node = node.parent

    def handle_data(self, data):
        if self.current_node:
            self.current_node.text_content += data

    def handle_comment(self, data):
        self.comments.append(data)

    @classmethod
    def parse_html(cls, html_content: str) -> 'HTMLDOMInspector':
        inspector = cls()
        inspector.feed(html_content)
        return inspector

    def find_all(self, tag: Optional[str] = None, class_name: Optional[str] = None, attr: Optional[Tuple[str, str]] = None) -> List[DOMNode]:
        return self.root.find_all(tag=tag, class_name=class_name, attr=attr)

    def find_first(self, tag: Optional[str] = None, class_name: Optional[str] = None, attr: Optional[Tuple[str, str]] = None) -> Optional[DOMNode]:
        return self.root.find_first(tag=tag, class_name=class_name, attr=attr)

class CSSAnalyzer:
    """Analyzes CSS tokens, typography, and responsive media query rules."""
    def __init__(self, css_content: str):
        self.raw_css = css_content
        self.variables = self._extract_css_variables()

    def _extract_css_variables(self) -> Dict[str, str]:
        vars_map = {}
        # Matches --variable-name: value;
        pattern = re.compile(r'(--[a-zA-Z0-9_\-]+)\s*:\s*([^;]+);')
        for match in pattern.finditer(self.raw_css):
            name = match.group(1).strip()
            val = match.group(2).strip()
            vars_map[name] = val
        return vars_map

    def has_token(self, token_name: str, expected_val_substring: Optional[str] = None) -> bool:
        if token_name not in self.variables:
            return False
        if expected_val_substring:
            return expected_val_substring.lower() in self.variables[token_name].lower()
        return True

    def find_font_families(self) -> List[str]:
        pattern = re.compile(r'font-family\s*:\s*([^;]+);', re.IGNORECASE)
        return [m.group(1).strip() for m in pattern.finditer(self.raw_css)]

    def has_clamp_typography(self) -> bool:
        return "clamp(" in self.raw_css.lower()

    def has_class_definition(self, class_name: str) -> bool:
        cls_pattern = re.compile(rf'\.{re.escape(class_name)}\b')
        return bool(cls_pattern.search(self.raw_css))

def run_sentinel_script() -> Tuple[int, str, str]:
    """Runs scripts/cosimo_sentinel.py and returns (exit_code, stdout, stderr)."""
    script_path = ROOT_DIR / "scripts" / "cosimo_sentinel.py"
    if not script_path.exists():
        return (-1, "", f"Script not found: {script_path}")
    res = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    return (res.returncode, res.stdout, res.stderr)
