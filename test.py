import urllib
import base64
import hmac
import time
import uuid
import random
from hashlib import sha1
import datetime
import sys
import os

url = 'https://tds.fj-1.res.sgmc.sgcc.com.cn/?'
Action = 'DescribeAlarmEventList'
CurrentPage = 1
From = 'sas'
PageSize = 20
Format = 'JSON'
Version = '2018-12-03'
'Signature=?????'
SignatureMethod = 'HMAC-SHA1'
SignatureNonce = uuid.uuid4()
SignatureVersion = 1.0
AccessKeyId = 'YTmb9KJ2V8b8h4nY'
Timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
AccessKeySecret = 'qoftK9ZHczhhueO5rji1wfbhXMvOX'

parameters = {
    "Action": Action,
    "CurrentPage": CurrentPage,
    "From": From,
    "PageSize": PageSize,
    "Format": Format,
    "Version": Version,
    "SignatureMethod": SignatureMethod,
    "SignatureNonce": SignatureNonce,
    "SignatureVersion": SignatureVersion,
    "AccessKeyId": AccessKeyId,
    "Timestamp": Timestamp
}


def make_Signature():
    sortedparameters = sorted(parameters.items(), key=lambda x: x[0])
    print(sortedparameters)
    return sortedparameters
str = make_Signature()


def percentEncode(str):
    res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res  # 这里构造一个编码函数，对一个字符串进行编码，返回编码后的字符串


percentEncode(str)
