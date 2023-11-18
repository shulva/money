from flask import Flask
from flask import request
import sys

sys.path.append("weworkapi_python/callback")
import WXBizMsgCrypt3
import xml.etree.cElementTree as xml_et
import requests
import search_api_info
import gpt_query

app = Flask(__name__)

corp_id = "ww1a53d7b005ccd4cf"
corp_secret = 'im4AekttVO8eKm2D31M3zdTF2qD-D8giHd5XyLdVFmU'
token = 'qvZWNNf'
EncodingAESKey = 'MxN7OjDOB2XFqZDGTHDH646YCN9DWHJKj5lxHNm9cYq'
ip = '124.220.52.35'
url_push = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access}'
url_get_access = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={ID}&corpsecret={SECRET}'
agent_id = 1000002
old_msg = 0 #查重

@app.route('/url_test', methods=['GET'])
def back_get():
    get_data = request.args.to_dict()
    msg = get_data.get('msg_signature')
    time = get_data.get('timestamp')
    nonce = get_data.get('nonce')
    echostr = get_data.get('echostr')

    wxcpt = WXBizMsgCrypt3.WXBizMsgCrypt(token, EncodingAESKey, corp_id)

    print(msg)
    print(time)
    print(nonce)
    print(echostr)

    ret, sEchoStr = wxcpt.VerifyURL(msg, time, nonce, echostr)
    if ret != 0:
        print("ERR: VerifyURL ret: " + str(ret))
        sys.exit(1)
    else:
        print("done VerifyURL")
        return sEchoStr


def app_push(text):
    url = url_get_access.format(ID=corp_id, SECRET=corp_secret)
    response = requests.get(url)
    access_token = response.json()['access_token']

    text_push = ''
    if text == '余额':
        text_push = search_api_info.search_api_info_money()
    else:
        text_push = gpt_query.query_text(text)

    HEADER = {"Content-Type":"application/json"}

    data = {
        "touser": "@all",
        "toparty": "@all",
        "totag": "@all",
        "msgtype": "text",
        "agentid": agent_id,
        "text": {
            "content": "{text}".format(text=text_push)
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 1,
        "duplicate_check_interval": 1800
    }

    response_push = requests.post(url_push.format(access=access_token), json=data,headers=HEADER)
    print(response_push.json())


@app.route('/url_test', methods=['POST'])
def back_post():
    get_data = request.args.to_dict()
    msg = get_data.get('msg_signature')
    time = get_data.get('timestamp')
    nonce = get_data.get('nonce')

    global old_msg
    if old_msg == msg:
        return ''

    old_msg = msg

    wxcpt = WXBizMsgCrypt3.WXBizMsgCrypt(token, EncodingAESKey, corp_id)

    ret, sMsg = wxcpt.DecryptMsg(request.data, msg, time, nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        sys.exit(1)

    xml_tree = xml_et.fromstring(sMsg)
    content = xml_tree.find("Content").text

    '''
        xml_text_tree = xml_et.fromstring(sRespData)
        for Content in xml_text_tree.iter("Content"):
            if content == "余额":
                Content.text = search_api_info.search_api_info_money()
            else:
                Content.text = gpt_query.query_text(content)
                break
    '''
    # sRespData = xml_et.tostring(xml_text_tree,encoding='unicode')

    sRespData = "<xml><ToUserName>ww1436e0e65a779aee</ToUserName>" \
                "<FromUserName>ChenJiaShun</FromUserName>" \
                "<CreateTime>1476422779</CreateTime>" \
                "<MsgType>text</MsgType>" \
                "<Content>稍等</Content>" \
                "<MsgId>1456453720</MsgId>" \
                "<AgentID>1000002</AgentID></xml>"
    ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, time, nonce)

    if ret != 0:
        print("ERR: EncryptMsg ret: " + str(ret))
        sys.exit(1)
    try:
        print('-----------------------------------------------')
        return sEncryptMsg
    finally:
        app_push(content)


@app.route('/')
def hello_world():  # put application's code here
    return "hello"


if __name__ == '__main__':
    print(sys.version)
    app.run()
