# SnakeAgent

AI agent that plays the Google Snake game autonomously, aiming to maximize the score within 2 minutes.

Made by: [Cristian Motta](https://github.com/cmottao), [Esteban Barrera](https://github.com/tebanspam11)

---

## Overview

SnakeAIAgent is an autonomous AI system designed to play the Google Snake game. The agent continuously computes safe paths to the apple while avoiding collisions, using BFS and A* pathfinding algorithms combined with a tail-following strategy for survival.

The AI is capable of real-time gameplay, detecting the apple via screen capture and pixel color analysis, and executing moves automatically with consistent timing.

SnakeAIAgent also includes a simulation module that allows users to run multiple games in a controlled environment, generating performance statistics such as average score, survival time, and percentage of games reaching the time limit.

This project demonstrates a combination of pathfinding algorithms, real-time control, and simulation-based evaluation, making it an advanced example of AI applied to classic games.

---

## How to Use

1. **Install dependencies**

```
pip install -r requirements.txt
```

2. **Adjust board and game settings in `config.py`**


1. **Run the AI in real-time**

```
python main.py
```

- You have **3 seconds** to switch to the Google Snake game window.
- The AI will start playing automatically.
