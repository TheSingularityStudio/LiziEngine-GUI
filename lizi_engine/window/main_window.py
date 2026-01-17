"""
主窗口模块 - 提供 PyQt6 主窗口
包含菜单栏、工具栏和嵌入的 OpenGL 渲染器
"""
import sys
from typing import Optional
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QStatusBar, QLabel
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QAction, QKeySequence, QMouseEvent, QWheelEvent, QKeyEvent

from ..core.events import Event, EventType, event_bus
from ..core.state import state_manager
from ..input import input_handler
from ..graphics.opengl_widget import OpenGLWidget


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self, app_core, title: str = "LiziEngine", width: int = 800, height: int = 600):
        super().__init__()

        self._app_core = app_core
        self._title = title
        self._width = width
        self._height = height

        # OpenGL 渲染器
        self._opengl_widget = None

        # 定时器用于渲染循环
        self._render_timer = None

        # 初始化UI
        self._init_ui()

        # 订阅事件
        event_bus.subscribe(EventType.APP_INITIALIZED, self)

    def _init_ui(self) -> None:
        """初始化用户界面"""
        self.setWindowTitle(self._title)
        self.setGeometry(100, 100, self._width, self._height)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout(central_widget)

        # 创建OpenGL渲染器
        self._opengl_widget = OpenGLWidget(self._app_core)
        layout.addWidget(self._opengl_widget)

        # 创建菜单栏
        self._create_menu_bar()

        # 创建状态栏
        self._create_status_bar()

        # 设置渲染定时器
        self._render_timer = QTimer(self)
        self._render_timer.timeout.connect(self._render_frame)
        self._render_timer.start(16)  # ~60 FPS

    def _create_menu_bar(self) -> None:
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')

        # 退出动作
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 视图菜单
        view_menu = menubar.addMenu('视图(&V)')

        # 重置视图动作
        reset_view_action = QAction('重置视图(&R)', self)
        reset_view_action.setShortcut('R')
        reset_view_action.triggered.connect(self._reset_view)
        view_menu.addAction(reset_view_action)

        # 切换网格动作
        toggle_grid_action = QAction('切换网格(&G)', self)
        toggle_grid_action.setShortcut('G')
        toggle_grid_action.triggered.connect(self._toggle_grid)
        view_menu.addAction(toggle_grid_action)

        # 网格菜单
        grid_menu = menubar.addMenu('网格(&G)')

        # 清空网格动作
        clear_grid_action = QAction('清空网格(&C)', self)
        clear_grid_action.setShortcut('C')
        clear_grid_action.triggered.connect(self._clear_grid)
        grid_menu.addAction(clear_grid_action)

    def _create_status_bar(self) -> None:
        """创建状态栏"""
        self.status_bar = self.statusBar()

        # 添加状态标签
        self.fps_label = QLabel("FPS: 0")
        self.status_bar.addWidget(self.fps_label)

        self.grid_size_label = QLabel("网格: 0x0")
        self.status_bar.addWidget(self.grid_size_label)

    def _render_frame(self) -> None:
        """渲染一帧"""
        if self._opengl_widget:
            self._opengl_widget.update()

        # 更新状态栏
        self._update_status_bar()

    def _update_status_bar(self) -> None:
        """更新状态栏信息"""
        # FPS (这里简化处理，实际应该计算真实FPS)
        fps = state_manager.get("target_fps", 60)
        self.fps_label.setText(f"FPS: {fps}")

        # 网格大小
        width = state_manager.get("grid_width", 0)
        height = state_manager.get("grid_height", 0)
        self.grid_size_label.setText(f"网格: {width}x{height}")

    def _reset_view(self) -> None:
        """重置视图"""
        event_bus.publish(Event(
            EventType.RESET_VIEW,
            {},
            "MainWindow"
        ))

    def _toggle_grid(self) -> None:
        """切换网格显示"""
        event_bus.publish(Event(
            EventType.TOGGLE_GRID,
            {},
            "MainWindow"
        ))

    def _clear_grid(self) -> None:
        """清空网格"""
        event_bus.publish(Event(
            EventType.CLEAR_GRID,
            {},
            "MainWindow"
        ))

    def handle(self, event: Event) -> None:
        """处理事件"""
        if event.type == EventType.APP_INITIALIZED:
            if "width" in event.data and "height" in event.data:
                self._width = event.data["width"]
                self._height = event.data["height"]
                self.resize(self._width, self._height)

    def closeEvent(self, event) -> None:
        """窗口关闭事件"""
        # 停止渲染定时器
        if self._render_timer:
            self._render_timer.stop()

        # 清理OpenGL资源
        if self._opengl_widget:
            self._opengl_widget.cleanup()

        # 发布应用关闭事件
        event_bus.publish(Event(
            EventType.APP_SHUTDOWN,
            {},
            "MainWindow"
        ))

        event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """处理键盘按键事件"""
        key = event.key()

        # 发布键盘按下事件
        event_bus.publish(Event(
            EventType.KEY_PRESSED,
            {
                "key": key,
                "text": event.text(),
                "modifiers": event.modifiers().value
            },
            "MainWindow"
        ))

        # 处理特定按键
        if key == Qt.Key.Key_Space:
            # 空格键 - 重新生成模式
            event_bus.publish(Event(
                EventType.SPACE_PRESSED,
                {},
                "MainWindow"
            ))
        elif key == Qt.Key.Key_U:
            # U键 - 切换实时更新
            event_bus.publish(Event(
                EventType.TOGGLE_UPDATE,
                {},
                "MainWindow"
            ))

        # 调用父类方法处理菜单快捷键等
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """处理鼠标按下事件"""
        button = event.button()
        pos = event.position()

        # 获取鼠标位置相对于OpenGL widget的坐标
        if self._opengl_widget:
            widget_pos = self._opengl_widget.pos()
            relative_x = pos.x() - widget_pos.x()
            relative_y = pos.y() - widget_pos.y()
        else:
            relative_x = pos.x()
            relative_y = pos.y()

        # 更新状态管理器中的鼠标位置
        state_manager.set("mouse_x", relative_x)
        state_manager.set("mouse_y", relative_y)

        # 触发input_handler鼠标按下事件 (使用PyQt6按钮值)
        input_handler.handle_mouse_button_event(button.value, 1, (relative_x, relative_y), event.modifiers())

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """处理鼠标释放事件"""
        button = event.button()
        pos = event.position()

        # 获取鼠标位置相对于OpenGL widget的坐标
        if self._opengl_widget:
            widget_pos = self._opengl_widget.pos()
            relative_x = pos.x() - widget_pos.x()
            relative_y = pos.y() - widget_pos.y()
        else:
            relative_x = pos.x()
            relative_y = pos.y()

        # 更新状态管理器中的鼠标位置
        state_manager.set("mouse_x", relative_x)
        state_manager.set("mouse_y", relative_y)

        # 触发input_handler鼠标释放事件
        input_handler.handle_mouse_button_event(button.value, 0, (relative_x, relative_y), event.modifiers())  # RELEASE action

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """处理鼠标移动事件"""
        pos = event.position()

        # 获取鼠标位置相对于OpenGL widget的坐标
        if self._opengl_widget:
            widget_pos = self._opengl_widget.pos()
            relative_x = pos.x() - widget_pos.x()
            relative_y = pos.y() - widget_pos.y()
        else:
            relative_x = pos.x()
            relative_y = pos.y()

        # 更新状态管理器中的鼠标位置
        state_manager.set("mouse_x", relative_x)
        state_manager.set("mouse_y", relative_y)

        # 触发input_handler鼠标移动事件
        input_handler.handle_mouse_move_event((relative_x, relative_y), event.buttons(), event.modifiers())

        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """处理鼠标滚轮事件"""
        delta = event.angleDelta()
        pos = event.position()

        # 获取鼠标位置相对于OpenGL widget的坐标
        if self._opengl_widget:
            widget_pos = self._opengl_widget.pos()
            relative_x = pos.x() - widget_pos.x()
            relative_y = pos.y() - widget_pos.y()
        else:
            relative_x = pos.x()
            relative_y = pos.y()

        # 触发input_handler滚轮事件
        input_handler.handle_scroll_event((delta.x() / 120.0, delta.y() / 120.0), (relative_x, relative_y), event.modifiers())

        super().wheelEvent(event)

    @property
    def opengl_widget(self) -> Optional[OpenGLWidget]:
        """获取OpenGL渲染器"""
        return self._opengl_widget
