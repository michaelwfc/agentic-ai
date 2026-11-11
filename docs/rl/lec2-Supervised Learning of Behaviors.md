# Lecture 2 — Supervised Learning of Behaviors

CS 185/285 · UC Berkeley · Instructor: Sergey Levine · 39 pages

## 1. Executive Summary

This lecture introduces Imitation Learning, focusing on a fundamental algorithm called Behavioral Cloning (BC) and its limitations.

The central idea is:

> Instead of explicitly programming an agent how to perform a task, we let it learn by observing demonstrations from an expert.

For example, rather than manually programming all the rules required to drive a car, we collect driving demonstrations from a human and train a neural network to predict the human's actions.

However, there is a critical problem: Behavioral Cloning can perform well on training data but fail when deployed in the real environment.

The reason is distributional shift: the agent encounters states that are different from those in its training demonstrations. Its mistakes can push it into increasingly unfamiliar states, causing further mistakes.

The lecture explains why this happens, provides a theoretical analysis of how errors accumulate, and introduces DAgger (Dataset Aggregation) as a solution.

## 2. From Supervised Learning to Imitation Learning

### 2.1 What is Imitation Learning?

Imitation Learning is a machine learning paradigm in which an agent learns a policy by observing demonstrations of an expert.

Consider autonomous driving:

