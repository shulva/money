from flask import Flask
from flask import request
import sys

sys.path.append("weworkapi_python/callback")
import WXBizMsgCrypt3
import xml.etree.cElementTree as xml_et

import search_api_info
import gpt_query
app = Flask(__name__)

corp_id = "ww1a53d7b005ccd4cf"
token = 'qvZWNNf'
EncodingAESKey = 'MxN7OjDOB2XFqZDGTHDH646YCN9DWHJKj5lxHNm9cYq'
ip = '124.220.52.35'


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


@app.route('/url_test', methods=['POST'])
def back_post():
    get_data = request.args.to_dict()
    msg = get_data.get('msg_signature')
    time = get_data.get('timestamp')
    nonce = get_data.get('nonce')

    wxcpt = WXBizMsgCrypt3.WXBizMsgCrypt(token, EncodingAESKey, corp_id)

    ret, sMsg = wxcpt.DecryptMsg(request.data, msg, time, nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        sys.exit(1)

    xml_tree = xml_et.fromstring(sMsg)
    content = xml_tree.find("Content").text

    sRespData = "<xml><ToUserName>ww1436e0e65a779aee</ToUserName>" \
                "<FromUserName>ChenJiaShun</FromUserName>" \
                "<CreateTime>1476422779</CreateTime>" \
                "<MsgType>text</MsgType>" \
                "<Content>你好</Content>" \
                "<MsgId>1456453720</MsgId>" \
                "<AgentID>1000002</AgentID></xml>"

    xml_text_tree = xml_et.fromstring(sRespData)
    for Content in xml_text_tree.iter("Content"):
        if content == "余额":
            Content.text = search_api_info.search_api_info_money()
        else:
            Content.text = gpt_query.query_text(content)
            break

    print("----------------------------------------------")
    sRespData = xml_et.tostring(xml_text_tree,encoding='unicode')

    ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, time, nonce)

    if ret != 0:
        print("ERR: EncryptMsg ret: " + str(ret))
        sys.exit(1)

    return sEncryptMsg


@app.route('/')
def hello_world():  # put application's code here
    return "hello"


if __name__ == '__main__':
    print(sys.version)
    app.run()
