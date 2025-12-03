# B-Recon 🔍  
Auto Recon Toolkit + AI Chat Assistant

B-Recon started as a simple Python recon script (`cli.py`) and grew into a more serious tool:

- A **classic CLI recon** pipeline (no AI, just Python + external tools).
- A **web-based AI chat** that sits on top of the recon engine and explains results like a “security GPT”.

The flow is simple:  
You give it a domain → it runs recon (subdomains, ports, tech stack, screenshots, reports) → the AI helps you understand what you got.

---

## 🔧 What B-Recon Can Do

### 1. Classic CLI Recon (`cli.py` - without AI)

This is the original part of the project.

From the terminal you can:

- Run a **full recon pipeline** on a domain.
- Enumerate **subdomains** and **deep subdomains**.
- Pull **CT logs** (certificate transparency).
- Detect **technologies** used by the target.
- Run a **port scan** and save results as JSON.
- Scrape **emails** from interesting endpoints.
- Take **screenshots** of discovered assets.
- Generate reports:
  - Technical markdown report → `report.md`
  - Executive / human summary → `executive_summary.txt`
  - HTML report → `report.html`

Results are saved under:

```text
autorecon-results/<domain>/

for example:

autorecon-results/tesla.com/

2. B-Recon AI Chat (FastAPI + Ollama)

On top of the recon engine there is a web chat UI with an AI assistant:

    Modern chat-style interface (bubbles, avatars, typing indicator).

    Connects to a local LLM via Ollama (for example llama3.2:1b).

    Understands natural language commands like:

        Do a full recon on tesla.com

        Scan subdomains of paypal.com

        What does an open 3389 port mean?

    Decides when to:

        Actually run a scan, or

        Just answer your question from knowledge.

    Reads recon output (JSON + text) and gives you a human explanation.

During long scans, the chat shows a live progress panel, for example:

    Step 1/8: Subdomains scan started

    Step 1/8: Subdomains scan finished

    Step 2/8: Deep subdomains scan started

    ...

    FULL recon pipeline completed successfully

After a full scan, B-Recon can:

    Summarize:

        Key subdomains

        Open ports & services

        Technologies and stack

        Emails (if found)

        Interesting notes / potential risk areas

    Offer download links (via the API) for:

        Technical report (report.md)

        Human summary (executive_summary.txt)

🗂 Project Structure (high level)

Rough layout (names may be slightly different on your machine):

.
├── autorecon/
│   ├── cli.py               # Original CLI recon entrypoint (no AI)
│   ├── ...                  # Subdomain / ports / screenshots / reports helpers
├── ai_agent.py              # Logic for calling the LLM (Ollama) + summarizing results
├── api/
│   ├── ask_ai.py            # FastAPI app: /ai, /chat, /progress, /download...
├── templates/
│   ├── chat.html            # B-Recon web chat UI (HTML + inline JS/CSS)
├── autorecon-results/       # Scan output (subdomains, ports, reports, screenshots, etc.)
├── requirements.txt
├── commands.txt
└── README.md

📦 Requirements (short version)

    Full list is in requirements.txt, this is just the idea.

System:

    Linux environment (developed and tested on Kali).

    Python 3.11+ recommended.

    Typical recon tools installed, for example:

        nmap

        ffuf

        curl, wget

    For technologies / screenshots you may need a headless browser setup
    (e.g. Playwright / Chromium), depending on how you configure it.

Python (core libraries):

    fastapi, uvicorn

    pydantic

    requests

    tqdm

    ollama

    jinja2 (for templates, if used)

LLM / Ollama:

    Ollama

    running locally.

    A model pulled, for example:

ollama pull llama3.2:1b

Make sure the model name inside ai_agent.py matches what you actually pulled.
🚀 Getting Started
1. Clone & Setup

git clone <your-repo-url> b-recon
cd b-recon

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

Install the external tools you need, for example (Debian / Kali):

sudo apt update
sudo apt install -y nmap ffuf

Start Ollama and pull the model:

ollama serve        # if needed
ollama pull llama3.2:1b

🖥️ Using the Classic CLI (cli.py)

Run from inside the repo (with the virtualenv activated).

Full recon example:

python autorecon/cli.py full tesla.com

This will:

    Enumerate subdomains

    Deep-scan subdomains

    Pull CT logs

    Detect technologies

    Scrape emails

    Run a port scan

    Take screenshots (if enabled)

    Generate reports

Result folder example:

autorecon-results/tesla.com/
  ├── subdomains...
  ├── deep_subdomains_found.txt
  ├── ports.json
  ├── technologies.json
  ├── emails_found.txt
  ├── screenshots/
  ├── report.md
  ├── executive_summary.txt
  └── report.html

Depending on how cli.py is implemented, you might also have commands like:

# Only subdomains
python autorecon/cli.py subdomains tesla.com

# Only port scan
python autorecon/cli.py ports tesla.com

# Only screenshots
python autorecon/cli.py screenshots tesla.com

# Help
python autorecon/cli.py -h

💬 Using the B-Recon AI Chat

    Run the FastAPI app

uvicorn api.ask_ai:app --host 0.0.0.0 --port 8000 --reload

    Open the chat UI in your browser

http://127.0.0.1:8000/chat/

You’ll see:

    Chat bubbles (You / B-Recon).

    Status indicator (“API: online”).

    Small hints with example prompts.

    Example prompts

Inside the chat, try:

    Do a full recon on tesla.com

    Scan subdomains of paypal.com

    What does an open 3389 port mean?

    Explain the last scan on tesla.com

If B-Recon decides this is a long scan, it will:

    Kick off the recon pipeline for that domain.

    Show a scrolling “progress bubble” (using /progress?domain=...).

    When done, read the JSON/text results and answer in plain language.

📥 Downloading Reports from the Chat

After a full recon, B-Recon can offer download links (for example):

    Technical report (report.md)

    Human summary (executive_summary.txt)

These are usually exposed as endpoints like:

/download/report?domain=tesla.com
/download/summary?domain=tesla.com

Opening these URLs in your browser will download the files to your machine.
🧠 How It’s Wired (High-Level)

    autorecon/cli.py
    Orchestrates the classic recon steps:

        scan_subdomains

        scan_deep_subdomains

        scan_ct_logs

        detect_technologies

        email_scraper

        run_port_scan

        screenshot_all

        generate_report, generate_human_summary, generate_html_report

    ai_agent.py

        Talks to Ollama (LLM).

        Detects intent from natural language.

        On scan-related questions:

            Triggers the recon flow (via CLI / internal calls).

            Reads the output files.

            Builds a human-readable summary.

    api/ask_ai.py

        FastAPI app exposing:

            /ai?question=... – main AI endpoint.

            /chat/ – serves the web UI.

            /progress?domain=... – used by the front-end to show live progress.

            /download/... – endpoints for reports.

    templates/chat.html

        The HTML/JS/CSS for the chat interface.

        Handles:

            Sending messages to /ai

            Rendering messages as chat bubbles

            Polling /progress during scans

            Auto-scrolling, typing indicator, etc.

⚠️ Disclaimer

This is a personal / learning project, not a fully hardened production scanner.

You are responsible for how you use it.

Only run recon on:

    Domains you own, or

    Domains where you have clear permission to test.

Random scanning on the internet can get you blocked, shouted at, or worse.
