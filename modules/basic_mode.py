"""
模式二&模式三：有基础认知模式 + 资深从业者模式
模式二：根据用户选择的角色（引导教练/落地顾问）执行
模式三：资深从业者专属的深度共创流程
"""

from typing import Dict, Any, List, Callable
from enum import Enum


class BasicPhase(Enum):
    """有基础认知模式阶段"""
    等待开始 = 0
    # 引导教练子模式
    玩法梳理 = 1      # 请用户梳理核心玩法
    用户定位 = 2      # 请用户定位目标用户
    行为路径 = 3      # 请用户描述行为路径
    需求挖掘 = 4      # 请用户挖掘需求
    痛点识别 = 5      # 请用户识别痛点
    方案对比 = 6      # 请用户对比现有方案
    优先级确定 = 7    # 请用户确定优先级
    解决方案 = 8      # 请用户提出解决方案
    差异化分析 = 9    # 请用户分析差异化
    环节清单 = 10     # 请用户列出核心环节
    资源盘点 = 11     # 请用户盘点资源
    盈利设计 = 12     # 请用户设计盈利
    验证设计 = 13     # 请用户设计验证
    迭代预案 = 14     # 请用户制定迭代预案
    # 落地顾问子模式（与陌生模式类似，但内容更深度）
    顾问基础认知 = 15
    顾问用户锁定 = 16
    顾问痛点拆解 = 17
    顾问方案匹配 = 18
    顾问闭环设计 = 19
    最终输出 = 20
    完成 = 99


class SeniorPhase(Enum):
    """资深从业者模式阶段"""
    等待开始 = 0
    个性化诉求 = 1     # 挖掘个性化需求
    行业痛点 = 2        # 行业核心痛点
    差异化定位 = 3      # 差异化用户定位
    空白需求 = 4       # 空白需求挖掘
    初步思路 = 5       # 初步解决思路
    最小闭环 = 6        # 最小落地闭环
    风险预案 = 7        # 风险与不确定因素
    个性化指标 = 8      # 个性化验证指标
    共创完善 = 9        # 共创完善方案
    完成 = 99


