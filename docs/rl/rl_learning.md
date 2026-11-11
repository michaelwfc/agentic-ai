

This repository is for reinforment learning and implementation


# CS 285: Deep Reinforcement Learning, Spring 2026

- [CS 285: Deep Reinforcement Learning](http://rail.eecs.berkeley.edu/deeprlcourse/)
- [CS 285: Deep Reinforcement Learning, Spring 2026| Bilibili](https://www.bilibili.com/video/BV16S896YEpK/?spm_id_from=333.337.search-card.all.click&vd_source=b3d4057adb36b9b243dc8d7a6fc41295)
- [CS 285: Deep Reinforcement Learning, Spring 2026| Youtube](https://www.youtube.com/watch?v=DD8APgTEix4&list=PLKq1TCpsv3Y4)


## CS294-112 Deep Reinforcement Learning
- [CS294-112（2018秋季）伯克利大学深度强化学习课程 Deep Reinforcement Learning](https://www.bilibili.com/video/av45975902/?from=search&seid=870673246538758620&vd_source=b3d4057adb36b9b243dc8d7a6fc41295)
- [CS294-112（2018秋季）](https://rail.eecs.berkeley.edu/deeprlcourse-fa18/)


-----


# 强化学习（Reinforcement Learning）学习课程与资源精选

> **资料调研基准：2026 年 11 月 7 日**  
> **学习对象：** 具备机器学习、深度学习及 NLP/GenAI 工程经验的开发者  
> **学习目标：** 系统掌握传统强化学习、Deep RL、LLM RL 和 Agentic RL 的理论与工程实践。

## 一、学习方向与技术体系

当前强化学习有两个值得重点关注的方向：

1. **Traditional RL / Deep RL**
   - MDP、Dynamic Programming
   - Q-Learning、Policy Gradient
   - Actor-Critic、PPO、SAC
   - Offline RL、Model-Based RL

2. **RL for LLMs / Agentic RL**
   - RLHF、Reward Modeling
   - DPO、PPO、GRPO、RLOO
   - RLVR、Reasoning
   - Tool-use Agents、Multi-turn Agent Training

建议先建立传统 RL 的数学和算法基础，再深入 LLM RL。否则容易只会调用训练框架，而不能理解算法原理和训练稳定性。

---

## Self-learning Courses:

- [UCL Course on RL-AlphaGo项目负责人David Silver](https://www.davidsilver.uk/teaching/) 
- [强化学习的数学原理](https://www.bilibili.com/video/BV1sd4y167NS/?p=8&spm_id_from=pageDriver&vd_source=b3d4057adb36b9b243dc8d7a6fc41295)
  [Book-Mathmatical-Foundation-of-Reinforcement-Learning](https://github.com/MathFoundationRL/Book-Mathmatical-Foundation-of-Reinforcement-Learning)
- [Hugging Face-Deep Reinforcement Learning Course](https://huggingface.co/learn/deep-rl-course/unit0/introduction)
  [github-huggingface/deep-rl-class](https://github.com/huggingface/deep-rl-class)
- [Deep Mind-强化学习高阶课程 Deep Reinforcement Learning](https://www.bilibili.com/video/av45444509/?from=search&seid=4510347850534739671&vd_source=b3d4057adb36b9b243dc8d7a6fc41295)



## 二、大学顶尖课程（优先推荐）


  

  

| 课程 / 资源 | 来源 | 核心内容 | 时效性判断 | 权威性 | 视频资源 | Lab / 作业 / 项目 | 适合程度 | 综合建议 |
|---|---|---|---|---|---|---|---|---|
| **CS 285: Deep Reinforcement Learning, Spring 2026** | [UC Berkeley](https://rail.eecs.berkeley.edu/deeprlcourse/) | Deep RL、Imitation Learning、Policy Gradient、Actor-Critic、Q-Learning、Model-Based RL、Offline RL、Exploration、LLM RL | 2026 最新 | 极高，Sergey Levine | 有课程 Slides；公开视频需按具体学期核实 | HW1 Imitation Learning；HW2 Policy Gradients；HW3 Q-Learning / Actor-Critic；HW4 LLM RL；HW5 Offline RL；Final Project | 极高 | **首选。** 特别关注 2026 年的 LLM RL 作业和 Offline-to-Online RL 项目。  CS 294-112 (2015-2018年)-> CS 285 (2019年至今)|
| **CS224R: Deep Reinforcement Learning, Spring 2025** | [Stanford University](https://cs224r.stanford.edu/spring_2025/) | Deep RL、Imitation Learning、Policy Gradient、Actor-Critic、Offline RL、Model-Based RL、Reward Learning、Robotics、Language Modeling | 2025 较新 | 极高，Stanford | 有课程视频 | 4 次编程作业、PyTorch 实现、Final Project | 极高 | 适合有 ML 基础的开发者，偏深度学习和工程应用。 |
| **CS234: Reinforcement Learning, Winter 2026** | [Stanford University](https://web.stanford.edu/class/cs234/) | MDP、Dynamic Programming、Q-Learning、Policy Search、Offline RL、Imitation Learning、RLHF、Exploration、MCTS | 2026 最新 | 极高，Emma Brunskill | Lecture Materials、Slides 和视频资源 | Coding Assignments、Midterm、Final Project | 极高 | **最推荐的 RL 理论基础课。** |
| **6.7920: Reinforcement Learning: Foundations and Methods, Fall 2026** | [MIT](https://web.mit.edu/6.7920/www/) | Dynamic Programming、MDP、Bellman Equation、Value / Policy Iteration、Monte Carlo、TD、Q-Learning、Bandits、Approximate DP | 2026 最新 | 极高，MIT | 官方 Lecture Slides，视频公开情况需核实 | Homework、Problem Sets、Computational Exercises、Final Project | 高，偏数学理论 | 理论深度首选，适合深入理解 RL 数学原理、收敛性和优化理论。 |
| **10-703: Deep Reinforcement Learning and Control, Fall 2025** | [CMU](https://cmudeeprl.github.io/703website_f25/) | Deep RL、Imitation Learning、Robot Control、Sparse Reward、Curiosity、Policy Learning | 2025 较新 | 极高，Carnegie Mellon University | 官方课程材料，视频公开情况需核实 | 编程实验、算法实现、研究论文和项目 | 高 | 适合从 RL 进入 Robotics、Embodied AI 和控制领域。 |
| **QM 590: Reinforcement Learning and Large Language Models, Fall 2026** | [Purdue University](https://web.ics.purdue.edu/~sun244/qm590_fall2026.html) | Bandits、MDP、Policy Gradient、PPO、Transformers、RLHF、DPO、LLM Evaluation、RLVR、GRPO、Agentic RL | 2026 最新 | 高，Purdue University | 官方 Lecture Slides，视频待核实 | 课程演示和实践内容，后续作业以课程更新为准 | 极高 | **非常值得关注。** 直接将传统 RL 与 LLM 后训练、Reasoning 和 Agent 联系起来。 |

### 课程观察

2026 年的课程内容已经开始明显向 LLM RL 靠拢：

- Berkeley CS285 Spring 2026：设置独立的 LLM RL 作业。
- Stanford CS234 Winter 2026：将 RLHF 纳入课程。
- Purdue QM590 Fall 2026：将 GRPO、RLVR、Agentic RL 纳入教学计划。

学习 RL 已经没有必要将传统 RL 和 LLM RL 完全割裂开来。



---

## 三、在线课程与系统化视频资源

| 课程 / 资源 | 来源 | 核心内容 | 时效性判断 | 权威性 | 视频资源 | Lab / 作业 / 项目 | 适合程度 | 综合建议 |
|---|---|---|---|---|---|---|---|---|
| **Deep Reinforcement Learning Course** | [Hugging Face](https://huggingface.co/learn/deep-rl-course/en/unit0/introduction) | Q-Learning、DQN、Policy Gradient、Actor-Critic、深度 RL 算法及常用框架 | 理论基础仍有效，维护频率较低 | 高，HF 官方 | 有配套视频 | Google Colab、Stable-Baselines3、CleanRL、Sample Factory、AI 游戏挑战 | 极高 | **入门实践首选。** 免费、开源，理论和 Notebook 配套较好。注意官方已标注 Low-maintenance。 |
| **Reinforcement Learning Specialization** | [University of Alberta / Coursera](https://www.coursera.org/specializations/reinforcement-learning) | Fundamentals、Sample-based Learning、Prediction and Control、Function Approximation、Policy Gradient | 经典课程，技术基础依然有效 | 高 | 有系统视频 | Python 编程作业、RL 算法实现 | 高 | 适合从零系统学习 RL，有 ML 背景的人可能觉得节奏偏慢。 |
| **Reinforcement Learning from Human Feedback** | [DeepLearning.AI](https://www.deeplearning.ai/courses/reinforcement-learning-from-human-feedback) | Preference Dataset、Reward Modeling、RLHF Pipeline、LLM Fine-tuning | 经典 RLHF 实践，需结合新方法补充 | 高 | 有视频 | 6 Lessons、4 Code Examples、Llama 2 RLHF 微调实践 | 极高 | 快速理解 RLHF 完整工作流，但不是 2026 最新 RL 方法的完整教程。 |
| **Reinforcement Fine-Tuning LLMs with GRPO** | [DeepLearning.AI](https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-grpo) | GRPO、Reward Function、LLM-as-a-Judge、Reasoning、Reinforcement Fine-Tuning | 2026 技术方向相关 | 高 | 有视频 | 10 Lessons、7 Code Examples、Wordle RL 训练实验 | 极高 | **LLM RL 专项首选。** 快速理解 GRPO 和奖励设计。 |
| **David Silver: Reinforcement Learning Lectures** | [UCL](https://www.davidsilver.uk/teaching/) | MDP、Bellman Equation、Dynamic Programming、Monte Carlo、TD Learning、Q-Learning、Policy Gradient | 经典内容，基础理论不过时 | 极高 | 完整视频系列 | 课后习题和算法练习 | 极高 | **RL 理论入门的经典资源。** |
| **Spinning Up in Deep RL** | [OpenAI](https://spinningup.openai.com/en/latest/) | Policy Optimization、VPG、TRPO、PPO、DDPG、TD3、SAC、算法推导和实现 | 经典资源，部分实现和生态需更新 | 极高 | 理论讲解和配套材料 | PyTorch 实现、算法实验、代码阅读 | 高 | 深入理解 Policy Optimization 和 PPO 的优秀资源。 |

### 在线课程学习优先级

- 传统 RL：Hugging Face Deep RL + David Silver。
- 深度 RL：Stanford CS224R + OpenAI Spinning Up。
- LLM RL：DeepLearning.AI 的 RLHF + GRPO 两门短课。

---

## 四、LLM RL 工程框架与实践资源

这一部分是重点。

传统 RL 课程通常以 Atari、MuJoCo、机器人控制为实验环境，而 LLM RL 的训练对象是 Transformer，训练过程涉及：

- Policy Model：待优化的 LLM
- Reference Model：参考模型
- Reward Model / Verifiable Reward
- Value Model / Critic
- Rollout Generation
- Advantage Estimation
- Policy Optimization
- KL Regularization
- Distributed Training

| 课程 / 资源 | 来源 | 核心内容 | 时效性判断 | 权威性 | 视频资源 | Lab / 作业 / 项目 | 适合程度 | 综合建议 |
|---|---|---|---|---|---|---|---|---|
| **TRL (Transformers Reinforcement Learning)** | [Hugging Face](https://huggingface.co/docs/trl/en/index) | SFT、DPO、GRPO、PPO、RLOO、Reward Modeling、LLM Post-training | 持续更新 | 高，HF 官方 | 官方文档和教程为主 | Trainer、Example、完整模型训练实验 | 极高 | **首选工程框架。** 从 GRPOTrainer、RewardTrainer、DPOTrainer 入手。 |
| **OpenRLHF** | [GitHub](https://github.com/OpenRLHF/OpenRLHF) | PPO、GRPO、DPO、RM、Distributed RLHF、Ray、vLLM | 持续迭代，需关注版本 | 高，开源社区项目 | 文档和代码为主 | 分布式 RLHF、模型训练、Rollout、Reward Model | 极高 | 适合深入理解企业级 RLHF 训练系统和分布式架构。 |
| **verl (Volcano Engine RL)** | [GitHub](https://github.com/volcengine/verl) | PPO、GRPO、Agentic RL、分布式 Rollout、训练与推理解耦 | 前沿工程方向 | 高，开源框架 | 文档、技术分享为主 | 分布式 LLM RL、异步 Rollout、Agent 训练 | 极高 | 值得深入研究，尤其适合理解大模型强化学习的系统架构。 |
| **DeepSpeed-Chat** | [Microsoft GitHub](https://github.com/microsoft/DeepSpeedExamples/tree/master/applications/DeepSpeed-Chat) | RLHF 三阶段训练、SFT、Reward Model、PPO | 经典工程资料 | 高，Microsoft | 文档和代码 | 完整 RLHF Pipeline | 中高 | 适合理解 RLHF 历史工程架构，不建议作为唯一的新项目框架。 |
| **CleanRL** | [GitHub](https://github.com/vwxyzjn/cleanrl) | PPO、DQN、SAC 等算法的单文件实现 | 持续维护，基础算法成熟 | 高，开源研究社区 | 代码讲解为主 | 单文件 PyTorch 实现、实验复现 | 极高 | **理解算法实现的最佳补充。** 建议自己从头实现 PPO，再对照 CleanRL。 |
| **Gymnasium** | [Farama Foundation](https://gymnasium.farama.org/) | RL Environment、MDP、Environment API、Simulation | 持续维护 | 高，RL 开源生态基础设施 | 文档和示例 | 自定义环境、Agent 交互、Benchmark | 高 | 适合建立传统 RL 实验环境。 |
| **OpenAI Gym / MuJoCo Benchmarks** | [Gymnasium](https://gymnasium.farama.org/) | Continuous Control、Atari、Simulation、Benchmark | 经典实验生态 | 高 | 社区视频和论文 | DQN、PPO、SAC 等算法 Benchmark | 高 | 用于评估和比较 RL 算法，关注 Sample Efficiency 和稳定性。 |

### 重要概念：DPO、PPO、GRPO 的区别

DPO 不等同于传统意义上的在线强化学习。

| 方法 | 核心机制 | 是否需要在线环境交互 | 主要用途 |
|---|---|---|---|
| SFT | Supervised Learning | 否 | 模仿高质量示例 |
| DPO | Preference Optimization | 否，通常使用离线偏好数据 | 对齐人类偏好 |
| Reward Modeling | Preference-based Reward Learning | 否 | 学习奖励函数 |
| PPO | Policy Gradient + Clipped Objective | 通常需要在线采样 | RLHF、策略优化 |
| GRPO | Group-relative Advantage Estimation + Policy Optimization | 通常需要生成采样 | LLM Reasoning、RLVR |
| RLOO | Leave-One-Out Baseline + Policy Optimization | 通常需要生成采样 | LLM 后训练 |

建议把这些方法放在同一张技术知识图谱中学习，而不是简单视为互相替代的算法。

---

## 五、经典教材与论文资源

| 课程 / 资源 | 来源 | 核心内容 | 时效性判断 | 权威性 | 视频资源 | Lab / 作业 / 项目 | 适合程度 | 综合建议 |
|---|---|---|---|---|---|---|---|---|
| **Reinforcement Learning: An Introduction (2nd Edition)** | [Sutton & Barto](http://incompleteideas.net/book/the-book-2nd.html) | MDP、Dynamic Programming、Monte Carlo、TD、Q-Learning、Policy Gradient | 经典教材，长期有效 | 极高 | 无配套完整课程视频 | 书中算法和习题 | 极高 | **RL 必读教材。** 作为整个学习过程的理论参考书。 |
| **Algorithms for Reinforcement Learning** | [Csaba Szepesvári](https://sites.ualberta.ca/~szepesva/papers/RLAlgsInMDPs.pdf) | RL 算法、理论分析、MDP、函数近似 | 经典，偏理论 | 极高 | 无 | 数学推导、理论习题 | 高 | 深入研究算法理论和收敛性质。 |
| **Trust Region Policy Optimization (TRPO)** | [论文](https://arxiv.org/abs/1502.05477) | Trust Region、Policy Optimization、KL Constraint | 2015，经典基础 | 极高 | 可结合 Spinning Up 学习 | 算法复现 | 高 | 理解 PPO 的重要前置论文。 |
| **Proximal Policy Optimization Algorithms (PPO)** | [论文](https://arxiv.org/abs/1707.06347) | Clipped Surrogate Objective、Policy Gradient、Advantage | 2017，经典基础 | 极高 | Spinning Up 有相关讲解 | PyTorch PPO 实现 | 极高 | 传统 RL 和 RLHF 都非常重要的基础算法。 |
| **Deep Reinforcement Learning from Human Preferences** | [论文](https://arxiv.org/abs/1706.03741) | Human Preference、Reward Learning、Human Feedback | 2017，经典基础 | 极高 | 可结合 RLHF 课程 | Reward Model 实现 | 高 | 理解现代 RLHF 的重要理论起点。 |
| **Direct Preference Optimization: Your Language Model is Secretly a Reward Model** | [论文](https://arxiv.org/abs/2305.18290) | Preference Optimization、Implicit Reward Model、DPO Objective | 2023，经典方法 | 极高 | DeepLearning.AI 有相关课程 | DPO 微调实践 | 极高 | 必须理解它与 PPO-RLHF 的差异。 |
| **DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models** | [论文](https://arxiv.org/abs/2402.03300) | GRPO、数学推理、RL Training、Reward Design | 2024，重要基础 | 高 | 论文和技术分享 | GRPO 复现 | 极高 | 理解 GRPO 的重要论文。 |
| **DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning** | [论文](https://arxiv.org/abs/2501.12948) | RLVR、Reasoning、GRPO、Cold Start、Reward Design | 2025，重要技术参考 | 高 | 技术分享和论文解读 | Reasoning RL 复现 | 极高 | **LLM Reasoning RL 必读。** 重点理解可验证奖励与模型推理能力提升。 |

---

## 六、综合推荐：优先学习资源

| 优先级 | 资源 | 推荐理由 |
|---|---|---|
| P0 | Berkeley CS285 — Spring 2026 | Deep RL 系统课程，关注 LLM RL 和 Offline RL |
| P0 | Stanford CS234 — Winter 2026 | 补齐 MDP、Bellman、Q-Learning、Policy Gradient 等基础 |
| P0 | Stanford CS224R — Spring 2025 | 深入理解深度 RL 算法和工程应用 |
| P0 | DeepLearning.AI — GRPO | 快速进入 LLM Reinforcement Fine-Tuning |
| P0 | Hugging Face TRL + verl | 从算法原理进入真实 LLM 训练工程 |
| P1 | Sutton & Barto | 理论参考书，持续阅读 |
| P1 | MIT 6.7920 | 数学理论深化，选读 |
| P1 | DeepSeek-R1 / DeepSeekMath | 最新研究方法，持续阅读 |

---

## 七、12 周学习路线

考虑到已有 NLP、Transformer、PyTorch 和 GenAI 应用开发背景，不建议完全按照传统 RL 入门课程从头学起。

建议：

- 4 周掌握传统 RL 核心理论
- 4 周深入 Deep RL 和 PPO
- 4 周集中研究 LLM RL

每周建议投入 6–10 小时。

### Phase 1：RL Fundamentals（Week 1–4）

目标：建立数学和算法基础。

| 周次 | 学习内容 | 推荐资源 | 实践目标 |
|---|---|---|---|
| Week 1 | MDP、Return、Value Function | CS234、Sutton | 实现 GridWorld |
| Week 2 | Bellman Equation、DP | CS234、MIT 6.7920 | Value Iteration |
| Week 3 | Monte Carlo、TD、Q-Learning | David Silver | 实现 Q-Learning |
| Week 4 | Policy Gradient、REINFORCE | CS285 | 实现 REINFORCE |

### Phase 2：Deep RL（Week 5–8）

目标：深入策略优化和深度神经网络。

| 周次 | 学习内容 | 推荐资源 | 实践目标 |
|---|---|---|---|
| Week 5 | Actor-Critic、A2C | CS285 | 实现 Actor-Critic |
| Week 6 | PPO、TRPO、GAE | Spinning Up | 从零实现 PPO |
| Week 7 | SAC、DDPG、Continuous Control | CS285 | MuJoCo 实验 |
| Week 8 | Offline RL、Imitation Learning | CS285、CS224R | 实现 Behavioral Cloning |

### Phase 3：LLM Reinforcement Learning（Week 9–12）

目标：重点转向 GenAI 和 Agent 训练。

| 周次 | 学习内容 | 推荐资源 | 实践目标 |
|---|---|---|---|
| Week 9 | RLHF、Reward Model | DeepLearning.AI、PPO | 实现 Reward Model |
| Week 10 | DPO、PPO for LLM | DPO Paper、TRL | 微调小模型 |
| Week 11 | GRPO、RLVR | DeepSeekMath、DeepSeek-R1 | 实现 GRPO |
| Week 12 | Agentic RL、Tool-use RL | Berkeley CS285、verl | 训练一个工具调用 Agent |

---

## 八、建议完成的 4 个实战项目

强化学习特别依赖实验经验，尤其是 Reward Design、训练稳定性和采样效率。

| 项目 | 技术栈 | 主要目标 | 难度 |
|---|---|---|---|
| Project 1：GridWorld RL | Python、NumPy | 实现 Value Iteration、Policy Iteration、Q-Learning | 入门 |
| Project 2：PPO Agent | PyTorch、Gymnasium、CleanRL | 从零实现 PPO，训练 CartPole / LunarLander | 中级 |
| Project 3：LLM RLHF | Transformers、TRL、LoRA | 完成 SFT → Reward Model → PPO | 高级 |
| Project 4：LLM Reasoning with GRPO | Qwen、TRL、verl、vLLM | 使用可验证奖励训练数学或代码推理模型 | 高级 |

### Project 4：基于 GRPO 的 LLM Reasoning

建议选择 1B–3B 级别的开源模型，以数学计算或 Python 代码生成作为任务。

```text
Base Model
(Qwen 1.5B / 3B)
      |
      v
Rollout Generation
(针对同一个 Prompt 生成多个候选回答)
      |
      v
Reward Function
(答案正确性、代码执行结果、格式约束)
      |
      v
GRPO Optimization
(Group-relative Advantage,
 Policy Update, KL Regularization)
      |
      v
Trained Reasoning Model
(比较训练前后的准确率、泛化能力和训练稳定性)
```

该项目可以把以下技术串联起来：

- RL 理论
- Transformer
- Reward Engineering
- 模型微调
- 训练系统工程
- 模型评估

形成完整的技术闭环。

---

## 九、强化学习技术知识图谱

```text
Reinforcement Learning
|
+-- 1. RL Fundamentals
|   |
|   +-- MDP
|   +-- Bellman Equation
|   +-- Dynamic Programming
|   +-- Monte Carlo
|   +-- Temporal Difference
|   +-- Q-Learning
|
+-- 2. Deep RL
|   |
|   +-- Value-Based RL
|   |   +-- DQN
|   |   +-- Double DQN
|   |   +-- Dueling DQN
|   |
|   +-- Policy-Based RL
|       +-- REINFORCE
|       +-- Actor-Critic
|       +-- PPO
|       +-- SAC
|
+-- 3. RL for LLMs
|   |
|   +-- RLHF
|   +-- Reward Modeling
|   +-- PPO
|   +-- DPO
|   +-- GRPO
|   +-- RLOO
|
+-- 4. Advanced LLM RL
|   |
|   +-- Reasoning RL
|   |   +-- RLVR
|   |   +-- Math Reasoning
|   |   +-- Code Reasoning
|   |   +-- Verifiable Rewards
|   |
|   +-- Agentic RL
|       +-- Tool Use
|       +-- Multi-turn Interaction
|       +-- Environment Interaction
|
+-- 5. RL Systems Engineering
    |
    +-- Hugging Face TRL
    +-- verl
    +-- OpenRLHF
    +-- vLLM
    +-- Distributed Rollout
    +-- Evaluation
```

---

## 十、最终学习建议

建议采用下面这套组合，而不是同时学习十几门课程：

| 优先级 | 资源 | 用途 | 建议投入 |
|---|---|---|---|
| P0 | Stanford CS234 2026 | RL 数学和算法基础 | 2 周 |
| P0 | Berkeley CS285 2026 | Deep RL 核心课程 | 3 周 |
| P0 | Stanford CS224R 2025 | 深度 RL 工程实践 | 2 周 |
| P0 | DeepLearning.AI GRPO | LLM RL 快速入门 | 3–5 天 |
| P0 | TRL + verl | LLM RL 工程训练 | 2 周 |
| P1 | Sutton & Barto | 理论参考书 | 持续阅读 |
| P1 | MIT 6.7920 | 数学理论深化 | 选读 |
| P1 | DeepSeek-R1 / DeepSeekMath | 最新研究方法 | 持续阅读 |

### 核心建议

不要只关注 GRPO 和 DeepSeek-R1。

真正有价值的能力是理解从：

**MDP → Policy Gradient → Advantage Estimation → PPO → RLHF → GRPO → RLVR → Agentic RL**

整个技术演进过程。

面对新的 RL 算法时，应该能够从以下几个方面分析：

1. Objective Function：优化目标是什么？
2. Gradient Estimation：梯度如何估计？
3. Sampling Mechanism：训练数据如何采样？
4. Reward Design：奖励如何设计？
5. Training Stability：如何保证训练稳定？
6. Evaluation：如何验证模型确实获得了能力提升？

这样才能从使用 RL Trainer 的工程师，逐步成长为能够理解、实现、评估和改进 RL 算法的工程研究人员。

---

## 参考资源入口

- [Berkeley CS285](https://rail.eecs.berkeley.edu/deeprlcourse/)
- [Stanford CS234](https://web.stanford.edu/class/cs234/)
- [Stanford CS224R](https://cs224r.stanford.edu/spring_2025/)
- [MIT 6.7920](https://web.mit.edu/6.7920/www/)
- [Purdue QM590](https://web.ics.purdue.edu/~sun244/qm590_fall2026.html)
- [Hugging Face Deep RL Course](https://huggingface.co/learn/deep-rl-course/en/unit0/introduction)
- [Hugging Face TRL](https://huggingface.co/docs/trl/en/index)
- [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)
- [verl](https://github.com/volcengine/verl)
- [CleanRL](https://github.com/vwxyzjn/cleanrl)
- [Sutton & Barto](http://incompleteideas.net/book/the-book-2nd.html)
- [DeepSeek-R1 Paper](https://arxiv.org/abs/2501.12948)
- [DeepSeekMath Paper](https://arxiv.org/abs/2402.03300)


- deepmind.google/
- [深度强化学习综述](https://coladrill.github.io/2018/10/21/%E6%B7%B1%E5%BA%A6%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0%E7%BB%BC%E8%BF%B0/)


# Tools

- [gym](https://github.com/openai/gym)
- [PyBullet Quickstart Guide](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit?tab=t.0#heading=h.2ye70wns7io3)



# Textbooks

- [Reinforcement Learning: An Introduction, Sutton and Barto, 2nd Edition](http://incompleteideas.net/book/the-book-2nd.html)
  