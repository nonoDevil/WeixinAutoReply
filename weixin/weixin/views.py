# coding: utf-8 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import xml.etree.ElementTree as ET
import time,hashlib
import datetime

#微信公共主页开发模式设置的token，http://mp.weixin.qq.com/
#此处用TOKEN代替，可自行更改，但要和开发模式设置的一致
TOKEN = "TOKEN"

#由于django防止csrf攻击的特性，导致请求无法正常获取，所以此处用@csrf_exempt关闭此特性
#根据微信文档说明GET用来响应微信校验，POST用来传递回复信息
@csrf_exempt
def handleRequest(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response
    elif request.method == 'POST':
        response = HttpResponse(responseMsg(request),content_type="application/xml")
        return response
    else:
        return None

#检测微信服务器发来的签名
def checkSignature(request):
    global TOKEN
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)

    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        return None

#响应用户输入，回复文本信息
#当微信服务器发送'Hello2BizUser'消息时，说明此用户是刚关注微信公共主页
#PS:现在用户关注公共主页时，微信服务器发送的不再是'Hello2BizUser'文本消息
#而是一个subscribe事件
def responseMsg(request):
    rawStr = smart_str(request.raw_post_data)
    #rawStr = smart_str(request.POST['XML'])
    msg = paraseMsgXml(ET.fromstring(rawStr))
    if msg['Content'] == 'Hello2BizUser':
        replyContent = '感谢关注!'
    else:
        replyContent = 'Hello'
        

    return getReplyXml(msg,replyContent)

#解析微信服务器发过来的xml
def paraseMsgXml(rootElem):
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg

#回复文本消息,使用微信指定的xml格式
def getReplyXml(msg,replyContent):
    TextReply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
    TextReply = TextReply % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',replyContent)
    return TextReply
