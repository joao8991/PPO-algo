import torch
import torch.optim as optim
from PPO import PPO
from environment import SimpleEnvironment
import matplotlib.pyplot as plt



# Hyperparameters
input_dim = 2 + 2 + 2  # 2 for player position + 2 for apple positions
# input_dim = 4  # 2 for player position + 2 for apple positions
output_dim = 4  # 7 possible directions
clip_epsilon = 0.2
value_coeff = 0.5
entropy_coeff = 0.01
epochs = 1000  # Number of training epochs
episodes = 200  # Number of environment steps per epoch

# Create environment and PPO agent
env = SimpleEnvironment()
ppo_agent = PPO(input_dim, output_dim, clip_epsilon, value_coeff, entropy_coeff)
optimizer = optim.Adam(ppo_agent.actor_critic.parameters(), lr=0.00005)

# Training loop
epoch_rewards = []
for epoch in range(epochs):

    dones_amount = 0
    steps_to_done = 0
    distance_to_apple_list = []
    for _ in range(episodes):
        states = []
        actions = []
        old_probs = []
        rewards = []
        values = []
        dones = []

        
        state = env.get_state()
        steps = 30
        for _ in range(steps):  # Limit the number of steps per episode to avoid infinite loops
            states.append(state)
            action, prob, value = ppo_agent.get_action(state)
            actions.append(action)
            old_probs.append(prob)
            values.append(value)
            
            reward = env.move_player(action)
            rewards.append(reward)
            
            done = env.is_game_over()
            dones.append(done)
            
            state = env.get_state()
            steps_to_done+=1
            if done:
                break
        distance_to_apple = env.distance_to_apple()
        distance_to_apple_list.append(distance_to_apple)
        env.reset_state()
        
        # Compute advantages and update policy and value networks
        returns = torch.FloatTensor([sum(rewards)] * len(rewards))
        advantages = returns - torch.cat(values)
        
        optimizer.zero_grad()
        actor_loss, critic_loss = ppo_agent.update(states, torch.tensor(actions), 
                                                   torch.tensor(old_probs), advantages, returns)
        total_loss = actor_loss + critic_loss

        optimizer.step()

    # Print training statistics
    avg_reward = sum(rewards)/len(rewards)
    avg_distance_to_apple_list = sum(distance_to_apple_list)/len(distance_to_apple_list)
    avg_steps = steps_to_done/episodes
    epoch_rewards.append(avg_reward)

    print(f"Epc:{epoch + 1}, ActorLoss: {actor_loss:.4f}, CriticLoss: {critic_loss:.4f}, AvgReward: {avg_reward:.4f}, AvgSteps: {avg_steps:.3f} AvgDist: {avg_distance_to_apple_list:.3f}")

# After training, you can use the trained agent to play the game and make decisions

# Create a plot of episode rewards
plt.figure(figsize=(10, 6))
plt.plot(avg_distance_to_apple_list, linestyle='-', color='b', label='Episode Rewards')
# plt.axhline(y=average_reward, color='r', linestyle='--', label=f'Average Reward: {average_reward:.2f}')
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Average Rewards per Episode')
plt.legend()
plt.grid(True)
plt.show()