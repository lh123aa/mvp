"""
测试 data_loader 模块
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.data_loader import (
    load_industry_data,
    get_all_industries,
    search_industries,
    get_user_group_by_budget,
    get_pain_points_template
)


def test_get_all_industries():
    """测试获取所有行业"""
    industries = get_all_industries()
    
    assert isinstance(industries, list)
    assert len(industries) > 0
    
    # 检查必需的行业
    assert "跨境电商" in industries
    assert "AI服务" in industries
    
    print("✓ 获取所有行业测试通过")


def test_load_industry_data():
    """测试加载单个行业数据"""
    # 测试获取存在的行业
    data = load_industry_data("跨境电商")
    assert data is not None
    assert "用户群体" in data
    assert "轻量化方案" in data
    assert "常见痛点" in data
    assert "验证指标" in data
    
    # 测试获取不存在的行业
    data = load_industry_data("不存在的行业")
    assert data is None
    
    print("✓ 加载行业数据测试通过")


def test_search_industries():
    """测试搜索行业"""
    results = search_industries("电商")
    assert isinstance(results, list)
    assert len(results) > 0  # 跨境电商或私域电商
    
    # 不区分大小写搜索
    results = search_industries("ai")
    assert isinstance(results, list)
    
    results = search_industries("短视频")
    assert isinstance(results, list)
    
    print("✓ 搜索行业测试通过")


def test_get_user_group_by_budget():
    """测试根据预算获取用户群体"""
    # 0成本
    groups = get_user_group_by_budget("0成本")
    assert isinstance(groups, list)
    assert len(groups) > 0
    
    # 5000元内
    groups = get_user_group_by_budget("5000元内")
    assert isinstance(groups, list)
    
    # 其他
    groups = get_user_group_by_budget("20000元")
    assert isinstance(groups, list)
    
    print("✓ 获取用户群体测试通过")


def test_pain_points_template():
    """测试痛点模板"""
    template = get_pain_points_template()
    
    assert isinstance(template, list)
    assert len(template) > 0
    
    # 检查模板结构
    item = template[0]
    assert "核心方向" in item
    assert "表层痛点" in item
    assert "底层痛点" in item
    
    print("✓ 痛点模板测试通过")


def test_industry_structure():
    """测试行业数据结构"""
    industries = get_all_industries()
    
    required_fields = ["用户群体", "轻量化方案", "常见痛点", "验证指标"]
    
    for industry_name in industries:
        data = load_industry_data(industry_name)
        for field in required_fields:
            assert field in data, f"{industry_name} 缺少 {field} 字段"
    
    print("✓ 行业数据结构测试通过")


if __name__ == "__main__":
    test_get_all_industries()
    test_load_industry_data()
    test_search_industries()
    test_get_user_group_by_budget()
    test_pain_points_template()
    test_industry_structure()
    print("\n所有测试通过！")