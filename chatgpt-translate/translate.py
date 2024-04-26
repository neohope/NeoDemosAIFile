#!/usr/bin/env python3
# -*- coding utf-8 -*-

import os
import time
import openai
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


# 读取apikey
def get_api_key():
    with open("config.yaml", "r", encoding="utf-8") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        openai.api_key = yaml_data["openai"]["api_key"]


# 把输入翻译为英文
def translate_talk(text):
    messages = []
    messages.append( {"role": "system", "content": "You are a translator who translates the user's words into Chinese"})
    messages.append( {"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0.5, max_tokens=2048, n=1
    )
    return response["choices"][0]["message"]["content"]


# 把输入翻译为英文
def translate_completion(text):
    prompt = """Please translate the following article into Chinese: 

    {}
    """.format(text)

    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
        )
    return response["choices"][0]["message"]["content"]


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
                if len(line) + len(english) < 1024 :
                  english = english + '\n' +line
                else :
                  if len(english) > 0:
                    chinese = chinese + '\n' + translate_talk(english)
                  english = line
                  time.sleep(20)
            
            if len(english) > 0:
                chinese = chinese + '\n' +  translate_talk(english)
                english = ''
                time.sleep(20)
            
            fo = open(os.path.join(cn_dir, name), 'w' ,encoding = 'utf-8')
            fo.write(chinese)
            fo.close()


if __name__ == '__main__':
    get_api_key()
    enum_and_translate_files("../en", "../zh")
