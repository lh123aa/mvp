"""
Demand Miner Skill 入口点
用于响应关键词触发
"""
import sys
import os
from typing import Dict, Any, Optional

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interact import DemandMiner


class DemandMinerSkill:
    """Demand Miner Skill 接口类"""
    
    def __init__(self):
        self.skill_name = "demand-miner"
        self.description = "陌生领域需求痛点挖掘与最小商业闭环落地全适配系统"
        self.trigger_keywords = [
            "产品分析", "项目分析", "商业分析", "商业闭环", 
            "需求挖掘", "商业模式", "创业分析", "副业规划"
        ]
    
    def execute(self, user_input: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行skill
        :param user_input: 用户输入
        :param context: 上下文信息
        :return: 执行结果
        """
        try:
            # 返回可启动交互的标志
            return {
                "status": "success",
                "action": "start_interactive_session",
                "skill_name": self.skill_name,
                "user_input": user_input,
                "context": context or {}
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"启动失败: {str(e)}",
                "skill_name": self.skill_name
            }
    
    def can_handle(self, query: str) -> bool:
        """
        判断skill是否能处理查询
        :param query: 查询字符串
        :return: 是否能处理
        """
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in [
            "产品分析", "项目分析", "商业分析", "商业闭环", 
            "需求挖掘", "商业模式", "创业分析", "副业规划"
        ])
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取skill信息
        :return: skill信息
        """
        return {
            "name": self.skill_name,
            "description": self.description,
            "trigger_keywords": self.trigger_keywords,
            "version": "0.1.0"
        }


# 全局实例
skill_instance = DemandMinerSkill()


def handle_request(user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    处理请求的入口函数
    :param user_input: 用户输入
    :param context: 上下文
    :return: 响应结果
    """
    return skill_instance.execute(user_input, context)


def can_handle_query(query: str) -> bool:
    """
    判断是否能处理查询
    :param query: 查询字符串
    :return: 是否能处理
    """
    return skill_instance.can_handle(query)


def get_skill_info() -> Dict[str, Any]:
    """
    获取skill信息
    :return: skill信息
    """
    return skill_instance.get_info()


if __name__ == "__main__":
    # 当直接运行此文件时，启动交互式会话
    import json
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = handle_request(user_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 直接启动交互式会话
        dm = DemandMiner()
        dm.start()