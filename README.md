BeatMind

BeatMind is an AI-powered music production mentor that guides producers section-by-section through the beat creation process. It combines a genre-aware knowledge base with a graph-based "ripple effect" engine, so when a producer changes one part of a track, BeatMind can intelligently suggest what else should update to keep the beat cohesive.

What it does
Guided, section-by-section workflow — walks producers through building a beat step by step instead of leaving them with a blank project
Ripple effect engine — uses graph data structures and BFS traversal (graph.py) to propagate the impact of a change (e.g. a new drum pattern) to related sections, so suggestions stay musically consistent
Session memory — tracks state and prior decisions across a session (session.py) so the AI's guidance builds on what's already been made, rather than treating each prompt in isolation
Genre-aware knowledge base — curated production knowledge (knowledge_base/) spanning House, Dubstep, Trap, Drill, and Brazilian Phonk, informed by 6 years of personal production experience
Claude API integration — powers the conversational mentorship layer on top of the structured production logic
Tech stack
Backend: Python, Flask
AI: Claude API
Frontend: HTML/CSS, JavaScript
Core logic: Graph algorithms (BFS traversal) for the ripple effect engine
Project structure
BeatMind/
├── app.py                  # Flask application entry point
├── beatmind/
│   ├── graph.py             # Ripple effect engine (graph + BFS)
│   ├── knowledge.py         # Genre knowledge base logic
│   └── session.py           # Session state / memory tracking
├── knowledge_base/          # Genre-specific production knowledge (txt)
├── static/                  # JS, CSS, logo
└── templates/               # HTML templates
Status

BeatMind is an active work in progress, built as a personal project to combine music production experience with software engineering and AI.

About

Built by Jad Alzoubi, a Software Engineering student at Arizona State University.
