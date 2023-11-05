from actor_critic import ActorCritic
import torch

def test_actor_output_shape():
    input_dim = 10
    output_dim = 3
    actor_critic = ActorCritic(input_dim, output_dim)
    state = torch.tensor([1.0] * input_dim)
    policy, value = actor_critic.forward(state)

    assert len(policy) == output_dim
    assert len(value) == 1

def test_policy_output_sum_is_1():
    input_dim = 10
    output_dim = 3
    actor_critic = ActorCritic(input_dim, output_dim)
    state = torch.tensor([1.0] * input_dim)
    policy,_ = actor_critic.forward(state)

    assert sum(policy) == 1


test_actor_output_shape()