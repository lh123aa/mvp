"""
Demand Miner 交互式对话入口 v2.0
修复版：解决重复确认、方案过滤、按需回答、进度提示
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

from modules.pre_alignment import PreAlignmentModule, AlignmentPhase
from modules.dialogue_recorder import DialogueRecorder
from modules.auto_reviewer import AutoReviewer
from utils.state_manager import StateManager
from utils.constraint_filter import ConstraintFilter, UserConstraints


# 进度总步数
TOTAL_STEPS = 6


class DemandMiner:
    """需求挖掘系统 v2.0"""
    
    def __init__(self):
        self.recorder = DialogueRecorder()
        self.state_mgr = StateManager()
        self.pre_align = PreAlignmentModule()
        self.session_id = None
        self.current_phase = None
        self.current_step = 0  # 当前步数
        self.profile = {}  # 用户画像
        self.skip_next_confirm = False  # 跳过下次确认
    
    def start(self, user_input: str = None):
        """开始新对话"""
        print("\n" + "="*60)
        print("欢迎使用 Demand Miner - 需求挖掘系统 v2.0")
        print("="*60)
        print("\n我将帮你分析需求并设计最小商业闭环。")
        print("让我们开始吧！\n")
        
        # 创建会话
        session = self.state_mgr.create_session(user_input or "新对话")
        self.session_id = session["session_id"]
        
        # 开始前置对齐
        self.current_phase = AlignmentPhase.核心目标
        self.current_step = 0
        self._ask_pre_alignment()
    
    def _show_progress(self):
        """显示进度"""
        remaining = TOTAL_STEPS - self.current_step
        print(f"\n[进度: 第{self.current_step}步, 剩余约{remaining}步]")
    
    def _ask_pre_alignment(self):
        """前置对齐问答"""
        task = self.pre_align.get_current_question(self.current_phase)
        
        self._show_progress()
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
            self.profile.update(profile_updates)
            self.state_mgr.update_user_profile(self.session_id, self.profile)
        
        # 检查是否跳过下次确认
        if self.skip_next_confirm:
            self.skip_next_confirm = False
            # 直接进入下一阶段
            next_phase, _ = self.pre_align.get_next_phase(
                self.current_phase, 
                user_input, 
                self.profile
            )
            if next_phase == AlignmentPhase.完成:
                self._start_main_flow()
            else:
                self.current_phase = next_phase
                self.current_step += 1
                self._ask_pre_alignment()
            return
        
        # 下一阶段
        next_phase, msg = self.pre_align.get_next_phase(
            self.current_phase, 
            user_input, 
            self.profile
        )
        
        print(f"\n>>> {msg}")
        
        if next_phase == AlignmentPhase.完成:
            self._start_main_flow()
        else:
            self.current_phase = next_phase
            self.current_step += 1
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
        print(f"\n{'='*60}")
        print("开始正式分析...")
        print(f"{'='*60}")
        
        # 显示用户画像
        print(f"\n📋 你的画像: {self.profile.get('核心目标')} | {self.profile.get('认知层级')} | {self.profile.get('预算约束')}")
        
        # 执行6步流程
        self._step1_basic_cognition()
    
    def _step1_basic_cognition(self):
        """步骤1: 基础认知"""
        self.current_step = 1
        self._show_progress()
        
        target = self.profile.get("核心目标", "")
        print(f"\n{'='*40}")
        print(f"【1. 基础认知】关于{target}")
        
        # 输出基础认知内容（简化版）
        print(f"\n{target}的核心定义和主流玩法...")
        
        print("\n问题: 以上清楚吗？")
        answer = input("回答: ").strip()
        
        # 检查用户是否需要补充
        if "补充" in answer or "更多" in answer:
            print("\n请说你想了解的具体方向:")
            interest = input("回答: ").strip()
            # 按需回答
            if "盈利" in interest or "赚钱" in interest:
                print(f"\n{target}的盈利方式：...")
            elif "用户" in interest or "客户" in interest:
                print(f"\n{target}的目标用户：...")
            else:
                print(f"\n关于{target}的{interest}，我补充：...")
            
            # 不再重复确认，直接下一步
            self.skip_next_confirm = True
        
        self.recorder.record_turn(self.session_id, {
            "阶段": "基础认知",
            "环节": "基础认知确认",
            "问题": "是否清晰",
            "用户回答": answer,
            "AI输出": ""
        })
        
        self._step2_user_group()
    
    def _step2_user_group(self):
        """步骤2: 目标用户"""
        self.current_step = 2
        self._show_progress()
        
        budget = self.profile.get("预算约束", "")
        print(f"\n{'='*40}")
        print("【2. 目标用户】")
        
        # 根据预算筛选用户群体
        if "0成本" in budget:
            print("推荐用户群体(0成本优先):")
            print("  A. 职场新人 - 有稳定收入愿意尝试")
            print("  B. 全职妈妈 - 精打细算愿意为孩子付费")
        else:
            print("推荐用户群体:")
            print("  A. 职场新人")
            print("  B. 全职妈妈")
            print("  C. 小镇青年")
        
        answer = input("\n选择: ").strip()
        
        # 记录
        self.recorder.record_turn(self.session_id, {
            "阶段": "目标用户",
            "环节": "用户选择",
            "问题": "选择用户群体",
            "用户回答": answer,
            "AI输出": ""
        })
        
        self._step3_pain_point()
    
    def _step3_pain_point(self):
        """步骤3: 痛点"""
        self.current_step = 3
        self._show_progress()
        
        print(f"\n{'='*40}")
        print("【3. 痛点拆解】")
        
        print("核心痛点方向:")
        print("  A. 获客难/流量获取")
        print("  B. 变现难/转化率低")  
        print("  C. 启动难/门槛高")
        
        answer = input("\n选择: ").strip()
        
        self.recorder.record_turn(self.session_id, {
            "阶段": "痛点拆解",
            "环节": "痛点选择",
            "问题": "选择痛点",
            "用户回答": answer,
            "AI输出": ""
        })
        
        self._step4_solution()
    
    def _step4_solution(self):
        """步骤4: 解决方案"""
        self.current_step = 4
        self._show_progress()
        
        budget = self.profile.get("预算约束", "")
        print(f"\n{'='*40}")
        print("【4. 解决方案】")
        
        # 根据预算严格过滤方案
        solutions = []
        
        if "0成本" in budget:
            print("符合预算的方案(0成本):")
            print("  A. 知识付费分销 - 0成本")
            print("  B. 内容创作 - 0成本")
        elif "5000" in budget:
            print("符合预算的方案(5000元内):")
            print("  A. 知识付费分销 - 0成本")
            print("  B. 工具/SOP模板 - 500元内")
            print("  C. 私教服务 - 2000元内")
        else:
            print("方案选项:")
            print("  A. 轻量化方案")
            print("  B. 中等方案")
            print("  C. 深度方案")
        
        answer = input("\n选择: ").strip()
        
        self.recorder.record_turn(self.session_id, {
            "阶段": "解决方案",
            "环节": "方案选择",
            "问题": "选择方案",
            "用户回答": answer,
            "AI输出": ""
        })
        
        self._step5_closed_loop()
    
    def _step5_closed_loop(self):
        """步骤5: 闭环设计"""
        self.current_step = 5
        self._show_progress()
        
        print(f"\n{'='*40}")
        print("【5. 最小商业闭环】")
        
        print("\n核心环节:")
        print("  引流 → 价值传递 → 信任建立 → 转化 → 复购")
        
        print("\n验证指标:")
        print("  - 获客成本 < 20元")
        print("  - 转化率 > 3%")
        
        answer = input("\n符合预期吗? ").strip()
        
        self.recorder.record_turn(self.session_id, {
            "阶段": "闭环设计",
            "环节": "闭环确认",
            "问题": "是否符合预期",
            "用户回答": answer,
            "AI输出": ""
        })
        
        self._step6_final()
    
    def _step6_final(self):
        """步骤6: 最终输出"""
        self.current_step = 6
        self._show_progress()
        
        print(f"\n{'='*40}")
        print("【6. 最终方案】")
        print("\n方案概述: ...")
        
        answer = input("\n满意吗? ").strip()
        
        self.recorder.record_turn(self.session_id, {
            "阶段": "最终输出",
            "环节": "最终确认",
            "问题": "是否满意",
            "用户回答": answer,
            "AI输出": ""
        })
        
        self._finish()
    
    def _finish(self):
        """完成对话"""
        print("\n" + "="*60)
        print("对话完成！")
        print("="*60)
        
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
