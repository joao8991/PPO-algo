import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from actor_critic import ActorCritic

class PPO:
    def __init__(self, input_dim, output_dim, clip_epsilon=0.2, value_coeff=0.5, entropy_coeff=0.01):
        self.actor_critic = ActorCritic(input_dim, output_dim)
        self.optimizer = optim.Adam(self.actor_critic.parameters(), lr=0.001)
        self.clip_epsilon = clip_epsilon
        self.value_coeff = value_coeff
        self.entropy_coeff = entropy_coeff

    def get_action(self, state):
        state = torch.tensor(state, dtype=torch.float32)
        policy, value = self.actor_critic.forward(state)
        action_probs = policy.detach().numpy()
        action = np.random.choice(len(action_probs), p=action_probs)
        return action, action_probs[action], value

    def update(self, states, actions, old_probs, advantages, returns):
        states =  torch.tensor(states, dtype=torch.float32)
        actions = actions.clone().detach()
        old_probs = old_probs.clone().detach()
        advantages = advantages.clone().detach()
        returns = returns.clone().detach()

        policy, values = self.actor_critic(states)
        action_masks = nn.functional.one_hot(actions, num_classes=policy.size(-1))

        new_probs = torch.sum(policy * action_masks, dim=1)
        ratio = new_probs / old_probs
        surrogate_obj1 = ratio * advantages
        surrogate_obj2 = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
        policy_loss = -torch.min(surrogate_obj1, surrogate_obj2).mean()

        value_loss = nn.functional.smooth_l1_loss(values, returns)

        entropy = torch.sum(policy * torch.log(policy), dim=1).mean()

        policy_loss_value = policy_loss.item()
        value_loss_value = value_loss.item()
        entropy_loss_value = -self.entropy_coeff * entropy.item()

        total_loss = policy_loss + self.value_coeff * value_loss - self.entropy_coeff * entropy

        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

        return policy_loss_value, value_loss_value
