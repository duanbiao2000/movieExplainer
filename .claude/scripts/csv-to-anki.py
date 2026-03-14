#!/usr/bin/env python3
"""
CSV to Anki .apkg 转换器
将 anki-deck.csv 转换为可直接导入的 .apkg 文件

依赖安装: pip install genanki
"""

import csv
import genanki
import os
import sys

# Anki 模型 ID (自定义数字)
MODEL_ID = 1607394011
DECK_ID = 1607394012


def create_anki_model():
    """创建 Anki 卡片模型"""
    return genanki.Model(
        MODEL_ID,
        'IELTS Model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
            {
                'name': 'IELTS Card',
                'qfmt': '<div class="front">{{Front}}</div>',
                'afmt': '''
{{FrontSide}}

<hr id="answer">

<div class="back">{{Back}}</div>

<style>
.front { font-size: 24px; text-align: center; padding: 20px; }
.back { font-size: 18px; line-height: 1.6; padding: 20px; }
b { color: #007bff; }
</style>
''',
            },
        ],
        css='''
.card {
    font-family: Arial, sans-serif;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
.front { font-size: 24px; text-align: center; padding: 20px; }
.back { font-size: 18px; line-height: 1.6; padding: 20px; text-align: left; }
b { color: #007bff; font-weight: bold; }
hr { border: none; border-top: 2px solid #ddd; margin: 20px 0; }
''',
    )


def parse_csv(csv_path):
    """解析 CSV 文件，返回卡片列表"""
    notes = []
    model = create_anki_model()

    with open(csv_path, 'r', encoding='utf-8') as f:
        # 读取所有行
        lines = f.readlines()

        # 找到数据开始的行（跳过注释和空行）
        data_start = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#'):
                data_start = i
                break

        # 从数据开始解析
        data_lines = lines[data_start:]

        # 手动解析制表符分隔的 CSV
        for i, line in enumerate(data_lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # 跳过表头
            if i == 0 and line.startswith('Front'):
                continue

            # 按制表符分割（但不分割引号内的制表符）
            parts = []
            current = ''
            in_quotes = False

            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                    current += char
                elif char == '\t' and not in_quotes:
                    parts.append(current)
                    current = ''
                else:
                    current += char

            if current:
                parts.append(current)

            # 至少需要 Front 和 Back 两列
            if len(parts) >= 2:
                # 去除引号
                front = parts[0].strip('"')
                back = parts[1].strip('"')
                tags = parts[2].strip('"') if len(parts) > 2 else ''

                if front and back:
                    # 解析标签（空格分隔）
                    tag_list = tags.split() if tags else []

                    note = genanki.Note(
                        model=model,
                        fields=[front, back],
                        tags=tag_list
                    )
                    notes.append(note)

    return notes, model


def get_deck_name(csv_path):
    """从 CSV 文件路径提取卡组名称"""
    base_name = os.path.basename(csv_path)
    if base_name == 'anki-deck.csv':
        return "MovieExplainer"
    return base_name.replace('.csv', '')


def csv_to_apkg(csv_path, output_path=None):
    """将 CSV 转换为 .apkg 文件"""
    if not os.path.exists(csv_path):
        print(f"错误: 文件不存在 - {csv_path}")
        return False

    # 解析 CSV
    notes, model = parse_csv(csv_path)

    if not notes:
        print("错误: CSV 文件中没有有效的卡片数据")
        return False

    # 创建卡组
    deck_name = get_deck_name(csv_path)
    deck = genanki.Deck(DECK_ID, deck_name)

    for note in notes:
        deck.add_note(note)

    # 确定输出路径
    if output_path is None:
        output_path = csv_path.replace('.csv', '.apkg')

    # 生成 .apkg 文件
    genanki.Package(deck).write_to_file(output_path)

    print(f"[OK] Successfully generated: {output_path}")
    print(f"[INFO] Card count: {len(notes)}")
    print(f"[INFO] Deck name: {deck_name}")

    return True


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python csv-to-anki.py <csv文件路径> [输出文件路径]")
        print("\n示例:")
        print("  python csv-to-anki.py anki-deck.csv")
        print("  python csv-to-anki.py anki-deck.csv my-deck.apkg")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    csv_to_apkg(csv_path, output_path)


if __name__ == '__main__':
    main()
