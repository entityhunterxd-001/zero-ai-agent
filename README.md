<div align="center">

```text
  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ╚══███╔╝██╔═══██╗██╔══██╗██╔═══██╗██╔════╝
    ███╔╝ ██║   ██║██████╔╝██║   ██║███████╗
   ███╝  ██║   ██║██╔══██╗██║   ██║╚════██║
  ███████╗╚██████╔╝██║  ██║██████╔╝███████║
  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ═════╝ ╚══════╝
```

**An autonomous AI research assistant powered by LangGraph, Rust, and Ollama**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🌟 Overview

**Zero AI Agent** is not just a chatbot—it's a fully autonomous research assistant that lives in your terminal. Built with a **high-performance Rust web scraper** for blazing-fast data extraction and orchestrated by **LangGraph**, it autonomously searches the internet, scrapes relevant articles, and synthesizes information into clear, concise summaries.

Whether you need the latest trending news, deep-dive research on a specific URL, or automated daily briefings scheduled in the background, Zero AI Agent handles it all while running securely on your local machine via Ollama.

---

## ✨ Features

### 🧠 Autonomous Intelligence
- **ReAct Agent Pattern**: Uses LangGraph's Reason + Act framework to autonomously decide when to search, scrape, and synthesize
- **Multi-Step Reasoning**: Breaks down complex queries into actionable steps
- **Self-Correction**: Automatically retries failed operations and validates results

### 🦀 Blazing Fast Web Scraping
- **Custom Rust Binary**: Memory-safe, lightning-fast web scraping using `reqwest` and `scraper`
- **Clean Data Extraction**: Automatically strips HTML and extracts meaningful content
- **Parallel Processing**: Handles multiple URLs efficiently

### 📅 Background Task Scheduling
- **Automated Tasks**: Schedule recurring tasks like "Get me tech news every day at 9 AM"
- **Persistent Scheduler**: Tasks survive agent restarts
- **Easy Management**: Add, remove, and list scheduled tasks via natural language

### 🧠 Dual-Layer Memory System
- **Short-Term Memory**: Remembers your recent conversation context (last 20 messages)
- **Long-Term Memory**: Persists important facts about you (name, preferences, rules) across sessions
- **Automatic Recall**: Agent automatically uses saved memories to personalize responses

### 🏠 Privacy-First LLM
- **Local Execution**: Runs entirely on your machine using Ollama
- **No Data Leaks**: Your queries and scraped data never leave your computer
- **Flexible Models**: Supports Llama 3, Gemma, Mistral, and any Ollama-compatible model

### 🎨 Beautiful CLI Interface
- **Rich Terminal UI**: Colorful banners, tables, and progress indicators
- **Interactive Setup**: Easy-to-use setup wizard for first-time configuration
- **Cross-Platform**: Works on Windows, Linux, macOS, and Termux (Android)

---

## 🚀 Quick Start

### Prerequisites

Before installing Zero AI Agent, ensure you have:

