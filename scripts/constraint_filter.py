"""
约束过滤模块
根据用户的预算、周期、目标约束过滤选项
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class UserConstraints:
    """用户约束条件"""
    budget_constraint: str = ""      # 0成本/5000内/5000-20000/其他
    period_constraint: str = ""      # 1个月/3个月/6个月/其他
    core_target: str = ""      # 副业试水/创业立项/行业研究/职业转型
    
    # 解析后的数值
    budget_limit: Optional[int] = None   # 数值(元)
    period_limit: Optional[int] = None    # 数值(月)


class ConstraintFilter:
    """约束过滤器"""
    
    # 预算映射
    BUDGET_MAP = {
        "0成本": 0,
        "5000元内": 5000,
        "5000-20000元": 20000,
        "20000以上": 999999
    }
    
    # 周期映射
    PERIOD_MAP = {
        "1个月": 1,
        "3个月": 3,
        "6个月": 6,
        "6个月以上": 99
    }
    
    def __init__(self, constraints: UserConstraints):
        self.constraints = constraints
        self._parse_constraints()
    
    def _parse_constraints(self) -> None:
        """解析约束为数值"""
        budget = self.constraints.budget_constraint
        period = self.constraints.period_constraint
        
        for key, value in self.BUDGET_MAP.items():
            if key in budget:
                self.constraints.budget_limit = value
                break
        
        for key, value in self.PERIOD_MAP.items():
            if key in period:
                self.constraints.period_limit = value
                break
    
    def filter_options(self, options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤选项列表"""
        if not options:
            return []
        
        filtered = []
        for option in options:
            if self._is_option_valid(option):
                filtered.append(option)
        
        # 如果过滤后为空，返回原列表（避免用户无选项可选）
        return filtered if filtered else options
    
    def _is_option_valid(self, option: Dict[str, Any]) -> bool:
        """检查选项是否满足约束"""
        # 检查成本
        if "成本" in option and option["成本"] is not None:
            cost = option["成本"]
            if isinstance(cost, str):
                # 解析成本字符串
                if "0成本" in cost or cost == "0":
                    cost_value = 0
                elif "元" in cost:
                    try:
                        cost_value = int(cost.replace("元", "").replace(",", ""))
                    except:
                        cost_value = 999999
                else:
                    cost_value = 999999
            else:
                cost_value = cost
            
            if self.constraints.budget_limit is not None:
                if cost_value > self.constraints.budget_limit:
                    return False
        
        # 检查周期
        if "周期" in option and option["周期"] is not None:
            period = option["周期"]
            if isinstance(period, str):
                if "1个月" in period:
                    period_value = 1
                elif "3个月" in period:
                    period_value = 3
                elif "6个月" in period:
                    period_value = 6
                else:
                    period_value = 99
            else:
                period_value = period
            
            if self.constraints.period_limit is not None:
                if period_value > self.constraints.period_limit:
                    return False
        
        return True
    
    def get_constraint_summary(self) -> str:
        """获取约束摘要文本"""
        parts = []
        if self.constraints.budget_constraint:
            parts.append(f"预算: {self.constraints.budget_constraint}")
        if self.constraints.period_constraint:
            parts.append(f"周期: {self.constraints.period_constraint}")
        if self.constraints.core_target:
            parts.append(f"目标: {self.constraints.core_target}")
        return " | ".join(parts) if parts else "无明确约束"


def create_filter_from_session(session: Dict[str, Any]) -> ConstraintFilter:
    """从会话创建过滤器"""
    user_profile = session.get("user_profile", {})
    constraints = UserConstraints(
        budget_constraint=user_profile.get("预算约束", ""),
        period_constraint=user_profile.get("周期约束", ""),
        core_target=user_profile.get("核心目标", "")
    )
    return ConstraintFilter(constraints)


