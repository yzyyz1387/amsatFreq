# python3
# -*- coding: utf-8 -*-
# @Time    : 2024-05-07 19:26
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : ToJson.py
# @Software: PyCharm
import json
import markdown
from pathlib import Path


def md_to_json(md_path:Path, out: str) -> dict:
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()
    sat_info = []
    temp_ = ''
    return_dict = {}

    pre_handle = md.split('<!--more-->')
    sat_sum = pre_handle[0]
    msg = pre_handle[1] if len(pre_handle) > 1 else ''

    sat_sum = sat_sum.strip().split('\n')

    for sat in sat_sum:
        if sat == '':
            sat_info.append(temp_)
            temp_ = ''
            continue
        temp_ = temp_ + sat + '\n'
    for i in sat_info:
        return_dict.update(mk_sat_detl(i))
    msg_html = markdown.markdown(msg)
    return_dict['msg'] = msg_html
    to_json = json.dumps(return_dict, ensure_ascii=False, sort_keys=True, indent=4)
    # print(to_json)
    with open(f"{out}.json", "w", encoding="utf-8") as f:
        f.write(to_json)
        print(f"已生成{out}.json")
    return return_dict


def mk_sat_detl(sat_info: str) -> dict:
    temp_list = sat_info.split('\n')
    return_list = []
    return_dict = {}
    for line in temp_list:
        line = line.replace(' ', '')
        ctx = line.split('|')
        for i in ctx:
            if i == '':
                ctx.remove(i)
        if len(ctx) == 0:
            continue
        return_list.append(ctx)
    return_list.pop(1) if len(return_list) > 2 else ...
    return_dict[return_list[0][0]] = return_list[1:]
    return return_dict


if __name__ == '__main__':
    md_to_json(Path("README.md"),"satFreq")

