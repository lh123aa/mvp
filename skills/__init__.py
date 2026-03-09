"""
Demand Miner Skills 包
提供标准化的skills接口
"""

import os

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 辅助脚本
from scripts.constraint_filter import (
    ConstraintFilter,
    UserConstraints,
    get_constraint_params,
    get_constraint_guidance_text
)

from scripts.data_loader import (
    load_industry_data,
    get_all_industries,
    get_user_group_by_budget,
    get_pain_points_template
)


def get_skill_info():
    """获取skill信息"""
    return {
        "name": "demand-miner",
        "version": "1.0.0",
        "description": "需求挖掘与最小商业闭环分析",
        "main_file": "SKILL.md",
        "config": "skill.yaml",
        "scripts": "scripts/",
        "resources": "resources/",
        "data": "data/",
        "trigger_keywords": [
            "产品分析", "项目分析", "商业分析", "商业闭环",
            "需求挖掘", "商业模式", "创业分析", "副业规划"
        ]
    }


def get_skill_content():
    """获取SKILL.md内容"""
    skill_path = os.path.join(PROJECT_ROOT, "SKILL.md")
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


__all__ = [
    # 主文档
    "get_skill_info",
    "get_skill_content",
    # 约束过滤
    "ConstraintFilter",
    "UserConstraints",
    "get_constraint_params",
    "get_constraint_guidance_text",
    # 数据加载
    "load_industry_data",
    "get_all_industries",
    "get_user_group_by_budget",
    "get_pain_points_template"
]

# Skills 元信息
__skills__ = {
    "demand-miner": {
        "name": "demand-miner",
        "version": "1.0.0",
        "description": "需求挖掘与最小商业闭环分析",
        "main_file": "SKILL.md",
        "config": "skill.yaml",
        "scripts": "scripts/",
        "resources": "resources/",
        "data": "data/"
    }
}
