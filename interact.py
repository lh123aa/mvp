"""
Demand Miner 交互式对话入口
真正的用户交互界面
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

from modules.pre_alignment import PreAlignmentModule, AlignmentPhase
from modules.stranger_mode import StrangerModeExecutor, StrangerPhase
from modules.basic_mode import BasicModeExecutor, create_basic_executor
from modules.senior_mode import SeniorModeExecutor, create_senior_executor
from modules.dialogue_recorder import DialogueRecorder
from modules.auto_reviewer import AutoReviewer
from utils.state_manager import StateManager


class DemandMiner:
    """需求挖掘系统"""
    
    def __init__(self):
        self.recorder = DialogueRecorder()
        self.state_mgr = StateManager()
        self.pre_align = PreAlignmentModule()
        self.session_id = None
        self.current_phase = None
        self.executor = None
        
    def start(self, user_input: str = None):
        """开始新对话"""
        print("\n" + "="*60)
        print("欢迎使用 Demand Miner - 需求挖掘系统")
        print("="*60)
        print("\n我将帮你分析需求并设计最小商业闭环。")
        print("让我们开始吧！\n")
        
        # 创建会话
        session = self.state_mgr.create_session(user_input or "新对话")
        self.session_id = session["session_id"]
        print(f"[会话ID: {self.session_id}]")
        
        # 开始前置对齐
        self.current_phase = AlignmentPhase.核心目标
        self._ask_pre_alignment()
    
    def _ask_pre_alignment(self):
        """前置对齐问答"""
        task = self.pre_align.get_current_question(self.current_phase)
        
        print("\n" + "-"*40)
        print(f"【{task['环节']}】")
        print(task["问题"])
        
        if task.get("选项"):
            print("\n可选:")
            for opt in task["选项"]:
                print(f"  {opt['label']}")
        
        # 获取用户回答
        user_input = input("\n你的回答: ").strip()
        
        # 记录
        self.recorder.record_turn(self.session_id, {
            "阶段": "前置对齐",
            "环节": task["环节"],
            "问题": task["问题"],
            "用户回答": user_input,
            "AI输出": ""
        })
        
        # 更新用户画像
        profile_updates = self._parse_pre_answer(task["环节"], user_input)
        if profile_updates:
            self.state_mgr.update_user_profile(self.session_id, profile_updates)
        
        # 下一阶段
        next_phase, msg = self.pre_align.get_next_phase(
            self.current_phase, 
            user_input, 
            self.state_mgr.load_session(self.session_id)["user_profile"]
        )
        
        print(f"\n>>> {msg}")
        
        if next_phase == AlignmentPhase.完成:
            self._start_main_flow()
        else:
            self.current_phase = next_phase
            self._ask_pre_alignment()
    
    def _parse_pre_answer(self, phase: str, answer: str) -> dict:
        """解析前置回答"""
        updates = {}
        
        if phase == "核心目标":
            updates["核心目标"] = answer
        elif phase == "核心目的":
            if "副业" in answer: updates["核心目的"] = "副业试水"
            elif "创业" in answer: updates["核心目的"] = "创业立项"
            elif "行业" in answer or "学习" in answer: updates["核心目的"] = "行业研究学习"
            elif "职业" in answer: updates["核心目的"] = "职业转型规划"
        elif phase == "认知层级":
            updates["认知层级"] = answer
        elif phase == "预算周期":
            if "0成本" in answer:
                updates["预算约束"] = "0成本"
                updates["周期约束"] = "1个月"
            elif "5000" in answer:
                updates["预算约束"] = "5000元内"
                updates["周期约束"] = "3个月"
            elif "20000" in answer:
                updates["预算约束"] = "5000-20000元"
                updates["周期约束"] = "6个月"
        elif phase == "服务模式":
            updates["服务模式"] = answer
            
        return updates
    
    def _start_main_flow(self):
        """开始主流程"""
        session = self.state_mgr.load_session(self.session_id)
        profile = session["user_profile"]
        
        print(f"\n{'='*60}")
        print("开始正式分析...")
        print(f"{'='*60}")
        
        # 根据认知层级选择模式
        cognition = profile.get("认知层级", "")
        
        if cognition == "完全陌生":
            self._run_stranger_mode(profile)
        elif cognition == "有基础认知":
            self._run_basic_mode(profile)
        elif cognition == "资深从业者":
            self._run_senior_mode(profile)
        else:
            self._run_stranger_mode(profile)
    
    def _run_stranger_mode(self, profile):
        """陌生模式"""
        constraints = {
            "预算约束": profile.get("预算约束", ""),
            "周期约束": profile.get("周期约束", "")
        }
        
        executor = StrangerModeExecutor(profile, constraints)
        phase = StrangerPhase.基础认知
        
        while phase != StrangerPhase.完成:
            task = executor.get_current_task(phase)
            
            if task.get("是最终环节"):
                break
            
            print("\n" + "-"*40)
            print(f"【{task['阶段']}】{task['环节']}")
            
            # 输出AI内容
            if task.get("AI输出"):
                print(task["AI输出"][:500] + "..." if len(task.get("AI输出", "")) > 500 else task.get("AI输出", ""))
            
            print("\n" + task["提问"])
            
            if task.get("选项"):
                print("\n可选:")
                for opt in task["选项"]:
                    print(f"  {opt['label']}")
            
            user_input = input("\n你的回答: ").strip()
            
            # 记录
            self.recorder.record_turn(self.session_id, {
                "阶段": task["阶段"],
                "环节": task["环节"],
                "问题": task["提问"],
                "用户回答": user_input,
                "AI输出": task.get("AI输出", "")
            })
            
            # 收集信息
            self.state_mgr.collect_info(self.session_id, task.get("记录键", ""), user_input)
            
            phase = StrangerPhase(phase.value + 1)
        
        self._finish()

    def _run_basic_mode(self, profile):
        """有基础认知模式"""
        role = profile.get("服务模式", "引导教练")  # 默认为引导教练
        executor = create_basic_executor(profile, role)
        
        # 根据角色确定问题数量
        total_questions = len(executor.COACH_QUESTIONS) if role == "引导教练" else 6
        
        current_index = 0
        while current_index < total_questions:
            task = executor.get_current_question(current_index)
            
            if task.get("是最终环节"):
                break
            
            print("\n" + "-"*40)
            print(f"【{task['阶段']}】{task['环节']}")
            
            # 输出AI内容（如果有）
            if task.get("AI输出"):
                print(task["AI输出"][:500] + "..." if len(task.get("AI输出", "")) > 500 else task.get("AI输出", ""))
            
            print("\n" + task["问题"])
            
            if task.get("提示"):
                print(f"\n提示: {task['提示']}")
            
            user_input = input("\n你的回答: ").strip()
            
            # 记录
            self.recorder.record_turn(self.session_id, {
                "阶段": task["阶段"],
                "环节": task["环节"],
                "问题": task["问题"],
                "用户回答": user_input,
                "AI输出": task.get("AI输出", "")
            })
            
            # 收集信息
            self.state_mgr.collect_info(self.session_id, task.get("记录键", ""), user_input)
            
            current_index += 1
        
        self._finish()

    def _run_senior_mode(self, profile):
        """资深从业者模式"""
        executor = create_senior_executor(profile)
        current_index = 0
        total_questions = len(executor.SENIOR_QUESTIONS)
        
        while current_index < total_questions:
            task = executor.get_current_task(current_index)
            
            if task.get("是最终环节"):
                break
            
            print("\n" + "-"*40)
            print(f"【{task['阶段']}】{task['环节']}")
            
            # 输出AI内容
            if task.get("AI输出"):
                print(task["AI输出"])
            
            print("\n" + task["问题"])
            
            if task.get("说明"):
                print(f"\n说明: {task['说明']}")
            
            user_input = input("\n你的回答: ").strip()
            
            # 记录
            self.recorder.record_turn(self.session_id, {
                "阶段": task["阶段"],
                "环节": task["环节"],
                "问题": task["问题"],
                "用户回答": user_input,
                "AI输出": task.get("AI输出", "")
            })
            
            # 收集信息
            self.state_mgr.collect_info(self.session_id, task.get("记录键", ""), user_input)
            
            current_index += 1
        
        self._finish()

    def _finish(self):
        """完成对话"""
        print("\n" + "="*60)
        print("对话完成！")
        print("="*60)
        
        print("\n请对你的体验进行评价:")
        satisfaction = input("满意程度 (1-5分): ").strip()
        
        self.recorder.finalize_session(self.session_id, {
            "内容": "完整方案已生成",
            "用户确认": "已完成",
            "满意度": satisfaction or "未知"
        })
        
        # 自动复盘
        reviewer = AutoReviewer()
        review = reviewer.generate_review(self.session_id)
        
        print("\n" + "="*60)
        print("【复盘结果】")
        print("="*60)
        print(f"流程: {review['流程路径']['完整路径']}")
        print(f"亮点: {review['发现亮点']}")
        if review['发现问题']:
            print(f"问题: {review['发现问题']}")
        print(f"建议: {[s['内容'] for s in review['优化建议']]}")
        
        print("\n感谢使用！")


def main():
    dm = DemandMiner()
    dm.start()


if __name__ == "__main__":
    main()