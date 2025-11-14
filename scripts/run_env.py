import gymnasium as gym
import custom_env

def main():
    env = gym.make("Team7-v0", render_mode="human")
    obs, info = env.reset()
    total = 0

    for _ in range(500):
        action = env.unwrapped.action_type.actions_indexes["IDLE"]
        obs, reward, terminated, truncated, info = env.step(action)
        total += reward
        if terminated or truncated:
            print(f"Episode finished. Total reward: {total:.2f}")
            break

    env.close()

if __name__ == "__main__":
    main()
