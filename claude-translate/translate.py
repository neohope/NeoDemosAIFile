#!/usr/bin/env python3
# -*- coding utf-8 -*-

import os
import time
import anthropic
import yaml


'''
批量文本翻译

# for windows
set PATH=%PYTHON_HOME%;%PATH%
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python translate.py

# for linux
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python translate.py
'''

max_len=10000

# 读取apikey
def get_api_key():
    api_key = ""
    with open("config.yaml", "r", encoding="utf-8") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        api_key = yaml_data["anthropic"]["api_key"]
    return api_key


# 把输入翻译为英文
def translate(text):
    prompt = """请将下面的LeTex文件内容，从应为翻译为中文，保留LeTex格式: 

    {}
    """.format(text)

    msg = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=max_len,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return msg


# 枚举并翻译文件，仅支持一层目录
def enum_and_translate_files(en_dir,cn_dir):
    for root, dirs, files in os.walk(en_dir, topdown=False):
        for name in files:
            print(os.path.join(en_dir, name))
            fi = open(os.path.join(en_dir, name), 'r' ,encoding = 'utf-8')
            lines = fi.readlines()
            fi.close()
            
            english = ""
            chinese = ""
            for line in lines:
                if len(line) + len(english) < max_len :
                  english = english + '\n' +line
                else :
                  if len(english) > 0:
                    chinese = chinese + '\n' + translate(english)
                  english = line
                  time.sleep(20)
            
            if len(english) > 0:
                chinese = chinese + '\n' +  translate(english)
                english = ''
                time.sleep(20)
            
            fo = open(os.path.join(cn_dir, name), 'w' ,encoding = 'utf-8')
            fo.write(chinese)
            fo.close()


if __name__ == '__main__':
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=get_api_key(),
    )
    enum_and_translate_files("../en", "../zh")
