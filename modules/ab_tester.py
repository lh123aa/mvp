"""
A/B Testing 模块
支持新旧版本对比测试
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class TestVersion(Enum):
    """测试版本"""
    A = "A"  # 对照组（旧版本）
    B = "B"  # 实验组（新版本）


@dataclass
class TestConfig:
    """测试配置"""
    test_id: str
    name: str
    version_a_config: Dict[str, Any]  # A版本配置
    version_b_config: Dict[str, Any]  # B版本配置
    traffic_split: float = 0.5  # A版本流量比例
    start_time: str
    end_time: Optional[str] = None
    status: str = "draft"  # draft/running/paused/completed


@dataclass
class TestResult:
    """单次测试结果"""
    session_id: str
    test_version: str
    timestamp: str
    metrics: Dict[str, Any]


class ABTester:
    """A/B测试管理器"""
    
    def __init__(self, data_dir: str = "E:/学习/MVP/demand-miner/data"):
        self.data_dir = Path(data_dir)
        self.tests_dir = self.data_dir / "ab_tests"
        self.tests_dir.mkdir(parents=True, exist_ok=True)
    
    # ========== 测试管理 ==========
    
    def create_test(self, test_config: TestConfig) -> str:
        """创建新测试"""
        test_file = self.tests_dir / f"{test_config.test_id}.json"
        
        test_data = {
            "config": asdict(test_config),
            "results": [],
            "created_at": datetime.now().isoformat() + "Z"
        }
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        return test_config.test_id
    
    def get_test(self, test_id: str) -> Optional[Dict]:
        """获取测试配置"""
        test_file = self.tests_dir / f"{test_id}.json"
        
        if not test_file.exists():
            return None
        
        with open(test_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_tests(self) -> List[Dict]:
        """列出所有测试"""
        tests = []
        
        for f in sorted(self.tests_dir.glob("*.json"), 
                       key=lambda x: x.stat().st_mtime, reverse=True):
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                tests.append({
                    "test_id": data["config"]["test_id"],
                    "name": data["config"]["name"],
                    "status": data["config"]["status"],
                    "result_count": len(data.get("results", []))
                })
        
        return tests
    
    # ========== 版本分配 ==========
    
    def assign_version(self, test_id: str) -> str:
        """
        分配测试版本
        返回: "A" 或 "B"
        """
        test = self.get_test(test_id)
        if not test:
            return "A"  # 默认返回A
        
        config = test["config"]
        
        # 检查测试状态
        if config["status"] != "running":
            return "A"
        
        # 检查时间
        start = datetime.fromisoformat(config["start_time"].replace("Z", "+00:00"))
        if datetime.now() < start:
            return "A"
        
        if config["end_time"]:
            end = datetime.fromisoformat(config["end_time"].replace("Z", "+00:00"))
            if datetime.now() > end:
                return "A"
        
        # 按流量比例分配
        split = config.get("traffic_split", 0.5)
        return "A" if random.random() < split else "B"
    
    def get_version_config(self, test_id: str, version: str) -> Dict[str, Any]:
        """获取版本配置"""
        test = self.get_test(test_id)
        if not test:
            return {}
        
        config = test["config"]
        if version == "B":
            return config.get("version_b_config", {})
        else:
            return config.get("version_a_config", {})
    
    # ========== 结果记录 ==========
    
    def record_result(self, test_id: str, result: TestResult) -> None:
        """记录测试结果"""
        test_file = self.tests_dir / f"{test_id}.json"
        
        if not test_file.exists():
            return
        
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        test_data["results"].append(asdict(result))
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    # ========== 统计分析 ==========
    
    def analyze_test(self, test_id: str) -> Dict[str, Any]:
        """分析测试结果"""
        test = self.get_test(test_id)
        if not test:
            return {"error": "Test not found"}
        
        results = test.get("results", [])
        
        # 分离A/B结果
        results_a = [r for r in results if r["test_version"] == "A"]
        results_b = [r for r in results if r["test_version"] == "B"]
        
        # 计算各版本指标
        metrics_a = self._calc_metrics(results_a)
        metrics_b = self._calc_metrics(results_b)
        
        # 计算提升比例
        improvement = {}
        for key in metrics_a:
            if metrics_a[key] and metrics_b[key] and metrics_a[key] != 0:
                improvement[key] = round((metrics_b[key] - metrics_a[key]) / metrics_a[key] * 100, 2)
        
        return {
            "test_id": test_id,
            "test_name": test["config"]["name"],
            "total_samples": len(results),
            "version_a": {
                "samples": len(results_a),
                "metrics": metrics_a
            },
            "version_b": {
                "samples": len(results_b),
                "metrics": metrics_b
            },
            "improvement": improvement,
            "conclusion": self._get_conclusion(improvement)
        }
    
    def _calc_metrics(self, results: List[Dict]) -> Dict[str, float]:
        """计算指标均值"""
        if not results:
            return {}
        
        # 收集所有指标
        all_metrics = {}
        for r in results:
            for key, value in r.get("metrics", {}).items():
                if isinstance(value, (int, float)):
                    if key not in all_metrics:
                        all_metrics[key] = []
                    all_metrics[key].append(value)
        
        # 计算均值
        return {
            key: round(sum(values) / len(values), 2) 
            for key, values in all_metrics.items()
        }
    
    def _get_conclusion(self, improvement: Dict[str, float]) -> str:
        """生成结论"""
        if not improvement:
            return "数据不足，无法得出结论"
        
        positive = sum(1 for v in improvement.values() if v > 0)
        negative = sum(1 for v in improvement.values() if v < 0)
        
        if positive > negative:
            return "B版本表现更优，建议切换到B版本"
        elif negative > positive:
            return "A版本表现更优，建议保持A版本"
        else:
            return "A/B版本表现相近，无明显差异"
    
    # ========== 测试控制 ==========
    
    def start_test(self, test_id: str) -> bool:
        """启动测试"""
        test_file = self.tests_dir / f"{test_id}.json"
        
        if not test_file.exists():
            return False
        
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        test_data["config"]["status"] = "running"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def pause_test(self, test_id: str) -> bool:
        """暂停测试"""
        test_file = self.tests_dir / f"{test_id}.json"
        
        if not test_file.exists():
            return False
        
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        test_data["config"]["status"] = "paused"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def complete_test(self, test_id: str) -> bool:
        """完成测试"""
        test_file = self.tests_dir / f"{test_id}.json"
        
        if not test_file.exists():
            return False
        
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        test_data["config"]["status"] = "completed"
        test_data["config"]["end_time"] = datetime.now().isoformat() + "Z"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        return True


# 预定义测试配置

DEFAULT_AB_TESTS = {
    "constraint_filter_test": {
        "name": "约束过滤逻辑测试",
        "description": "测试生成阶段嵌入约束 vs 事后过滤",
        "version_a": {
            "约束方式": "事后过滤"
        },
        "version_b": {
            "约束方式": "生成阶段嵌入"
        }
    },
    "opener_test": {
        "name": "资深从业者开场问题测试",
        "description": "测试破冰式开场 vs 抽象式开场",
        "version_a": {
            "开场问题": "抽象式",
            "问题": "你本次拆解分析的核心诉求，除了已明确的目标之外，还有哪些个性化的需求与期待？"
        },
        "version_b": {
            "开场问题": "破冰式",
            "问题": "在你想要做的这个方向上，之前有没有尝试过什么？如果有，卡在哪里、遇到了什么困难？"
        }
    },
    "question_format_test": {
        "name": "问题格式测试",
        "description": "测试带选项的问题 vs 开放式问题",
        "version_a": {
            "问题格式": "开放式"
        },
        "version_b": {
            "问题格式": "带选项"
        }
    }
}


# 全局实例
_ab_tester = None

def get_ab_tester() -> ABTester:
    """获取A/B测试器单例"""
    global _ab_tester
    if _ab_tester is None:
        _ab_tester = ABTester()
    return _ab_tester
