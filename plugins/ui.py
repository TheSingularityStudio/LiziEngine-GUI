"""
UI 管理模块：封装用户交互回调、鼠标拖拽与滚轮缩放处理
将与输入相关的逻辑从示例中抽离，便于维护和复用。
使用 Controller 模块处理业务逻辑。
"""
from typing import Tuple
import numpy as np
from lizi_engine.input import input_handler, KeyMap, MouseMap


class UIManager:
    def __init__(self, app_core, window, controller, marker_system):
        self.app_core = app_core
        self.window = window
        self.controller = controller
        self.marker_system = marker_system

        self.enable_update = True

        # 保持最后鼠标位置以便拖拽计算（像素坐标）
        self._last_mouse_x = None
        self._last_mouse_y = None

        # 鼠标按钮状态
        self._mouse_buttons_pressed = set()  # 使用集合跟踪按下的按钮

        # 左键按下时选择的标记
        self._selected_marker = None

    def register_callbacks(self, grid: np.ndarray, on_space=None, on_r=None, on_g=None, on_c=None, on_u=None, on_v=None, on_f=None):
        self._grid = grid

        def on_space_press():
            # 优先使用外部提供的回调（用于切换模式等）
            if callable(on_space):
                try:
                    on_space()
                    return
                except Exception as e:
                    print(f"[错误] on_space 回调异常: {e}")
            # 无外部回调时不执行默认行为

        def on_r_press():
            if callable(on_r):
                try:
                    on_r()
                    return
                except Exception as e:
                    print(f"[错误] on_r 回调异常: {e}")
            try:
                self.controller.reset_view()
            except Exception as e:
                print(f"[错误] reset_view 异常: {e}")

        def on_g_press():
            if callable(on_g):
                try:
                    on_g()
                    return
                except Exception as e:
                    print(f"[错误] on_g 回调异常: {e}")
            try:
                self.controller.toggle_grid()
            except Exception as e:
                print(f"[错误] toggle_grid 异常: {e}")

        def on_c_press():
            if callable(on_c):
                try:
                    on_c()
                    return
                except Exception as e:
                    print(f"[错误] on_c 回调异常: {e}")
            try:
                self.controller.clear_grid()
            except Exception as e:
                print(f"[错误] clear_grid 异常: {e}")
            try:
                # 标记系统也应清空标记
                self.marker_system.clear_markers()
            except Exception as e:
                print(f"[错误] clear_markers 异常: {e}")

        def on_v_press():
            if callable(on_v):
                try:
                    on_v()
                    return
                except Exception as e:
                    print(f"[错误] on_v 回调异常: {e}")
            try:
                self.controller.switch_vector_field_direction()
            except Exception as e:
                print(f"[错误] switch_vector_field_direction 异常: {e}")

        def on_u_press():
            if callable(on_u):
                try:
                    on_u()
                    return
                except Exception as e:
                    print(f"[错误] on_u 回调异常: {e}")

        def on_f_press():
            if callable(on_f):
                try:
                    on_f()
                    return
                except Exception as e:
                    print(f"[错误] on_f 回调异常: {e}")
            try:
                from lizi_engine.core.state import state_manager
                mx = state_manager.get("mouse_x", 0.0)
                my = state_manager.get("mouse_y", 0.0)
                self.controller.place_vector_field(mx, my)
            except Exception as e:
                print(f"[错误] 处理f键按下时发生异常: {e}")

        def on_mouse_left_press():
            try:
                # 添加左键到按下按钮集合
                self._mouse_buttons_pressed.add(1)  # 左键

                from lizi_engine.core.state import state_manager
                mx = state_manager.get("mouse_x", 0.0)
                my = state_manager.get("mouse_y", 0.0)
                self._selected_marker = self.controller.handle_mouse_left_press(mx, my)
            except Exception as e:
                print(f"[错误] 处理鼠标左键按下时发生异常: {e}")

        def on_mouse_left_release():
            # 从按下按钮集合中移除左键
            self._mouse_buttons_pressed.discard(1)
            self._selected_marker = None

        def on_mouse_middle_press():
            # 添加中键到按下按钮集合
            self._mouse_buttons_pressed.add(2)  # 中键
            # 初始化最后鼠标位置以避免拖拽时的跳跃
            from lizi_engine.core.state import state_manager
            self._last_mouse_x = state_manager.get("mouse_x", 0.0)
            self._last_mouse_y = state_manager.get("mouse_y", 0.0)

        def on_mouse_middle_release():
            # 从按下按钮集合中移除中键
            self._mouse_buttons_pressed.discard(2)

        # 注册键盘和鼠标回调 (使用PyQt6动作常量: 1=PRESS, 0=RELEASE)
        input_handler.register_key_callback(KeyMap.SPACE, 1, on_space_press)  # PRESS
        input_handler.register_key_callback(KeyMap.R, 1, on_r_press)  # PRESS
        input_handler.register_key_callback(KeyMap.G, 1, on_g_press)  # PRESS
        input_handler.register_key_callback(KeyMap.C, 1, on_c_press)  # PRESS
        input_handler.register_key_callback(KeyMap.U, 1, on_u_press)  # PRESS
        input_handler.register_key_callback(KeyMap.V, 1, on_v_press)  # PRESS
        input_handler.register_key_callback(KeyMap.F, 1, on_f_press)  # PRESS

        input_handler.register_mouse_callback(MouseMap.LEFT, 1, on_mouse_left_press)  # PRESS
        input_handler.register_mouse_callback(MouseMap.LEFT, 0, on_mouse_left_release)  # RELEASE
        input_handler.register_mouse_callback(MouseMap.MIDDLE, 1, on_mouse_middle_press)  # PRESS
        input_handler.register_mouse_callback(MouseMap.MIDDLE, 0, on_mouse_middle_release)  # RELEASE

    def process_mouse_drag(self):
        from lizi_engine.core.state import state_manager
        # 处理鼠标左键持续按下，在标记位置添加向量
        if 1 in self._mouse_buttons_pressed and self._selected_marker is not None:
            try:
                mx = state_manager.get("mouse_x", 0.0)
                my = state_manager.get("mouse_y", 0.0)
                self.controller.handle_mouse_drag(mx, my, self._selected_marker)
            except Exception as e:
                print(f"[错误] 处理左键持续按下时发生异常: {e}")

        # 只在鼠标中键按下时才允许拖动视图
        if 2 in self._mouse_buttons_pressed:  # 中键
            try:
                x = state_manager.get("mouse_x", 0.0)
                y = state_manager.get("mouse_y", 0.0)

                dx = x - (self._last_mouse_x if self._last_mouse_x is not None else x)
                dy = y - (self._last_mouse_y if self._last_mouse_y is not None else y)

                self.controller.handle_mouse_drag_view(dx, dy)

                self._last_mouse_x = x
                self._last_mouse_y = y
            except Exception as e:
                print(f"[错误] process_mouse_drag_view 异常: {e}")
        else:
            # 清除上次位置，避免下次拖拽跳跃
            self._last_mouse_x = None
            self._last_mouse_y = None

    def process_scroll(self):
        window = self.window
        if hasattr(window, "_scroll_y") and window._scroll_y != 0:
            try:
                self.controller.handle_scroll_zoom(window._scroll_y)
            except Exception as e:
                print(f"[错误] process_scroll 异常: {e}")

            window._scroll_y = 0

    def update_markers(self, grid: np.ndarray, dt: float = 1.0, clear_threshold: float = 1e-3):
        """使用标记系统更新标记位置

        Args:
            grid: 向量场网格
            dt: 时间步长
            clear_threshold: 清除阈值，低于此平均幅值的标记将被清除
        """
        self.marker_system.update_markers(grid, dt, clear_threshold)

