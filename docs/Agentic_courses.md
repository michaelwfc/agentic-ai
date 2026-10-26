# AI Courses

结合你的背景——已经有 NLP/GenAI 工程经验，也在关注 RAG、Agent、Tool Calling、MCP、模型微调，以及金融领域的 AI 应用——我建议你不要把学习路线局限在某一所大学的 Agent 课程上。

更值得投入的路线，是把大学课程的系统性、顶尖实验室的最新研究，以及工业界的工程实践结合起来。 尤其是 Agent 工程，真正的难点不仅是让模型调用工具，还包括任务规划、状态管理、持久化执行、上下文工程、评估、可靠性、安全性和成本控制。

你在微信上看到的 Stanford CS329Z、CS329A、CMU AI Agents 等课程都值得进一步核实和关注。不过，要区分三件事：正式开设的大学课程、公开的自学课程，以及个人对课程的中文整理。后者可以帮助理解，但不应替代原始课程官网、讲义和作业。

下面我按知名度、技术深度和对实际工程工作的价值，整理一份值得优先考虑的课程清单。

## 一、优先推荐的知名课程：大学课程与 Agent 专项

这张表优先列出与你的工程背景最匹配的课程。课程链接尽量使用官方来源，方便你直接查看讲义、视频和作业。

[Untitled](Untitled%203fc198c00c328035810bfa0b38d9bcdb.csv)

## 二、我更建议补充的课程：工业界、开源生态与专项训练

大学课程通常覆盖面广、理论体系强，但如果你想把知识迅速用于工作，以下课程和技术资料往往更直接。

[Untitled](Untitled%203fc198c00c32800091defed079c3f85c.csv)

官方入口：

