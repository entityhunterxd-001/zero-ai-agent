import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".zero_agent"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CAPABILITIES = {
    "model_info": {
        "name": "",
        "type": "local", # or "cloud"
        "base_url": "http://localhost:11434"
    },
    "agent_capabilities": [
        "search_internet: Searches the web using DuckDuckGo",
        "scrape_website: High-performance Rust scraping of specific URLs",
        "schedule_task: Schedules recurring background tasks",
        "remove_task: Cancels scheduled background tasks",
        "save_memory: Remembers user facts and preferences permanently"
    ],
    "system_rules": [
        "Always use tools to verify facts before answering.",
        "Save important user details to long-term memory immediately.",
        "Keep responses concise and formatted in Markdown."
    ]
}

def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def save_config(config: dict):
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None