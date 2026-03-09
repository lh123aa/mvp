"""
Demand Miner Skill 标准入口
符合skill规范的入口文件
"""

from skill import handle_request, can_handle_query, get_skill_info
from typing import Dict, Any, Optional


def execute(user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Skill 执行函数
    :param user_input: 用户输入
    :param context: 上下文信息
    :return: 执行结果
    """
    return handle_request(user_input, context)


def can_handle(user_input: str) -> bool:
    """
    判断是否可以处理用户输入
    :param user_input: 用户输入
    :return: 是否可以处理
    """
    return can_handle_query(user_input)


def get_info() -> Dict[str, Any]:
    """
    获取Skill信息
    :return: Skill信息
    """
    return get_skill_info()


# 兼容旧版接口
def handle_skill_request(user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    处理skill请求（兼容接口）
    :param user_input: 用户输入
    :param context: 上下文
    :return: 响应结果
    """
    return execute(user_input, context)


if __name__ == "__main__":
    # 当直接运行此文件时，提供简单的测试
    import sys
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = execute(user_input)
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Demand Miner Skill - 标准入口")
        print("使用方法: python skill_entry.py [您的请求内容]")
        print("例如: python skill_entry.py 项目分析")