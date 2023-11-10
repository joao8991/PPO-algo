import torch
from PPO import PPO
from environment_running import RunningEnvironment
import matplotlib.pyplot as plt



# Hyperparameters
input_dim = 85  # 2 for player position + 2 for apple positions
# input_dim = 4  # 2 for player position + 2 for apple positions
output_dim = 16  # 7 possible directions
clip_epsilon = 0.2
value_coeff = 0.5
entropy_coeff = 0.01
epochs = 1000  # Number of training epochs
episodes = 200  # Number of environment steps per epoch

# Create environment and PPO agent
env = RunningEnvironment(28, 0, 0)
ppo_agent = PPO(input_dim, output_dim, clip_epsilon, value_coeff, entropy_coeff)

# Training loop
epoch_rewards = []
for epoch in range(epochs):

    steps_to_done = 0
    for _ in range(episodes):
        states = []
        actions = []
        old_probs = []
        rewards = []
        values = []
        dones = []
        end_fitnesses = []
        
        state,end_fitness = env.get_state()
        steps = 28*2
        for _ in range(steps):  # Limit the number of steps per episode to avoid infinite loops
            states.append(state)
            action, prob, value = ppo_agent.get_action(state)
            actions.append(action)
            old_probs.append(prob)
            values.append(value)
            
            reward = env.act(action)
            rewards.append(reward)
            
            done = env.is_game_over()
            
            state,end_fitness = env.get_state()

            if done:
                break
        
        end_fitnesses.append(end_fitness)

        # Compute advantages and update policy and value networks
        returns = torch.FloatTensor([sum(rewards)] * len(rewards))
        advantages = returns - torch.cat(values)
        
        actor_loss, critic_loss = ppo_agent.update(states, torch.tensor(actions), 
                                                   torch.tensor(old_probs), advantages, returns)
        total_loss = actor_loss + critic_loss


    # Print training statistics
    avg_reward = sum(rewards)/len(rewards)
    avg_end_fitnesses = sum(end_fitnesses)/len(end_fitnesses)
    avg_steps = steps_to_done/episodes
    epoch_rewards.append(avg_reward)

    print(f"Epc:{epoch + 1}, ActorLoss: {actor_loss:.4f}, CriticLoss: {critic_loss:.4f}, AvgReward: {avg_reward:.4f}, AvgEndFit: {avg_end_fitnesses:.4f}")
