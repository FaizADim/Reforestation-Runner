# Reforestation Runner

Reforestation Runner is a short, side-scrolling Pygame game about restoring a forest. Jump over wildfire and fallen-timber hazards, collect water drops, and plant as many trees as possible.
[!Watch the Demo](https://www.youtube.com/watch?v=GCg99wqyfy8)

## Gameplay

- **Jump:** Press `Space` to jump.
- **Restart:** Press `Space` after a collision to start a new run.
- **Collect water drops:** Each drop adds one tree to the background and the score.
- **Avoid hazards:** Contact with a fire or fallen log ends the run.
- **Build your record:** Your distance and speed increase as you run.

![800 x 400 Pygame window](https://img.shields.io/badge/window-800x400-34%2C139%2C34)

## Requirements

- Python 3.10 or newer
- Pygame CE

## Run locally

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pygame-ce
python main.py
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

To leave the virtual environment:

```bash
deactivate
```

## Controls

| Key | Action |
| --- | --- |
| `Space` | Jump |
| `Space` (game over) | Restart |
| Window close button | Quit |

## Project structure

```text
.
├── main.py
├── README.md
└── .venv/  # optional local virtual environment
```