class BasicModeExecutor:
    """有基础认知模式执行器"""
    
    # 引导教练问题列表（每个问题都要符合"新手友好转换规则"）
    COACH_QUESTIONS = [
        {
            "key": "玩法梳理",
            "问题": "请你梳理一下，你了解的这个领域，贴合你核心目标与约束的核心玩法、主流盈利模式分别是什么？",
            "提示": "可以从这几个方向思考：服务变现、产品带货、内容变现、技能咨询等",
            "记录键": "核心玩法"
        },
        {
            "key": "用户定位",
            "问题": "结合你的核心目标，你想要服务的核心目标用户群体是哪一类？",
            "提示": "可以参考这几个标签：年龄、职业、核心场景、收入水平等",
            "记录键": "目标用户"
        },
        {
            "key": "行为路径",
            "问题": "这类目标用户，在对应场景中，从产生需求到完成付费的完整行为路径是怎样的？",
            "提示": "想想用户从'不知道'到'知道'到'想要'到'购买'的整个过程",
            "记录键": "用户行为路径"
        },
        {
            "key": "需求挖掘",
            "问题": "在这个完整的行为路径中，你认为用户最核心的、未被满足的刚性需求有哪些？",
            "提示": "想想用户在每个环节最想要什么",
            "记录键": "核心需求"
        },
        {
            "key": "痛点识别",
            "问题": "对应这些需求，用户当前面临的最强烈的痛点是什么？请区分表层的麻烦，和底层未被解决的核心问题。",
            "提示": "表层：麻烦；底层：未被解决的核心问题",
            "记录键": "痛点"
        },
        {
            "key": "方案对比",
            "问题": "这些痛点当前有没有被其他玩家解决？如果有，解决得好不好，存在哪些核心不足？",
            "提示": "现有方案哪里做得不够好",
            "记录键": "现有方案分析"
        },
        {
            "key": "优先级确定",
            "问题": "结合用户付费意愿、痛点强烈程度、解决难度，你认为优先级最高的1-2个核心痛点是什么？",
            "提示": "哪个痛点最痛、用户最愿意付费、相对容易解决",
            "记录键": "痛点优先级"
        },
        {
            "key": "解决方案",
            "问题": "针对这1-2个核心痛点，你能提供的、符合你成本与周期约束的轻量化核心解决方案是什么？",
            "提示": "用一句话说明：帮什么人，解决什么问题，带来什么核心好处",
            "记录键": "解决方案"
        },
        {
            "key": "差异化分析",
            "问题": "这个解决方案，和当前市场上的其他方案相比，核心的差异化优势是什么？",
            "提示": "你有什么别人没有的",
            "记录键": "差异化优势"
        },
        {
            "key": "环节清单",
            "问题": "要跑通这个方案的最小商业闭环，你需要完成的核心环节有哪些？",
            "提示": "引流→转化→交付→复购",
            "记录键": "核心环节"
        },
        {
            "key": "资源盘点",
            "问题": "针对每个核心环节，你能用到的、最低成本的落地资源与渠道分别是什么？",
            "提示": "你有什么资源可以用",
            "记录键": "可用资源"
        },
        {
            "key": "盈利设计",
            "问题": "你设计的这个最小商业闭环，核心的盈利模式与对应的定价标准是什么？",
            "提示": "怎么赚钱、卖多少钱",
            "记录键": "盈利模式"
        },
        {
            "key": "验证设计",
            "问题": "要验证这个闭环是否能跑通，你设定的最小验证周期与核心验证成功指标是什么？",
            "提示": "多久验证、成功的标准是什么",
            "记录键": "验证指标"
        },
        {
            "key": "迭代预案",
            "问题": "如果验证达标，你下一步的迭代优化方向是什么？如果验证不达标，你预设的调整预案是什么？",
            "提示": "成了怎么做、不成怎么做",
            "记录键": "迭代预案"
        }
    ]
    
    def __init__(self, user_profile: Dict[str, str], constraints: Dict[str, str], 
                 role: str = "引导教练"):
        self.profile = user_profile
        self.constraints = constraints
        self.role = role  # "引导教练" 或 "落地顾问"
        self.current_index = 0
        
        # 如果是落地顾问，使用简化版流程
        if role == "落地顾问":
            self.questions = self.COACH_QUESTIONS[:6]  # 只保留前6个关键问题
        else:
            self.coach_questions = self.COACH_QUESTIONS
    
    def get_current_question(self, current_index: int = None) -> Dict[str, Any]:
        """获取当前问题"""
        if current_index is not None:
            self.current_index = current_index
        
        if self.role == "落地顾问":
            return self._get_advisor_question()
        else:
            return self._get_coach_question()
    
    def _get_coach_question(self) -> Dict[str, Any]:
        """获取引导教练问题"""
        if self.current_index >= len(self.COACH_QUESTIONS):
            return {"是最终环节": True}
        
        q = self.COACH_QUESTIONS[self.current_index]
        return {
            "阶段": "引导教练",
            "环节": q["key"],
            "问题": q["问题"],
            "提示": q.get("提示", ""),
            "选项": [],  # 引导教练模式不做选项限制
            "记录键": q["记录键"],
            "进度": f"{self.current_index + 1}/{len(self.COACH_QUESTIONS)}"
        }
    def _get_advisor_question(self) -> Dict[str, Any]:
        """
        获取落地顾问问题（有基础认知版本）
        与完全陌生版本的区别：
        1. 跳过基础认知环节，直接进入深度分析
        2. 可以引用用户已有的认知进行追问
        3. 方案更加专业化
        """
        
        # 有基础认知+落地顾问的差异化问题列表
        advisor_questions = [
            {
                "key": "深度认知确认",
                "问题": "你对这个领域已有一定的了解，能否分享一下你目前掌握的核心玩法是什么？",
                "说明": "跳过基础认知，直接确认用户的已有认知",
                "跳过条件": "用户回答过于简单时"
            },
            {
                "key": "经验总结",
                "问题": "基于你的了解，你认为这个领域最容易成功的切入点是什么？有没有尝试过？",
                "说明": "挖掘用户的实操经验",
                "跳过条件": "用户表示没有经验"
            },
            {
                "key": "深度痛点",
                "问题": "在你自己尝试或了解的过程中，最困扰你的问题是什么？",
                "说明": "比陌生模式更深入",
                "跳过条件": "无"
            },
            {
                "key": "资源盘点",
                "问题": "你目前有哪些可用的资源（人脉、技能、资金、渠道等）？",
                "说明": "基于用户已有认知定制方案",
                "跳过条件": "无"
            },
            {
                "key": "专业方案",
                "问题": "结合你的资源和经验，你希望我提供什么深度的方案支持？",
                "说明": "可以选择标准方案或深度定制",
                "跳过条件": "无"
            },
            {
                "key": "最终确认",
                "问题": "这个方案是否符合你的预期？",
                "说明": "确认后完成",
                "跳过条件": "无"
            }
        ]
        
        if self.current_index >= len(advisor_questions):
            return {"是最终环节": True}
        
        q = advisor_questions[self.current_index]
        return {
            "阶段": "有基础认知-落地顾问",
            "环节": q["key"],
            "问题": q["问题"],
            "说明": q.get("说明", ""),
            "记录键": q["key"],
            "差异化": True,  # 标记为差异化版本
            "进度": f"{self.current_index + 1}/{len(advisor_questions)}"
        }
    def _get_advisor_question(self) -> Dict[str, Any]:
        """获取落地顾问问题（与陌生模式类似但更深度）"""
        # 简化实现，调用陌生模式的方法
        from modules.stranger_mode import create_stranger_executor
        executor = create_stranger_executor(self.profile)
        
        from modules.stranger_mode import StrangerPhase
        phase_map = {
            0: StrangerPhase.基础认知,
            1: StrangerPhase.用户群体,
            2: StrangerPhase.痛点拆解,
            3: StrangerPhase.方案匹配,
            4: StrangerPhase.闭环设计,
            5: StrangerPhase.最终输出
        }
        
        phase = phase_map.get(self.current_index, StrangerPhase.基础认知)
        return executor.get_current_task(phase)
    
    def get_next_question_index(self, current_index: int, user_answer: str) -> int:
        """获取下一问题索引"""
        # 检查是否是"不知道"触发容错
        if self._is_dont_know(user_answer):
            # 连续2次不知道会触发容错，这里简化处理
            # 实际应该检查连续次数
            pass
        
        return current_index + 1
    
    def _is_dont_know(self, answer: str) -> bool:
        """判断用户是否表示不知道"""
        dont_know_keywords = ["不知道", "不懂", "不太清楚", "无法回答", "说不清"]
        return any(kw in answer for kw in dont_know_keywords)
    
    def is_completed(self, current_index: int = None) -> bool:
        """检查是否完成"""
        if current_index is not None:
            self.current_index = current_index
        
        if self.role == "落地顾问":
            return self.current_index >= 6
        else:
            return self.current_index >= len(self.COACH_QUESTIONS)
    
    def generate_summary(self, collected_answers: Dict[str, str]) -> str:
        """生成完整梳理汇总"""
        lines = [
            "# 完整需求梳理汇总",
            "",
            f"核心目标：{self.profile.get('核心目标', '')}",
            f"核心目的：{self.profile.get('核心目的', '')}",
            f"认知层级：{self.profile.get('认知层级', '')}",
            "",
            "---",
            ""
        ]
        
        for key, answer in collected_answers.items():
            lines.append(f"## {key}")
            lines.append(answer)
            lines.append("")
        
        return "\n".join(lines)


