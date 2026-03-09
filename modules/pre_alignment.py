"""
前置对齐模块
负责4个单问题的顺序询问，构建用户画像
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class AlignmentPhase(Enum):
    """对齐阶段"""
    等待开始 = 0
    核心目标 = 1      # 问题1
    核心目的 = 2      # 问题2
    认知层级 = 3      # 问题3
    预算周期 = 4      # 问题4
    服务模式 = 5      # 仅当认知层级为"有基础认知/资深从业者"时
    完成 = 99


# 前置问题配置
PRE_ALIGNMENT_QUESTIONS = {
    AlignmentPhase.核心目标: {
        "问题": "你本次想要拆解分析的核心目标，是具体的职业、某类商业赛道，还是一款特定的产品？请同时告知该目标的具体名称或赛道方向。",
        "说明": "例如：短视频带货、跨境电商、在线教育、独立开发者的SaaS产品等",
        "记录键": "核心目标"
    },
    AlignmentPhase.核心目的: {
        "问题": "你本次做需求挖掘与最小闭环设计的核心目标是什么？",
        "选项": [
            {"label": "A. 副业试水落地", "value": "副业试水"},
            {"label": "B. 创业立项分析", "value": "创业立项"},
            {"label": "C. 行业研究学习", "value": "行业研究学习"},
            {"label": "D. 职业转型规划", "value": "职业转型规划"},
            {"label": "E. 其他", "value": "其他", "需要补充": True}
        ],
        "说明": "请从以上选项中选择",
        "记录键": "核心目的"
    },
    AlignmentPhase.认知层级: {
        "问题": "你对这个目标领域，目前的认知程度符合以下哪一种？",
        "选项": [
            {
                "label": "A. 完全陌生",
                "value": "完全陌生",
                "说明": "仅听过名字，完全不了解行业规则、玩法、相关内容"
            },
            {
                "label": "B. 有基础认知",
                "value": "有基础认知",
                "说明": "了解行业基础定义、主流玩法，有少量相关了解"
            },
            {
                "label": "C. 资深从业者",
                "value": "资深从业者",
                "说明": "深耕该领域，有丰富的实操经验与行业认知"
            }
        ],
        "说明": "请从以上选项中选择",
        "记录键": "认知层级"
    },
    AlignmentPhase.预算周期: {
        "问题": "你希望这个最小商业闭环的落地周期与可投入的成本预算上限大概是怎样的？",
        "选项": [
            {"label": "A. 0成本，1个月内落地", "value": "0成本,1个月"},
            {"label": "B. 低预算（5000元内），3个月内落地", "value": "5000元内,3个月"},
            {"label": "C. 中预算（5000-20000元），6个月内落地", "value": "5000-20000元,6个月"},
            {"label": "D. 其他（请补充）", "value": "其他", "需要补充": True}
        ],
        "说明": "请从以上选项中选择，或补充你的具体约束",
        "记录键": "预算周期"
    },
    AlignmentPhase.服务模式: {
        "问题": "你希望我以哪种方式为你服务？",
        "选项": [
            {
                "label": "A. 引导教练",
                "value": "引导教练",
                "说明": "通过提问引导你自己梳理思考，完成完整的思考闭环"
            },
            {
                "label": "B. 落地顾问",
                "value": "落地顾问",
                "说明": "我全程主导输出，直接给你贴合约束的可落地分析与方案，仅在需要你做决策时提问"
            },
            {
                "label": "C. 深度共创",
                "value": "深度共创",
                "说明": "和你一起深度拆解共创，挖掘你的个性化需求，共同完善方案"
            }
        ],
        "说明": "请从以上选项中选择",
        "记录键": "服务模式"
    }
}


@dataclass
class AlignmentResult:
    """对齐结果"""
    核心目标: str = ""
    核心目的: str = ""
    认知层级: str = ""
    预算约束: str = ""
    周期约束: str = ""
    服务模式: str = ""
    是否完成: bool = False


class PreAlignmentModule:
    """前置对齐模块"""
    
    def __init__(self):
        self.questions = PRE_ALIGNMENT_QUESTIONS
    
    def get_current_question(self, current_phase: AlignmentPhase) -> Dict[str, Any]:
        """获取当前问题"""
        config = self.questions.get(current_phase, {})
        return {
            "阶段": "前置对齐",
            "环节": current_phase.name,
            "问题": config.get("问题", ""),
            "选项": config.get("选项", []),
            "说明": config.get("说明", ""),
            "记录键": config.get("记录键", "")
        }
    
    def get_next_phase(self, current_phase: AlignmentPhase, user_answer: str, 
                       current_profile: Dict[str, str]) -> Tuple[AlignmentPhase, str]:
        """
        根据用户回答确定下一阶段
        返回: (下一阶段, 响应消息)
        """
        # 记录当前回答
        if current_phase == AlignmentPhase.核心目标:
            current_profile["核心目标"] = user_answer
            next_phase = AlignmentPhase.核心目的
            msg = f"好的，你本次的核心目标是：{user_answer}"
            
        elif current_phase == AlignmentPhase.核心目的:
            current_profile["核心目的"] = user_answer
            # 解析选项，提取目的
            if "副业" in user_answer:
                current_profile["核心目的"] = "副业试水"
            elif "创业" in user_answer:
                current_profile["核心目的"] = "创业立项"
            elif "行业" in user_answer or "学习" in user_answer:
                current_profile["核心目的"] = "行业研究学习"
            elif "职业" in user_answer or "转型" in user_answer:
                current_profile["核心目的"] = "职业转型规划"
            
            next_phase = AlignmentPhase.认知层级
            msg = f"明白了，你做这事的核心目的是：{current_profile['核心目的']}"
            
        elif current_phase == AlignmentPhase.认知层级:
            current_profile["认知层级"] = user_answer
            next_phase = AlignmentPhase.预算周期
            msg = f"好的，你目前对该领域的认知层级是：{user_answer}"
            
        elif current_phase == AlignmentPhase.预算周期:
            # 解析预算和周期
            budget, period = self._parse_budget_period(user_answer)
            current_profile["预算约束"] = budget
            current_profile["周期约束"] = period
            
            # 判断是否需要询问服务模式
            if current_profile.get("认知层级") in ["有基础认知", "资深从业者"]:
                next_phase = AlignmentPhase.服务模式
                msg = f"好的，你的预算是{budget}，周期是{period}。"
            else:
                # 完全陌生直接默认落地顾问
                current_profile["服务模式"] = "落地顾问"
                next_phase = AlignmentPhase.完成
                msg = f"好的，基于你的情况，我将作为「落地顾问」为你服务。"
                
        elif current_phase == AlignmentPhase.服务模式:
            current_profile["服务模式"] = user_answer
            next_phase = AlignmentPhase.完成
            
            mode_desc = {
                "引导教练": "引导教练",
                "落地顾问": "落地顾问",
                "深度共创": "深度共创"
            }.get(user_answer, "落地顾问")
            msg = f"好的，我将作为「{mode_desc}」为你服务。"
        
        else:
            next_phase = AlignmentPhase.完成
            msg = "前置对齐完成"
        
        return next_phase, msg
    
    def _parse_budget_period(self, answer: str) -> Tuple[str, str]:
        """解析预算和周期"""
        budget = "未明确"
        period = "未明确"
        
        if "0成本" in answer:
            budget = "0成本"
            period = "1个月"
        elif "5000元内" in answer:
            budget = "5000元内"
            period = "3个月"
        elif "5000-20000" in answer:
            budget = "5000-20000元"
            period = "6个月"
        elif "其他" in answer:
            # 尝试从回答中提取
            budget = "自定义"
            period = "自定义"
        
        return budget, period
    
    def get_progress(self, current_phase: AlignmentPhase) -> Dict[str, Any]:
        """获取进度信息"""
        total = len(AlignmentPhase) - 1  # 减去等待开始
        current = current_phase.value
        
        # 调整：完全陌生少一个阶段
        if current_phase.value > AlignmentPhase.服务模式.value:
            current = current - 1
            
        return {
            "当前阶段": f"前置对齐 ({current_phase.name})",
            "进度": int((current / 4) * 100) if current <= 4 else 100,
            "预估剩余": max(0, 4 - current)
        }
    
    def is_completed(self, current_phase: AlignmentPhase) -> bool:
        """检查是否完成"""
        return current_phase == AlignmentPhase.完成
    
    def get_final_profile(self, profile: Dict[str, str]) -> AlignmentResult:
        """获取最终用户画像"""
        return AlignmentResult(
            核心目标=profile.get("核心目标", ""),
            核心目的=profile.get("核心目的", ""),
            认知层级=profile.get("认知层级", ""),
            预算约束=profile.get("预算约束", ""),
            周期约束=profile.get("周期约束", ""),
            服务模式=profile.get("服务模式", "落地顾问"),
            是否完成=True
        )


# 全局实例
_pre_alignment_module = None

def get_pre_alignment_module() -> PreAlignmentModule:
    """获取前置对齐模块单例"""
    global _pre_alignment_module
    if _pre_alignment_module is None:
        _pre_alignment_module = PreAlignmentModule()
    return _pre_alignment_module