[Welcome to the 🤗 AI Agents Course · Hugging Face](https://images.openai.com/static-rsc-4/jXPqVKQxd_TXl5cKu3i9zIm5Xa1p3uyRWoNOFyqyChkw0qV9FETW-JMkIF2E9d5-tGvBenpX3ghBhiLXePUHvXULVowBA-Aecr9it58vPlRK86A-8SuRZrdJ-gFbMdRWL4_WoacNzDZRlrI-AwP4iigjxgvY5jV6NJ2WMDpyEoE?purpose=inline)

Hugging Face Agents Course

[免费学习与实践](https://huggingface.co/learn/agents-course?utm_source=chatgpt.com)

[Claude Academy · Learn to work and build with Claude](https://images.openai.com/static-rsc-4/-CJ0PsaU9WDH7asNIkkL8KYi2QDBShcTP07VleMAvPWzxE7Tbx0N748HmDLzTjiSjcn5GlORlF3pWQjj9hHel6Y7yNvP8902OfpYDLhIvtf3-pTmlrlbZcnawB9Kwk9TuLRfJyiZZMF4FcGpKleCz9gAVO6oS91bhp7fRfmExj0?purpose=inline)

Anthropic 开发者课程

[Claude API、MCP、Skills 与 Subagents](https://academy.claude.com/collections/build-with-claude?utm_source=chatgpt.com)

[Building Effective Agents 技术文章](https://www.anthropic.com/engineering/building-effective-agents?utm_source=chatgpt.com)

[Evaluating AI Agents - DeepLearning.AI](https://images.openai.com/static-rsc-4/KpDNaWYfcGx54Kr5Yp3diJExz4XN91518NIAV3JI4heOKS7ZiqgdQ6QZyZ4Oi1eaJTM19ZrQ8RuzeRYhxQJ4ESeAp1zKtisegw-oTqAg2da8btthrh-FhWp28co6T7UFi6dCslTKkFirHtcHvu-zQQ6SThWaF76x5wfA58mbSZk?purpose=inline)

Agent 评估

[Evaluating AI Agents](https://www.deeplearning.ai/courses/evaluating-ai-agents/?utm_source=chatgpt.com)

[Retrieval Augmented Generation (RAG) | Coursera](https://images.openai.com/static-rsc-4/QNJ22wvG-QRFELrMhtCniSzFWsKVE8O3h3htbgcKskyKkuKdyIwB7I3EtJLajgBBGOD4rk3SQ2A-QPF2aDImQSZREW80DSgD26v-8FVM38Ef14TJjJIk2YmkjTunwHCcVvEB0Zr0TdQp9JvzG3XATSsFW42KTUPPrqtxKJhbk-U?purpose=inline)

RAG 工程

[RAG 专项课程](https://www.deeplearning.ai/courses/retrieval-augmented-generation/?utm_source=chatgpt.com)

[#generativeai #googlecloud #devops | Gulnaz Khabibullina](https://images.openai.com/static-rsc-4/XXWpDO3p8zDLXRuY3nAdogFNkLfKWbeGxxsWZHa1hQpQ2sQh1jMgsi8TGI80Mw3bfsRb4cEqnNscvBtYLxFapcuOc8eQUgHSBk2fw7IE3Ry-qE_L4sYFPS9MqsoFTgIb_r2edhiaLv-YiR0diYXybbZ3Re-0JJBoDDJMzhXGslg?purpose=inline)

Google Cloud GenAI

[官方学习路径](https://cloud.google.com/learn/training/machinelearning-ai?utm_source=chatgpt.com)

## 三、怎么选择：按学习目标比较

如果不打算把所有课程都学完，我建议根据下面的目标筛选。

| 你的学习目标 | 优先学习 | 原因 |
| --- | --- | --- |
| 系统掌握 Agent 架构与工程设计 | Stanford CS329Z | 覆盖从组件到系统的完整设计与评估 |
| 理解 Agent 的推理、规划与自主能力 | CMU 11-768 + Stanford CS329A | 更深入地研究长期任务、Verifier、搜索与自我改进 |
| 快速提升 Agent 开发能力 | DeepLearning.AI Agentic AI + Hugging Face Agents Course | 短课程与代码实践结合，容易形成可运行的项目 |
| 提升生产环境的可靠性 | Evaluating AI Agents + Anthropic Building Effective Agents | 强调可观测性、评估、错误定位和架构复杂度控制 |
| 深入 RAG 与企业知识库 | DeepLearning.AI RAG + Stanford CS329Z | 同时覆盖检索技术和整体系统工程 |
| 学习 AI Coding 与代码库级 Agent | Stanford CS146S + Claude Academy | 聚焦 AI 辅助开发、工具使用和复杂任务执行 |
| 研究 Agent 训练、搜索和验证 | CMU 11-768 + UC Berkeley Advanced LLM Agents | 从工程实现进一步走向推理、后训练与程序验证 |

## 四、针对你的背景，我推荐的 8 周学习路线

你已经有 GenAI 工程经验，因此不需要从最基础的“什么是生成式 AI”开始。我建议以 Stanford CS329Z 为主线，结合短课程和动手项目，把学习成果沉淀成可以复用的工程能力。

## 01–02

第 1–2 周

Agent 架构与基本原理

学习：Stanford CS329Z、DeepLearning.AI Agentic AI、Anthropic Building Effective Agents。

实践：从一个简单的 LLM + Tool Calling 系统开始，分别实现固定 Workflow 和自主 Agent，比较两者的复杂度与成功率。

## 03–04

第 3–4 周

状态、记忆、工具和长任务

学习：CMU 11-768、Hugging Face Agents Course、Anthropic MCP 资料。

实践：使用 LangGraph 实现状态持久化、重试、人工审批、工具权限控制和任务恢复。

## 05–06

第 5–6 周

评估、可靠性和成本

学习：Evaluating AI Agents、DeepLearning.AI RAG。

实践：建立离线测试集，记录 Trace、工具调用成功率、任务完成率、答案正确性、延迟、Token 消耗和单任务成本。

## 07–08

第 7–8 周

构建一个完整的企业级 Agent

以金融研究、基金文档分析或合规规则助手为场景，整合 RAG、工具调用、工作流、审计日志、评估和人工审批。

最终产出：可运行的项目、架构图、评估报告、成本分析，以及失败案例分析。

这里最重要的一点是：不要只以“Agent 能否完成任务”作为学习成果，而要验证它在什么情况下会失败，以及失败能否被发现、解释和控制。 这也是从 Demo 走向企业级生产系统的关键。

对于金融领域的应用，我尤其建议将数据血缘、可复现性、审计日志、权限控制和人工审批纳入最终项目，而不是等到上线时才补。

