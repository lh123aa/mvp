# Demand Miner - Demand Mining & Minimum Viable Business Loop

> 🏭 **Demand Mining & Business Loop Analysis System**  
> Help users explore unfamiliar domains and achieve minimum viable business landing

## Overview

Demand Miner is an intelligent demand mining skill based on iFlow CLI. It helps users:
- Deeply analyze user pain points and unmet needs
- Design low-cost, quickly verifiable business loops
- Precisely target user groups
- Recommend optimal solutions based on constraints

## Quick Start

### Trigger

Enter any of these keywords in iFlow CLI:
```
Product Analysis, Project Analysis, Business Analysis, Business Loop
Demand Mining, Business Model, Entrepreneurship Analysis, Side Hustle Planning
```

### Workflow

1. **Trigger Skill**: Enter a keyword
2. **Pre-alignment**: Answer 4 questions to build user profile
3. **Select Mode**: Enter analysis mode based on knowledge level
4. **Get Solution**: Receive customized demand analysis & business loop plan

## Features

### 🎯 Pre-alignment System
Build precise user profile through 4 dimensions:
- Core Goal
- Core Purpose (Side Hustle/Startup/Learning/Transition)
- Knowledge Level (Novice/Intermediate/Expert)
- Budget & Timeline Constraints

### 🔄 Three Analysis Modes

| Mode | Target Audience | Approach |
|------|-----------------|----------|
| Implementation Advisor | Complete Novice | AI-led, complete solution output |
| Guide Coach | Some Foundation | Guided questioning, co-analysis |
| Deep Co-creation | Industry Expert | In-depth discussion, personalized needs |

### ⚡ Constraint Filtering
- Budget: Free / Under ¥5,000 / Under ¥20,000
- Timeline: 1 month / 3 months / 6 months

### 📊 Industry Data
Coverage of multiple industries:
- Cross-border E-commerce
- AI Services
- Short Video Commerce
- Online Education
- Private Domain E-commerce
- Local Life Services
- Health & Wellness
- New Media Operations
- Cross-border Services

## Project Structure

```
demand-miner/
├── SKILL.md              # Main skill document
├── skill.yaml            # Skill configuration
├── README.md             # This file
├── README_EN.md          # English version
├── skills/               # Skills package entry
│   └── __init__.py
├── scripts/              # Helper scripts
│   ├── __init__.py
│   ├── constraint_filter.py
│   └── data_loader.py
├── resources/            # Resource data
│   ├── industries.json
│   └── questions.json
├── data/                 # Data storage
│   ├── sessions/
│   ├── reviews/
│   └── stats/
└── docs/                 # Documentation
    ├── 迭代日志.md       # Changelog
    └── 开发文档.md       # Development docs
```

## Version

- **Current Version**: 1.0.0
- **Last Updated**: 2026-03-09

---

💡 **Tip**: Trigger the skill and complete pre-alignment for in-depth analysis.
