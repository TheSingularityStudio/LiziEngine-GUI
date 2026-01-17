# PyQt6 GUI 集成计划

## 信息收集
- 当前引擎使用 GLFW 进行窗口管理和 OpenGL 进行渲染，通过 VectorFieldRenderer 处理。
- VectorFieldRenderer 负责 OpenGL 着色器编译、VAO/VBO 管理，以及向量场、网格、标记和背景的渲染。
- AppCore 管理状态、事件、网格、视图和 FPS 限制。
- window 模块处理 GLFW 初始化、回调和渲染循环。

## 计划
1. **更新依赖：** 在 requirements.txt 中添加 PyQt6。
2. **创建 GUI 模块：** 开发新的 `lizi_engine/gui/` 模块，包括：
   - `MainWindow` 类，继承自 QMainWindow。
   - `OpenGLWidget` 类，继承自 QOpenGLWidget，用于嵌入原生渲染器。
3. **集成渲染器：** 修改 VectorFieldRenderer，使其与 QOpenGLWidget 的 OpenGL 上下文兼容。
4. **更新应用核心：** 修改 AppCore，使用 PyQt6 GUI 而非 GLFW 窗口。
5. **事件处理：** 适配输入处理到 Qt 的事件系统，同时保留现有的事件总线。
6. **主循环：** 用 Qt 的 QApplication 事件循环替换 GLFW 的循环。

## 需要编辑的文件
- `requirements.txt`：添加 PyQt6。
- `lizi_engine/core/app.py`：更新初始化以使用 GUI。
- 新文件：`lizi_engine/gui/__init__.py`、`lizi_engine/gui/main_window.py`、`lizi_engine/gui/opengl_widget.py`。
- 修改 `lizi_engine/graphics/renderer.py`：适配 QOpenGLWidget 上下文。

## 后续步骤
- 测试 GUI 初始化和渲染。
- 确保输入事件（鼠标、键盘）正常工作。
- 验证性能和兼容性。