class SeniorModeExecutor:
    """资深从业者模式执行器"""
    SENIOR_QUESTIONS = [
        {
            "key": "破冰开场",
            "问题": "在你想要做的这个方向上，之前有没有尝试过什么？如果有，卡在哪里、遇到了什么困难？",
            "说明": "用具体场景破冰，帮助资深用户回想起具体经历"
        },
        {
            "key": "个性化诉求",
            "问题": "你本次拆解分析的核心诉求，除了已明确的目标之外，还有哪些个性化的需求与期待？",
            "改进": "资深从业者通常心里有苦说不出，建议用具体场景破冰"
        },
        {
            "key": "行业痛点",
            "问题": "你在该领域深耕的过程中，发现当前行业最核心的痛点、最空白的机会点分别是什么？"
        },
        {
            "key": "差异化定位",
            "问题": "结合你的资源与能力，你想要锁定的核心目标用户群体，与行业主流玩家相比，有哪些差异化的定位？"
        },
        {
            "key": "空白需求",
            "问题": "针对这个差异化的用户群体，你发现了哪些行业主流玩家未覆盖的、未被满足的核心需求与痛点？"
        },
        {
            "key": "初步思路",
            "问题": "针对这些核心痛点，你目前已经有了哪些初步的解决方案思路？"
        },
        {
            "key": "最小闭环",
            "问题": "结合你的成本、周期约束，你认为这个解决方案的最小落地闭环，需要包含哪些核心环节？"
        },
        {
            "key": "风险预案",
            "问题": "你认为这个闭环落地过程中，最大的风险与不确定因素是什么？你预设的应对方案是什么？"
        },
        {
            "key": "个性化指标",
            "问题": "你设定的闭环验证成功的核心指标，与行业通用指标相比，有哪些个性化的标准？"
        }
    ]
    
    def __init__(self, user_profile: Dict[str, str], constraints: Dict[str, str]):
        self.profile = user_profile
        self.constraints = constraints
        self.current_index = 0
    
    def get_current_question(self, current_index: int = None) -> Dict[str, Any]:
        """获取当前问题"""
        if current_index is not None:
            self.current_index = current_index
        
        if self.current_index >= len(self.SENIOR_QUESTIONS):
            return {"是最终环节": True}
        
        q = self.SENIOR_QUESTIONS[self.current_index]
        return {
            "阶段": "深度共创",
            "环节": q["key"],
            "问题": q["问题"],
            "改进建议": q.get("改进", ""),
            "记录键": q["key"],
            "进度": f"{self.current_index + 1}/{len(self.SENIOR_QUESTIONS)}"
        }
    
    def get_next_index(self, current_index: int) -> int:
        """获取下一问题索引"""
        return current_index + 1
    
    def is_completed(self, current_index: int = None) -> bool:
        """检查是否完成"""
        if current_index is not None:
            self.current_index = current_index
        return self.current_index >= len(self.SENIOR_QUESTIONS)
    
    def generate_summary(self, collected_answers: Dict[str, str]) -> str:
        """生成深度拆解汇总"""
        lines = [
            "# 深度共创方案汇总",
            "",
            f"核心目标：{self.profile.get('核心目标', '')}",
            f"核心目的：{self.profile.get('核心目的', '')}",
            f"服务模式：深度共创",
            "",
            "---",
            ""
        ]
        
        for key, answer in collected_answers.items():
            lines.append(f"## {key}")
            lines.append(answer)
            lines.append("")
        
        lines.append("---")
        lines.append("**以上是基于你的深度共创生成的完整方案**")
        
        return "\n".join(lines)


def create_basic_executor(user_profile: Dict[str, str], role: str = "引导教练") -> BasicModeExecutor:
    """创建有基础认知模式执行器"""
    constraints = {
        "预算约束": user_profile.get("预算约束", ""),
        "周期约束": user_profile.get("周期约束", "")
    }
    return BasicModeExecutor(user_profile, constraints, role)


def create_senior_executor(user_profile: Dict[str, str]) -> SeniorModeExecutor:
    """创建资深从业者模式执行器"""
    constraints = {
        "预算约束": user_profile.get("预算约束", ""),
        "周期约束": user_profile.get("周期约束", "")
    }
    return SeniorModeExecutor(user_profile, constraints)