[台灣發展自駕車機會在哪？專訪 ADAS 系統專家郭峻因教授 - INSIDE](https://images.openai.com/static-rsc-4/Y-fe6hIL-rtcWoGlNHQN1ocb5LeBxu8QJjlnHBFzhhPhYUZ_PcGLJZdHECTPpFfFRSXj3c8UAb70o4TctTrh23QO4NVQUndjyPbOYX16UphhK5FhN_k19itaHQBu8yO9kEChkVMoVlXVMRHnZJ5k3iVBELZgl-YmsFEvF8W3Sjw?purpose=inline)

[inside.com.tw](https://www.inside.com.tw/article/19125-taiwan-develops-self-driving-opportunities?utm_source=chatgpt.com)

A human driver observes the road and performs actions:

- Input: Camera image / environment observation.
- Output: Steering, acceleration, braking.
- Objective: Learn to reproduce the human driver's behavior.

We can formulate this as learning a policy:

\[ a_t = \pi_\theta(s_t) \]

Where:

| Symbol            | Meaning                                                        |
| ----------------- | -------------------------------------------------------------- |
| \(s_t\)         | State or observation at time \(t\)                           |
| \(a_t\)         | Action taken at time \(t\)                                   |
| \(\pi_\theta\) | Policy parameterized by neural network parameters \(\theta\) |

The goal is to learn a policy that behaves similarly to the expert.

### 2.2 Connection to Maximum Likelihood Estimation

The lecture establishes a connection between imitation learning and supervised learning.

Suppose we have expert demonstrations:

\[ D = {(s_i,a_i)}_{i=1}^{N} \]

We train a model to predict the expert's action given an observed state.

This is maximum likelihood estimation (MLE):

\[ \theta^* = \arg\max_\theta \sum_{i=1}^{N} \log \pi_\theta(a_i|s_i) \]

Equivalently, minimize negative log-likelihood:

\[ \mathcal{L}(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \log \pi_\theta(a_i|s_i) \]

This approach is called Behavioral Cloning (BC).

The key insight:

Behavioral Cloning transforms a sequential decision-making problem into a supervised learning problem.

## 3. Behavioral Cloning Algorithm

The lecture presents a straightforward three-step process.

[Xue Bin (Jason) Peng](https://images.openai.com/static-rsc-4/CrkA-Lf77fpK8fK5r_twBFnkEyB3OICyYeVHKBunCdYkNHoWuXOvfWMrSVQBUgvDaNcZxPz456I9IN7fT_ovBEZnJs87gIzOEzMn9mndnr0YP1oD6ssbu6qQ2TXmHaX2RqrWxa7PNMiLXhfBCtlObLCdTHPeTYR4jSLdlrkrsvg?purpose=inline)

[xbpeng.github.io](https://xbpeng.github.io/teaching/cmpt_729/?utm_source=chatgpt.com)

### Step 1: Collect expert demonstrations

Ask a human expert to perform the task and record the observations and actions.

A demonstration trajectory is:

\[ \tau = (s_0,a_0,s_1,a_1,\ldots,s_T,a_T) \]

For example:

| Observation                  | Expert action     |
| ---------------------------- | ----------------- |
| Car approaching a curve      | Turn left         |
| Car approaching intersection | Brake             |
| Road is straight             | Maintain steering |
| Obstacle ahead               | Turn right        |

### Step 2: Train a neural network

Use supervised learning to train a model on the demonstration dataset.

A typical architecture:

[Know Your Camera \[ICRA 2026\]](https://images.openai.com/static-rsc-4/PqhDpubKJpdFMlEV2Kjxs6edlEL9KfP-REN7VdDcETc29I6Z6KorWl7DStcCLO_fkq5HckhlfEJ-_AeXg1_wY2M2206s60S9_VlLIf5SHArCCS2UtaZWUMyRqRfCmBiKFqy70uJmK3e31gj7JF7Yq_hEEkZvoEfhcXxge03ZavU?purpose=inline)

[ripl.github.io](https://ripl.github.io/know_your_camera/?utm_source=chatgpt.com)

- Encoder: extracts features from observations.
- Policy network: predicts action distribution parameters.
- Output: action prediction or action distribution.

The lecture mentions ViT and ResNet as examples of encoders.

### Step 3: Execute the learned policy

Deploy the trained policy in the environment.

The model receives observations and predicts actions.

### 3.1 Discrete vs. Continuous Actions

The lecture distinguishes two types of action spaces.

| Property         | Discrete actions              | Continuous actions      |
| ---------------- | ----------------------------- | ----------------------- |
| Action space     | Finite choices                | Continuous values       |
| Examples         | LLM tokens, Atari key presses | Steering, acceleration  |
| Network output   | Logits                        | Distribution parameters |
| Typical modeling | Categorical distribution      | Gaussian distribution   |

For discrete actions:

\[ \pi_\theta(a|s)= \operatorname{Softmax}(f_\theta(s)) \]

For continuous actions, a common example is a Gaussian policy:

\[ \pi_\theta(a|s) = \mathcal{N}(\mu_\theta(s),\sigma_\theta^2(s)) \]

The network predicts the distribution parameters, from which an action can be sampled.

## 4. Does Behavioral Cloning Work?

Key problem of the lecture

The lecture gives two contrasting examples:

- Behavioral Cloning can fail.
- Behavioral Cloning can also work very well.

It references two autonomous driving examples:

1. ALVINN (1989): Autonomous Land Vehicle In a Neural Network.
2. NVIDIA's autonomous driving research (Bojarski et al., 2016).

[PPT - Advanced Topics in Robotics CS493/790 (X) PowerPoint Presentation - ID:245258](https://images.openai.com/static-rsc-4/XpBorpgpXa2DKf405_pShmZRp9lo5PEaiknzA9MpCPn_OecPJ3ixrJEpJR_YG_q1GcwQ3XBp2jwSu5mkp-Jbkf-4n4ohvF-GGCoF8u50-ChjGGt9OEj1Z3zLLbObuWBLyucIvSe8uwcAv2lPJHiIiUpC7vWfyYTkI3qoJe63z3E?purpose=inline)

[NVidia - AI platform for autonomous driving - Speaker Deck](https://images.openai.com/static-rsc-4/6ACsIg3Zt6Q9urEi7XCg7XbfZ9_sbExjHnUBy49lpHHrzp2fY3NdcXeHGkR9TTVLKEcyWjccUTkkvO4pXZzbG8zbWbL4C_-u3h0w55ItG1_PFAowRiuKLKqzPLjQBAk6SHOQryNg5BpT38Wg2cHyy8Vye4EvyO-AsRB94tBoCAE?purpose=inline)

[GitHub - apolanco3225/Clone-Driving-Behavior-SDC-Nanodegree: Deploy of NVIDIA's convnet architecture to clone driving behaviour in a game based environment created by Udacity. The model was trained to output a steering angle to an autonomous vehicle in order to drive on a virtual tracks. · GitHub](https://images.openai.com/static-rsc-4/ySiwqFiRYjYgj66YNkdUD1eRaLFT00_ywd7h9iTRJ6knMD595tekBrdga9dEY9k3cYA3CtEEKJtXVpO0822KRfzB9MNZk07Oa4StDja3r4Dj1T21uwJIFX6cYWXn5D7drhLIqHZQMup4O2GcX0QjRb_6lNiXxHzfy9IynLgWcVg?purpose=inline)

8

Why does the same general approach sometimes succeed and sometimes fail?

The answer is distributional shift.

### 4.1 The i.i.d. Assumption

Traditional supervised learning generally assumes training and test samples are independently and identically distributed (i.i.d.).

In simplified form:

\[ s_{\text{train}} \sim D \]

\[ s_{\text{test}} \sim D \]

The model is expected to generalize to new samples drawn from the same distribution.

But imitation learning has a special characteristic:

The model's actions influence which states it encounters next.

This means the model influences its own future input distribution.

### 4.2 Distributional Shift

Consider a self-driving car.

1. During training, the expert drives primarily in the center of the lane.
2. The learned policy makes a small steering mistake.
3. The car moves slightly toward the edge of the lane.
4. This creates an unfamiliar observation.
5. The model makes another mistake.
6. The car moves further away from the intended trajectory.

[Robot Learning Part 1: Background & Current State of the Field – Foundation Models & Robotics](https://images.openai.com/static-rsc-4/W8bc_X-2ovCyzmM-Sn0wgZ35N8himSVrGy7jJHMiUCBUJvKG5zQ7Z4BpppsdsUsw2HbM_S7ZMxmE8TXVKbO9Pgzj9_r015Gw7OnOz7DvB-SpVMlhQlJWSp5BN5CbFmlLyhIl4Vs0XxU5895RC_am4cXFhb32N4OixTQwj-XgUVA?purpose=inline)

[layernorm.dev](https://layernorm.dev/posts/robotics/1-background/?utm_source=chatgpt.com)

This creates a feedback loop:

\[ \text{Prediction Error} \rightarrow \text{State Deviation} \rightarrow \text{Distribution Shift} \rightarrow \text{More Prediction Errors} \]

This is fundamentally different from ordinary supervised learning.

## 5. Theoretical Analysis: How Bad Can It Be?

The lecture introduces theoretical analysis to understand how prediction errors accumulate over time.

### 5.1 Basic Error Model

Assume:

- The trajectory has length \(T\).
- The probability of making a mistake at each timestep is \(\epsilon\).
- Each mistake incurs a cost of 1.

The expected total number of mistakes is:

\[ \mathbb{E}[C] = \sum_{t=1}^{T} P(\text{mistake at time }t) \]

If the probability of making a mistake is constant and independent of the state:

\[ \mathbb{E}[C] = T\epsilon \]

However, this assumption is unrealistic for imitation learning because previous actions influence future states.

### 5.2 Compounding Errors

The more general analysis considers how mistakes affect subsequent states.

The important result presented in the lecture is:

\[ \boxed{O(T^2\epsilon)} \]

Under the lecture's worst-case analysis, the total cost can grow quadratically with the trajectory horizon.

Here:

- \(T\): trajectory length (horizon).
- \(\epsilon\): probability of making a mistake on the training distribution.

Compare the two cases:

| Learning scenario                                           | Expected error growth                            |
| ----------------------------------------------------------- | ------------------------------------------------ |
| Standard supervised learning, under fixed test distribution | \(O(T\epsilon)\) for T independent predictions |
| Behavioral cloning, worst-case sequential setting           | \(O(T^2\epsilon)\)                             |

Why quadratic?

A mistake at an early timestep can affect many subsequent timesteps.

For example:

- Mistake at timestep 1 can affect approximately \(T\) future steps.
- Mistake at timestep 2 can affect approximately \(T-1\) future steps.
- Mistake at timestep 3 can affect approximately \(T-2\) future steps.

The cumulative effect can be proportional to:

\[ \epsilon(T+(T-1)+\cdots+1) \]

\[ = \epsilon\frac{T(T+1)}{2} = O(T^2\epsilon) \]

This is the central theoretical warning of the lecture.

Note: This is a worst-case bound, not a prediction that every practical imitation-learning system will exhibit quadratic error growth.

### 5.3 Why Is This Analysis Pessimistic?

The lecture points out an important distinction:

In reality, agents can sometimes recover from mistakes.

For example:

- A car drifts slightly toward the edge.
- The driver corrects the steering.
- The vehicle returns to the center of the lane.

However, there is a paradox:

> Imitation learning can work better if the demonstrations contain more mistakes and recoveries.

Why?

Because the training data then contains examples of states outside the ideal expert trajectory, including recovery behavior.

The model learns not only how to behave correctly but also how to recover from deviations.

This is an important insight for demonstration collection.

## 6. How Can We Fix Distributional Shift?

The lecture introduces several approaches:

1. Change the algorithm: DAgger.
2. Use more powerful models with fewer mistakes.
3. Improve data collection and augmentation.
4. Use multi-task learning.

The main algorithm discussed is DAgger.

### 6.1 DAgger — Dataset Aggregation

Main algorithmic solution

DAgger was introduced by Ross et al. (2011).

Its central idea:

Instead of training only on expert demonstrations collected before deployment, collect additional training data from states encountered by the learned policy.

[3: An overview of DAGGER from \[Bagnell, 2015\]. In each iteration,... | Download Scientific Diagram](https://images.openai.com/static-rsc-4/5dfXh6rTR4mE9HQclyFwM--XUWFP8uW9hge1ncdbDvmT5aEk7vyzWb3czpBwMVB38r1lsgLGl9cqZIaLFiRKOTgct7_S-Zqm5Ex1l08-PSMgplthGnt6plklTGV5_K_uNtkfejx-hlKEPHgzrchoyiCe-JszDWWUTk_nrlUzMv4?purpose=inline)

[researchgate.net](https://www.researchgate.net/figure/An-overview-of-DAGGER-from-Bagnell-2015-In-each-iteration-DAGGER-generates-new_fig5_324035135?utm_source=chatgpt.com)

### Behavioral Cloning vs. DAgger

| Aspect               | Behavioral Cloning             | DAgger                              |
| -------------------- | ------------------------------ | ----------------------------------- |
| Initial data         | Expert demonstrations          | Expert demonstrations               |
| Training states      | Primarily expert states        | Expert and learner-visited states   |
| Data collection      | Usually one initial collection | Iterative                           |
| Labels               | Expert actions                 | Expert labels on encountered states |
| Distributional shift | Not explicitly addressed       | Explicitly addressed                |

### 6.2 DAgger Algorithm

The basic process:

Step 1 — Initialize dataset

Collect expert demonstrations:

\[ D_0 = {(s,a^*)} \]

Where \(a^*\) represents the expert's action.

Step 2 — Train the policy

Train a policy using the current dataset:

\[ \pi_1 = \operatorname{Train}(D_0) \]

Step 3 — Execute the learned policy

Allow the learned policy to interact with the environment and collect the states it visits.

\[ s_t \sim d_{\pi_1} \]

Here, \(d_{\pi_1}\) is the state distribution induced by policy \(\pi_1\).

Step 4 — Ask the expert to label those states

For every collected state, query the expert for the correct action:

\[ a_t^* = \pi^*(s_t) \]

Step 5 — Aggregate the dataset

Add the newly labeled examples:

\[ D_1 = D_0 \cup {(s_t,a_t^*)} \]

Step 6 — Retrain

Train the next policy:

\[ \pi_2 = \operatorname{Train}(D_1) \]

Repeat the process.

### 6.3 Why Does DAgger Work?

The key difference is the training distribution.

Behavioral Cloning:

\[ s \sim d_{\pi^*} \]

DAgger:

\[ s \sim d_{\pi} \]

Where:

- \(d_{\pi^*}\): State distribution generated by the expert.
- \(d_\pi\): State distribution generated by the learned policy.

The learned policy is trained on states it actually encounters, rather than exclusively on states generated by the expert.

This directly addresses the distributional shift problem.

### 6.4 A Common DAgger Variant

The lecture also discusses a common variant and asks whether it still guarantees fixing distributional shift.

This is an important theoretical question.

The guarantee depends on how the learner and expert policies are mixed during data collection, whether the learner visits relevant states, and whether the expert can provide reliable labels for those states.

The lecture's extracted text does not contain enough detail about the variant's exact formulation to establish its guarantee.

## 7. Important Connections to Modern AI

Although this lecture uses autonomous driving as its main example, its ideas are highly relevant to modern AI systems.

### 7.1 Connection to LLM Fine-Tuning

Behavioral Cloning is closely related to supervised fine-tuning (SFT).

| Imitation Learning    | LLM Training                                |
| --------------------- | ------------------------------------------- |
| Expert demonstrations | Human-written instruction-response examples |
| State                 | Context / conversation history              |
| Action                | Next token                                  |
| Expert policy         | Demonstrator's behavior                     |
| Learned policy        | Fine-tuned LLM                              |
| Behavioral Cloning    | Supervised Fine-Tuning                      |

For example, an LLM is trained on demonstrations:

\[ P_\theta(y_t|x,y_{<t}) \]

It learns to predict the next token based on the previous context.

However, there is an important difference between ordinary SFT and sequential interactive imitation learning:

- During teacher-forced SFT, the model conditions on ground-truth previous tokens.
- During autoregressive generation, it conditions on its own previously generated tokens.

An early generation error can therefore produce contexts that were not represented in the training data.

This is closely related to exposure bias.

### 7.2 Connection to Reinforcement Learning

Imitation learning and reinforcement learning solve related problems but use different sources of supervision.

| Dimension       | Imitation Learning        | Reinforcement Learning            |
| --------------- | ------------------------- | --------------------------------- |
| Learning signal | Expert demonstrations     | Rewards                           |
| Objective       | Reproduce expert behavior | Maximize expected reward          |
| Expert required | Usually yes               | Not necessarily                   |
| Exploration     | Depends on algorithm      | Often essential                   |
| Main challenge  | Distributional shift      | Exploration and credit assignment |

An important conceptual distinction:

Imitation learning answers:

How can an agent learn to behave like an expert?

Reinforcement learning answers:

How can an agent learn behavior that maximizes a reward?

They can also be combined, for example by using demonstrations to initialize an RL policy.

### 7.3 Connection to Agentic AI

Consider an LLM agent that uses tools.

Training demonstrations may contain:

1. User asks a question.
2. Agent calls a search tool.
3. Tool returns information.
4. Agent summarizes the results.

But during deployment, the agent might:

- Select an incorrect tool.
- Receive an unexpected tool response.
- Generate malformed arguments.
- Enter a conversation state absent from training examples.

This resembles distributional shift in imitation learning.

A robust agent should therefore be trained and evaluated on realistic interaction trajectories, including failure and recovery states.

## 8. Key Takeaways

| # | Concept              | Key understanding                                                            |
| - | -------------------- | ---------------------------------------------------------------------------- |
| 1 | Imitation Learning   | Learn behavior from expert demonstrations                                    |
| 2 | Behavioral Cloning   | Convert imitation learning into supervised learning                          |
| 3 | MLE                  | Maximize the likelihood of expert actions                                    |
| 4 | Distributional Shift | Learned policy encounters states absent from training data                   |
| 5 | Compounding Errors   | Early mistakes can create additional future mistakes                         |
| 6 | Worst-case Analysis  | Error can grow as \(O(T^2\epsilon)\)                                       |
| 7 | DAgger               | Aggregate expert-labeled data from learner-visited states                    |
| 8 | Recovery Behavior    | Demonstrations should include recovery examples, not only ideal trajectories |

The most important lesson:

Behavioral Cloning is not simply supervised learning applied to sequential data. Because the learned policy controls its future observations, the training and deployment distributions can diverge.

DAgger addresses this by iteratively collecting and labeling data from the learner's own state distribution.

## 9. Further Reading and References

The following papers are explicitly referenced in the lecture.

| Paper                                                                                                 | Year | Contribution                                          |
| ----------------------------------------------------------------------------------------------------- | ---- | ----------------------------------------------------- |
| ALVINN                                                                                                | 1989 | Early neural-network-based autonomous driving         |
| Bojarski et al., End to End Learning for Self-Driving Cars                                            | 2016 | Learning steering directly from camera images         |
| Ross et al., A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning | 2011 | Theoretical analysis of imitation learning and DAgger |

Additional useful conceptual connections:

- Exposure Bias in autoregressive language models.
- Dataset Aggregation in sequential prediction.
- Covariate Shift in statistical learning.
- Offline RL vs. Online RL.
- Learning from Demonstrations (LfD).

## 10. Knowledge Check

These questions are intended to test whether you understand the underlying mechanisms rather than simply remember definitions.

Lecture 2 assessment

0/4 answered

1\. Why can Behavioral Cloning fail even when its training accuracy is very high?

A. The neural network cannot represent continuous actions

B. The learned policy changes the distribution of future states

C. Maximum likelihood estimation does not converge

D. The expert demonstrations are always noisy

2\. Why can a small prediction error at an early timestep become much more costly?

A. It increases the model parameter count

B. It changes future states and can cause additional errors

C. It makes the training dataset smaller

D. It changes the action space

3\. What is the fundamental difference between DAgger and ordinary Behavioral Cloning?

A. DAgger removes the expert

B. DAgger uses reinforcement learning instead of supervised learning

C. DAgger aggregates expert-labeled states visited by the learner

D. DAgger only uses larger neural networks

4\. What is the relationship between Behavioral Cloning and LLM SFT?

A. Both learn from expert input-output demonstrations using supervised objectives

B. Both require a reward model

C. Both require online reinforcement learning

D. They are unrelated learning paradigms

Submit answers

Suggested next learning step: Study the original DAgger paper by Ross et al. (2011), focusing on the theoretical connection between online learning, no-regret algorithms, and imitation learning. This will help bridge the gap between supervised learning and reinforcement learning.