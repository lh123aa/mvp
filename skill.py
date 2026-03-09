"""
Demand Miner 标准 Skill 实现
将原有模块整合为单一入口的skill项目
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class UserConstraints:
    """用户约束条件"""
    budget_constraint: str = ""
    period_constraint: str = ""
    core_target: str = ""
    budget_limit: Optional[int] = None
    period_limit: Optional[int] = None


class ConstraintFilter:
    """约束过滤器"""
    
    BUDGET_MAP = {
        "0成本": 0,
        "5000元内": 5000,
        "5000-20000元": 20000,
        "20000以上": 999999
    }
    
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


class SkillProcessor:
    """技能处理器"""
    
    def __init__(self):
        self.session_data = {}
        self.current_step = 0
        self.user_profile = {}
        self.analysis_result = {}
        
        # 扩展行业模板
        self.extended_industries = {
            "跨境电商": {
                "用户群体": ["海归", "留学生", "有货源的工厂主", "电商从业者"],
                "轻量化方案": [
                    {"名称": "一件代发", "成本": "1000", "周期": "1个月"},
                    {"名称": "独立站Dropshipping", "成本": "3000", "周期": "2个月"},
                    {"名称": "亚马逊FBA试水", "成本": "10000", "周期": "3个月"}
                ],
                "常见痛点": ["物流难", "语言障碍", "选品困难", "规则变化快"],
                "验证指标": {
                    "及格": "月销售额>500美元",
                    "良好": "月销售额>2000美元",
                    "优秀": "月销售额>10000美元"
                }
            },
            "AI服务": {
                "用户群体": ["企业主", "程序员", "设计师", "内容创作者"],
                "轻量化方案": [
                    {"名称": "AI提示词分享", "成本": "0", "周期": "1周"},
                    {"名称": "AI工具测评", "成本": "200", "周期": "2周"},
                    {"名称": "AI应用定制", "成本": "3000", "周期": "1个月"}
                ],
                "常见痛点": ["技术门槛高", "应用场景不清", "变现模式不明"],
                "验证指标": {
                    "及格": "付费用户>20人",
                    "良好": "付费用户>100人",
                    "优秀": "付费用户>500人"
                }
            }
        }
    
    def process_request(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        处理请求的主要入口函数
        :param user_input: 用户输入
        :param context: 上下文信息
        :return: 处理结果
        """
        try:
            # 解析用户意图
            intent = self._identify_intent(user_input)
            
            if intent == "分析启动":
                return self._start_analysis(user_input)
            elif intent == "继续分析":
                return self._continue_analysis(user_input)
            else:
                return self._handle_general_request(user_input)
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"处理请求时发生错误: {str(e)}",
                "skill_name": "demand-miner"
            }
    
    def _identify_intent(self, user_input: str) -> str:
        """识别用户意图"""
        user_input_lower = user_input.lower()
        
        # 分析启动意图关键词
        analysis_keywords = ["项目分析", "商业分析", "需求挖掘", "商业模式", "创业分析", "副业规划", "产品分析"]
        
        for keyword in analysis_keywords:
            if keyword in user_input_lower:
                return "分析启动"
        
        # 判断是否为继续分析
        if hasattr(self, 'analysis_in_progress') and self.analysis_in_progress:
            return "继续分析"
        
        return "general"
    
    def _start_analysis(self, user_input: str) -> Dict[str, Any]:
        """开始分析流程"""
        # 初始化会话
        session_id = f"skill_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}"
        self.session_data[session_id] = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "user_input": user_input,
            "current_phase": "start",
            "user_profile": {}
        }
        
        # 识别核心目标
        core_target = self._extract_core_target(user_input)
        
        # 开始前置对齐流程
        alignment_result = self._run_pre_alignment(user_input, core_target)
        
        # 执行深度分析
        analysis_result = self._perform_analysis(alignment_result)
        
        # 生成最终报告
        report = self._generate_report(alignment_result, analysis_result)
        
        return {
            "status": "success",
            "skill_name": "demand-miner",
            "type": "analysis_result",
            "session_id": session_id,
            "alignment_result": alignment_result,
            "analysis_result": analysis_result,
            "final_report": report
        }
    
    def _extract_core_target(self, user_input: str) -> str:
        """提取核心目标"""
        # 简化实现，实际可使用更复杂的NLP方法
        if "项目" in user_input:
            return "项目分析"
        elif "商业" in user_input:
            return "商业模式"
        elif "创业" in user_input:
            return "创业分析"
        elif "副业" in user_input:
            return "副业规划"
        else:
            return "需求分析"
    
    def _run_pre_alignment(self, user_input: str, core_target: str) -> Dict[str, Any]:
        """执行前置对齐流程"""
        # 这里简化实现，实际应该按顺序询问4个问题
        return {
            "核心目标": core_target,
            "核心目的": self._infer_purpose(user_input),
            "认知层级": self._infer_cognition_level(user_input),
            "预算约束": self._infer_budget(user_input),
            "周期约束": self._infer_period(user_input)
        }
    
    def _infer_purpose(self, user_input: str) -> str:
        """推断用户目的"""
        if "副业" in user_input:
            return "副业试水"
        elif "创业" in user_input or "商业" in user_input:
            return "创业立项"
        elif "研究" in user_input or "学习" in user_input:
            return "行业研究学习"
        else:
            return "创业立项"
    
    def _infer_cognition_level(self, user_input: str) -> str:
        """推断认知层级"""
        # 简化推断，实际可使用更复杂的逻辑
        return "完全陌生"  # 默认为完全陌生，因为是初次分析
    
    def _infer_budget(self, user_input: str) -> str:
        """推断预算"""
        if "0成本" in user_input or "零成本" in user_input:
            return "0成本"
        elif "小投入" in user_input or "低成本" in user_input:
            return "5000元内"
        else:
            return "5000元内"  # 默认预算
    
    def _infer_period(self, user_input: str) -> str:
        """推断周期"""
        if "快速" in user_input or "短期" in user_input:
            return "1个月"
        else:
            return "3个月"  # 默认周期
    
    def _perform_analysis(self, alignment_result: Dict[str, Any]) -> Dict[str, Any]:
        """执行深度分析"""
        core_target = alignment_result.get("核心目标", "")
        
        # 初始化约束过滤器
        constraints = UserConstraints(
            budget_constraint=alignment_result.get("预算约束", ""),
            period_constraint=alignment_result.get("周期约束", ""),
            core_target=core_target
        )
        constraint_filter = ConstraintFilter(constraints)
        
        # 获取行业数据
        industry_data = self.extended_industries.get(core_target, self.extended_industries.get("AI服务", {}))
        
        # 应用约束过滤
        if "轻量化方案" in industry_data:
            filtered_solutions = constraint_filter.filter_options(industry_data["轻量化方案"])
        else:
            # 默认方案
            default_solutions = [
                {"名称": "知识付费分销", "成本": "0", "周期": "1周"},
                {"名称": "内容创作", "成本": "0", "周期": "2周"},
                {"名称": "咨询服务", "成本": "500", "周期": "2周"}
            ]
            filtered_solutions = constraint_filter.filter_options(default_solutions)
        
        # 生成分析结果
        return {
            "核心认知": f"{core_target}的核心概念、主流玩法和发展趋势",
            "目标用户": self._get_target_users(alignment_result),
            "痛点分析": self._get_pain_points(alignment_result),
            "解决方案": filtered_solutions,
            "商业闭环": self._get_closed_loop(alignment_result),
            "验证指标": self._get_verification_metrics(alignment_result)
        }
    
    def _get_target_users(self, alignment_result: Dict[str, Any]) -> List[str]:
        """获取目标用户"""
        budget = alignment_result.get("预算约束", "")
        
        if "0成本" in budget:
            return [
                "职场新人 - 有稳定收入愿意尝试",
                "全职妈妈 - 精打细算但有需求",
                "学生群体 - 时间多但资金有限"
            ]
        else:
            return [
                "职场新人",
                "全职妈妈", 
                "有特定需求的用户群体"
            ]
    
    def _get_pain_points(self, alignment_result: Dict[str, Any]) -> List[Dict[str, str]]:
        """获取痛点分析"""
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
    
    def _get_closed_loop(self, alignment_result: Dict[str, Any]) -> Dict[str, Any]:
        """获取商业闭环设计"""
        return {
            "核心逻辑": "引流 → 价值传递 → 信任建立 → 转化 → 复购",
            "关键环节": [
                {"名称": "引流获客", "渠道": "内容平台/社群", "资源": "免费内容引流"},
                {"名称": "价值传递", "渠道": "私域/社群", "资源": "免费内容/低价产品"},
                {"名称": "信任建立", "渠道": "案例展示/口碑", "资源": "用户见证/专业知识"},
                {"名称": "转化成交", "渠道": "私聊/社群发售", "资源": "标准化话术"}
            ],
            "盈利模式": "产品带货/服务变现/佣金分成",
            "验证周期": "2-4周",
            "验证指标": "获客成本 < 10元 / 转化率 > 3% / 复购率 > 10%",
            "迭代方向": "验证成功后扩大流量渠道",
            "调整预案": "如果验证不达标，调整引流渠道或优化转化话术"
        }
    
    def _get_verification_metrics(self, alignment_result: Dict[str, Any]) -> Dict[str, str]:
        """获取验证指标"""
        return {
            "及格": "初步验证通过",
            "良好": "达到预期效果", 
            "优秀": "超出预期效果"
        }
    
    def _generate_report(self, alignment_result: Dict[str, Any], analysis_result: Dict[str, Any]) -> str:
        """生成最终报告"""
        report = [
            "# 需求挖掘与最小商业闭环分析报告",
            "",
            "## 用户画像",
            f"- 核心目标: {alignment_result.get('核心目标', '未知')}",
            f"- 核心目的: {alignment_result.get('核心目的', '未知')}",
            f"- 认知层级: {alignment_result.get('认知层级', '未知')}",
            f"- 预算约束: {alignment_result.get('预算约束', '未知')}",
            f"- 周期约束: {alignment_result.get('周期约束', '未知')}",
            "",
            "## 核心认知", 
            f"{analysis_result.get('核心认知', '待分析')}",
            "",
            "## 目标用户群体", 
        ]
        
        for i, user in enumerate(analysis_result.get('目标用户', []), 1):
            report.append(f"{i}. {user}")
        
        report.append("\n## 痛点分析")
        for pain_point in analysis_result.get('痛点分析', []):
            report.append(f"### {pain_point['核心方向']}")
            report.append(f"- 表层痛点: {pain_point['表层痛点']}")
            report.append(f"- 底层痛点: {pain_point['底层痛点']}")
        
        report.append("\n## 解决方案")
        for i, solution in enumerate(analysis_result.get('解决方案', []), 1):
            report.append(f"### 方案{i}: {solution['名称']}")
            report.append(f"- 成本: {solution['成本']}")
            report.append(f"- 周期: {solution['周期']}")
        
        report.append("\n## 最小商业闭环")
        closed_loop = analysis_result.get('商业闭环', {})
        report.append(f"**核心逻辑**: {closed_loop.get('核心逻辑', '待设计')}")
        
        report.append("\n**关键环节**:")
        for step in closed_loop.get('关键环节', []):
            report.append(f"- {step['名称']}: 通过{step['渠道']}使用{step['资源']}")
        
        report.append(f"\n**盈利模式**: {closed_loop.get('盈利模式', '待确定')}")
        report.append(f"**验证指标**: {closed_loop.get('验证指标', '待确定')}")
        
        return "\n".join(report)
    
    def _handle_general_request(self, user_input: str) -> Dict[str, Any]:
        """处理一般请求"""
        return {
            "status": "success",
            "skill_name": "demand-miner",
            "type": "general_response",
            "message": f"已收到您的请求: {user_input}",
            "capabilities": [
                "项目分析",
                "商业分析", 
                "需求挖掘",
                "商业模式设计",
                "最小商业闭环规划"
            ]
        }


