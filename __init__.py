bl_info = {
    "name": "Addon Dev Helper: Pack & Update",
    "author": "YourName",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > N Panel > Dev > Addon Dev Helper",
    "description": "指定开发中的插件目录，一键打包为ZIP，卸载同名旧版本并安装启用新版本。",
    "category": "Development",
}

import bpy
import importlib
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty

# 不在顶层导入子模块的类，避免启用阶段的导入竞态/旧缓存问题
_ops_mod = None
_ui_mod  = None


class ADH_AddonPreferences(AddonPreferences):
    # 使用包名作为 bl_idname，确保首选项与插件绑定
    bl_idname = __name__

    dev_addon_dir: StringProperty(
        name="开发插件目录",
        subtype='DIR_PATH',
        description="你的正在开发的插件根目录（内含 __init__.py）",
        default="",
    )

    output_dir: StringProperty(
        name="ZIP 输出目录",
        subtype='DIR_PATH',
        description="打包ZIP的输出目录；留空则使用系统临时目录",
        default="",
    )

    overwrite_install: BoolProperty(
        name="覆盖安装（如存在）",
        description="安装时允许覆盖已存在的相同文件",
        default=True,
    )

    auto_enable: BoolProperty(
        name="安装后自动启用",
        default=True,
    )

    def draw(self, context):
        # 这里的按钮仍然可用；具体 operator 在 ops 模块注册后就会存在
        layout = self.layout
        col = layout.column()
        col.prop(self, "dev_addon_dir")
        col.prop(self, "output_dir")
        col.prop(self, "overwrite_install")
        col.prop(self, "auto_enable")

        layout.separator()
        row = layout.row(align=True)
        row.operator("adh.pack_zip", text="打包为 ZIP")
        row.operator("adh.install_update", text="安装/覆盖", icon='IMPORT')
        layout.operator("adh.pack_and_update", text="打包并安装启用", icon='RECOVER_LAST')


def register():
    global _ops_mod, _ui_mod

    # 延迟导入，且在开发迭代时支持热重载
    from . import ops as _ops
    from . import ui as _ui

    if _ops_mod is None:
        _ops_mod = _ops
    else:
        importlib.reload(_ops_mod)

    if _ui_mod is None:
        _ui_mod = _ui
    else:
        importlib.reload(_ui_mod)

    # 先注册首选项类，再注册子模块（其中包含面板与 operators）
    bpy.utils.register_class(ADH_AddonPreferences)
    _ops_mod.register()
    _ui_mod.register()


def unregister():
    global _ops_mod, _ui_mod

    # 逆序卸载
    if _ui_mod:
        _ui_mod.unregister()
    if _ops_mod:
        _ops_mod.unregister()
    bpy.utils.unregister_class(ADH_AddonPreferences)
