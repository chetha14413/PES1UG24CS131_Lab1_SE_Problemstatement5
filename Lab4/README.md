# Lab 4 — Balloon Pop

## Student Details

- **SRN:** PES1UG24CS131
- **Lab:** Lab 4 — Vibe Coding
- **Project:** Balloon Pop
- **Language:** Python
- **Library:** Pygame

---

## Project Overview

This project is a modular Balloon Pop game developed as part of Lab 4.

The original project contains a deliberate click-detection defect. The objective
of this lab is to inspect the existing implementation, reproduce the defect,
fix it, and extend the game with additional gameplay features using an LLM as a
coding assistant.

The project is kept modular and all game state is maintained in memory.

---

## Original Project

The project consists of the following main components:

```text
balloon-pop/
├── main.py
├── requirements.txt
└── game/
    ├── game_engine.py
    ├── balloon.py
    ├── click_detection.py
    └── renderer.py
