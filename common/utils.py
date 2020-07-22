# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 11:08
# @Author  : Fighter
import base64


def get_base64(pict_file):
    """
    图片转base64
    """
    pict_file_data = open(pict_file, 'rb')
    pict_base64_01 = base64.b64encode(pict_file_data.read())
    pict_base64 = str(pict_base64_01, encoding='utf-8')  # 此句话适用于python3
    pict_file_data.close()

    return pict_base64


if __name__ == '__main__':
    url = r'D:\副驾驶安全带（有）-100张\TIM截图20190521162551.jpg'
    get_base64(url)
