# Addon Dev Helper

**Addon Dev Helper** 是一个 Blender 开发辅助插件，功能是：

- 指定一个**正在开发的插件目录**（含 `__init__.py`）。
- 一键 **打包该目录为 ZIP**。
- 自动 **卸载同名旧插件**，并 **安装 + 启用新版本**。
- 在 **3D 视口右侧 N 面板** 提供控制面板，随时一键更新。

非常适合插件开发者调试和迭代。

---

## 功能特性

- [x] 自动打包插件为 ZIP（排除 `.git/`、`__pycache__/`、`.vscode/` 等常见目录和临时文件）。
- [x] 自动覆盖安装，避免手动卸载/导入的繁琐步骤。
- [x] 可选 **自动启用** 并保存首选项。
- [x] 首选项页和 N 面板都有入口，随时可操作。
- [x] 兼容 Blender 4.2（去掉了部分旧的 icon 枚举）。

---

## 安装

1. 将整个文件夹 `addon_dev_helper/` 拷贝到 Blender 的插件目录：

   - Windows  
     `%APPDATA%\Blender Foundation\Blender\<版本号>\scripts\addons\`

   - macOS  
     `~/Library/Application Support/Blender/<版本号>/scripts/addons/`

   - Linux  
     `~/.config/blender/<版本号>/scripts/addons/`

2. 启动 Blender，在 **编辑 > 首选项 > 插件** 搜索 **Addon Dev Helper** 并启用。

---

## 使用方法

### 在首选项中
1. 在插件的首选项里设置：
   - **开发插件目录**：指向你正在开发的插件的根目录（必须包含 `__init__.py`）。
   - **ZIP 输出目录**（可选）：打包后的 ZIP 保存位置（不填则使用系统临时目录）。
   - **覆盖安装**、**安装后自动启用**：可勾选。

2. 点击按钮：
   - **打包为 ZIP**  
   - **安装/覆盖**  
   - **打包并安装启用**（推荐，通常只需要这一键即可）

### 在 3D 视口（推荐）
1. 打开 3D 视口，按 `N` 键，进入右侧 **Dev** 标签页。  
2. 在 **Addon Dev Helper** 面板中，直接点 **打包并导入（覆盖安装）**。  
   - 会自动打包 → 卸载旧版 → 安装新版 → 启用。

---

## 示例工作流

1. 修改你的插件源代码（例如 `my_addon/__init__.py`）。  
2. 在 Blender 里点击 **打包并导入（覆盖安装）**。  
3. 新的代码即刻生效，无需手动打包/导入。  
4. 重复迭代开发

---

## 注意事项

- 插件目录名就是 Blender 启用时的模块名，需与 `__init__.py` 一致。  
- 旧的 `__pycache__` 可能导致残留错误，升级插件时如果出问题，请删除： %APPDATA%\Blender Foundation\Blender<版本号>\scripts\addons\addon_dev_helper\
然后重新复制文件夹。  