1. **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
2. **Ollama** - [Download Ollama](https://ollama.ai/)
3. **Rust** (optional, will be auto-installed during setup) - [Install Rust](https://rustup.rs/)

### Step 1: Install uv (Python Package Manager)

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation:**
```bash
uv --version
```

### Step 2: Install Zero AI Agent

Install the agent globally with a single command:

```bash
uv tool install git+https://github.com/entityhunterxd-001/zero-ai-agent
```

This will:
- Download the latest code from GitHub
- Create an isolated virtual environment
- Install all dependencies (LangChain, Rich, DDGS, etc.)
- Make the `zero-ai-agent` command available globally

### Step 3: Run the Setup Wizard

```bash
zero-ai-agent setup
```

The setup wizard will guide you through:

1. **Ollama Configuration**
   - Choose between local or cloud Ollama
   - Enter your Ollama API base URL (default: `http://localhost:11434`)
   - Select your preferred model (e.g., `llama3`, `gemma2`, `mistral`)

2. **Rust Scraper Compilation**
   - Automatically detects if Rust is installed
   - Compiles the high-performance web scraper
   - Saves the binary to `~/.zero_agent/`

3. **Configuration Save**
   - Creates `~/.zero_agent/config.json` with your settings
   - Ready to use immediately!

### Step 4: Start the Agent

```bash
zero-ai-agent run
```

You'll see the beautiful banner, capabilities table, and then you can start chatting!

---

## 📖 Usage Examples

### Basic Conversation
```
👤 You: Hello, my name is Alex

🤖 Agent: Hello Alex! Nice to meet you. I've saved your name to memory.
```

### Web Research
```
👤 You: What are the latest AI news headlines today?

🤖 Agent: [Autonomously searches DuckDuckGo, scrapes top articles, and summarizes]
```

### URL Scraping
```
👤 You: Can you scrape and summarize https://en.wikipedia.org/wiki/Rust_(programming_language)

🤖 Agent: [Uses Rust scraper to fetch clean content and provides summary]
```

### Task Scheduling
```
👤 You: Schedule a daily task at 09:00 to give me top tech news

🤖 Agent: Successfully scheduled 'top tech news' for 09:00 daily.
```

### Task Management
```
👤 You: Remove the tech news task

🤖 Agent: Successfully removed 1 task(s) matching 'tech news'.
```

### Memory Recall
```
👤 You: What's my name?

🤖 Agent: Your name is Alex.
```

---

## 🛠️ Commands Reference

| Command | Description |
|---------|-------------|
| `zero-ai-agent setup` | Run the interactive setup wizard |
| `zero-ai-agent run` | Start the interactive AI agent |
| `zero-ai-agent status` | Check current configuration and status |
| `zero-ai-agent --help` | Show all available commands |

---

## 🔧 Configuration

After setup, your configuration is stored in `~/.zero_agent/config.json`:

```json
{
  "model_info": {
    "name": "llama3",
    "type": "local",
    "base_url": "http://localhost:11434"
  },
  "agent_capabilities": [
    "search_internet: Searches the web using DuckDuckGo",
    "scrape_website: High-performance Rust scraping of specific URLs",
    "schedule_task: Schedules recurring background tasks",
    "remove_task: Cancels scheduled background tasks",
    "save_memory: Remembers user facts and preferences permanently"
  ]
}
```

### Change Model

To switch to a different model:

```bash
zero-ai-agent setup
```

Then enter the new model name when prompted (e.g., `gemma2`, `mistral`, `codellama`).

### Manual Configuration Edit

You can also manually edit `~/.zero_agent/config.json` to change settings.

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Rich CLI + Typer Commands)                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 LangGraph Agent                          │
│         (ReAct Pattern + Tool Calling)                   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌──▼──────────┐
│   Search     │ │ Scrape  │ │  Schedule   │
│   Tool       │ │ Tool    │ │  Tool       │
│ (DuckDuckGo) │ │ (Rust)  │ │ (Background)│
└──────────────┘ └─────────┘ └─────────────┘
```

---

## 🔒 Privacy & Security

- **100% Local**: All processing happens on your machine
- **No Telemetry**: Zero data collection or tracking
- **Encrypted Storage**: Memory and history stored locally in JSON
- **Open Source**: Fully auditable code on GitHub

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
uv tool uninstall zero-ai-agent
uv tool install git+https://github.com/entityhunterxd-001/zero-ai-agent --reinstall
```

### Rust compilation fails
Ensure Rust is installed:
```bash
rustc --version
```

If not installed:
- **Windows**: Download from https://rustup.rs/
- **macOS/Linux**: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

### Ollama connection refused
Make sure Ollama is running:
```bash
ollama serve
```

### Agent can't remember my name
Check if memory file exists:
```bash
cat ~/.zero_agent/memory.json
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - LLM orchestration framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Rust](https://www.rust-lang.org/) - High-performance systems programming
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Typer](https://github.com/tiangolo/typer) - CLI framework
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

---

## 📞 Support

- **GitHub Issues**: [Report a bug](https://github.com/entityhunterxd-001/zero-ai-agent/issues)
- **Discussions**: [Ask a question](https://github.com/entityhunterxd-001/zero-ai-agent/discussions)

---

<div align="center">

**Made with ❤️ by [entityhunterxd-001](https://github.com/entityhunterxd-001)**

⭐ Star this repo if you find it useful!

</div>
