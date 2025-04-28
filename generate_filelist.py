# -*- coding: utf-8 -*-
import os
import json

# 配置
ROOT_DIR_NAME = 'SYSTEM'  # 需要扫描的目录名称
OUTPUT_FILE = 'filelist.json' # 输出的 JSON 文件名
# 如果需要，可以添加要忽略的文件扩展名或文件名
IGNORED_ITEMS = {'.DS_Store', '.git', '.gitignore'} # 忽略 macOS 的 .DS_Store 和 Git 相关文件

def scan_directory(dir_path):
    """递归扫描目录并构建嵌套字典。"""
    tree = {}
    try:
        # 列出目录项，处理可能的权限错误
        items = [item for item in os.listdir(dir_path) if item not in IGNORED_ITEMS]
    except OSError as e:
        print(f"警告：无法列出目录 {dir_path}: {e}")
        return {} # 如果目录无法读取，返回空字典

    for item in items:
        item_path = os.path.join(dir_path, item)
        try:
            if os.path.isdir(item_path):
                # 是目录，进行递归
                tree[item] = {
                    "type": "directory",
                    "children": scan_directory(item_path) # 递归调用
                }
            elif os.path.isfile(item_path):
                # 是文件
                tree[item] = {
                    "type": "file"
                }
            # 忽略其他类型，如符号链接等
        except OSError as e:
             print(f"警告：无法访问 {item_path}: {e}") # 处理无法访问的文件或目录
    return tree

def main():
    """主函数，用于生成 JSON 文件。"""
    # 获取脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 SYSTEM 目录的完整路径
    system_dir_path = os.path.join(script_dir, ROOT_DIR_NAME)
    # 构建输出文件的完整路径
    output_path = os.path.join(script_dir, OUTPUT_FILE)

    if not os.path.isdir(system_dir_path):
        print(f"错误：在 {script_dir} 中未找到目录 '{ROOT_DIR_NAME}'")
        return

    print(f"正在扫描目录: {system_dir_path}...")
    # 扫描根 'SYSTEM' 目录
    children_structure = scan_directory(system_dir_path)

    # 构建最终的 JSON 结构，包含根对象
    final_structure = {
        "name": ROOT_DIR_NAME,
        "type": "directory",
        "children": children_structure
    }

    print(f"正在将文件列表写入: {output_path}...")
    try:
        # 使用 'w' 模式打开文件（写入），指定 utf-8 编码
        with open(output_path, 'w', encoding='utf-8') as f:
            # ensure_ascii=False 确保非 ASCII 文件名正确写入，indent=2 实现美观的缩进
            json.dump(final_structure, f, ensure_ascii=False, indent=2)
        print("成功生成 filelist.json!")
    except IOError as e:
        print(f"错误：写入 JSON 文件时出错: {e}")

# 当脚本直接运行时，调用 main 函数
if __name__ == '__main__':
    main()