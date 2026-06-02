import os
import json
import subprocess
import time
import threading
import schedule
from datetime import datetime
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from duckduckgo_search import DDGS
from rich.console import Console

console = Console()

# ==========================================
# CONFIGURATION
# ==========================================
BASE_DIR = Path.home() / ".zero_agent"
RUST_BINARY_NAME = "rust_scraper.exe" if os.name == "nt" else "rust_scraper"
RUST_BINARY_PATH = BASE_DIR / RUST_BINARY_NAME

SCHEDULES_FILE = BASE_DIR / "schedules.json"
MEMORY_FILE = BASE_DIR / "memory.json"
HISTORY_FILE = BASE_DIR / "chat_history.json"

reload_schedules_flag = True

# ==========================================
# MEMORY MANAGEMENT
# ==========================================
def load_long_term_memory() -> list:
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    return []

def load_short_term_history() -> list:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try: 
                history = json.load(f)
                return [HumanMessage(content=m["content"]) if m["role"] == "human" else AIMessage(content=m["content"]) for m in history]
            except: return []
    return []

def save_short_term_history(messages: list):
    clean_history = []
    for msg in messages[-20:]: 
        if isinstance(msg, (HumanMessage, AIMessage)):
            clean_history.append({"role": "human" if isinstance(msg, HumanMessage) else "ai", "content": msg.content})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(clean_history, f, indent=4)

# ==========================================
# TOOLS
# ==========================================
@tool
def search_internet(query: str) -> str:
    """Search the internet for recent information."""
    console.print(f"   🔍 [Tool] Searching for: '{query}'...")
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if not results: return "No results found."
            return "\n---\n".join([f"Title: {r['title']}\nURL: {r['href']}\n" for r in results])
    except Exception as e: return f"Search failed: {str(e)}"

@tool
def scrape_website(url: str) -> str:
    """Scrape the full text content of a specific URL using the Rust scraper."""
    console.print(f"   🕷️  [Tool] Rust Scraper fetching: {url}...")
    if not RUST_BINARY_PATH.exists(): return "Error: Rust scraper binary not found."
    try:
        result = subprocess.run([str(RUST_BINARY_PATH), url], capture_output=True, text=True, check=True, timeout=30)
        data = json.loads(result.stdout)
        return f"Title: {data.get('title')}\nContent:\n{data.get('content', '')[:3000]}"
    except Exception as e: return f"Scraping failed: {str(e)}"

@tool
def schedule_task(task_description: str, time_str: str, frequency: str) -> str:
    """Schedules a recurring task."""
    console.print(f"   📅 [Tool] Scheduling: '{task_description}' at {time_str} {frequency}")
    schedules = []
    if SCHEDULES_FILE.exists():
        with open(SCHEDULES_FILE, "r") as f:
            try: schedules = json.load(f)
            except: schedules = []

    new_task = {"id": str(len(schedules) + 1), "description": task_description, "time": time_str, "frequency": frequency}
    schedules.append(new_task)
    with open(SCHEDULES_FILE, "w") as f: json.dump(schedules, f, indent=4)
    
    global reload_schedules_flag
    reload_schedules_flag = True
    return f"Successfully scheduled '{task_description}' for {time_str} {frequency}."

@tool
def remove_task(task_description_keyword: str) -> str:
    """Removes a scheduled task."""
    console.print(f"   🗑️  [Tool] Removing task: '{task_description_keyword}'")
    if not SCHEDULES_FILE.exists(): return "No tasks found."
    
    with open(SCHEDULES_FILE, "r") as f:
        try: schedules = json.load(f)
        except: return "Error reading file."

    keyword = task_description_keyword.lower()
    original_count = len(schedules)
    schedules = [t for t in schedules if keyword not in t['description'].lower()]
    
    with open(SCHEDULES_FILE, "w") as f: json.dump(schedules, f, indent=4)
    global reload_schedules_flag
    reload_schedules_flag = True
    return f"Removed {original_count - len(schedules)} task(s)."

