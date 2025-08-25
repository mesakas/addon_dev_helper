import bpy
from bpy.types import Panel


def _get_prefs_safe():
    """
    安全地获取本插件的首选项；若未启用或异常，返回 None。
    """
    try:
        return bpy.context.preferences.addons[__package__].preferences
    except Exception:
        return None


# 仍保留首选项页中的说明面板（可选）
class ADH_PT_preferences_panel(Panel):
    bl_space_type = 'PREFERENCES'
    bl_region_type = 'WINDOW'
    bl_context = "addons"
    bl_label = "Addon Dev Helper"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="在本页下方的 Addon Dev Helper 首选项中配置并使用按钮。")


# 新增：3D 视口右侧 N 面板
class ADH_PT_sidebar_panel(Panel):
    bl_space_type = 'VIEW_3D'      # 视口
    bl_region_type = 'UI'          # N 面板
    bl_category = 'Dev'            # 侧栏标签名（可按需改）
    bl_label = 'Addon Dev Helper'  # 面板标题
    bl_idname = 'ADH_PT_sidebar_panel'

    def draw(self, context):
        layout = self.layout
        prefs = _get_prefs_safe()

        if not prefs:
            # 插件未启用或获取失败
            box = layout.box()
            box.label(text="无法获取首选项，请在首选项中启用本插件。", icon='ERROR')
            return

        # 路径区域
        box = layout.box()
        box.label(text="开发插件目录（根目录）")
        box.prop(prefs, "dev_addon_dir", text="")
        box.separator()

        box.label(text="ZIP 输出目录（可选）")
        box.prop(prefs, "output_dir", text="")

        # 选项
        row = box.row(align=True)
        row.prop(prefs, "overwrite_install")
        row.prop(prefs, "auto_enable")

        layout.separator()

        # 操作按钮
        col = layout.column(align=True)
        col.operator("adh.pack_and_update", text="打包并导入（覆盖安装）", icon='RECOVER_LAST')

        # 也提供分步按钮（可选）
        row = layout.row(align=True)
        row.operator("adh.pack_zip", text="仅打包 ZIP")
        row.operator("adh.install_update", text="仅安装/覆盖", icon='IMPORT')


def register():
    bpy.utils.register_class(ADH_PT_preferences_panel)
    bpy.utils.register_class(ADH_PT_sidebar_panel)


def unregister():
    bpy.utils.unregister_class(ADH_PT_sidebar_panel)
    bpy.utils.unregister_class(ADH_PT_preferences_panel)
