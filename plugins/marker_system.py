
"""
标记系统插件：管理向量场中的标记点
提供标记点的创建、更新和渲染功能。
"""
from typing import List, Dict, Any
import numpy as np
from lizi_engine.compute.vector_field import vector_calculator

class MarkerSystem:
    """标记系统，用于管理向量场中的标记点"""

    def __init__(self, app_core):
        self.app_core = app_core
        # 标记列表，存储浮点网格坐标 {'x':float,'y':float}
        self.markers = []

    def add_marker(self, x: float, y: float, mag: float = 1.0) -> None:
        """添加一个新标记

        Args:
            x: 标记的x坐标（浮点）
            y: 标记的y坐标（浮点）
            mag: 标记的初始幅值（可选）
        """
        marker = {"x": float(x), "y": float(y), "mag": float(mag)}
        self.markers.append(marker)
        self._sync_to_state_manager()

    def clear_markers(self) -> None:
        """清除所有标记"""
        self.markers = []
        self._sync_to_state_manager()

    def get_markers(self) -> List[Dict[str, float]]:
        """获取所有标记

        Returns:
            标记列表
        """
        return list(self.markers)

    def update_markers(self, grid: np.ndarray, neighborhood: int = 5,
                      move_factor: float = 1.0, clear_threshold: float = 1e-3) -> None:
        """根据周围向量平均方向移动标记以收敛到中心。

        算法：在每个标记的邻域内计算平均向量(mean_v)，将标记按 -mean_v * move_factor 偏移。
        这对径向场有效：向外的平均向量的负方向指向中心。

        Args:
            grid: 向量场网格
            neighborhood: 邻域大小
            move_factor: 移动因子
            clear_threshold: 清除阈值，低于此平均幅值的标记将被清除
        """
        if not hasattr(grid, "ndim"):
            return

        # 优先从全局状态同步标记（如果其他模块在放置向量场时添加了标记）
        try:
            stored = self.app_core.state_manager.get("markers", None)
            if stored is not None:
                self.markers = list(stored)
        except Exception:
            pass

        # 检查网格维度是否有效
        if grid.ndim < 3 or grid.shape[2] < 2:
            return

        h, w = grid.shape[0], grid.shape[1]

        # 期望 grid 最后一维至少 2，代表 vx, vy
        new_markers = []

        # 提取vx和vy分量，避免重复索引
        vx_field = grid[:, :, 0]
        vy_field = grid[:, :, 1]

        for m in self.markers:
            x = m.get("x", 0.0)
            y = m.get("y", 0.0)

            # 整数邻域范围
            cx = int(round(x))
            cy = int(round(y))

            sx = max(0, cx - neighborhood)
            ex = min(w - 1, cx + neighborhood)
            sy = max(0, cy - neighborhood)
            ey = min(h - 1, cy + neighborhood)

            # 使用numpy切片代替循环，提高性能
            try:
                # 提取邻域内的向量场
                vx_neighborhood = vx_field[sy:ey+1, sx:ex+1]
                vy_neighborhood = vy_field[sy:ey+1, sx:ex+1]

                # 计算幅值
                mags = np.sqrt(vx_neighborhood**2 + vy_neighborhood**2)

                # 跳过无效区域
                if vx_neighborhood.size == 0 or vy_neighborhood.size == 0:
                    new_markers.append(m)
                    continue

                # 计算加权平均
                weighted_vx = np.sum(vx_neighborhood * mags)
                weighted_vy = np.sum(vy_neighborhood * mags)
                sum_mag = np.sum(mags)
                count = vx_neighborhood.size

                if count == 0 or sum_mag == 0:
                    # 没有有效向量，保留标记以便后续检查
                    new_markers.append(m)
                    continue

                mean_vx = weighted_vx / count
                mean_vy = weighted_vy / count
                avg_mag = sum_mag / count

                # 如果邻域内平均幅值低于阈值，自动移除该标记
                if avg_mag < clear_threshold:
                    continue

                # 正方向朝向可能的中心
                dx = mean_vx * move_factor
                dy = mean_vy * move_factor

                # 更新浮点位置
                new_x = max(0.0, min(w - 1.0, x + dx))
                new_y = max(0.0, min(h - 1.0, y + dy))

                # 创建径向模式
                #vector_calculator.create_radial_pattern(grid,center=(new_x,new_y), radius=2.0, magnitude=m["mag"])
                # 创建微小向量影响
                self.create_tiny_vector(grid, new_x, new_y, m["mag"])

                m["x"] = new_x
                m["y"] = new_y
                new_markers.append(m)

            except Exception as e:
                # 添加更详细的错误日志
                print(f"Error updating marker at ({x}, {y}): {str(e)}")
                # 保留标记以便后续检查
                new_markers.append(m)
                continue

        # 更新内部标记列表并写回 state_manager 以便界面绘制或外部使用
        self.markers = new_markers
        self._sync_to_state_manager()

    def create_tiny_vector(self, grid: np.ndarray, x: float, y: float, mag: float = 1.0, vx: float = 0.0, vy: float = 0.0) -> None:
        # 在指定位置创建一个微小的向量场影响,只影响位置本身及上下左右四个邻居
        if not hasattr(grid, "ndim"):
            return

        h, w = grid.shape[0], grid.shape[1]

        # 确保坐标在有效范围内
        x = max(0.0, min(w - 1.0, float(x)))
        y = max(0.0, min(h - 1.0, float(y)))

        # 计算整数坐标
        cx = int(round(x))
        cy = int(round(y))

        # 只影响当前位置及其上下左右邻居
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if abs(dx) + abs(dy) == 1:  # 上下左右邻居
                    nx = cx + dx
                    ny = cy + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        try:
                            if grid.ndim >= 3 and grid.shape[2] >= 2:
                                grid[ny, nx, 0] += dx * mag
                                grid[ny, nx, 1] += dy * mag
                        except Exception:
                            continue
        #当前位置的向量值为vx,vy
        if grid.ndim >= 3 and grid.shape[2] >= 2:
            try:
                grid[cy, cx, 0] += vx * mag
                grid[cy, cx, 1] += vy * mag
            except Exception:
                pass

    def _sync_to_state_manager(self) -> None:
        """将标记列表同步到状态管理器"""
        try:
            self.app_core.state_manager.set("markers", list(self.markers))
        except Exception:
            pass
