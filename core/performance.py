"""
性能监控模块 - 提供应用程序的性能监控和调试功能
"""
import numpy as np
try:
    import psutil
except ImportError:
    psutil = None
from typing import Dict, Any, Optional, List


class DebugTools:
    """调试工具类，用于帮助调试和优化程序"""

    @staticmethod
    def print_grid_info(grid):
        """打印网格信息"""
        if grid is None:
            print("网格为空")
            return

        h, w = grid.shape[:2]
        print(f"网格尺寸: {h}x{w}")
        print(f"网格总点数: {h*w}")

        # 计算统计信息
        vectors = grid.reshape(-1, 2)
        magnitudes = np.sqrt(vectors[:, 0]**2 + vectors[:, 1]**2)

        print(f"向量幅度 - 最小: {np.min(magnitudes):.3f}, 最大: {np.max(magnitudes):.3f}, 平均: {np.mean(magnitudes):.3f}")
        print(f"零向量数量: {np.sum(magnitudes == 0)}")

    @staticmethod
    def analyze_performance_bottleneck(average_times):
        """分析性能瓶颈"""
        total_time = average_times.get('update_time', 0) + average_times.get('render_time', 0)

        if total_time == 0:
            print("无法分析性能瓶颈：总时间为0")
            return

        update_percent = (average_times.get('update_time', 0) / total_time) * 100
        render_percent = (average_times.get('render_time', 0) / total_time) * 100

        print(f"性能瓶颈分析:")
        print(f"更新时间占比: {update_percent:.1f}%")
        print(f"渲染时间占比: {render_percent:.1f}%")

        if update_percent > render_percent:
            print("主要瓶颈：计算/更新")
        else:
            print("主要瓶颈：渲染")

    @staticmethod
    def suggest_optimizations(grid_size, use_opencl):
        """提供优化建议"""
        print(f"优化建议:")

        if grid_size > 1000000:
            print("- 考虑使用更大的网格块或分块处理")
        elif grid_size > 100000:
            print("- 考虑启用GPU加速（如果可用）")

        if not use_opencl:
            print("- 考虑启用OpenCL以获得更好的性能")

        print("- 减少不必要的渲染调用")
        print("- 使用对象池减少内存分配")
        print("- 考虑使用多线程处理CPU密集型任务")


class MemoryMonitor:
    """内存监控器，用于跟踪程序的内存使用情况"""

    def __init__(self):
        self.enabled = True
        self.sample_interval = 1.0  # 采样间隔（秒）
        self.last_sample_time = 0
        self.memory_samples = []
        self.max_samples = 100

    def update(self, current_time):
        """更新内存监控"""
        if not self.enabled:
            return

        if current_time - self.last_sample_time >= self.sample_interval:
            try:
                if psutil is None:
                    return
                process = psutil.Process()
                memory_info = process.memory_info()

                sample = {
                    "time": current_time,
                    "rss": memory_info.rss,  # 物理内存使用量
                    "vms": memory_info.vms,  # 虚拟内存使用量
                    "cpu_percent": process.cpu_percent()
                }

                self.memory_samples.append(sample)

                if len(self.memory_samples) > self.max_samples:
                    self.memory_samples.pop(0)

                self.last_sample_time = current_time

            except ImportError:
                print("[内存监控] psutil未安装，无法监控内存使用情况")
                self.enabled = False
            except Exception as e:
                print(f"[内存监控] 获取内存信息时出错: {e}")

    def get_memory_stats(self):
        """获取内存统计信息"""
        if not self.memory_samples:
            return None

        rss_values = [s["rss"] for s in self.memory_samples]
        vms_values = [s["vms"] for s in self.memory_samples]

        return {
            "current_rss": rss_values[-1],
            "current_vms": vms_values[-1],
            "avg_rss": sum(rss_values) / len(rss_values),
            "max_rss": max(rss_values),
            "min_rss": min(rss_values),
            "samples": len(self.memory_samples)
        }

    def print_memory_stats(self):
        """打印内存统计信息"""
        stats = self.get_memory_stats()
        if stats is None:
            print("没有内存数据可用")
            return

        print("=== 内存使用统计 ===")
        print(f"当前物理内存: {stats['current_rss'] / 1024 / 1024:.1f} MB")
        print(f"当前虚拟内存: {stats['current_vms'] / 1024 / 1024:.1f} MB")
        print(f"平均物理内存: {stats['avg_rss'] / 1024 / 1024:.1f} MB")
        print(f"最大物理内存: {stats['max_rss'] / 1024 / 1024:.1f} MB")
        print(f"样本数量: {stats['samples']}")
        print("=====================")

    def reset(self):
        """重置内存监控数据"""
        self.memory_samples = []
        self.last_sample_time = 0


