"""
OpenGL Widget 模块 - 提供 PyQt6 OpenGL 渲染器
集成向量场渲染器到 Qt 窗口系统
"""
import sys
from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtGui import QSurfaceFormat
from OpenGL.GL import *
from ..core.events import Event, EventType, event_bus
from ..core.state import state_manager
from .renderer import VectorFieldRenderer


class OpenGLWidget(QOpenGLWidget):
    """OpenGL渲染器Widget"""

    def __init__(self, app_core, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._app_core = app_core

        # 设置OpenGL格式为兼容性模式
        format = QSurfaceFormat()
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
        self.setFormat(format)

        # 渲染器
        self._renderer = VectorFieldRenderer()

        # 渲染状态
        self._initialized = False

        # 订阅事件
        event_bus.subscribe(EventType.GRID_UPDATED, self)
        event_bus.subscribe(EventType.VIEW_RESET, self)
        event_bus.subscribe(EventType.TOGGLE_GRID, self)
        event_bus.subscribe(EventType.VIEW_CHANGED, self)

    def initializeGL(self) -> None:
        """初始化OpenGL"""
        try:
            # 设置OpenGL状态
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            # 初始化渲染器
            self._renderer.initialize()
            self._initialized = True

            print("[OpenGL Widget] 初始化成功")
        except Exception as e:
            print(f"[OpenGL Widget] 初始化失败: {e}")
            self._initialized = False

    def resizeGL(self, width: int, height: int) -> None:
        """调整OpenGL视口大小"""
        glViewport(0, 0, width, height)

    def paintGL(self) -> None:
        """渲染OpenGL内容"""
        if not self._initialized:
            return

        try:
            # 获取状态
            grid = self._app_core.grid_manager.grid
            cell_size = state_manager.get("cell_size", 1.0)
            cam_x = state_manager.get("cam_x", 0.0)
            cam_y = state_manager.get("cam_y", 0.0)
            cam_zoom = state_manager.get("cam_zoom", 1.0)
            grid_width = state_manager.get("grid_width", 640)
            grid_height = state_manager.get("grid_height", 480)

            # 渲染背景
            self._renderer.render_background()

            # 渲染标记
            self._renderer.render_markers(cell_size, cam_x, cam_y, cam_zoom, self.width(), self.height())

            # 渲染网格和向量场
            if grid is not None:
                self._renderer.render_grid(grid, cell_size, cam_x, cam_y, cam_zoom, self.width(), self.height())
                self._renderer.render_vector_field(grid, cell_size, cam_x, cam_y, cam_zoom, self.width(), self.height())

        except Exception as e:
            print(f"[OpenGL Widget] 渲染错误: {e}")

    def update(self) -> None:
        """更新渲染"""
        super().update()

    def cleanup(self) -> None:
        """清理资源"""
        if self._renderer:
            self._renderer.cleanup()
        self._initialized = False

    def handle(self, event: Event) -> None:
        """处理事件"""
        if event.type in [EventType.GRID_UPDATED, EventType.VIEW_RESET, EventType.TOGGLE_GRID, EventType.VIEW_CHANGED]:
            # 触发重绘
            self.update()
