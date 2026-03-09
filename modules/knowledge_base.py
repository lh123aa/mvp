"""
知识库模块
行业方案库、案例库的基础框架
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class KnowledgeBase:
    """知识库管理器"""
    
    def __init__(self, kb_dir: str = "E:/学习/MVP/demand-miner/data/knowledge"):
        self.kb_dir = Path(kb_dir)
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        
        # 子目录
        self.schemes_dir = self.kb_dir / "schemes"  # 方案库
        self.cases_dir = self.kb_dir / "cases"        # 案例库
        self.insights_dir = self.kb_dir / "insights"  # 洞察库
        
        for d in [self.schemes_dir, self.cases_dir, self.insights_dir]:
            d.mkdir(exist_ok=True)
    
    # ========== 方案库管理 ==========
    
    def add_scheme(self, industry: str, scheme: Dict[str, Any]) -> None:
        """添加方案到方案库"""
        file_path = self.schemes_dir / f"{industry}.json"
        
        schemes = []
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                schemes = json.load(f)
        
        # 添加元数据
        scheme["添加时间"] = datetime.now().isoformat() + "Z"
        scheme["使用次数"] = 0
        scheme["满意度评分"] = None
        
        schemes.append(scheme)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(schemes, f, ensure_ascii=False, indent=2)
    
    def get_schemes(self, industry: str, filters: Optional[Dict] = None) -> List[Dict]:
        """获取方案列表（可筛选）"""
        file_path = self.schemes_dir / f"{industry}.json"
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            schemes = json.load(f)
        
        # 如果有筛选条件
        if filters:
            filtered = []
            for s in schemes:
                match = True
                for key, value in filters.items():
                    if s.get(key) != value:
                        match = False
                        break
                if match:
                    filtered.append(s)
            return filtered
        
        return schemes
    
    def update_scheme_stats(self, industry: str, scheme_name: str, 
                          satisfaction: Optional[int] = None) -> None:
        """更新方案使用统计"""
        file_path = self.schemes_dir / f"{industry}.json"
        
        if not file_path.exists():
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            schemes = json.load(f)
        
        for s in schemes:
            if s.get("名称") == scheme_name:
                s["使用次数"] = s.get("使用次数", 0) + 1
                if satisfaction is not None:
                    # 更新满意度评分（加权平均）
                    old_score = s.get("满意度评分")
                    if old_score is None:
                        s["满意度评分"] = satisfaction
                    else:
                        s["满意度评分"] = (old_score + satisfaction) / 2
                break
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(schemes, f, ensure_ascii=False, indent=2)
    
    # ========== 案例库管理 ==========
    
    def add_case(self, industry: str, case: Dict[str, Any]) -> None:
        """添加案例到案例库"""
        file_path = self.cases_dir / f"{industry}.json"
        
        cases = []
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                cases = json.load(f)
        
        case["添加时间"] = datetime.now().isoformat() + "Z"
        cases.append(case)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cases, f, ensure_ascii=False, indent=2)
    
    def get_cases(self, industry: str, tags: Optional[List[str]] = None) -> List[Dict]:
        """获取案例列表"""
        file_path = self.cases_dir / f"{industry}.json"
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        if tags:
            filtered = []
            for c in cases:
                case_tags = c.get("标签", [])
                if any(t in case_tags for t in tags):
                    filtered.append(c)
            return filtered
        
        return cases
    
    # ========== 洞察库管理 ==========
    
    def add_insight(self, insight_type: str, content: str, 
                   source: str = "manual") -> None:
        """添加洞察"""
        file_path = self.insights_dir / f"{insight_type}.json"
        
        insights = []
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                insights = json.load(f)
        
        insights.append({
            "内容": content,
            "来源": source,
            "添加时间": datetime.now().isoformat() + "Z"
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)
    
    def get_insights(self, insight_type: str) -> List[Dict]:
        """获取洞察列表"""
        file_path = self.insights_dir / f"{insight_type}.json"
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # ========== 统计功能 ==========
    
    def get_industry_stats(self, industry: str) -> Dict[str, Any]:
        """获取行业统计"""
        schemes = self.get_schemes(industry)
        cases = self.get_cases(industry)
        
        # 计算满意度
        satisfactions = [s.get("满意度评分") for s in schemes 
                        if s.get("满意度评分") is not None]
        avg_satisfaction = sum(satisfactions) / len(satisfactions) if satisfactions else None
        
        return {
            "行业": industry,
            "方案数量": len(schemes),
            "案例数量": len(cases),
            "平均满意度": round(avg_satisfaction, 1) if avg_satisfaction else None,
            "热门方案": sorted(schemes, key=lambda x: x.get("使用次数", 0), reverse=True)[:3]
        }
    
    def get_all_industries(self) -> List[str]:
        """获取所有行业列表"""
        industries = set()
        
        for f in self.schemes_dir.glob("*.json"):
            industries.add(f.stem)
        
        for f in self.cases_dir.glob("*.json"):
            industries.add(f.stem)
        
        return sorted(list(industries))


# ========== 预定义行业模板 ==========

INDUSTRY_TEMPLATES = {
    "短视频带货": {
        "用户群体": ["职场新人", "全职妈妈", "小镇青年", "学生党"],
        "轻量化方案": [
            {"名称": "无货源带货", "成本": "0", "周期": "1个月"},
            {"名称": "书单号带货", "成本": "0", "周期": "2周"},
            {"名称": "小程序cps", "成本": "100", "周期": "1周"}
        ],
        "常见痛点": ["不会剪辑", "没有货源", "流量获取难", "转化率低"],
        "验证指标": {
            "及格": "单日GMV>100元",
            "良好": "单日GMV>500元",
            "优秀": "单日GMV>2000元"
        }
    },
    "知识付费": {
        "用户群体": ["职场人士", "创业者", "学生", "自由职业者"],
        "轻量化方案": [
            {"名称": "分销推广", "成本": "0", "周期": "1周"},
            {"名称": "付费社群", "成本": "500", "周期": "1个月"},
            {"名称": "专栏课程", "成本": "2000", "周期": "2个月"}
        ],
        "常见痛点": ["内容制作难", "获客成本高", "定价困难", "复购率低"],
        "验证指标": {
            "及格": "付费用户>50人",
            "良好": "付费用户>200人",
            "优秀": "付费用户>1000人"
        }
    },
    "本地生活": {
        "用户群体": ["本地居民", "上班族", "学生", "游客"],
        "轻量化方案": [
            {"名称": "探店达人", "成本": "0", "周期": "2周"},
            {"名称": "本地社群", "成本": "300", "周期": "1个月"},
            {"名称": "商家cps", "成本": "500", "周期": "1个月"}
        ],
        "常见痛点": ["商家资源难找", "用户习惯难培养", "变现模式不清"],
        "验证指标": {
            "及格": "月GMV>1000元",
            "良好": "月GMV>5000元",
            "优秀": "月GMV>20000元"
        }
    }
}


def init_knowledge_base(kb: KnowledgeBase) -> None:
    """初始化知识库（预填充行业模板）"""
    for industry, template in INDUSTRY_TEMPLATES.items():
        # 添加方案模板
        for scheme in template.get("轻量化方案", []):
            kb.add_scheme(industry, {
                "名称": scheme["名称"],
                "成本": scheme["成本"],
                "周期": scheme["周期"],
                "用户群体": template.get("用户群体", []),
                "标签": ["模板", "轻量化"]
            })


# 全局实例
_knowledge_base = None

def get_knowledge_base() -> KnowledgeBase:
    """获取知识库单例"""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base
