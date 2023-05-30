# -*- coding:utf-8 -*-
# File Name: tampermonkey.py
# Author: Codebat_Raymond
# Date: 5/27/2023

import requests
data = {
    "group": "tt-test",
    "action": "toutiao",
    'url':'https://www.toutiao.com/api/pc/list/feed?offset=0&channel_id=94349549395&max_behot_time=0&category=pc_profile_channel&disable_raw_data=true&aid=24&app_name=toutiao_web'
    }
sign = requests.get("http://127.0.0.1:5620/business-demo/invoke",params=data )
_signature = sign.json().get('data')

url = 'https://www.toutiao.com/api/pc/list/feed?offset=0&channel_id=94349549395&max_behot_time=0&category=pc_profile_channel&disable_raw_data=true&aid=24&app_name=toutiao_web&_signature={}'.format(_signature)

print(url)