# 全局处理器实例
processor = SkillProcessor()


def handle_request(user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Skill 标准入口函数
    :param user_input: 用户输入
    :param context: 上下文信息
    :return: 处理结果
    """
    return processor.process_request(user_input, context)


def can_handle_query(query: str) -> bool:
    """
    判断是否能处理查询
    :param query: 查询字符串
    :return: 是否能处理
    """
    query_lower = query.lower()
    trigger_keywords = [
        "产品分析", "项目分析", "商业分析", "商业闭环", 
        "需求挖掘", "商业模式", "创业分析", "副业规划"
    ]
    
    return any(keyword in query_lower for keyword in trigger_keywords)


def get_skill_info() -> Dict[str, Any]:
    """
    获取skill信息
    :return: skill信息
    """
    return {
        "name": "demand-miner",
        "version": "1.0.0",
        "description": "需求挖掘与最小商业闭环分析Skill",
        "trigger_keywords": [
            "产品分析", "项目分析", "商业分析", "商业闭环", 
            "需求挖掘", "商业模式", "创业分析", "副业规划"
        ],
        "capabilities": [
            "用户画像构建",
            "目标用户分析",
            "痛点挖掘",
            "解决方案匹配",
            "商业闭环设计",
            "验证指标制定"
        ]
    }
