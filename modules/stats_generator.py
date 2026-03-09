"""
汇总统计模块
生成周/月统计报告
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import Counter
from dateutil import parser as dateparser


class StatsGenerator:
    """统计生成器"""
    
    def __init__(self, data_dir: str = "E:/学习/MVP/demand-miner/data"):
        self.data_dir = Path(data_dir)
        self.sessions_dir = self.data_dir / "sessions"
        self.reviews_dir = self.data_dir / "reviews"
        self.stats_dir = self.data_dir / "stats"
        self.stats_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_weekly_stats(self, week_start: str = None) -> Dict[str, Any]:
        """生成周统计"""
        if week_start:
            start = datetime.fromisoformat(week_start)
        else:
            # 默认本周
            today = datetime.now()
            start = today - timedelta(days=today.weekday())
            start = start.replace(hour=0, minute=0, second=0)
        
        end = start + timedelta(days=7)
        
        return self._generate_stats(start, end, "weekly")
    
    def generate_monthly_stats(self, month_start: str = None) -> Dict[str, Any]:
        """生成月统计"""
        if month_start:
            start = datetime.fromisoformat(month_start)
        else:
            today = datetime.now()
            start = today.replace(day=1, hour=0, minute=0, second=0)
        
        # 下个月第一天
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)
        
        return self._generate_stats(start, end, "monthly")
    
    def _generate_stats(self, start: datetime, end: datetime, 
                       stats_type: str) -> Dict[str, Any]:
        """生成统计"""
        # 收集该时间段内的会话
        sessions = []
        for f in self.sessions_dir.glob("*.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                s = json.load(fp)
                created = dateparser.parse(s.get("created_at", ""))
                if start <= created < end:
                    sessions.append(s)
        
        # 统计各项指标
        total = len(sessions)
        completed = sum(1 for s in sessions if "completed_at" in s)
        abandoned = sum(1 for s in sessions if s.get("metadata", {}).get("用户中途放弃", False))
        
        # 用户画像分布
       认知层级分布 = Counter(s.get("user_profile", {}).get("认知层级", "") for s in sessions)
        核心目的分布 = Counter(s.get("user_profile", {}).get("核心目的", "") for s in sessions)
        
        # 流程统计
        total_rounds = sum(s.get("metadata", {}).get("总轮次", 0) for s in sessions)
        avg_rounds = total_rounds / total if total > 0 else 0
        
        total_duration = sum(s.get("metadata", {}).get("总耗时_分钟", 0) for s in sessions)
        avg_duration = total_duration / total if total > 0 else 0
        
        # 满意度统计
        satisfactions = []
        for s in sessions:
            final = s.get("final_output", {})
            if final.get("满意度"):
                satisfactions.append(final.get("满意度"))
        satisfaction_dist = Counter(satisfactions)
        
        # 问题统计（从复盘中获取）
        problem_stats = self._get_problem_stats(start, end)
        
        stats = {
            "统计类型": stats_type,
            "统计周期": {
                "开始": start.isoformat() + "Z",
                "结束": end.isoformat() + "Z"
            },
            "基础统计": {
                "总会话数": total,
                "完成数": completed,
                "放弃数": abandoned,
                "完成率": round(completed / total * 100, 1) if total > 0 else 0
            },
            "用户画像分布": {
                "认知层级": dict(认知层级分布),
                "核心目的": dict(核心目的分布)
            },
            "流程效率": {
                "总轮次": total_rounds,
                "平均轮次": round(avg_rounds, 1),
                "总耗时_分钟": round(total_duration, 1),
                "平均耗时_分钟": round(avg_duration, 1)
            },
            "满意度分布": dict(satisfaction_dist),
            "高频问题": problem_stats.get("高频问题", []),
            "待优化项": problem_stats.get("待优化项", [])
        }
        
        # 保存统计
        self._save_stats(stats, stats_type, start)
        
        return stats
    
    def _get_problem_stats(self, start: datetime, end: datetime) -> Dict[str, Any]:
        """从复盘中获取问题统计"""
        problems = []
        
        for f in self.reviews_dir.glob("*_review.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                r = json.load(fp)
                review_time = dateparser.parse(r.get("复盘时间", ""))
                if start <= review_time < end:
                    # 收集问题
                    for issue in r.get("发现问题", []):
                        problems.append(issue)
                    
                    # 收集待优化项
                    for suggestion in r.get("优化建议", []):
                        problems.append(suggestion.get("内容", ""))
        
        problem_counts = Counter(problems)
        
        return {
            "高频问题": [
                {"问题": p, "出现次数": c}
                for p, c in problem_counts.most_common(5)
            ],
            "待优化项": list(set(problems))[:5]
        }
    
    def _save_stats(self, stats: Dict, stats_type: str, period_start: datetime) -> None:
        """保存统计"""
        if stats_type == "weekly":
            filename = f"weekly_{period_start.strftime('%Y-W%W')}.json"
        else:
            filename = f"monthly_{period_start.strftime('%Y-%m')}.json"
        
        stats_file = self.stats_dir / filename
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    
    def get_latest_stats(self, stats_type: str = "weekly") -> Optional[Dict]:
        """获取最新统计"""
        pattern = f"{stats_type}_*.json"
        
        files = sorted(self.stats_dir.glob(pattern), 
                      key=lambda x: x.stat().st_mtime, 
                      reverse=True)
        
        if not files:
            return None
        
        with open(files[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_trend_analysis(self, metrics: List[str] = None) -> Dict[str, Any]:
        """获取趋势分析"""
        if metrics is None:
            metrics = ["完成率", "平均轮次", "满意度"]
        
        # 获取最近4周的周报
        weekly_files = sorted(self.stats_dir.glob("weekly_*.json"), 
                            key=lambda x: x.name)[-4:]
        
        trends = {m: [] for m in metrics}
        labels = []
        
        for f in weekly_files:
            with open(f, 'r', encoding='utf-8') as fp:
                stats = json.load(fp)
                labels.append(f["统计周期"]["开始"][:10])
                
                if "完成率" in metrics:
                    trends["完成率"].append(stats["基础统计"].get("完成率", 0))
                
                if "平均轮次" in metrics:
                    trends["平均轮次"].append(stats["流程效率"].get("平均轮次", 0))
                
                if "满意度" in metrics:
                    # 简化：计算满意度比例
                    sat_dist = stats.get("满意度分布", {})
                    total = sum(sat_dist.values())
                    if total > 0:
                        good = sat_dist.get("满意", 0)
                        trends["满意度"].append(round(good / total * 100, 1))
                    else:
                        trends["满意度"].append(0)
        
        return {
            "指标": trends,
            "周期": labels,
            "分析": self._analyze_trends(trends)
        }
    
    def _analyze_trends(self, trends: Dict[str, List]) -> Dict[str, str]:
        """分析趋势"""
        analysis = {}
        
        for metric, values in trends.items():
            if len(values) < 2:
                analysis[metric] = "数据不足"
                continue
            
            first = values[0]
            last = values[-1]
            change = last - first
            
            if abs(change) < 5:
                analysis[metric] = f"基本稳定 ({change:+.1f}%)"
            elif change > 0:
                analysis[metric] = f"上升趋势 ({change:+.1f}%)"
            else:
                analysis[metric] = f"下降趋势 ({change:+.1f}%)"
        return analysis
    
    # ========== 问题质量分析 ==========
    
    def analyze_question_quality(self, days: int = 30) -> Dict[str, Any]:
        """
        分析问题质量
        按环节维度统计问题有效性
        """
        from datetime import timedelta
        from dateutil import parser as dateparser
        
        # 收集会话
        cutoff = datetime.now() - timedelta(days=days)
        sessions = []
        
        for f in self.sessions_dir.glob("*.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                s = json.load(fp)
                created = dateparser.parse(s.get("created_at", ""))
                if created >= cutoff:
                    sessions.append(s)
        
        # 按环节统计
        phase_stats = {}
        grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        
        for session in sessions:
            for turn in session.get("history", []):
                phase = turn.get("环节", "未知")
                quality = turn.get("问题有效性", {})
                grade = quality.get("等级", "F")
                
                if phase not in phase_stats:
                    phase_stats[phase] = {
                        "总数": 0,
                        "评分总和": 0,
                        "等级分布": {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
                    }
                
                phase_stats[phase]["总数"] += 1
                phase_stats[phase]["评分总和"] += quality.get("评分", 0)
                phase_stats[phase]["等级分布"][grade] = phase_stats[phase]["等级分布"].get(grade, 0) + 1
                grade_dist[grade] = grade_dist.get(grade, 0) + 1
        
        # 计算统计数据
        result_phases = {}
        for phase, stats in phase_stats.items():
            avg_score = stats["评分总和"] / stats["总数"] if stats["总数"] > 0 else 0
            grade_pct = {g: round(c / stats["总数"] * 100, 1) for g, c in stats["等级分布"].items()}
            result_phases[phase] = {
                "问题数": stats["总数"],
                "平均评分": round(avg_score, 1),
                "等级分布": stats["等级分布"],
                "等级比例": grade_pct
            }
        
        return {
            "分析周期": f"最近{days}天",
            "总会话数": len(sessions),
            "总问题数": sum(s["总数"] for s in phase_stats.values()),
            "各环节统计": result_phases,
            "整体等级分布": grade_dist,
            "待优化环节": self._find_problematic_phases(result_phases)
        }
    
    def _find_problematic_phases(self, phase_stats: Dict) -> List[Dict]:
        """找出需要优化的问题环节"""
        problems = []
        for phase, stats in phase_stats.items():
            if stats["平均评分"] < 60:
                problems.append({
                    "环节": phase,
                    "原因": f"平均评分仅{stats['平均评分']}分，低于60分",
                    "建议": "考虑拆分问题或提供更多示例"
                })
            low_grade_pct = stats["等级比例"].get("D", 0) + stats["等级比例"].get("F", 0)
            if low_grade_pct > 30:
                problems.append({
                    "环节": phase,
                    "原因": f"低质量回答占比{low_grade_pct}%，超过30%",
                    "建议": "问题可能过于抽象，考虑简化或提供选项"
                })
        return problems[:5]


# 全局实例
        return analysis


# 全局实例
_stats_generator = None

def get_stats_generator() -> StatsGenerator:
    """获取统计生成器单例"""
    global _stats_generator
    if _stats_generator is None:
        _stats_generator = StatsGenerator()
    return _stats_generator
