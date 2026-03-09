"""
模式一：完全陌生模式（落地顾问角色）
适用于：完全陌生的用户
核心规则：AI 主导输出，仅决策时单问题提问
"""
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# 导入约束过滤模块
from utils.constraint_filter import (
    ConstraintFilter, 
    UserConstraints,
    get_constraint_params,
    get_constraint_guidance_text
)


class StrangerPhase(Enum):
    """陌生模式阶段"""
    等待开始 = 0
    基础认知 = 1        # 环节1：基础认知极简补齐
    用户群体 = 2       # 环节2：目标用户群体锁定
    痛点拆解 = 3       # 环节3：需求与痛点深度拆解
    方案匹配 = 4       # 环节4：轻量化解决方案匹配
    闭环设计 = 5       # 环节5：最小商业闭环完整设计
    最终输出 = 6      # 环节6：最终方案输出
    完成 = 99


class StrangerModeExecutor:
    """
    完全陌生模式执行器
    核心：AI 主导输出，用户仅做选择题
    """
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
    
    def get_current_task(self, current_phase: StrangerPhase) -> Dict[str, Any]:
        """获取当前任务"""
        phase_handlers = {
            StrangerPhase.基础认知: self._get_cognition_task,
            StrangerPhase.用户群体: self._get_user_group_task,
            StrangerPhase.痛点拆解: self._get_pain_point_task,
            StrangerPhase.方案匹配: self._get_solution_task,
            StrangerPhase.闭环设计: self._get_closed_loop_task,
            StrangerPhase.最终输出: self._get_final_output_task
        }
        
        handler = phase_handlers.get(current_phase, self._get_cognition_task)
        return handler()
    
    def _get_cognition_task(self) -> Dict[str, Any]:
        """环节1：基础认知极简补齐"""
        return {
            "阶段": "基础认知极简补齐",
            "环节": "领域基础认知",
            "AI输出": self._generate_basic_cognition(),
            "提问": "以上基础认知是否清晰？是否需要补充某部分的内容？",
            "选项": [
                {"label": "A. 基本清晰，继续下一步", "value": "清晰"},
                {"label": "B. 需要补充...", "value": "需要补充"}
            ],
            "记录键": "基础认知确认"
        }
    
    def _get_user_group_task(self) -> Dict[str, Any]:
        """环节2：目标用户群体锁定"""
        groups = self._generate_target_groups()
        
        return {
            "阶段": "目标用户群体锁定",
            "环节": "目标用户群体",
            "AI输出": self._format_user_groups(groups),
            "提问": "请你从以上3个群体中，选择1个你最想服务的核心目标用户群体",
            "选项": [
                {"label": f"A. {groups[0]['标签']}", "value": groups[0]["标签"]},
                {"label": f"B. {groups[1]['标签']}", "value": groups[1]["标签"]},
                {"label": f"C. {groups[2]['标签']}", "value": groups[2]["标签"]},
                {"label": "D. 其他群体", "value": "其他"}
            ],
            "记录键": "目标用户群体"
        }
    
    def _get_pain_point_task(self) -> Dict[str, Any]:
        """环节3：需求与痛点深度拆解"""
        pain_points = self._generate_pain_points()
        
        return {
            "阶段": "需求与痛点深度拆解",
            "环节": "需求痛点拆解",
            "AI输出": self._format_pain_points(pain_points),
            "提问": "以上拆解的需求与痛点中，你最想切入解决的核心方向是哪一个？",
            "选项": [
                {"label": f"A. {pain_points[0]['核心方向']}", "value": pain_points[0]["核心方向"]},
                {"label": f"B. {pain_points[1]['核心方向']}", "value": pain_points[1]["核心方向"]},
                {"label": f"C. {pain_points[2]['核心方向']}", "value": pain_points[2]["核心方向"]},
                {"label": "D. 其他方向", "value": "其他"}
            ],
            "记录键": "核心痛点方向"
        }
    
    def _get_solution_task(self) -> Dict[str, Any]:
        """环节4：轻量化解决方案匹配"""
        solutions = self._generate_solutions()
        
        return {
            "阶段": "轻量化解决方案匹配",
            "环节": "解决方案匹配",
            "AI输出": self._format_solutions(solutions),
            "提问": "请你从以上3个方案中，选择1个你最想落地的核心解决方案",
            "选项": [
                {"label": f"A. {solutions[0]['名称']}", "value": solutions[0]["名称"]},
                {"label": f"B. {solutions[1]['名称']}", "value": solutions[1]["名称"]},
                {"label": f"C. {solutions[2]['名称']}", "value": solutions[2]["名称"]},
                {"label": "D. 其他方案", "value": "其他"}
            ],
            "记录键": "选定方案"
        }
    
    def _get_closed_loop_task(self) -> Dict[str, Any]:
        """环节5：最小商业闭环完整设计"""
        closed_loop = self._generate_closed_loop()
        
        return {
            "阶段": "最小商业闭环完整设计",
            "环节": "闭环设计",
            "AI输出": self._format_closed_loop(closed_loop),
            "提问": "以上闭环设计是否符合你的预期？是否需要针对某部分进行优化调整？",
            "选项": [
                {"label": "A. 符合预期，继续", "value": "符合预期"},
                {"label": "B. 需要调整...", "value": "需要调整"}
            ],
            "记录键": "闭环设计确认"
        }
    
    def _get_final_output_task(self) -> Dict[str, Any]:
        """环节6：最终方案输出"""
        return {
            "阶段": "最终方案输出",
            "环节": "最终方案",
            "AI输出": self._generate_final_plan(),
            "提问": "方案已完成。你对这个方案满意吗？是否需要进一步优化？",
            "选项": [
                {"label": "A. 满意，完成", "value": "满意"},
                {"label": "B. 需要优化", "value": "需要优化"}
            ],
            "记录键": "最终确认",
            "是最终环节": True
        }
    
    # ========== 内容生成方法 ==========
    
    def _generate_basic_cognition(self) -> str:
        """生成基础认知内容"""
        target = self.core_target
        
        # 根据目标领域生成基础认知
        cognition_parts = [
            f"## 【{target}】基础认知",
            "",
            "### 一、核心定义",
            f"{target}是指...",
            "",
            "### 二、主流玩法与盈利模式",
            "1. 模式A：...（收益来源：...）",
            "2. 模式B：...（收益来源：...）",
            "3. 模式C：...（收益来源：...）",
            "",
            "### 三、对应你目标的门槛与注意事项",
            f"- 适合你的轻量化切入点：...",
            f"- 需要避开的坑：...",
            f"- 最小启动所需：..."
        ]
        
        return "\n".join(cognition_parts)
    
    def _generate_target_groups(self) -> List[Dict[str, Any]]:
        """生成目标用户群体（嵌入约束条件）"""
        target = self.core_target
        params = self.constraint_params
        
        # 根据约束条件调整用户群体
        # 预算越低，越适合选择时间灵活、付费意愿稳定的群体
        groups = [
            {
                "标签": "职场新人/副业刚需",
                "核心特征": "25-32岁，工作1-5年，有稳定收入但想开拓副业",
                "核心场景": "下班后、周末时间操作",
                "付费潜力": "中等，单价 sensitive",
                "匹配度": self._calc_match_score("职场新人", params)
            },
            {
                "标签": "全职妈妈/灵活就业",
                "核心特征": "28-40岁，需要兼顾家庭，时间碎片化",
                "核心场景": "孩子上学后、晚间时间",
                "付费潜力": "中等，注重性价比",
                "匹配度": self._calc_match_score("全职妈妈", params)
            },
            {
                "标签": "小镇青年/下沉市场",
                "核心特征": "22-35岁，在二三线城市，追求额外收入",
                "核心场景": "晚间、节假日",
                "付费潜力": "较低，价格敏感",
                "匹配度": self._calc_match_score("小镇青年", params)
            }
        ]
        
        # 按匹配度排序
        groups.sort(key=lambda x: x.get("匹配度", 0), reverse=True)
        
        return groups
    
    def _calc_match_score(self, group_type: str, params: Dict) -> float:
        """计算用户群体与约束的匹配度"""
        score = 50  # 基础分
        budget = params.get("预算上限", 999999)
        
        # 预算越低，越适合选择价格不敏感的群体
        if budget == 0:
            if group_type in ["职场新人"]:
                score += 30  # 有稳定收入，愿意尝试
            elif group_type in ["全职妈妈"]:
                score += 20  # 精打细算但愿意为孩子付费
        elif budget <= 5000:
            score += 20
        
        return score
    
    def _format_user_groups(self, groups: List[Dict]) -> str:
        """格式化用户群体输出"""
        lines = ["## 3个最易落地的核心目标用户群体", ""]
        
        for i, g in enumerate(groups, 1):
            lines.append(f"### {i}. {g['标签']}")
            lines.append(f"   - 核心特征：{g['核心特征']}")
            lines.append(f"   - 核心场景：{g['核心场景']}")
            lines.append(f"   - 付费潜力：{g['付费潜力']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_pain_points(self) -> List[Dict[str, Any]]:
        """生成痛点分析"""
        target = self.core_target
        
        return [
            {
                "核心方向": "获客难/流量获取",
                "表层痛点": "不知道从哪里找客户",
                "底层痛点": "没有流量渠道，不懂引流方法"
            },
            {
                "核心方向": "变现难/转化率低",
                "表层痛点": "有人看但没人买",
                "底层痛点": "不懂销售转化，缺少信任背书"
            },
            {
                "核心方向": "启动难/门槛高",
                "表层痛点": "想做但不知道怎么做",
                "底层痛点": "缺少方法论指引，不知道从哪开始"
            }
        ]
    
    def _format_pain_points(self, pain_points: List[Dict]) -> str:
        """格式化痛点输出"""
        lines = ["## 需求与痛点深度拆解", ""]
        
        for p in pain_points:
            lines.append(f"### {p['核心方向']}")
            lines.append(f"   - 表层痛点：{p['表层痛点']}")
            lines.append(f"   - 底层痛点：{p['底层痛点']}")
            lines.append("")
        
        lines.append("### 机会点")
        lines.append("当前市场现有方案的核心不足与可切入的机会点...")
        
        return "\n".join(lines)
    
    def _generate_solutions(self) -> List[Dict[str, Any]]:
        """生成解决方案（基于约束参数）"""
        params = self.constraint_params
        budget = self.预算
        
        # 使用约束参数生成符合预算和周期的方案
        solutions = []
        
        # 方案1：零成本方案
        if params["预算上限"] >= 0:
            solutions.append({
                "名称": "知识付费分销/推广",
                "核心价值": "利用现有资源进行推广变现，无需前期投入",
                "差异化优势": "零成本启动，风险最低",
                "落地难度": "低",
                "成本": "0",
                "周期": "1-2周"
            })
        
        # 方案2：低成本方案
        if params["预算上限"] >= 500:
            solutions.append({
                "名称": "标准化工具/SOP模板",
                "核心价值": "提供可复用的标准化工具，提升效率",
                "差异化优势": "一次制作，长期使用",
                "落地难度": "中",
                "成本": "500元内",
                "周期": "2-4周"
            })
        
        # 方案3：中等成本方案
        if params["预算上限"] >= 2000 and params["周期上限"] >= 1:
            solutions.append({
                "名称": "私教/陪跑服务",
                "核心价值": "提供一对一深度指导，保证效果",
                "差异化优势": "高客单价，可持续复购",
                "落地难度": "中",
                "成本": "2000元内",
                "周期": "1个月"
            })
        
        # 如果过滤后为空，至少返回一个方案
        if not solutions:
            solutions.append({
                "名称": "资源整合方案",
                "核心价值": "整合现有资源进行变现",
                "差异化优势": "灵活适配任何预算",
                "落地难度": "中",
                "成本": "视资源情况",
                "周期": "1-3个月"
            })
        
        return solutions
    
    def _format_solutions(self, solutions: List[Dict]) -> str:
        """格式化解决方案输出"""
        lines = ["## 3个符合约束的轻量化解决方案", ""]
        
        for i, s in enumerate(solutions, 1):
            lines.append(f"### {i}. {s['名称']}")
            lines.append(f"   - 核心价值：{s['核心价值']}")
            lines.append(f"   - 差异化优势：{s['差异化优势']}")
            lines.append(f"   - 落地难度：{s['落地难度']}")
            lines.append(f"   - 预估成本：{s['成本']}")
            lines.append(f"   - 预估周期：{s['周期']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_closed_loop(self) -> Dict[str, Any]:
        """生成闭环设计"""
        return {
            "核心逻辑": "引流 → 价值传递 → 信任建立 → 转化 → 复购",
            "环节": [
                {
                    "名称": "引流获客",
                    "最低成本渠道": "短视频/内容平台",
                    "可用资源": "免费内容引流"
                },
                {
                    "名称": "价值传递",
                    "最低成本渠道": "私域/社群",
                    "可用资源": "免费内容/低价产品"
                },
                {
                    "名称": "信任建立",
                    "最低成本渠道": "案例展示/口碑",
                    "可用资源": "用户见证/专业知识"
                },
                {
                    "名称": "转化成交",
                    "最低成本渠道": "私聊/社群发售",
                    "可用资源": "标准化话术"
                }
            ],
            "盈利模式": "产品带货/服务变现/佣金分成",
            "定价标准": "根据你选择的方案确定",
            "验证周期": "2-4周",
            "验证指标": "获客成本 < 10元 / 转化率 > 3% / 复购率 > 10%",
            "迭代方向": "验证成功后扩大流量渠道",
            "调整预案": "如果验证不达标，调整引流渠道或优化转化话术"
        }
    
    def _format_closed_loop(self, closed_loop: Dict) -> str:
        """格式化闭环输出"""
        lines = [
            "## 最小商业闭环完整设计",
            "",
            f"### 核心逻辑",
            closed_loop["核心逻辑"],
            "",
            "### 各环节设计"
        ]
        
        for step in closed_loop["环节"]:
            lines.append(f"#### {step['名称']}")
            lines.append(f"   - 最低成本渠道：{step['最低成本渠道']}")
            lines.append(f"   - 可用资源：{step['可用资源']}")
            lines.append("")
        
        lines.append(f"### 盈利模式")
        lines.append(closed_loop["盈利模式"])
        lines.append("")
        
        lines.append(f"### 定价标准")
        lines.append(closed_loop["定价标准"])
        lines.append("")
        
        lines.append(f"### 验证指标")
        lines.append(f"   - 最小验证周期：{closed_loop['验证周期']}")
        lines.append(f"   - 核心验证成功指标：{closed_loop['验证指标']}")
        lines.append("")
        
        lines.append(f"### 迭代与调整")
        lines.append(f"   - 验证达标后：{closed_loop['迭代方向']}")
        lines.append(f"   - 验证不达标：{closed_loop['调整预案']}")
        
        return "\n".join(lines)
    
    def _generate_final_plan(self) -> str:
        """生成最终方案"""
        return """
## 最终落地方案

基于以上所有环节的分析与选择，为你生成以下完整落地方案：

### 方案概述
（此处整合前面所有选择，形成完整方案）

### 立即可执行的动作清单
1. [ ] 动作1
2. [ ] 动作2
3. [ ] 动作3

### 关键里程碑
- 第1周：完成...
- 第2周：完成...
- 第3-4周：完成...

### 下一步建议
（给出具体的下一步行动建议）

---
**方案生成完成，祝你落地顺利！**
"""
    
    def get_progress(self, current_phase: StrangerPhase) -> Dict[str, Any]:
        """获取进度"""
        total = len(StrangerPhase) - 2  # 减去等待和完成
        current = current_phase.value
        
        return {
            "当前阶段": f"完全陌生模式 ({current_phase.name})",
            "进度": int((current / 6) * 100),
            "预估剩余": max(0, 6 - current)
        }


def create_stranger_executor(user_profile: Dict[str, str]) -> StrangerModeExecutor:
    """创建陌生模式执行器"""
    constraints = {
        "预算约束": user_profile.get("预算约束", ""),
        "周期约束": user_profile.get("周期约束", "")
    }
    return StrangerModeExecutor(user_profile, constraints)
