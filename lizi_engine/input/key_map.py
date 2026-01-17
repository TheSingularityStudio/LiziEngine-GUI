"""
键盘映射 - 定义常用键的映射
"""
from PyQt6.QtCore import Qt


class KeyMap:
    """键盘映射类，提供常用键的常量定义"""

    # 特殊键
    UNKNOWN = -1
    SPACE = Qt.Key.Key_Space.value
    APOSTROPHE = Qt.Key.Key_Apostrophe.value
    COMMA = Qt.Key.Key_Comma.value
    MINUS = Qt.Key.Key_Minus.value
    PERIOD = Qt.Key.Key_Period.value
    SLASH = Qt.Key.Key_Slash.value
    SEMICOLON = Qt.Key.Key_Semicolon.value
    EQUAL = Qt.Key.Key_Equal.value

    # 数字键
    _0 = Qt.Key.Key_0.value
    _1 = Qt.Key.Key_1.value
    _2 = Qt.Key.Key_2.value
    _3 = Qt.Key.Key_3.value
    _4 = Qt.Key.Key_4.value
    _5 = Qt.Key.Key_5.value
    _6 = Qt.Key.Key_6.value
    _7 = Qt.Key.Key_7.value
    _8 = Qt.Key.Key_8.value
    _9 = Qt.Key.Key_9.value

    # 字母键
    A = Qt.Key.Key_A.value
    B = Qt.Key.Key_B.value
    C = Qt.Key.Key_C.value
    D = Qt.Key.Key_D.value
    E = Qt.Key.Key_E.value
    F = Qt.Key.Key_F.value
    G = Qt.Key.Key_G.value
    H = Qt.Key.Key_H.value
    I = Qt.Key.Key_I.value
    J = Qt.Key.Key_J.value
    K = Qt.Key.Key_K.value
    L = Qt.Key.Key_L.value
    M = Qt.Key.Key_M.value
    N = Qt.Key.Key_N.value
    O = Qt.Key.Key_O.value
    P = Qt.Key.Key_P.value
    Q = Qt.Key.Key_Q.value
    R = Qt.Key.Key_R.value
    S = Qt.Key.Key_S.value
    T = Qt.Key.Key_T.value
    U = Qt.Key.Key_U.value
    V = Qt.Key.Key_V.value
    W = Qt.Key.Key_W.value
    X = Qt.Key.Key_X.value
    Y = Qt.Key.Key_Y.value
    Z = Qt.Key.Key_Z.value

    # 功能键
    F1 = Qt.Key.Key_F1.value
    F2 = Qt.Key.Key_F2.value
    F3 = Qt.Key.Key_F3.value
    F4 = Qt.Key.Key_F4.value
    F5 = Qt.Key.Key_F5.value
    F6 = Qt.Key.Key_F6.value
    F7 = Qt.Key.Key_F7.value
    F8 = Qt.Key.Key_F8.value
    F9 = Qt.Key.Key_F9.value
    F10 = Qt.Key.Key_F10.value
    F11 = Qt.Key.Key_F11.value
    F12 = Qt.Key.Key_F12.value

    # 方向键
    UP = Qt.Key.Key_Up.value
    DOWN = Qt.Key.Key_Down.value
    LEFT = Qt.Key.Key_Left.value
    RIGHT = Qt.Key.Key_Right.value

    # 特殊键
    LEFT_SHIFT = Qt.Key.Key_Shift.value
    RIGHT_SHIFT = Qt.Key.Key_Shift.value
    LEFT_CONTROL = Qt.Key.Key_Control.value
    RIGHT_CONTROL = Qt.Key.Key_Control.value
    LEFT_ALT = Qt.Key.Key_Alt.value
    RIGHT_ALT = Qt.Key.Key_Alt.value
    LEFT_SUPER = Qt.Key.Key_Meta.value
    RIGHT_SUPER = Qt.Key.Key_Meta.value
    TAB = Qt.Key.Key_Tab.value
    ENTER = Qt.Key.Key_Enter.value
    BACKSPACE = Qt.Key.Key_Backspace.value
    INSERT = Qt.Key.Key_Insert.value
    DELETE = Qt.Key.Key_Delete.value
    PAGE_UP = Qt.Key.Key_PageUp.value
    PAGE_DOWN = Qt.Key.Key_PageDown.value
    HOME = Qt.Key.Key_Home.value
    END = Qt.Key.Key_End.value
    CAPS_LOCK = Qt.Key.Key_CapsLock.value
    SCROLL_LOCK = Qt.Key.Key_ScrollLock.value
    NUM_LOCK = Qt.Key.Key_NumLock.value
    PRINT_SCREEN = Qt.Key.Key_Print.value
    PAUSE = Qt.Key.Key_Pause.value
    ESCAPE = Qt.Key.Key_Escape.value

    # 小键盘
    KP_0 = Qt.Key.Key_0.value  # Qt doesn't distinguish keypad from main keyboard
    KP_1 = Qt.Key.Key_1.value
    KP_2 = Qt.Key.Key_2.value
    KP_3 = Qt.Key.Key_3.value
    KP_4 = Qt.Key.Key_4.value
    KP_5 = Qt.Key.Key_5.value
    KP_6 = Qt.Key.Key_6.value
    KP_7 = Qt.Key.Key_7.value
    KP_8 = Qt.Key.Key_8.value
    KP_9 = Qt.Key.Key_9.value
    KP_DECIMAL = Qt.Key.Key_Period.value
    KP_DIVIDE = Qt.Key.Key_Slash.value
    KP_MULTIPLY = Qt.Key.Key_Asterisk.value
    KP_SUBTRACT = Qt.Key.Key_Minus.value
    KP_ADD = Qt.Key.Key_Plus.value
    KP_ENTER = Qt.Key.Key_Enter.value
    KP_EQUAL = Qt.Key.Key_Equal.value

    # 修饰键 (Qt uses different approach for modifiers)
    MOD_SHIFT = Qt.KeyboardModifier.ShiftModifier.value
    MOD_CONTROL = Qt.KeyboardModifier.ControlModifier.value
    MOD_ALT = Qt.KeyboardModifier.AltModifier.value
    MOD_SUPER = Qt.KeyboardModifier.MetaModifier.value

    @staticmethod
    def get_key_name(key: int) -> str:
        """获取键名

        Args:
            key: PyQt6键码

        Returns:
            str: 键名
        """
        key_names = {
            KeyMap.SPACE: "Space",
            KeyMap.APOSTROPHE: "'",
            KeyMap.COMMA: ",",
            KeyMap.MINUS: "-",
            KeyMap.PERIOD: ".",
            KeyMap.SLASH: "/",
            KeyMap.SEMICOLON: ";",
            KeyMap.EQUAL: "=",
            KeyMap._0: "0",
            KeyMap._1: "1",
            KeyMap._2: "2",
            KeyMap._3: "3",
            KeyMap._4: "4",
            KeyMap._5: "5",
            KeyMap._6: "6",
            KeyMap._7: "7",
            KeyMap._8: "8",
            KeyMap._9: "9",
            KeyMap.A: "A",
            KeyMap.B: "B",
            KeyMap.C: "C",
            KeyMap.D: "D",
            KeyMap.E: "E",
            KeyMap.F: "F",
            KeyMap.G: "G",
            KeyMap.H: "H",
            KeyMap.I: "I",
            KeyMap.J: "J",
            KeyMap.K: "K",
            KeyMap.L: "L",
            KeyMap.M: "M",
            KeyMap.N: "N",
            KeyMap.O: "O",
            KeyMap.P: "P",
            KeyMap.Q: "Q",
            KeyMap.R: "R",
            KeyMap.S: "S",
            KeyMap.T: "T",
            KeyMap.U: "U",
            KeyMap.V: "V",
            KeyMap.W: "W",
            KeyMap.X: "X",
            KeyMap.Y: "Y",
            KeyMap.Z: "Z",
            KeyMap.F1: "F1",
            KeyMap.F2: "F2",
            KeyMap.F3: "F3",
            KeyMap.F4: "F4",
            KeyMap.F5: "F5",
            KeyMap.F6: "F6",
            KeyMap.F7: "F7",
            KeyMap.F8: "F8",
            KeyMap.F9: "F9",
            KeyMap.F10: "F10",
            KeyMap.F11: "F11",
            KeyMap.F12: "F12",
            KeyMap.UP: "Up",
            KeyMap.DOWN: "Down",
            KeyMap.LEFT: "Left",
            KeyMap.RIGHT: "Right",
            KeyMap.LEFT_SHIFT: "Shift",
            KeyMap.RIGHT_SHIFT: "Shift",
            KeyMap.LEFT_CONTROL: "Control",
            KeyMap.RIGHT_CONTROL: "Control",
            KeyMap.LEFT_ALT: "Alt",
            KeyMap.RIGHT_ALT: "Alt",
            KeyMap.LEFT_SUPER: "Meta",
            KeyMap.RIGHT_SUPER: "Meta",
            KeyMap.TAB: "Tab",
            KeyMap.ENTER: "Enter",
            KeyMap.BACKSPACE: "Backspace",
            KeyMap.INSERT: "Insert",
            KeyMap.DELETE: "Delete",
            KeyMap.PAGE_UP: "Page Up",
            KeyMap.PAGE_DOWN: "Page Down",
            KeyMap.HOME: "Home",
            KeyMap.END: "End",
            KeyMap.CAPS_LOCK: "Caps Lock",
            KeyMap.SCROLL_LOCK: "Scroll Lock",
            KeyMap.NUM_LOCK: "Num Lock",
            KeyMap.PRINT_SCREEN: "Print Screen",
            KeyMap.PAUSE: "Pause",
            KeyMap.ESCAPE: "Escape",
            KeyMap.KP_0: "0",
            KeyMap.KP_1: "1",
            KeyMap.KP_2: "2",
            KeyMap.KP_3: "3",
            KeyMap.KP_4: "4",
            KeyMap.KP_5: "5",
            KeyMap.KP_6: "6",
            KeyMap.KP_7: "7",
            KeyMap.KP_8: "8",
            KeyMap.KP_9: "9",
            KeyMap.KP_DECIMAL: "Decimal",
            KeyMap.KP_DIVIDE: "Divide",
            KeyMap.KP_MULTIPLY: "Multiply",
            KeyMap.KP_SUBTRACT: "Subtract",
            KeyMap.KP_ADD: "Add",
            KeyMap.KP_ENTER: "Enter",
            KeyMap.KP_EQUAL: "Equal"
        }
        return key_names.get(key, "Unknown")
