# Contributing to LEO Core

We ❤️ contributions! Whether you’re fixing a typo or adding a new AI scoring agent — every PR helps.

---

## 🧩 Setup
```bash
git clone https://github.com/Yesh48/LEOlabs.git
cd LEOlabs/leo-core
pip install -r requirements.txt
pytest -q
🌱 Development Guidelines
Follow PEP8 and use clear docstrings

Keep agents modular — each should have a run(state) method

Use print() for debug logs; proper logging coming soon

Submit PRs with clear commit messages:

feat: add keyword density analyzer

fix: handle missing meta tags

🧪 Testing
pytest -q
💬 Community
Discussions and roadmap on:
👉 https://github.com/Yesh48/LEOlabs/discussions
