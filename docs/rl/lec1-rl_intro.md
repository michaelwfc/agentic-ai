

# Bayesian Network

In Reinforcement Learning (RL), a Bayesian Network (Bayes Net) is a graphical model that represents a joint probability distribution over multiple random variables using a graph of conditional dependencies and independencies.


The core idea of a Bayesian Network: Probability distributions with conditional independences

Let's build the intuition from probability theory to RL applications.

## 1. What is a Bayesian Network?

A Bayesian Network (BN) is a directed acyclic graph (DAG) in which:

- Each node represents a random variable.
- Each directed edge represents a direct probabilistic dependency.
- Each node has a conditional probability distribution (CPD) given its parents.
- The joint probability distribution can be factorized into a product of these conditional distributions.

For example, consider three variables:


- \(A\): Weather

- \(B\): Whether you carry an umbrella
- \(C\): Whether the ground is wet

\(P(A|B) = \frac{P(B|A)P(A)}{P(B)}\)

\(P(A\mid B)=\frac{0.85(0.20)}{0.25}=0.68\)


\(P(A)\)

\(P(B\mid A)\)

\(P(B\mid \neg A)\)

\(P(B)\)= 0.25

\(P(B\cap A)\)= 0.17

\(P(B\cap \neg A)\)= 0.08


Give feedback

A simple Bayesian Network might look like this:  Bayesian Network: Weather and Umbrella

Weather (A)

Umbrella (B) | Wet Ground (C)

Weather influences both umbrella usage and whether the ground is wet.

The joint probability distribution is:

\[ P(A,B,C)=P(A)P(B|A)P(C|A) \]

Notice that instead of storing a large joint probability table, we decompose it into three smaller probability distributions.

This is the key advantage of Bayesian Networks.

## 2. What does conditional independence mean?

This is probably the most important concept to understand.

Two random variables \(B\) and \(C\) are conditionally independent given \(A\) if:

\[ P(B,C|A)=P(B|A)P(C|A) \]

We write:

\[ B \perp C \mid A \]

It means:

Once we know A, knowing B gives us no additional information about C.

Consider our weather example:

- A = Weather
- B = Umbrella usage
- C = Wet ground

Suppose we already know that it is raining.

Knowing whether someone carries an umbrella does not provide additional information about whether the ground is wet, assuming the weather fully explains both variables.

This is conditional independence.

There are two important distinctions:

| Concept                  | Meaning                              |
| ------------------------ | ------------------------------------ |
| Independence             | \(P(B,C)=P(B)P(C)\)                |
| Conditional independence | \(P(B,C\\|A)=P(B\\|A)P(C\\|A)\) |

Importantly, conditional independence does not necessarily mean unconditional independence.

## 3. Why do we need Bayesian Networks?

The main reason is to simplify complex joint probability distributions.

Suppose we have 5 binary random variables:

\[ X_1,X_2,X_3,X_4,X_5 \]

A full joint probability distribution requires:

\[ 2^5=32 \]

entries, or 31 independent parameters.

For \(n\) binary variables, the number of independent parameters is:

\[ 2^n-1 \]

This grows exponentially.

However, if the variables have conditional independence relationships, we can factorize the joint distribution:

\[ P(X_1,\ldots,X_n) = \prod_{i=1}^{n}P(X_i|Parents(X_i)) \]

This can dramatically reduce the number of parameters.

For example, consider a simple chain:

\[ X_1 \rightarrow X_2 \rightarrow X_3 \]

Its joint distribution becomes:

\[ P(X_1,X_2,X_3) = P(X_1)P(X_2|X_1)P(X_3|X_2) \]

Instead of modeling all possible combinations directly, we model local dependencies.

## 4. How are Bayesian Networks related to Reinforcement Learning?

This is where things become interesting.

Reinforcement Learning involves several random variables:

| Variable       | Meaning                |
| -------------- | ---------------------- |
| \(S_t\)      | State at time \(t\)  |
| \(A_t\)      | Action at time \(t\) |
| \(R_t\)      | Reward at time \(t\) |
| \(S\_{t+1}\) | Next state             |
| \(A\_{t+1}\) | Next action            |

A standard Markov Decision Process (MDP) can be represented using a probabilistic graphical model.

Dynamic Bayesian Network for an MDP

Sₜ | Aₜ |  Rₜ₊₁ | Sₜ₊₁

Conceptual dependency structure, with arrows:

Sₜ ──> Aₜ

Sₜ, Aₜ ──> Sₜ₊₁

Sₜ, Aₜ ──> Rₜ₊₁

The corresponding probability factorization is:

\[ \begin{aligned} &P(S_t,A_t,R_{t+1},S_{t+1})\\ &=P(S_t)P(A_t|S_t)\\ &\quad \cdot P(S_{t+1}|S_t,A_t)\\ &\quad \cdot P(R_{t+1}|S_t,A_t) \end{aligned} \]

This captures the basic structure of an MDP:

1. The agent observes the current state \(S_t\).
2. The policy selects an action \(A_t\).
3. The environment generates the next state \(S_{t+1}\).
4. The environment generates a reward \(R_{t+1}\).

The important conditional independence assumption is:

\[ S_{t+1}\perp \text{Past}\mid(S_t,A_t) \]

In other words:

Given the current state and action, the next state does not depend on the entire history of previous states and actions.

This is precisely the Markov property.

## 5. Bayesian Networks vs. Markov Decision Processes

These concepts are related, but they are not the same.

| Aspect                   | Bayesian Network                     | MDP                                    |
| ------------------------ | ------------------------------------ | -------------------------------------- |
| Primary purpose          | Represent probabilistic dependencies | Model sequential decision-making       |
| Structure                | Directed acyclic graph               | State-transition system                |
| Main components          | Random variables and CPDs            | States, actions, rewards, transitions  |
| Conditional independence | Central modeling principle           | Markov property                        |
| Decision-making          | Not inherently included              | Explicitly models actions and policies |
| Optimization             | Not inherently included              | Maximize expected cumulative reward    |

A useful distinction:

- A Bayesian Network describes how random variables depend on each other.
- An MDP describes how an agent makes decisions and interacts with a stochastic environment over time.
- A Dynamic Bayesian Network can represent the probabilistic structure of an MDP across multiple time steps.

## 6. What should you remember?

There are three fundamental ideas worth remembering:

| Concept                  | Key takeaway                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| Bayesian Network         | A DAG representing a joint probability distribution                                           |
| Conditional Independence | Knowing one variable provides no additional information about another, given a third variable |
| Markov Property          | The future depends on the current state and action, not the entire history                    |

One final mathematical relationship:

\[ \boxed{ P(X_1,\ldots,X_n)= \prod_i P(X_i|Parents(X_i)) } \]

This is the fundamental factorization rule of Bayesian Networks.

My recommendation for your RL learning path: Study these concepts in the following order:

1. Probability theory: joint, marginal and conditional probability.
2. Conditional independence and Bayes' theorem.
3. Bayesian Networks and DAG factorization.
4. Markov chains and the Markov property.
5. Markov Decision Processes (MDPs).
6. Partially Observable MDPs (POMDPs).

The last topic is particularly interesting: in a POMDP, the agent cannot directly observe the true state and must maintain a probability distribution (belief state) over possible states. This connects Bayesian inference directly to reinforcement learning.