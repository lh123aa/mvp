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
├── skill_entry.py          # Skill 标准入口
├── skill.py                # Skill 主要实现
├── README.md               # 项目文档
├── modules/                # 核心模块（可选）
│   └── ...
├── utils/                  # 工具函数（可选）
│   └── ...
├── data/                   # 数据存储（可选）
│   ├── sessions/           # 对话记录
│   ├── reviews/            # 复盘小结
│   └── stats/              # 统计报告
└── docs/                   # 文档
    └── 迭代日志.md
```

### 使用方法

1. **作为独立程序运行**: `python interact.py`
2. **作为Skill调用**: 通过`skill.py`中的`handle_request`函数
3. **命令行调用**: `python skill_entry.py "项目分析"`

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
├── skill.py                # Main skill implementation
├── README.md               # Project documentation
├── modules/                # Core modules (optional)
│   └── ...
├── utils/                  # Utility functions (optional)
│   └── ...
├── data/                   # Data storage (optional)
│   ├── sessions/           # Conversation records
│   ├── reviews/            # Review summaries
│   └── stats/              # Statistical reports
└── docs/                   # Documentation
    └── 迭代日志.md
```

### Usage

1. **Standalone Execution**: `python interact.py`
2. **As a Skill**: Call `handle_request` function from `skill.py`
3. **Command Line**: `python skill_entry.py "Project Analysis"`

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

- v1.0.0 (2026-03-09): Refactored to standard skill structure
- v0.1.0 (2026-03-08): MVP Initial Release

## Developers

- Author: Sisyphus Agent
- Created on: 2026-03-09