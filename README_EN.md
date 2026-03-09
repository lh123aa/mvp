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
Market Analysis, User Research, Competitor Analysis, Review
```

### Workflow

1. **Trigger Skill**: Enter a keyword
2. **Pre-alignment**: Answer 5 questions to build user profile
3. **Select Mode**: Enter analysis mode based on knowledge level
4. **Get Solution**: Receive customized demand analysis & business loop plan
5. **Review**: End conversation triggers review for system improvement

## Features

### 🎯 Pre-alignment System
Build precise user profile through 5 dimensions:
- Core Goal
- Core Purpose (Side Hustle/Startup/Learning/Transition)
- Knowledge Level (Novice/Intermediate/Expert)
- Budget & Timeline Constraints
- Team Size (1 person / 1-3 people / 5+ people)

### 🔄 Three Analysis Modes

| Mode | Target Audience | Approach |
|------|----------------|----------|
| Implementation Advisor | Complete Novice | AI-led, complete solution output |
| Guide Coach | Some Foundation | Guided questioning, co-analysis |
| Deep Co-creation | Industry Expert | In-depth discussion, personalized needs |

### ⚡ Constraint Filtering
- Budget: Free / Under ¥5,000 / Under ¥20,000
- Timeline: 1 month / 3 months / 6 months
- Team Size: 1 person / 1-3 people / 5+ people

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

### 🔁 Review & Iteration
- Auto review conversation flow
- System response quality assessment
- Issue discovery & improvement suggestions
- Auto record to iteration log

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
│   ├── data_loader.py
│   └── review.py
├── tests/                # Unit tests
│   ├── test_constraint_filter.py
│   └── test_data_loader.py
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

## Tech Stack

- **Framework**: iFlow CLI Skills
- **Language**: Python 3.x
- **Data Format**: JSON
- **Documentation**: Markdown

## Testing

```bash
# Test constraint filter
python tests/test_constraint_filter.py

# Test data loader
python tests/test_data_loader.py
```

## Version

- **Current Version**: 1.0.2
- **Last Updated**: 2026-03-10

---

💡 **Tip**: Trigger the skill and complete pre-alignment for in-depth analysis.