"""
自动复盘模块
对话结束后自动生成复盘小结
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import Counter


class AutoReviewer:
    """自动复盘器"""
    
    def __init__(self, data_dir: str = "E:/学习/MVP/demand-miner/data"):
        self.data_dir = Path(data_dir)
        self.sessions_dir = self.data_dir / "sessions"
        self.reviews_dir = self.data_dir / "reviews"
        self.reviews_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_review(self, session_id: str) -> Dict[str, Any]:
        """生成单次对话的复盘"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return {"error": "Session not found"}
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session = json.load(f)
        
        review = {
            "session_id": session_id,
            "复盘时间": datetime.now().isoformat() + "Z",
            "用户画像": session.get("user_profile", {}),
            "流程路径": self._analyze_flow_path(session),
            "交互质量": self._analyze_interaction_quality(session),
            "输出质量": self._analyze_output_quality(session),
            "发现亮点": self._discover_highlights(session),
            "发现问题": self._discover_issues(session),
            "优化建议": self._generate_suggestions(session),
            "元数据": {
                "总轮次": session.get("metadata", {}).get("总轮次", 0),
                "总耗时_分钟": session.get("metadata", {}).get("总耗时_分钟", 0),
                "是否完成": "completed_at" in session,
                "用户满意度": session.get("final_output", {}).get("满意度", "未评价")
            }
        }
        
        self._save_review(review)
        
        return review
    
    def _analyze_flow_path(self, session: Dict) -> Dict[str, Any]:
        """分析流程路径"""
        history = session.get("history", [])
        phases = [h.get("阶段", "") for h in history]
        phase_counts = Counter(phases)
        
        return {
            "经过的阶段": list(phase_counts.keys()),
            "各阶段轮次": dict(phase_counts),
            "完整路径": " → ".join(phases) if phases else "无"
        }
    
    def _analyze_interaction_quality(self, session: Dict) -> Dict[str, Any]:
        """分析交互质量"""
        history = session.get("history", [])
        
        dont_know_count = 0
        skip_count = 0
        feedback_count = 0
        
        for h in history:
            answer = h.get("用户回答", "")
            if any(kw in answer for kw in ["不知道", "不懂", "不太清楚", "说不清"]):
                dont_know_count += 1
            
            feedback = h.get("用户反馈", "")
            if feedback:
                feedback_count += 1
        
        return {
            "有效交互轮次": len(history),
            "用户表示不知道次数": dont_know_count,
            "用户反馈次数": feedback_count,
            "平均每轮信息量": "待评估"
        }
    
    def _analyze_output_quality(self, session: Dict) -> Dict[str, Any]:
        """分析输出质量"""
        final_output = session.get("final_output", {})
        
        return {
            "最终方案是否生成": bool(final_output.get("内容", "")),
            "用户确认": final_output.get("用户确认", ""),
            "满意度": final_output.get("满意度", "未评价")
        }
    
    def _discover_highlights(self, session: Dict) -> List[str]:
        """发现亮点"""
        highlights = []
        
        history = session.get("history", [])
        if len(history) >= 6:
            highlights.append("完成了完整的对话流程")
        
        profile = session.get("user_profile", {})
        if all(profile.get(k) for k in ["核心目标", "核心目的", "认知层级", "预算约束"]):
            highlights.append("用户画像信息完整")
        
        final = session.get("final_output", {})
        if final.get("用户确认") == "符合预期":
            highlights.append("用户对方案表示认可")
        
        return highlights
    
    def _discover_issues(self, session: Dict) -> List[str]:
        """发现问题"""
        issues = []
        
        history = session.get("history", [])
        dont_know_turns = []
        
        for h in history:
            answer = h.get("用户回答", "")
            if any(kw in answer for kw in ["不知道", "不懂", "不太清楚"]):
                dont_know_turns.append(h.get("环节", ""))
        
        if len(dont_know_turns) >= 2:
            issues.append(f"用户多次表示不知道: {', '.join(dont_know_turns)}")
        
        if session.get("metadata", {}).get("用户中途放弃"):
            issues.append("用户中途放弃")
        
        final = session.get("final_output", {})
        if final.get("满意度") == "不满意":
            issues.append("用户对最终方案表示不满意")
        
        if session.get("user_profile", {}).get("认知层级") == "资深从业者":
            if history and len(history[0].get("用户回答", "")) < 20:
                issues.append("资深从业者模式开场问题可能过于抽象")
        
        return issues
    
    def _generate_suggestions(self, session: Dict) -> List[Dict[str, Any]]:
        """生成优化建议"""
        suggestions = []
        
        issues = self._discover_issues(session)
        
        for issue in issues:
            if "多次表示不知道" in issue:
                suggestions.append({
                    "类型": "问题优化",
                    "内容": "检查哪些问题导致用户频繁回答'不知道'，考虑拆分或简化"
                })
            
            if "资深从业者" in issue:
                suggestions.append({
                    "类型": "开场问题优化",
                    "内容": "资深从业者开场问题从'核心诉求是什么'改为'之前尝试过什么，卡在哪里'"
                })
            
            if "中途放弃" in issue:
                suggestions.append({
                    "类型": "流程优化",
                    "内容": "分析用户在哪一环节放弃，考虑增加进度提示或简化流程"
                })
        
        if not suggestions:
            suggestions.append({
                "类型": "保持观察",
                "内容": "继续收集数据，等待更多样本后进行更准确的分析"
            })
        
        return suggestions
    
    def _save_review(self, review: Dict) -> None:
        """保存复盘"""
        review_file = self.reviews_dir / f"{review['session_id']}_review.json"
        
        with open(review_file, 'w', encoding='utf-8') as f:
            json.dump(review, f, ensure_ascii=False, indent=2)
    
    def get_recent_reviews(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近复盘"""
        reviews = []
        
        for f in sorted(self.reviews_dir.glob("*_review.json"),
                       key=lambda x: x.stat().st_mtime,
                       reverse=True)[:limit]:
            with open(f, 'r', encoding='utf-8') as fp:
                reviews.append(json.load(fp))
        
        return reviews
    
    def get_unaddressed_suggestions(self) -> List[Dict[str, Any]]:
        """获取待处理的优化建议"""
        reviews = self.get_recent_reviews(limit=20)
        
        suggestion_counter = Counter()
        
        for review in reviews:
            for suggestion in review.get("优化建议", []):
                suggestion_counter[suggestion["内容"]] += 1
        
        return [
            {"建议": s, "出现次数": c}
            for s, c in suggestion_counter.items()
            if c >= 2
        ]


_reviewer = None

def get_reviewer() -> AutoReviewer:
    global _reviewer
    if _reviewer is None:
        _reviewer = AutoReviewer()
    return _reviewer
