import re
import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

LOCAL = Path(__file__).parent
OUTPUT_JSON_PATH = LOCAL / 'public' / 'satellite_data.json'
DATA_MD_PATH = LOCAL / 'data.md'



def parse_satellite_table(table_text: str) -> Dict[str, Any]:
    """解析单个卫星表格数据"""
    lines = table_text.strip().split('\n')

    # 获取卫星名称
    satellite_name = lines[0].split('|')[1].strip()

    # 初始化数据结构
    satellite_data = {
        "name": satellite_name,
        "frequencies": [],
        "status": "",
        "note": ""
    }

    # 获取表头（频率类型）
    headers = [h.strip() for h in lines[1].split('|')[1:-1]]

    # 找到阶段、状态和备注的行索引
    stages_start = 3  # 跳过表头和分隔符行
    status_row = -2  # 倒数第二行
    note_row = -1  # 最后一行

    # 解析频率数据
    for line in lines[stages_start:status_row]:
        cols = [col.strip() for col in line.split('|')[1:-1]]
        if not cols[0]:  # 跳过空行
            continue

        freq_data = {
            "stage": cols[0],
            "uplink": cols[1],
            "downlink": cols[2],
            "tone": cols[3],
            "shift": cols[4] if len(cols) > 4 else ""
        }
        satellite_data["frequencies"].append(freq_data)

    # 解析状态和备注
    status_cols = [col.strip() for col in lines[status_row].split('|')[1:-1]]
    note_cols = [col.strip() for col in lines[note_row].split('|')[1:-1]]

    satellite_data["status"] = status_cols[1]
    satellite_data["note"] = note_cols[1]

    return satellite_data


def parse_additional_content(text: str) -> Dict[str, Any]:
    """解析额外内容（包括所有标题层级）"""
    content_structure = {}
    current_h2 = None
    current_h3 = None
    current_content = []

    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('## '):
            # 处理二级标题
            if current_h2:
                if current_h3:
                    if isinstance(content_structure[current_h2], str):
                        content_structure[current_h2] = {
                            "content": content_structure[current_h2],
                            current_h3: '\n'.join(current_content).strip()
                        }
                    else:
                        content_structure[current_h2][current_h3] = '\n'.join(current_content).strip()
                else:
                    content_structure[current_h2] = '\n'.join(current_content).strip()

            current_h2 = line.replace('## ', '').strip()
            current_h3 = None
            current_content = []
            content_structure[current_h2] = {}

        elif line.startswith('### '):
            # 处理三级标题
            if current_h3:
                if isinstance(content_structure[current_h2], dict):
                    content_structure[current_h2][current_h3] = '\n'.join(current_content).strip()

            current_h3 = line.replace('### ', '').strip()
            current_content = []

        elif line != '<!--more-->':  # 忽略 more 标记
            current_content.append(line)

    # 处理最后一个部分
    if current_h2 and current_h3:
        content_structure[current_h2][current_h3] = '\n'.join(current_content).strip()
    elif current_h2:
        content_structure[current_h2] = '\n'.join(current_content).strip()

    return content_structure


def parse_md_to_json(md_content: str) -> Dict[str, Any]:
    """解析整个md文件内容"""
    # 分割卫星数据和额外内容
    parts = md_content.split('<!--more-->')
    satellite_tables_text = parts[0]
    additional_content = parts[1] if len(parts) > 1 else ""

    # 使用空行分割不同的表格
    table_texts = re.split(r'\n\s*\n', satellite_tables_text)

    # 解析所有卫星数据
    satellites = []
    for table in table_texts:
        if '|' in table:  # 确保是表格内容
            satellite = parse_satellite_table(table)
            satellites.append(satellite)

    # 解析额外内容
    additional_info = parse_additional_content(additional_content)

    # 构建最终的JSON结构
    result = {
        "satellites": satellites,
        "additional_content": additional_info,
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return result


def main():
    # 读取md文件
    with open(DATA_MD_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 解析内容
    json_data = parse_md_to_json(md_content)

    # 写入JSON文件
    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
        print("成功生成 satellite_data.json 文件")


if __name__ == "__main__":
    main() 