@tool
def save_memory(fact: str) -> str:
    """Save an important fact about the user or the agent to long-term memory."""
    console.print(f"   🧠 [Tool] Saving to long-term memory: '{fact}'")
    memory = load_long_term_memory()
    
    if any(fact.lower() in existing_fact.lower() for existing_fact in memory):
        return "That fact is already saved in memory."
        
    memory.append(fact)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)
    return "Memory saved successfully. I will remember this forever."

# ==========================================
# BACKGROUND SCHEDULER
# ==========================================
def execute_scheduled_task(task_description, model_name, base_url):
    console.print(f"\n{'='*20} ⏰ SCHEDULED TASK TRIGGERED {'='*20}")
    console.print(f"🧠 Executing: {task_description}")
    
    llm = ChatOllama(model=model_name, base_url=base_url, temperature=0.3)
    tools = [search_internet, scrape_website]
    agent = create_react_agent(llm, tools)
    
    try:
        response = agent.invoke({"messages": [("user", task_description)]})
        final_summary = response["messages"][-1].content
        console.print(f"\n🤖 RESULT:\n{final_summary}\n")
        with open(BASE_DIR / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w", encoding="utf-8") as f:
            f.write(final_summary)
    except Exception as e:
        console.print(f"❌ Error: {e}")
    console.print(f"{'='*60}\n")

def background_scheduler(model_name, base_url):
    global reload_schedules_flag
    while True:
        if reload_schedules_flag:
            schedule.clear()
            if SCHEDULES_FILE.exists():
                with open(SCHEDULES_FILE, "r") as f:
                    try:
                        schedules = json.load(f)
                        for task in schedules:
                            if task['frequency'] in ['daily', 'every day', 'day']:
                                schedule.every().day.at(task['time']).do(
                                    execute_scheduled_task, 
                                    task_description=task['description'],
                                    model_name=model_name,
                                    base_url=base_url
                                )
                    except: pass
            reload_schedules_flag = False
        schedule.run_pending()
        time.sleep(10)

# ==========================================
# MAIN AGENT LOOP
# ==========================================
def run_agent(config: dict):
    """Main agent loop that handles the interactive chat."""
    model_name = config["model_info"]["name"]
    base_url = config["model_info"]["base_url"]
    
    # Start Background Scheduler
    threading.Thread(target=background_scheduler, args=(model_name, base_url), daemon=True).start()
    
    # Load Memories & History
    long_term_memories = load_long_term_memory()
    chat_history = load_short_term_history()
    
    # Format long-term memory into the System Prompt
    memory_block = "\n".join([f"- {fact}" for fact in long_term_memories]) if long_term_memories else "No important facts saved yet."
    
    system_prompt = f"""You are a highly intelligent, autonomous AI research assistant.
    
    YOUR LONG-TERM MEMORY (Things you MUST always remember):
    {memory_block}
    
    If the user tells you their name, preferences, or gives you a permanent rule, use the 'save_memory' tool immediately.
    """

    # Initialize Agent
    llm = ChatOllama(model=model_name, base_url=base_url, temperature=0)
    tools = [search_internet, scrape_website, schedule_task, remove_task, save_memory]
    agent = create_react_agent(llm, tools)
    
    console.print("[bold green]✅ Agent is ready. Type 'quit' to exit.[/bold green]\n")

    # Interactive Chat Loop
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("\n[bold yellow]👋 Goodbye! Memories and history have been saved.[/bold yellow]")
                break
            if not user_input: continue
            
            console.print("\n[bold cyan]🧠 Thinking...[/bold cyan]")
            
            messages = [SystemMessage(content=system_prompt)] + chat_history + [HumanMessage(content=user_input)]
            response = agent.invoke({"messages": messages})
            
            final_ai_message = response["messages"][-1].content
            
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=final_ai_message))
            save_short_term_history(chat_history)
            
            console.print(f"\n[bold green]🤖 Agent:[/bold green]\n{final_ai_message}\n")
            
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]👋 Goodbye![/bold yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]❌ Error: {str(e)}[/bold red]\n")