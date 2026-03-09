"""
对话记录模块
负责自动保存对话过程为JSON文件
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class DialogueRecorder:
    """对话记录器"""
    
    def __init__(self, data_dir: str = "E:/学习/MVP/demand-miner/data"):
        self.data_dir = Path(data_dir)
        self.sessions_dir = self.data_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        self.unknown_keywords = ["不知道", "不懂", "不太清楚", "无法回答", "说不清", "随便", "都可以"]
        self.low_quality_keywords = ["可能吧", "也许", "不清楚", "不太懂"]
    
    def record_turn(self, session_id: str, turn_data: Dict[str, Any]) -> None:
        """记录单轮对话"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session = json.load(f)
        else:
            session = self._create_empty_session(session_id)
        
        answer = turn_data.get("用户回答", "")
        quality_score = self._calc_question_quality(answer)
        
        turn_record = {
            "turn_id": len(session.get("history", [])) + 1,
            "timestamp": datetime.now().isoformat() + "Z",
            "阶段": turn_data.get("阶段", ""),
            "环节": turn_data.get("环节", ""),
            "AI问题": turn_data.get("问题", ""),
            "用户回答": answer,
            "回答长度": len(answer),
            "AI输出": turn_data.get("AI输出", ""),
            "用户反馈": turn_data.get("用户反馈", ""),
            "问题有效性": {
                "评分": quality_score["评分"],
                "等级": quality_score["等级"],
                "标签": quality_score["标签"]
            }
        }
        
        if "history" not in session:
            session["history"] = []
        
        session["history"].append(turn_record)
        session["metadata"]["总轮次"] = len(session["history"])
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
    
    def _calc_question_quality(self, answer: str) -> Dict[str, Any]:
        """计算问题有效性评分"""
        if not answer:
            return {"评分": 0, "等级": "F", "标签": "未回答"}
        
        length = len(answer)
        if length < 5:
            length_score = 20
        elif length < 20:
            length_score = 40
        elif length < 50:
            length_score = 70
        elif length < 200:
            length_score = 90
        else:
            length_score = 100
        
        has_unknown = any(kw in answer for kw in self.unknown_keywords)
        has_low_quality = any(kw in answer for kw in self.low_quality_keywords)
        
        if has_unknown:
            keyword_score = 10
        elif has_low_quality:
            keyword_score = 40
        else:
            keyword_score = 100
        
        final_score = (length_score * 0.4 + keyword_score * 0.6)
        
        if final_score >= 80:
            grade = "A"
            label = "高质量回答"
        elif final_score >= 60:
            grade = "B"
            label = "中等质量"
        elif final_score >= 40:
            grade = "C"
            label = "低质量回答"
        else:
            grade = "D"
            label = "无效回答"
        
        return {
            "评分": round(final_score, 1),
            "等级": grade,
            "标签": label
        }
    
    def record_ai_output(self, session_id: str, ai_output: str, 
                        metadata: Optional[Dict] = None) -> None:
        """记录AI输出（不等待用户回答）"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session = json.load(f)
        else:
            return
        
        if "pending_outputs" not in session:
            session["pending_outputs"] = []
        
        pending = {
            "timestamp": datetime.now().isoformat() + "Z",
            "output": ai_output,
            "metadata": metadata or {}
        }
        session["pending_outputs"].append(pending)
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
    
    def record_user_feedback(self, session_id: str, feedback: str, 
                            feedback_type: str = "general") -> None:
        """记录用户反馈"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            return
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session = json.load(f)
        
        if "feedbacks" not in session:
            session["feedbacks"] = []
        
        session["feedbacks"].append({
            "timestamp": datetime.now().isoformat() + "Z",
            "type": feedback_type,
            "content": feedback
        })
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
    
    def finalize_session(self, session_id: str, final_data: Dict[str, Any]) -> None:
        """完成会话时调用"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            return
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session = json.load(f)
        
        session["final_output"] = {
            "timestamp": datetime.now().isoformat() + "Z",
            "content": final_data.get("内容", ""),
            "用户确认": final_data.get("用户确认", ""),
            "满意度": final_data.get("满意度", "")
        }
        
        session["completed_at"] = datetime.now().isoformat() + "Z"
        
        if "created_at" in session:
            try:
                start = datetime.fromisoformat(session["created_at"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(session["completed_at"].replace("Z", "+00:00"))
                duration = (end - start).total_seconds() / 60
                session["metadata"]["总耗时_分钟"] = round(duration, 1)
            except:
                pass
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
    
    def _create_empty_session(self, session_id: str) -> Dict[str, Any]:
        """创建空会话"""
        return {
            "session_id": session_id,
            "created_at": datetime.now().isoformat() + "Z",
            "user_profile": {},
            "current_state": {},
            "collected_info": {},
            "history": [],
            "pending_outputs": [],
            "feedbacks": [],
            "final_output": {},
            "metadata": {
                "总轮次": 0,
                "总耗时_分钟": 0,
                "用户中途放弃": False,
                "用户切换模式": False
            }
        }
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取会话摘要"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            return None
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session = json.load(f)
        
        return {
            "session_id": session_id,
            "创建时间": session.get("created_at", ""),
            "完成时间": session.get("completed_at", ""),
            "用户画像": session.get("user_profile", {}),
            "总轮次": session.get("metadata", {}).get("总轮次", 0),
            "总耗时": session.get("metadata", {}).get("总耗时_分钟", 0),
            "阶段": session.get("current_state", {}).get("阶段", ""),
            "是否完成": "completed_at" in session
        }
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的会话列表"""
        sessions = []
        
        for f in sorted(self.sessions_dir.glob("*.json"), 
                       key=lambda x: x.stat().st_mtime, 
                       reverse=True)[:limit]:
            with open(f, 'r', encoding='utf-8') as fp:
                s = json.load(fp)
                sessions.append({
                    "session_id": s.get("session_id", ""),
                    "创建时间": s.get("created_at", ""),
                    "核心目标": s.get("user_profile", {}).get("核心目标", ""),
                    "认知层级": s.get("user_profile", {}).get("认知层级", ""),
                    "总轮次": s.get("metadata", {}).get("总轮次", 0),
                    "是否完成": "completed_at" in s
                })
        
        return sessions


_recorder = None

def get_recorder() -> DialogueRecorder:
    global _recorder
    if _recorder is None:
        _recorder = DialogueRecorder()
    return _recorder
