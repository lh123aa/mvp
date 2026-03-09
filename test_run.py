"""
Demand Miner 系统测试脚本
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

from modules.pre_alignment import PreAlignmentModule, AlignmentPhase
from modules.dialogue_recorder import DialogueRecorder
from modules.auto_reviewer import AutoReviewer
from utils.state_manager import StateManager


def main():
    print("=" * 60)
    print("Demand Miner 系统测试")
    print("=" * 60)
    
    # 1. 初始化
    print("\n[1] 初始化...")
    recorder = DialogueRecorder()
    state_mgr = StateManager()
    pre_align = PreAlignmentModule()
    
    # 2. 创建会话
    print("\n[2] 创建会话...")
    session = state_mgr.create_session("短视频带货副业")
    session_id = session["session_id"]
    print(f"会话ID: {session_id}")
    
    # 3. 前置对齐
    print("\n[3] 前置对齐...")
    answers = {
        AlignmentPhase.核心目标: "短视频带货",
        AlignmentPhase.核心目的: "副业试水", 
        AlignmentPhase.认知层级: "完全陌生",
        AlignmentPhase.预算周期: "0成本，1个月"
    }
    
    current = AlignmentPhase.核心目标
    while current != AlignmentPhase.完成:
        task = pre_align.get_current_question(current)
        ans = answers.get(current, "继续")
        
        recorder.record_turn(session_id, {
            "阶段": "前置对齐",
            "环节": task["环节"],
            "问题": task["问题"],
            "用户回答": ans,
            "AI输出": ""
        })
        
        current, msg = pre_align.get_next_phase(current, ans, {})
        print(f"  {task['环节']}: 用户回答 '{ans}'")
    
    # 4. 完成
    print("\n[4] 完成会话...")
    recorder.finalize_session(session_id, {
        "内容": "方案完成",
        "用户确认": "符合预期",
        "满意度": "满意"
    })
    
    # 5. 复盘
    print("\n[5] 自动复盘...")
    reviewer = AutoReviewer()
    review = reviewer.generate_review(session_id)
    
    print("\n" + "=" * 60)
    print("【复盘结果】")
    print("=" * 60)
    print(f"会话ID: {review['session_id']}")
    print(f"流程路径: {review['流程路径']['完整路径']}")
    print(f"交互轮次: {review['交互质量']['有效交互轮次']}")
    print(f"发现亮点: {review['发现亮点']}")
    print(f"发现问题: {review['发现问题']}")
    print(f"优化建议: {[s['内容'] for s in review['优化建议']]}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
