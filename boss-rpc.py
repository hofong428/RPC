# -*- coding:utf-8 -*-
# File Name: boss-rpc.py
# Author: Codebat_Raymond
# Date: 5/29/2023
import requests

data= {
    "group": "rpc-boss",
    "action": "des",
    'e': 'JExF04lhTh8KXCL/fX7IC8Ww5IJXoOmlRVMTq5BoccA6tPloX5Jmgr9wRrmbirT5j1CtQnjqLvDfulkCGJmI2Q==',
    't': '1685292596373'
    }
# we can catch different cookie value when the a & t set well
sign = requests.get("http://127.0.0.1:5620/business-demo/invoke",params=data )
print(sign.text)