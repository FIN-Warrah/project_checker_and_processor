import os
import re


def find_chinese_start_positions(text):
    """ 查找字符串中连续的中文字符和标点的起始位置 """
    # 匹配中文字符、常用中文标点符号以及全角符号
    return [match.start() for match in re.finditer(r'[\u4e00-\u9fff\u3000-\u303f\uff01-\uff60]+', text)]


def print_tree(directory, ignored_extensions, prefix=''):
    """ 递归打印目录树，显示包含中文字符和标点的文件、行号、行内容和中文片段的起始位置 """
    if os.path.isdir(directory):
        for item in os.listdir(directory):
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                print_tree(path, ignored_extensions, prefix + '|   ')
            elif not any(item.endswith(ext) for ext in ignored_extensions):  # 忽略特定扩展名的文件
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    for i, line in enumerate(file, 1):
                        chinese_positions = find_chinese_start_positions(line)
                        if chinese_positions:
                            print(f"{prefix}+-- {path}: Line {i}, Start Positions: {chinese_positions}")
                            print(f"{prefix}|   {line.strip()}")


if __name__ == '__main__':
    # 使用示例
    input_directory = input("请输入目录路径：")
    ignored_extensions = ['.pt', '.bin', '.dat']  # 示例忽略的扩展名列表
    print_tree(input_directory, ignored_extensions)
