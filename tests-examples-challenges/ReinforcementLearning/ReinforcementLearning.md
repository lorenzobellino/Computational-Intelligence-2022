# Reinforcement Learning

it is part of machine learning, where the agent learns from the environment by interacting with it. The agent is rewarded for the correct actions and punished for the wrong ones. The agent learns from the rewards and tries to maximize the rewards.

**book recomendation** --> reinforcement learning by Richard Sutton and Andrew Barto

the idea is to formalize the sequential decision making process.
the elements involved are:
- Environment
- States ($S$)
- Actions ($A$)
- Rewards ($R$)
the **goal** is to maximaze the sum of the rewards.

at each time step $t = 0,1,...,n$ the agent is in a state $S_t$ and can perform an action $A_t$.
the environment then transitions to a new state $S_{t+1}$ and gives a reward $R_{t+1}$ based on a reward function $f_{R}(S_{t},A_{t})$

At some point in time $T$ the game ends and i can use the **expected retun of rewards** to evaluate the agent's performance, in this case the agent will be more concerned about the long term rewards instead of the near future rewards.

if the game doesn't end in a finite amount of time i can use the **discounted return of rewards**, in this case the agent is more interested in the rewards in the near future than in the ones in the far future.

## Reward Hypotesis
all goals can be formalized as maximizing the expected return of rewards.
each actions may have long term consequences because reward could be dalayed: -> it may be better to sacrifice immediate reward in order to gain more long-term reward (refueling your car now will prevent you from running out of gas several ours later)

## State
there are 2 different tyoe of state:
- **environment state** $S_{t}^{E}$: the state of the environment at time $t$, it might not be fully observable and may contain irrelevant information
- **Agent state** $S_{t}^{A}$: the state of the agent at time $t$, it is fully observable and is used by the agent as its internal representation

## Markov state
the future is independent of the past given the present.
the history of a state could be embedded in the state itself, in this case the state is called **Markov state**.

## Agent and environment
at each time $t$ the agent perform an action $A_{t}$, recieves an observation $O_{t}$ and a scalar reward $R_{t}$.
the environment recieves an action $A_{t}$ and transitions to a new state $S_{t+1}$ emits an observation $O_{t+1}$ and gives a scalar reward $R_{t+1}$.

if a state is fully observable:
$$O_{t} = S_{t}^{A} = S_{t}^{E}$$
if it is not fully observable (playnig poker):
$$O_{t} = S_{t}^{A} \neq S_{t}^{E}$$


## Agent's policy
is the definition of the egent behavior -> a map from state to action.
it is described by the punction $\pi(S_{t})$ that return an action $A_{t}$ given the state $S_{t}$.
the policy can be :
- **deterministic**: $A_{t} = \pi(S_{t})$
- **stochastic**: $\pi(a|s) = P[A_{t} = a|S_{t} = s]$

the **state-value vunction** $v_{\pi}(s)$ is the expected return $E$ starting from state $S$ and following policy $\pi$ until the end

the **action-value function** $q_{\pi}(s,a)$ is the expected return $E$ starting from state $S$ and taking action $A$ and following policy $\pi$ until the end.
$q_{\pi}$ is named the **Q-function**
$E_{\pi}$ is named **Q-value**





