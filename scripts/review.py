"""
复盘模块
封装对话复盘逻辑
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class ReviewGenerator:
    """复盘报告生成器"""
    
    def __init__(self, session_data: Dict[str, Any]):
        self.session_data = session_data
        self.user_profile = session_data.get("user_profile", {})
        self.conversation_history = session_data.get("history", [])
    
    def generate_review(self) -> str:
        """生成复盘报告"""
        return f"""## 对话复盘报告

### 对话概况
- 核心目标：{self.user_profile.get('核心目标', '未记录')}
- 认知层级：{self.user_profile.get('认知层级', '未记录')}
- 选用模式：{self.user_profile.get('服务模式', '未记录')}
- 对话轮次：{len(self.conversation_history)}轮

### 系统响应评估

| 评估项 | 评分 | 说明 |
|--------|------|------|
| 前置对齐 | {self._check_prealignment()} | {self._get_prealignment_note()} |
| 模式执行 | {self._check_mode_execution()} | {self._get_mode_note()} |
| 内容质量 | {self._check_content_quality()} | {self._get_content_note()} |
| 约束遵守 | {self._check_constraints()} | {self._get_constraint_note()} |

### 发现问题
{self._list_issues()}

### 迭代建议
{self._list_suggestions()}

### 下次改进重点
{self._get_improvement_focus()}
"""
    
    def _check_prealignment(self) -> str:
        """检查前置对齐是否完成"""
        required_fields = ['核心目标', '核心目的', '认知层级', '预算约束', '周期约束']
        completed = sum(1 for f in required_fields if self.user_profile.get(f))
        return "✓" if completed >= 4 else "✗"
    
    def _get_prealignment_note(self) -> str:
        """前置对齐说明"""
        if self._check_prealignment() == "✓":
            return "用户画像完整"
        return "需要补充用户画像信息"
    
    def _check_mode_execution(self) -> str:
        """检查模式执行"""
        mode = self.user_profile.get('服务模式', '')
        if mode:
            return "✓"
        return "✗"
    
    def _get_mode_note(self) -> str:
        """模式执行说明"""
        if self._check_mode_execution() == "✓":
            return "已选择合适的服务模式"
        return "未明确服务模式"
    
    def _check_content_quality(self) -> str:
        """检查内容质量"""
        # 基于对话轮次判断
        rounds = len(self.conversation_history)
        if rounds >= 5:
            return "✓"
        elif rounds >= 3:
            return "○"
        return "△"
    
    def _get_content_note(self) -> str:
        """内容质量说明"""
        quality = self._check_content_quality()
        if quality == "✓":
            return "对话内容充实"
        elif quality == "○":
            return "对话内容一般"
        return "对话内容偏少"
    
    def _check_constraints(self) -> str:
        """检查约束遵守"""
        budget = self.user_profile.get('预算约束', '')
        period = self.user_profile.get('周期约束', '')
        if budget and period:
            return "✓"
        return "○"
    
    def _get_constraint_note(self) -> str:
        """约束遵守说明"""
        if self._check_constraints() == "✓":
            return "已明确预算和周期约束"
        return "约束条件不完整"
    
    def _list_issues(self) -> str:
        """列出发现的问题"""
        issues = []
        
        if self._check_prealignment() == "✗":
            issues.append("1. 用户画像不完整")
        
        if self._check_mode_execution() == "✗":
            issues.append("2. 未明确服务模式")
        
        if self._check_content_quality() == "△":
            issues.append("3. 对话深度不够")
        
        if self._check_constraints() == "○":
            issues.append("4. 约束条件可能影响方案适配")
        
        if not issues:
            issues.append("1. 暂未发现明显问题")
        
        return "\n".join(issues)
    
    def _list_suggestions(self) -> str:
        """列出迭代建议"""
        suggestions = []
        
        if self._check_prealignment() == "✗":
            suggestions.append("1. 优化前置对齐流程，确保用户画像完整")
        
        if self._check_mode_execution() == "✗":
            suggestions.append("2. 明确服务模式选择逻辑")
        
        if self._check_content_quality() == "△":
            suggestions.append("3. 增加引导提问，提高对话深度")
        
        if self._check_constraints() == "○":
            suggestions.append("4. 加强约束条件确认")
        
        if not suggestions:
            suggestions.append("1. 保持当前服务质量")
        
        return "\n".join(suggestions)
    
    def _get_improvement_focus(self) -> str:
        """获取改进重点"""
        issues = []
        
        if self._check_prealignment() == "✗":
            issues.append("完善用户画像")
        
        if self._check_content_quality() == "△":
            issues.append("增加对话深度")
        
        if issues:
            return issues[0]
        
        return "继续保持现有流程优化"


def create_review_from_session(session_data: Dict[str, Any]) -> str:
    """从会话数据创建复盘报告"""
    generator = ReviewGenerator(session_data)
    return generator.generate_review()


def save_review_to_file(review_content: str, file_path: str = "docs/迭代日志.md") -> bool:
    """保存复盘报告到文件"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # 读取现有内容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = "# 迭代日志\n"
        
        # 添加复盘记录
        new_record = f"\n---\n\n## {timestamp} - 对话复盘\n{review_content}"
        
        # 插入到复盘记录区域
        if "## 对话复盘记录" in content:
            content = content.replace(
                "## 对话复盘记录",
                "## 对话复盘记录" + new_record
            )
        else:
            content += new_record
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"保存复盘失败: {e}")
        return False


# 示例用法
if __name__ == "__main__":
    # 示例会话数据
    sample_session = {
        "user_profile": {
            "核心目标": "短视频带货",
            "核心目的": "副业试水",
            "认知层级": "有基础认知",
            "预算约束": "5000元内",
            "周期约束": "3个月",
            "服务模式": "引导教练"
        },
        "history": [
            {"role": "user", "content": "我想做短视频带货"},
            {"role": "assistant", "content": "好的，我来帮你分析"},
            {"role": "user", "content": "我有一点了解"},
            {"role": "assistant", "content": "那我们来深入分析"}
        ]
    }
    
    # 生成复盘报告
    review = create_review_from_session(sample_session)
    print(review)