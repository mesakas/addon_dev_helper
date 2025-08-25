import os
import re
import zipfile
import tempfile

EXCLUDE_DIRS = {'.git', '.idea', '.vs', '.vscode', '__pycache__', 'build', 'dist', 'node_modules', '.svn'}
EXCLUDE_SUFFIXES = {'.pyc', '.pyo', '.blend1', '.blend2', '.zip', '.log'}
EXCLUDE_FILES = {'.DS_Store'}


def is_addon_root(path: str) -> bool:
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, '__init__.py'))


def read_bl_info(init_py: str):
    """从 __init__.py 里读出 bl_info 的 name 和 version"""
    if not os.path.isfile(init_py):
        return None, None
    text = open(init_py, 'r', encoding='utf-8', errors='ignore').read()
    name = None
    ver = None
    m_name = re.search(r"bl_info\\s*=\\s*\\{[\\s\\S]*?\\\"name\\\"\\s*:\\s*\\\"([^\\\"]+)\\\"", text)
    if m_name:
        name = m_name.group(1)
    m_ver = re.search(r"\\\"version\\\"\\s*:\\s*\\((\\s*\\d+\\s*,\\s*\\d+\\s*,\\s*\\d+\\s*)\\)", text)
    if m_ver:
        ver = tuple(int(x.strip()) for x in m_ver.group(1).split(','))
    return name, ver


def module_name_from_dir(path: str) -> str:
    return os.path.basename(os.path.abspath(path))


def ensure_output_dir(out_dir: str) -> str:
    if out_dir and os.path.isdir(out_dir):
        return out_dir
    return tempfile.gettempdir()


def should_exclude(rel_path: str) -> bool:
    parts = rel_path.replace('\\', '/').split('/')
    for p in parts[:-1]:
        if p in EXCLUDE_DIRS:
            return True
    base = parts[-1]
    if base in EXCLUDE_FILES:
        return True
    _, ext = os.path.splitext(base)
    if ext in EXCLUDE_SUFFIXES:
        return True
    return False


def make_zip_from_dir(src_dir: str, out_dir: str, zip_basename: str = None) -> str:
    assert is_addon_root(src_dir), f"不是合法的插件根目录：{src_dir}（缺少 __init__.py）"
    mod_name = module_name_from_dir(src_dir)
    name, ver = read_bl_info(os.path.join(src_dir, '__init__.py'))
    if zip_basename is None:
        if ver:
            zip_basename = f"{mod_name}-{ver[0]}.{ver[1]}.{ver[2]}"
        else:
            zip_basename = mod_name
    out_dir = ensure_output_dir(out_dir)
    zip_path = os.path.join(out_dir, f"{zip_basename}.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for fn in files:
                abs_path = os.path.join(root, fn)
                rel_path = os.path.relpath(abs_path, start=src_dir)
                if should_exclude(rel_path):
                    continue
                arcname = f"{mod_name}/" + rel_path.replace('\\', '/')
                zf.write(abs_path, arcname)
    return zip_path