class PerformanceMonitor:
    """性能监控器，用于跟踪和优化程序性能"""

    def __init__(self):
        self.metrics = {
            "frame_times": [],
            "update_times": [],
            "render_times": [],
            "opencl_times": [],
            "cpu_times": []
        }
        self.max_samples = 100  # 保留最近100个样本

    def record_frame_time(self, time_ms):
        """记录帧时间"""
        self.metrics["frame_times"].append(time_ms)
        if len(self.metrics["frame_times"]) > self.max_samples:
            self.metrics["frame_times"].pop(0)

    def record_update_time(self, time_ms):
        """记录更新时间"""
        self.metrics["update_times"].append(time_ms)
        if len(self.metrics["update_times"]) > self.max_samples:
            self.metrics["update_times"].pop(0)

    def record_render_time(self, time_ms):
        """记录渲染时间"""
        self.metrics["render_times"].append(time_ms)
        if len(self.metrics["render_times"]) > self.max_samples:
            self.metrics["render_times"].pop(0)

    def record_opencl_time(self, time_ms):
        """记录OpenCL计算时间"""
        self.metrics["opencl_times"].append(time_ms)
        if len(self.metrics["opencl_times"]) > self.max_samples:
            self.metrics["opencl_times"].pop(0)

    def record_cpu_time(self, time_ms):
        """记录CPU计算时间"""
        self.metrics["cpu_times"].append(time_ms)
        if len(self.metrics["cpu_times"]) > self.max_samples:
            self.metrics["cpu_times"].pop(0)

    def get_average_times(self):
        """获取平均时间"""
        return {
            "frame_time": np.mean(self.metrics["frame_times"]) if self.metrics["frame_times"] else 0,
            "update_time": np.mean(self.metrics["update_times"]) if self.metrics["update_times"] else 0,
            "render_time": np.mean(self.metrics["render_times"]) if self.metrics["render_times"] else 0,
            "opencl_time": np.mean(self.metrics["opencl_times"]) if self.metrics["opencl_times"] else 0,
            "cpu_time": np.mean(self.metrics["cpu_times"]) if self.metrics["cpu_times"] else 0
        }

    def get_fps(self):
        """获取FPS"""
        if not self.metrics["frame_times"]:
            return 0
        avg_frame_time = np.mean(self.metrics["frame_times"])
        return 1000.0 / avg_frame_time if avg_frame_time > 0 else 0

    def reset(self):
        """重置监控数据"""
        for key in self.metrics:
            self.metrics[key] = []

    def generate_report(self):
        """生成性能报告"""
        report = {
            "fps": self.get_fps(),
            "average_times": self.get_average_times(),
            "sample_counts": {key: len(values) for key, values in self.metrics.items()}
        }
        return report

    def print_report(self):
        """打印性能报告"""
        report = self.generate_report()
        print("=== 性能报告 ===")
        print(f"FPS: {report['fps']:.1f}")
        print(f"平均帧时间: {1000.0/report['fps']:.1f}ms" if report['fps'] > 0 else "平均帧时间: N/A")
        times = report['average_times']
        print(f"平均更新时间: {times['update_time']:.1f}ms")
        print(f"平均渲染时间: {times['render_time']:.1f}ms")
        print(f"样本数量: {report['sample_counts']}")
        print("================")


# 全局性能监控器实例
performance_monitor = PerformanceMonitor()
memory_monitor = MemoryMonitor()
debug_tools = DebugTools()
