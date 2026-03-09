"""
模式三：资深从业者模式（深度共创角色）
适用于：资深从业者的深度共创流程
核心规则：深度挖掘个性化需求，共创完善方案
"""

from typing import Dict, Any, List
from enum import Enum

# 导入约束过滤模块
from utils.constraint_filter import ConstraintFilter, UserConstraints, get_constraint_params


class SeniorPhase(Enum):
    """资深模式阶段"""
    等待开始 = 0
    破冰开场 = 1        # 破冰，了解用户过往经验
    个性化诉求 = 2      # 挖掘个性化需求
    行业痛点 = 3        # 深入行业痛点分析
    差异化定位 = 4      # 差异化用户定位
    空白需求 = 5        # 空白需求挖掘
    初步思路 = 6        # 初步解决思路
    最小闭环 = 7        # 最小落地闭环
    风险预案 = 8        # 风险与不确定因素
    个性化指标 = 9      # 个性化验证指标
    共创完善 = 10       # 共创完善方案
    最终输出 = 11       # 最终方案输出
    完成 = 99


class SeniorModeExecutor:
    """
    资深从业者模式执行器
    核心：深度共创，挖掘个性化需求
    """
    
    # 资深模式问题列表
    SENIOR_QUESTIONS = [
        {
            "阶段": "破冰开场",
            "环节": "破冰开场",
            "key": "破冰开场",
            "问题": "在你想要做的这个方向上，之前有没有尝试过什么？如果有，卡在哪里、遇到了什么困难？",
            "说明": "用具体场景破冰，帮助资深用户回想起具体经历",
            "记录键": "过往经验"
        },
        {
            "阶段": "个性化诉求",
            "环节": "个性化诉求",
            "key": "个性化诉求",
            "问题": "你本次拆解分析的核心诉求，除了已明确的目标之外，还有哪些个性化的需求与期待？",
            "说明": "挖掘资深从业者通常心里有苦说不出的需求",
            "记录键": "个性化诉求"
        },
        {
            "阶段": "行业痛点",
            "环节": "行业痛点",
            "key": "行业痛点",
            "问题": "你在该领域深耕的过程中，发现当前行业最核心的痛点、最空白的机会点分别是什么？",
            "说明": "利用资深从业者经验，挖掘深层痛点",
            "记录键": "行业痛点"
        },
        {
            "阶段": "差异化定位",
            "环节": "差异化定位",
            "key": "差异化定位",
            "问题": "结合你的资源与能力，你想要锁定的核心目标用户群体，与行业主流玩家相比，有哪些差异化的定位？",
            "说明": "基于资深经验，制定差异化策略",
            "记录键": "差异化定位"
        },
        {
            "阶段": "空白需求",
            "环节": "空白需求",
            "key": "空白需求",
            "问题": "针对这个差异化的用户群体，你发现了哪些行业主流玩家未覆盖的、未被满足的核心需求与痛点？",
            "说明": "挖掘空白市场机会",
            "记录键": "空白需求"
        },
        {
            "阶段": "初步思路",
            "环节": "初步思路",
            "key": "初步思路",
            "问题": "针对这些核心痛点，你目前已经有了哪些初步的解决方案思路？",
            "说明": "收集资深从业者的方案思路",
            "记录键": "初步思路"
        },
        {
            "阶段": "最小闭环",
            "环节": "最小闭环",
            "key": "最小闭环",
            "问题": "结合你的成本、周期约束，你认为这个解决方案的最小落地闭环，需要包含哪些核心环节？",
            "说明": "确定最小可行闭环",
            "记录键": "最小闭环"
        },
        {
            "阶段": "风险预案",
            "环节": "风险预案",
            "key": "风险预案",
            "问题": "你认为这个闭环落地过程中，最大的风险与不确定因素是什么？你预设的应对方案是什么？",
            "说明": "识别风险并制定应对策略",
            "记录键": "风险预案"
        },
        {
            "阶段": "个性化指标",
            "环节": "个性化指标",
            "key": "个性化指标",
            "问题": "你设定的闭环验证成功的核心指标，与行业通用指标相比，有哪些个性化的标准？",
            "说明": "制定个性化验证指标",
            "记录键": "个性化指标"
        },
        {
            "阶段": "共创完善",
            "环节": "共创完善",
            "key": "共创完善",
            "问题": "基于以上所有分析，我们一起共创完善这个方案，你认为还有哪些需要调整的地方？",
            "说明": "最终共创完善方案",
            "记录键": "共创完善"
        }
    ]
    
    def __init__(self, user_profile: Dict[str, str], constraints: Dict[str, str]):
        self.profile = user_profile
        self.constraints = constraints
        self.core_target = user_profile.get("核心目标", "")
        self.budget = constraints.get("预算约束", "")
        self.period = constraints.get("周期约束", "")
        
        # 初始化约束过滤器
        self.constraint_filter = ConstraintFilter(
            UserConstraints(
                budget_constraint=self.budget,
                period_constraint=self.period,
                core_target=user_profile.get("核心目标", "")
            )
        )
        
        # 获取约束参数（用于生成阶段）
        self.constraint_params = get_constraint_params(self.constraint_filter)
        self.current_index = 0
    
    def get_current_task(self, current_index: int = None) -> Dict[str, Any]:
        """获取当前任务"""
        if current_index is not None:
            self.current_index = current_index
        
        if self.current_index >= len(self.SENIOR_QUESTIONS):
            return self._get_final_output_task()
        
        q = self.SENIOR_QUESTIONS[self.current_index]
        return {
            "阶段": q["阶段"],
            "环节": q["环节"],
            "问题": q["问题"],
            "说明": q.get("说明", ""),
            "记录键": q["记录键"],
            "进度": f"{self.current_index + 1}/{len(self.SENIOR_QUESTIONS)}",
            "AI输出": self._generate_content_for_senior(q["key"])
        }
    
    def _generate_content_for_senior(self, key: str) -> str:
        """为资深从业者生成相关内容"""
        content_map = {
            "破冰开场": f"作为资深从业者，你对【{self.core_target}】领域肯定有深入的了解。让我们从你的实际经验出发，一起挖掘更深层的机会。",
            "个性化诉求": "基于你的行业经验，你可能有一些独特的视角和个性化的需求。让我们深入探讨这些方面。",
            "行业痛点": f"基于你深耕的经验，你对【{self.core_target}】领域的痛点和机会点肯定有独到见解。请分享你发现的核心痛点。",
            "差异化定位": "作为资深从业者，你有独特的优势。让我们一起制定差异化的用户定位策略。",
            "空白需求": "凭借你的经验，你可能发现了市场中未被满足的需求。请分享这些空白机会。",
            "初步思路": "基于你的专业经验，你可能已经有了一些解决方案的想法。请分享你的初步思路。",
            "最小闭环": f"结合你的预算（{self.budget}）和周期（{self.period}）约束，让我们设计最小可行的落地闭环。",
            "风险预案": "任何项目都面临风险。让我们一起识别潜在风险并制定应对预案。",
            "个性化指标": "让我们制定符合你个性化需求的验证指标。",
            "共创完善": "现在让我们一起共创，完善整个方案。"
        }
        return content_map.get(key, "")
    
    def _get_final_output_task(self) -> Dict[str, Any]:
        """环节：最终方案输出"""
        return {
            "阶段": "最终方案输出",
            "环节": "最终方案",
            "AI输出": self._generate_final_plan(),
            "提问": "深度共创方案已完成。你对这个方案满意吗？是否需要进一步优化？",
            "选项": [
                {"label": "A. 满意，完成", "value": "满意"},
                {"label": "B. 需要优化", "value": "需要优化"}
            ],
            "记录键": "最终确认",
            "是最终环节": True
        }
    
    def _generate_final_plan(self) -> str:
        """生成最终方案"""
        return f"""
# 深度共创最终方案

## 核心信息
- 核心目标：{self.core_target}
- 核心目的：{self.profile.get('核心目的', '')}
- 服务模式：深度共创

## 方案概要
（此处整合前面所有共创内容，形成完整方案）

### 核心价值主张
基于你的资深经验，我们共同确定的核心价值主张...

### 差异化定位
你的独特优势与差异化策略...

### 最小商业闭环
{self.core_target}的最小落地闭环设计...

### 验证指标
个性化验证指标与成功标准...

### 风险预案
已识别的风险与应对策略...

---
**资深从业者深度共创方案生成完成，祝你落地顺利！**
"""
    
    def get_next_task_index(self, current_index: int = None) -> int:
        """获取下一任务索引"""
        if current_index is not None:
            self.current_index = current_index
        return self.current_index + 1
    
    def is_completed(self, current_index: int = None) -> bool:
        """检查是否完成"""
        if current_index is not None:
            self.current_index = current_index
        return self.current_index >= len(self.SENIOR_QUESTIONS)
    
    def get_progress(self, current_index: int = None) -> Dict[str, Any]:
        """获取进度"""
        if current_index is not None:
            self.current_index = current_index
        total = len(self.SENIOR_QUESTIONS)
        current = self.current_index
        
        return {
            "当前阶段": "资深从业者模式",
            "进度": int((current / total) * 100) if total > 0 else 0,
            "预估剩余": max(0, total - current),
            "环节": self.SENIOR_QUESTIONS[current-1]["环节"] if current > 0 and current <= total else "开始"
        }


def create_senior_executor(user_profile: Dict[str, str]) -> SeniorModeExecutor:
    """创建资深从业者模式执行器"""
    constraints = {
        "预算约束": user_profile.get("预算约束", ""),
        "周期约束": user_profile.get("周期约束", "")
    }
    return SeniorModeExecutor(user_profile, constraints)