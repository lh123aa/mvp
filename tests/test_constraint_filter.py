"""
测试 constraint_filter 模块
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.constraint_filter import (
    UserConstraints, 
    ConstraintFilter, 
    create_filter_from_session,
    get_filtered_schemes
)


def test_budget_filter():
    """测试预算约束过滤"""
    # 测试 5000元内过滤
    constraints = UserConstraints(budget_constraint="5000元内")
    filter_obj = ConstraintFilter(constraints)
    
    options = [
        {"名称": "方案A", "成本": 3000},
        {"名称": "方案B", "成本": 8000},
        {"名称": "方案C", "成本": 5000}
    ]
    
    result = filter_obj.filter_options(options)
    assert len(result) == 2
    assert result[0]["名称"] == "方案A"
    assert result[1]["名称"] == "方案C"
    print("✓ 预算过滤测试通过")


def test_period_filter():
    """测试周期约束过滤"""
    constraints = UserConstraints(period_constraint="3个月")
    filter_obj = ConstraintFilter(constraints)
    
    options = [
        {"名称": "方案A", "周期": 1},
        {"名称": "方案B", "周期": 3},
        {"名称": "方案C", "周期": 6}
    ]
    
    result = filter_obj.filter_options(options)
    assert len(result) == 2
    print("✓ 周期过滤测试通过")


def test_team_size_filter():
    """测试团队人数约束过滤"""
    constraints = UserConstraints(team_size_constraint="1人")
    filter_obj = ConstraintFilter(constraints)
    
    assert filter_obj.constraints.team_size_limit == 1
    
    # 测试解析
    constraints2 = UserConstraints(team_size_constraint="2-3人")
    filter_obj2 = ConstraintFilter(constraints2)
    assert filter_obj2.constraints.team_size_limit == 3
    
    constraints3 = UserConstraints(team_size_constraint="5人以内")
    filter_obj3 = ConstraintFilter(constraints3)
    assert filter_obj3.constraints.team_size_limit == 5
    
    print("✓ 团队人数解析测试通过")


def test_constraint_summary():
    """测试约束摘要"""
    constraints = UserConstraints(
        budget_constraint="5000元内",
        period_constraint="3个月",
        team_size_constraint="1人",
        core_target="副业试水"
    )
    filter_obj = ConstraintFilter(constraints)
    
    summary = filter_obj.get_constraint_summary()
    assert "预算: 5000元内" in summary
    assert "周期: 3个月" in summary
    assert "团队: 1人" in summary
    assert "目标: 副业试水" in summary
    print("✓ 约束摘要测试通过")


def test_create_filter_from_session():
    """测试从会话创建过滤器"""
    session = {
        "user_profile": {
            "预算约束": "5000元内",
            "周期约束": "3个月",
            "团队人数": "1人",
            "核心目标": "副业试水"
        }
    }
    
    filter_obj = create_filter_from_session(session)
    assert filter_obj.constraints.budget_limit == 5000
    assert filter_obj.constraints.period_limit == 3
    assert filter_obj.constraints.team_size_limit == 1
    print("✓ 会话创建过滤器测试通过")


def test_filtered_schemes():
    """测试方案过滤"""
    constraints = UserConstraints(budget_constraint="500元内", period_constraint="1个月")
    filter_obj = ConstraintFilter(constraints)
    
    schemes = get_filtered_schemes(filter_obj, "副业试水")
    assert isinstance(schemes, list)
    print("✓ 方案过滤测试通过")


if __name__ == "__main__":
    test_budget_filter()
    test_period_filter()
    test_team_size_filter()
    test_constraint_summary()
    test_create_filter_from_session()
    test_filtered_schemes()
    print("\n所有测试通过！")
