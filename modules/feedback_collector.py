"""
用户反馈收集模块
落地结果追踪系统
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class FeedbackStatus(Enum):
    """反馈状态"""
    待跟进 = "待跟进"
    已联系 = "已联系"
    已落地 = "已落地"
    已放弃 = "已放弃"
    延期 = "延期"


class ImplementationResult(Enum):
    """落地结果"""
    大成功 = "大成功"  # 超预期
    成功 = "成功"      # 符合预期
    部分成功 = "部分成功"  # 有进展但未达预期
    失败 = "失败"      # 完全未落地
    未知 = "未知"


@dataclass
class UserFeedback:
    """用户反馈数据"""
    session_id: str
    user_id: Optional[str]
    方案名称: str
    反馈时间: str
    状态: str
    预期落地时间: str
    实际落地时间: Optional[str]
    落地结果: Optional[str]
    收入元: Optional[int]
    满意度: Optional[int]  # 1-5
    用户反馈内容: str
    改进建议: str


class FeedbackCollector:
    """用户反馈收集器"""
    
    def __init__(self, data_dir: str = "E:/学习/MVP/demand-miner/data"):
        self.data_dir = Path(data_dir)
        self.feedback_dir = self.data_dir / "feedbacks"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
    
    # ========== 反馈记录 ==========
    
    def create_followup(self, session_id: str, 方案名称: str, 
                      预期落地时间: str) -> str:
        """创建跟进记录"""
        feedback_id = f"fb_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        feedback = {
            "feedback_id": feedback_id,
            "session_id": session_id,
            "方案名称": 方案名称,
            "创建时间": datetime.now().isoformat() + "Z",
            "预期落地时间": 预期落地时间,
            "状态": FeedbackStatus.待跟进.value,
            "实际落地时间": None,
            "落地结果": None,
            "收入元": None,
            "满意度": None,
            "用户反馈内容": "",
            "改进建议": "",
            "跟进记录": []
        }
        
        # 保存
        feedback_file = self.feedback_dir / f"{feedback_id}.json"
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, ensure_ascii=False, indent=2)
        
        return feedback_id
    
    def update_feedback(self, feedback_id: str, updates: Dict[str, Any]) -> bool:
        """更新反馈"""
        feedback_file = self.feedback_dir / f"{feedback_id}.json"
        
        if not feedback_file.exists():
            return False
        
        with open(feedback_file, 'r', encoding='utf-8') as f:
            feedback = json.load(f)
        
        feedback.update(updates)
        feedback["更新时间"] = datetime.now().isoformat() + "Z"
        
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, ensure_ascii=False, indent=2)
        
        return True
    
    def add跟进记录(self, feedback_id: str, record: Dict[str, Any]) -> bool:
        """添加跟进记录"""
        feedback_file = self.feedback_dir / f"{feedback_id}.json"
        
        if not feedback_file.exists():
            return False
        
        with open(feedback_file, 'r', encoding='utf-8') as f:
            feedback = json.load(f)
        
        if "跟进记录" not in feedback:
            feedback["跟进记录"] = []
        
        record["时间"] = datetime.now().isoformat() + "Z"
        feedback["跟进记录"].append(record)
        
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, ensure_ascii=False, indent=2)
        
        return True
    
    # ========== 跟进管理 ==========
    
    def get_pending_followups(self, days_ahead: int = 7) -> List[Dict]:
        """获取待跟进列表"""
        from dateutil import parser as dateparser
        
        followups = []
        cutoff = datetime.now() + timedelta(days=days_ahead)
        
        for f in self.feedback_dir.glob("*.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                fb = json.load(fp)
                
                # 只看待跟进状态的
                if fb.get("状态") != FeedbackStatus.待跟进.value:
                    continue
                
                # 检查是否到期
                expected = fb.get("预期落地时间")
                if expected:
                    expected_date = dateparser.parse(expected)
                    if expected_date <= cutoff:
                        followups.append({
                            "feedback_id": fb["feedback_id"],
                            "session_id": fb["session_id"],
                            "方案名称": fb["方案名称"],
                            "预期落地时间": expected,
                            "已超时": expected_date < datetime.now()
                        })
        
        return sorted(followups, key=lambda x: x["预期落地时间"])
    
    def get_overdue_followups(self) -> List[Dict]:
        """获取逾期未跟进的列表"""
        return self.get_pending_followups(days_ahead=0)
    
    # ========== 统计与分析 ==========
    
    def get_feedback_stats(self, days: int = 30) -> Dict[str, Any]:
        """获取反馈统计"""
        from dateutil import parser as dateparser
        
        cutoff = datetime.now() - timedelta(days=days)
        
        feedbacks = []
        for f in self.feedback_dir.glob("*.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                fb = json.load(fp)
                created = dateparser.parse(fb.get("创建时间", ""))
                if created >= cutoff:
                    feedbacks.append(fb)
        
        # 状态分布
        status_dist = {}
        result_dist = {}
        
        for fb in feedbacks:
            status = fb.get("状态", "未知")
            status_dist[status] = status_dist.get(status, 0) + 1
            
            result = fb.get("落地结果")
            if result:
                result_dist[result] = result_dist.get(result, 0) + 1
        
        # 计算落地率
        total_with_result = sum(result_dist.values())
        success_count = result_dist.get("成功", 0) + result_dist.get("大成功", 0)
        success_rate = round(success_count / total_with_result * 100, 1) if total_with_result > 0 else 0
        
        # 计算平均满意度
        satisfactions = [fb.get("满意度") for fb in feedbacks if fb.get("满意度")]
        avg_satisfaction = round(sum(satisfactions) / len(satisfactions), 1) if satisfactions else 0
        
        # 计算平均收入
        incomes = [fb.get("收入元") for fb in feedbacks if fb.get("收入元") is not None]
        avg_income = round(sum(incomes) / len(incomes), 0) if incomes else 0
        
        return {
            "统计周期": f"最近{days}天",
            "总会话数": len(feedbacks),
            "状态分布": status_dist,
            "落地结果分布": result_dist,
            "落地率": f"{success_rate}%",
            "平均满意度": avg_satisfaction,
            "平均收入元": avg_income
        }
    
    def get_implementation_analysis(self) -> Dict[str, Any]:
        """获取落地分析报告"""
        all_feedbacks = []
        
        for f in self.feedback_dir.glob("*.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                all_feedbacks.append(json.load(fp))
        
        # 按方案分组
        scheme_stats = {}
        
        for fb in all_feedbacks:
            scheme = fb.get("方案名称", "未知")
            if scheme not in scheme_stats:
                scheme_stats[scheme] = {
                    "总数": 0,
                    "成功": 0,
                    "失败": 0,
                    "总收入": 0
                }
            
            scheme_stats[scheme]["总数"] += 1
            
            result = fb.get("落地结果")
            if result in ["成功", "大成功"]:
                scheme_stats[scheme]["成功"] += 1
            elif result == "失败":
                scheme_stats[scheme]["失败"] += 1
            
            income = fb.get("收入元")
            if income:
                scheme_stats[scheme]["总收入"] += income
        
        # 计算各方案成功率
        for scheme, stats in scheme_stats.items():
            if stats["总数"] > 0:
                stats["成功率"] = round(stats["成功"] / stats["总数"] * 100, 1)
            else:
                stats["成功率"] = 0
        
        return {
            "方案分析": scheme_stats,
            "最佳方案": max(scheme_stats.items(), key=lambda x: x[1].get("成功率", 0)) if scheme_stats else None
        }


# 跟进提醒模板
FOLLOWUP_TEMPLATES = {
    "3天": {
        "title": "方案落地进度确认",
        "message": "您好！距您上次获取方案已经3天了，想了解一下方案的落地进展如何？有没有开始执行？遇到什么困难？"
    },
    "7天": {
        "title": "落地结果回访",
        "message": "您好！一周过去了，想请您分享一下方案的实际落地情况。无论结果如何，您的反馈对我都非常重要。"
    },
    "14天": {
        "title": "效果复盘邀请",
        "message": "您好！已经两周了，想邀请您进行一次效果复盘。成功经验我们可以继续放大，失败经验我们也可以从中学习改进。"
    },
    "30天": {
        "title": "月度跟踪回访",
        "message": "您好！距离我们上次沟通已经一个月了，想了解一下方案的长期执行情况和最终结果。"
    }
}


# 全局实例
_feedback_collector = None

def get_feedback_collector() -> FeedbackCollector:
    """获取反馈收集器单例"""
    global _feedback_collector
    if _feedback_collector is None:
        _feedback_collector = FeedbackCollector()
    return _feedback_collector
