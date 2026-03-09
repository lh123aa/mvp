# 需求挖掘与最小商业闭环系统 (Demand Miner)

## 中文介绍

> 陌生领域需求痛点挖掘与最小商业闭环落地全适配系统

### 项目简介

基于认知层级适配的智能需求挖掘系统，帮助用户完成从"陌生领域探索"到"最小商业闭环落地"的全流程。

### 核心特性

- **认知层级适配**: 根据用户认知程度匹配不同服务模式
- **刚性约束优先**: 用户预算、周期、目标始终置顶
- **单问题递进**: 一次仅抛出一个问题，避免信息过载
- **自我迭代**: 每次对话自动记录、复盘、优化

### 目录结构

```
demand-miner/
├── skill.yaml              # Skill 定义配置
├── skill_entry.py          # Skill 标准接口
├── README.md               # 项目文档
├── interact.py             # 主交互入口
├── modules/                # 核心模块
│   ├── pre_alignment.py    # 前置对齐模块
│   ├── stranger_mode.py    # 陌生模式（落地顾问）
│   ├── basic_mode.py       # 基础模式（引导教练/落地顾问）
│   └── senior_mode.py      # 资深模式（深度共创）
├── utils/                  # 工具函数
│   ├── state_manager.py    # 状态管理
│   └── constraint_filter.py # 约束过滤
├── data/                   # 数据存储
│   ├── sessions/           # 对话记录
│   ├── reviews/            # 复盘小结
│   └── stats/              # 统计报告
└── docs/                   # 文档
    └── 迭代日志.md
```

### 使用方法

1. 启动系统: `python interact.py`
2. 系统将引导您完成4个前置对齐问题
3. 根据您的认知层级匹配相应服务模式
4. 获得贴合约束条件的商业闭环方案

### 触发关键词

- 产品分析
- 项目分析
- 商业分析
- 商业闭环
- 需求挖掘
- 商业模式
- 创业分析
- 副业规划

---

## English Introduction

> Demand Pain Point Mining and Minimum Business Loop Landing Full Adaptation System for Unfamiliar Domains

### Project Overview

An intelligent demand mining system based on cognitive level adaptation, helping users complete the entire process from "unfamiliar domain exploration" to "minimum business loop landing".

### Core Features

- **Cognitive Level Adaptation**: Match different service modes according to user's cognitive level
- **Rigid Constraint Priority**: User budget, timeline, and objectives always take precedence
- **Single Question Progression**: Only one question at a time, avoiding information overload
- **Self Iteration**: Automatic recording, review, and optimization after each conversation

### Directory Structure

```
demand-miner/
├── skill.yaml              # Skill definition configuration
├── skill_entry.py          # Skill standard interface
├── README.md               # Project documentation
├── interact.py             # Main interaction entry point
├── modules/                # Core modules
│   ├── pre_alignment.py    # Pre-alignment module
│   ├── stranger_mode.py    # Stranger mode (implementation advisor)
│   ├── basic_mode.py       # Basic mode (guidance coach/implementation advisor)
│   └── senior_mode.py      # Senior mode (deep collaboration)
├── utils/                  # Utility functions
│   ├── state_manager.py    # State management
│   └── constraint_filter.py # Constraint filtering
├── data/                   # Data storage
│   ├── sessions/           # Conversation records
│   ├── reviews/            # Review summaries
│   └── stats/              # Statistical reports
└── docs/                   # Documentation
    └── 迭代日志.md
```

### Usage

1. Start system: `python interact.py`
2. The system will guide you through 4 pre-alignment questions
3. Match appropriate service mode based on your cognitive level
4. Obtain a business loop solution that fits your constraints

### Trigger Keywords

- Product Analysis
- Project Analysis
- Business Analysis
- Business Loop
- Demand Mining
- Business Model
- Startup Analysis
- Side Business Planning

## Version History

- v0.1.0 (2026-03-09): MVP Initial Release

## Developers

- Author: Sisyphus Agent
- Created on: 2026-03-09