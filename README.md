# 需求挖掘与最小商业闭环系统 (Demand Miner)

> 陌生领域需求痛点挖掘与最小商业闭环落地全适配系统

## 项目简介

基于认知层级适配的智能需求挖掘系统，帮助用户完成从"陌生领域探索"到"最小商业闭环落地"的全流程。

## 核心特性

- **认知层级适配**: 根据用户认知程度匹配不同服务模式
- **刚性约束优先**: 用户预算、周期、目标始终置顶
- **单问题递进**: 一次仅抛出一个问题，避免信息过载
- **自我迭代**: 每次对话自动记录、复盘、优化

## 使用方式

### 作为独立应用启动
```bash
cd demand-miner
python interact.py
```

### 作为Skill使用
- **触发关键词**: "产品分析", "项目分析", "商业闭环", "需求挖掘", "商业模式", "创业分析", "副业规划"
- **调用方式**: 通过支持的AI助手或框架调用

## 目录结构

```
demand-miner/
├── skill.yaml              # Skill 定义配置
├── skill_entry.py          # Skill 入口点
├── README.md               # 项目说明
├── interact.py             # 交互入口
├── modules/                # 核心模块
│   ├── pre_alignment.py    # 前置对齐模块
│   ├── stranger_mode.py    # 陌生模式模块
│   ├── basic_mode.py       # 基础模式模块
│   ├── senior_mode.py      # 资深模式模块
│   ├── dialogue_recorder.py # 对话记录模块
│   ├── auto_reviewer.py    # 自动复盘模块
│   └── stats_generator.py  # 统计模块
├── utils/                  # 工具函数
│   ├── state_manager.py    # 状态管理
│   └── constraint_filter.py # 约束过滤
├── data/                   # 数据存储
│   ├── sessions/           # 对话记录
│   ├── reviews/           # 复盘小结
│   └── stats/             # 统计报告
├── docs/                   # 文档
│   └── 迭代日志.md
└── test_run.py             # 测试脚本
```

## 版本历史

- v0.1.0 (2026-03-09): MVP 初始版本

## 开发者

- 作者：Sisyphus Agent
- 创建日期：2026-03-09
