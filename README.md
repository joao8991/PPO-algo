# PPO-algo

## ActorCritic

Here are defined the NN that will be used for Actor and Critic

**Actor** is responsible for:

- given a state of the environment return the probablities of executing an action

So to initialize the class, it receives:

- the input_dim(amount of state properties)
- the output_dim(amount of possible actions)

**Critic** is responsible for:

- given a state of the environment returns the how good is the situation we are in. For example in football, if you have a penalty shot, you are in a very good situation.

This NN will learn how good is a situation.
