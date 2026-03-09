"""
状态管理模块
负责会话状态的创建、读取、更新、持久化
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class StateManager:
    """会话状态管理器"""
    
    def __init__(self, data_dir: str = "E:/学习/MVP/demand-miner/data"):
        self.data_dir = Path(data_dir)
        self.sessions_dir = self.data_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
    def create_session(self, user_input: Optional[str] = None) -> Dict[str, Any]:
        """创建新会话"""
        session_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}"
        
        session = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat() + "Z",
            "user_profile": {
                "核心目标": "",
                "核心目的": "",
                "认知层级": "",
                "预算约束": "",
                "周期约束": "",
                "服务模式": ""
            },
            "current_state": {
                "阶段": "前置对齐",
                "环节": "等待开始",
                "子环节索引": 0,
                "待回答问题": ""
            },
            "collected_info": {},
            "history": [],
            "metadata": {
                "总轮次": 0,
                "总耗时_分钟": 0,
                "用户中途放弃": False,
                "用户切换模式": False,
                "起始输入": user_input or ""
            }
        }
        
        # 保存到文件
        self._save_session(session)
        
        return session
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """加载会话"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新会话状态"""
        session = self.load_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # 深度更新
        for key, value in updates.items():
            if key in session:
                if isinstance(value, dict) and isinstance(session[key], dict):
                    session[key].update(value)
                else:
                    session[key] = value
        
        session["updated_at"] = datetime.now().isoformat() + "Z"
        self._save_session(session)
        
        return session
    
    def add_history(self, session_id: str, entry: Dict[str, Any]) -> None:
        """添加历史记录"""
        session = self.load_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        session["history"].append(entry)
        session["metadata"]["总轮次"] = len(session["history"])
        
        self._save_session(session)
    
    def update_user_profile(self, session_id: str, profile: Dict[str, str]) -> None:
        """更新用户画像"""
        session = self.load_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        session["user_profile"].update(profile)
        self._save_session(session)
    
    def update_current_state(self, session_id: str, state: Dict[str, Any]) -> None:
        """更新当前状态"""
        session = self.load_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        session["current_state"].update(state)
        self._save_session(session)
    
    def collect_info(self, session_id: str, key: str, value: Any) -> None:
        """收集信息"""
        session = self.load_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        session["collected_info"][key] = value
        self._save_session(session)
    
    def _save_session(self, session: Dict[str, Any]) -> None:
        """保存会话到文件"""
        session_id = session["session_id"]
        session_file = self.sessions_dir / f"{session_id}.json"
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
    
    def get_all_sessions(self) -> list:
        """获取所有会话"""
        sessions = []
        for f in self.sessions_dir.glob("*.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                sessions.append(json.load(fp))
        return sorted(sessions, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """获取会话摘要"""
        session = self.load_session(session_id)
        if not session:
            return {}
        
        return {
            "session_id": session["session_id"],
            "created_at": session["created_at"],
            "阶段": session["current_state"]["阶段"],
            "认知层级": session["user_profile"]["认知层级"],
            "核心目标": session["user_profile"]["核心目标"],
            "总轮次": session["metadata"]["总轮次"]
        }


# 全局实例
_state_manager = None

def get_state_manager() -> StateManager:
    """获取状态管理器单例"""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager
