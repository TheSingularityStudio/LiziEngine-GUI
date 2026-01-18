"""
输入处理器 - 处理用户输入事件 (PyQt6版本)
"""
import numpy as np
from typing import Dict, Any, Optional, Callable, List, Tuple
from PyQt6.QtCore import Qt
from ..core.events import Event, EventType, event_bus, EventHandler
from ..core.state import state_manager


class InputHandler(EventHandler):
    """输入处理器，管理键盘和鼠标输入"""

    def __init__(self):
        self._event_bus = event_bus
        self._state_manager = state_manager
        self._key_states = {}  # 存储按键状态
        self._mouse_buttons = {}  # 存储鼠标按钮状态
        self._mouse_position = (0.0, 0.0)  # 当前鼠标位置
        self._mouse_scroll = (0.0, 0.0)  # 当前鼠标滚轮位置
        self._key_callbacks = {}  # 按键回调函数
        self._mouse_callbacks = {}  # 鼠标回调函数

    def register_key_callback(self, key: int, action: int, callback: Callable):
        """注册键盘回调函数

        Args:
            key: PyQt6键码
            action: 动作 (PRESS=1, RELEASE=0, REPEAT=2)
            callback: 回调函数
        """
        key_id = f"{key}_{action}"
        self._key_callbacks[key_id] = callback

    def register_mouse_callback(self, button: int, action: int, callback: Callable):
        """注册鼠标回调函数

        Args:
            button: PyQt6鼠标按钮值
            action: 动作 (PRESS=1, RELEASE=0)
            callback: 回调函数
        """
        button_id = f"{button}_{action}"
        self._mouse_callbacks[button_id] = callback

    def is_key_pressed(self, key: int) -> bool:
        """检查按键是否按下

        Args:
            key: PyQt6键码

        Returns:
            bool: 按键是否按下
        """
        return self._key_states.get(key, False)

    def is_mouse_button_pressed(self, button: int) -> bool:
        """检查鼠标按钮是否按下

        Args:
            button: PyQt6鼠标按钮值

        Returns:
            bool: 鼠标按钮是否按下
        """
        return self._mouse_buttons.get(button, False)

    def get_mouse_position(self) -> Tuple[float, float]:
        """获取当前鼠标位置

        Returns:
            Tuple[float, float]: 鼠标位置 (x, y)
        """
        return self._mouse_position

    def get_mouse_scroll(self) -> Tuple[float, float]:
        """获取当前鼠标滚轮位置

        Returns:
            Tuple[float, float]: 鼠标滚轮位置 (x, y)
        """
        return self._mouse_scroll

    def reset_mouse_scroll(self) -> None:
        """重置鼠标滚轮位置为(0, 0)"""
        self._mouse_scroll = (0.0, 0.0)

    def handle_key_event(self, key: int, action: int, modifiers: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier):
        """处理键盘事件 (从PyQt6事件调用)

        Args:
            key: PyQt6键码
            action: 动作 (1=PRESS, 0=RELEASE)
            modifiers: PyQt6修饰键
        """
        # 更新按键状态
        if action == 1:  # PRESS
            self._key_states[key] = True
        elif action == 0:  # RELEASE
            self._key_states[key] = False

        # 触发按键事件
        event_type = EventType.KEY_PRESSED if action == 1 else EventType.KEY_RELEASED
        event = Event(
            type=event_type,
            data={
                "key": key,
                "modifiers": modifiers.value
            }
        )
        self._event_bus.publish(event)

        # 执行注册的回调函数
        key_id = f"{key}_{action}"
        if key_id in self._key_callbacks:
            self._key_callbacks[key_id]()

    def handle_mouse_button_event(self, button: int, action: int, position: Tuple[float, float],
                                  modifiers: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier):
        """处理鼠标按钮事件 (从PyQt6事件调用)

        Args:
            button: PyQt6鼠标按钮值
            action: 动作 (1=PRESS, 0=RELEASE)
            position: 鼠标位置 (x, y)
            modifiers: PyQt6修饰键
        """
        # 更新鼠标按钮状态
        if action == 1:  # PRESS
            self._mouse_buttons[button] = True
        elif action == 0:  # RELEASE
            self._mouse_buttons[button] = False

        # 更新鼠标位置
        self._mouse_position = position

        # 触发鼠标点击事件
        event = Event(
            type=EventType.MOUSE_CLICKED,
            data={
                "button": button,
                "action": action,
                "modifiers": modifiers.value,
                "position": position
            }
        )
        self._event_bus.publish(event)

        # 执行注册的回调函数
        button_id = f"{button}_{action}"
        if button_id in self._mouse_callbacks:
            self._mouse_callbacks[button_id]()

    def handle_mouse_move_event(self, position: Tuple[float, float], buttons: Qt.MouseButton = Qt.MouseButton.NoButton,
                                modifiers: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier):
        """处理鼠标移动事件 (从PyQt6事件调用)

        Args:
            position: 鼠标位置 (x, y)
            buttons: 按下的鼠标按钮
            modifiers: PyQt6修饰键
        """
        # 计算鼠标移动距离
        dx = position[0] - self._mouse_position[0]
        dy = position[1] - self._mouse_position[1]

        # 更新鼠标位置
        self._mouse_position = position

        # 更新鼠标按钮状态 (基于当前按下的按钮)
        self._mouse_buttons = {}
        if buttons & Qt.MouseButton.LeftButton:
            self._mouse_buttons[Qt.MouseButton.LeftButton.value] = True
        if buttons & Qt.MouseButton.RightButton:
            self._mouse_buttons[Qt.MouseButton.RightButton.value] = True
        if buttons & Qt.MouseButton.MiddleButton:
            self._mouse_buttons[Qt.MouseButton.MiddleButton.value] = True

        # 触发鼠标移动事件
        event = Event(
            type=EventType.MOUSE_MOVED,
            data={
                "position": position,
                "delta": (dx, dy),
                "buttons": buttons.value,
                "modifiers": modifiers.value
            }
        )
        self._event_bus.publish(event)

    def handle_scroll_event(self, delta: Tuple[float, float], position: Tuple[float, float],
                           modifiers: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier):
        """处理鼠标滚轮事件 (从PyQt6事件调用)

        Args:
            delta: 滚轮偏移 (x, y)
            position: 鼠标位置 (x, y)
            modifiers: PyQt6修饰键
        """
        # 更新滚轮位置 (累积)
        self._mouse_scroll = (self._mouse_scroll[0] + delta[0], self._mouse_scroll[1] + delta[1])

        # 触发滚轮事件
        event = Event(
            type=EventType.MOUSE_SCROLLED,
            data={
                "offset": delta,
                "position": position,
                "modifiers": modifiers.value
            }
        )
        self._event_bus.publish(event)


# 创建全局输入处理器实例
input_handler = InputHandler()