# 常用方案模板（带成本和周期信息）
SCHEME_TEMPLATES = {
    "副业试水": [
        {
            "名称": "知识付费分销",
            "成本": "0",
            "周期": "1周",
            "适用": ["完全陌生", "有基础认知"]
        },
        {
            "名称": "短视频带货(无货)",
            "成本": "0",
            "周期": "1个月",
            "适用": ["完全陌生", "有基础认知"]
        },
        {
            "名称": "技能咨询服务",
            "成本": "500",
            "周期": "2周",
            "适用": ["有基础认知", "资深从业者"]
        },
        {
            "名称": "私教/陪跑服务",
            "成本": "1000",
            "周期": "1个月",
            "适用": ["资深从业者"]
        }
    ],
    "创业立项": [
        {
            "名称": "最小MVP验证",
            "成本": "3000",
            "周期": "1个月",
            "适用": ["有基础认知", "资深从业者"]
        },
        {
            "名称": "私域变现模式",
            "成本": "5000",
            "周期": "3个月",
            "适用": ["有基础认知", "资深从业者"]
        },
        {
            "名称": "品牌代理模式",
            "成本": "10000",
            "周期": "6个月",
            "适用": ["资深从业者"]
        }
    ]
}


def get_filtered_schemes(constraint_filter: ConstraintFilter, target_type: str = "副业试水") -> List[Dict[str, Any]]:
    """获取符合约束的方案列表"""
    schemes = SCHEME_TEMPLATES.get(target_type, SCHEME_TEMPLATES["副业试水"])
    return constraint_filter.filter_options(schemes)


# ========== 生成阶段约束嵌入方法 ==========


def get_constraint_params(constraint_filter: ConstraintFilter) -> Dict[str, Any]:
    """
    获取生成阶段需要的约束参数
    用于在生成选项时直接嵌入约束条件
    """
    budget = constraint_filter.constraints.budget_limit or 999999
    period = constraint_filter.constraints.period_limit or 99
    
    # 根据约束确定可选的成本范围
    if budget == 0:
        cost_range = "0成本"
    elif budget <= 5000:
        cost_range = "0-5000元"
    elif budget <= 20000:
        cost_range = "0-20000元"
    else:
        cost_range = "0-50000元"
    
    # 根据约束确定可选的时间范围
    if period <= 1:
        time_range = "1周-1个月"
    elif period <= 3:
        time_range = "1周-3个月"
    elif period <= 6:
        time_range = "1周-6个月"
    else:
        time_range = "1周-12个月"
    
    return {
        "预算上限": budget,
        "周期上限": period,
        "成本范围": cost_range,
        "时间范围": time_range,
        "可用资源": _get_available_resources(budget, period)
    }


def _get_available_resources(budget: int, period: int) -> List[str]:
    """根据预算和周期确定可用的资源渠道"""
    resources = []
    
    # 免费渠道（预算=0或周期短）
    if budget == 0 or period <= 1:
        resources.extend([
            "短视频内容引流",
            "社交媒体免费推广",
            "社群裂变",
            "问答平台获客"
        ])
    
    # 低成本渠道（预算<5000）
    if budget <= 5000:
        resources.extend([
            "付费社群加入",
            "小额广告投放",
            "KOL合作（置换）",
            "工具/软件辅助"
        ])
    
    # 中等成本渠道（预算<=20000）
    if budget <= 20000:
        resources.extend([
            "付费KOL推广",
            "信息流广告",
            "线下活动",
            "代理分销"
        ])
    
    return resources if resources else ["自有人脉/资源"]


def get_constraint_guidance_text(constraint_filter: ConstraintFilter) -> str:
    """获取约束指导文本，用于生成时嵌入"""
    params = get_constraint_params(constraint_filter)
    
    return (
        f"【约束条件】请生成的方案必须满足以下条件："
        f"成本范围：{params['成本范围']}，"
        f"时间范围：{params['时间范围']}，"
        f"可使用资源：{', '.join(params['可用资源'][:3])}"
    )
