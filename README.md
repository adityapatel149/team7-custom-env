# 🛣️ Team7 Custom Environment (`Team7-v0`)

This repository holds **Team 7’s custom reinforcement-learning environment**, built on top of [Highway-Env](https://highway-env.farama.org/) and [Gymnasium](https://gymnasium.farama.org/).  
The environment is packaged as `custom_env`, and the environment ID is `Team7-v0`.

Currently:
- Observation type: **Lidar**  
- Default road and vehicle setup from Highway-Env.  
- Ready for further extension (custom vehicles, objects, reward-shaping, etc).

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/adityapatel149/team7-custom-env.git
cd team7-custom-env
```

### 2. (Optional) Set up a virtual environment
**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the package

Install the environment and its dependencies directly using the project’s `pyproject.toml`:
```bash
pip install -e .
```
This makes the `custom_env` package importable.

---

## ▶️ Running the Example Script

There's a demo script available:
```bash
python scripts/run_env.py
```
This will:
- Create the `Team7-v0` environment (`render_mode="human"` by default or can use `"rgb_array"` for frame capture).  
- Run a few steps (IDLE actions) and render the environment.  
- Print out total reward when the episode ends.

Example usage:
```python
import gymnasium as gym
import custom_env

env = gym.make("Team7-v0", render_mode="human")
obs, info = env.reset()

done = False
while not done:
    action = env.unwrapped.action_type.actions_indexes["IDLE"]
    obs, reward, done, truncated, info = env.step(action)
    env.render()

env.close()
```

---

## 🧩 Project Structure

```
team7-custom-env/
│
├── custom_env/
│   ├── __init__.py
│   ├── register.py
│   └── envs/
│       ├── __init__.py
│       └── my_env.py          	# MyEnv class, extends Highway-Env with Lidar observations
│
├── scripts/
│   └── run_env.py             	# Demo/test script for executing the environment
│
├── requirements.txt           	# List of deps
├── pyproject.toml       		#  Package metadata for pip install
└── README.md                  # This file
```

---

## 🚀 Next Steps

- Extend `MyEnv` to include **ghost vehicles** .  
- Add **static or dynamic objects** on the road.  
- Add high density traffic with **random aggressive braking**.
- Modify reward / termination logic to suit custom tasks (e.g., following rules, avoiding collisions).  
- Integrate training scripts using frameworks such as [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) or RLlib for policy learning.

---

## 🧑‍💻 Authors

**Team 7 — CS271: Reinforcement Learning (San José State University)**
Aditya Patel
Karan Jain
Shareen Rodrigues  
Instructor: Genya Ishigaki

---

## 📜 License

This project is intended for academic/research use.  
The core functionality builds upon Highway-Env © [Farama Foundation](https://highway-env.farama.org/).
