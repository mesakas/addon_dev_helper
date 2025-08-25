import bpy
import os
from bpy.types import Operator
from .utils import is_addon_root, module_name_from_dir, make_zip_from_dir


class ADH_OT_pack_zip(Operator):
    bl_idname = "adh.pack_zip"
    bl_label = "打包为 ZIP"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        src = prefs.dev_addon_dir
        if not is_addon_root(src):
            self.report({'ERROR'}, f"不是合法插件目录：{src}")
            return {'CANCELLED'}
        zip_path = make_zip_from_dir(src, prefs.output_dir)
        self.report({'INFO'}, f"已打包：{zip_path}")
        return {'FINISHED'}


class ADH_OT_install_update(Operator):
    bl_idname = "adh.install_update"
    bl_label = "卸载旧版并安装ZIP"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        src = prefs.dev_addon_dir
        if not is_addon_root(src):
            self.report({'ERROR'}, f"不是合法插件目录：{src}")
            return {'CANCELLED'}
        mod = module_name_from_dir(src)

        out_dir = prefs.output_dir or os.path.dirname(src)
        candidates = [
            os.path.join(out_dir, f) for f in os.listdir(out_dir)
            if f.startswith(mod) and f.endswith('.zip')
        ] if os.path.isdir(out_dir) else []

        if not candidates:
            self.report({'ERROR'}, "未找到可安装的ZIP，请先打包。")
            return {'CANCELLED'}
        zip_path = max(candidates, key=lambda p: os.path.getmtime(p))

        try:
            bpy.ops.preferences.addon_remove(module=mod)
        except Exception:
            pass

        ret = bpy.ops.preferences.addon_install(filepath=zip_path, overwrite=True)
        if 'CANCELLED' in ret:
            self.report({'ERROR'}, f"安装失败：{zip_path}")
            return {'CANCELLED'}

        if prefs.auto_enable:
            try:
                bpy.ops.preferences.addon_enable(module=mod)
                bpy.ops.wm.save_userpref()
            except Exception as e:
                self.report({'WARNING'}, f"已安装但未能启用：{e}")
        self.report({'INFO'}, f"已安装并启用：{mod}")
        return {'FINISHED'}


class ADH_OT_pack_and_update(Operator):
    bl_idname = "adh.pack_and_update"
    bl_label = "打包并安装启用"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        src = prefs.dev_addon_dir
        if not is_addon_root(src):
            self.report({'ERROR'}, f"不是合法插件目录：{src}")
            return {'CANCELLED'}
        zip_path = make_zip_from_dir(src, prefs.output_dir)

        mod = module_name_from_dir(src)
        try:
            bpy.ops.preferences.addon_remove(module=mod)
        except Exception:
            pass

        ret = bpy.ops.preferences.addon_install(filepath=zip_path, overwrite=True)
        if 'CANCELLED' in ret:
            self.report({'ERROR'}, f"安装失败：{zip_path}")
            return {'CANCELLED'}
        try:
            bpy.ops.preferences.addon_enable(module=mod)
            bpy.ops.wm.save_userpref()
        except Exception as e:
            self.report({'WARNING'}, f"已安装但未能启用：{e}")
        self.report({'INFO'}, f"完成：{zip_path}")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ADH_OT_pack_zip)
    bpy.utils.register_class(ADH_OT_install_update)
    bpy.utils.register_class(ADH_OT_pack_and_update)


def unregister():
    bpy.utils.unregister_class(ADH_OT_pack_and_update)
    bpy.utils.unregister_class(ADH_OT_install_update)
    bpy.utils.unregister_class(ADH_OT_pack_zip)
