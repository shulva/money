from flask import Flask
from flask import request
import search_api_info
import sys
from weworkapi_python.callback_json import WXBizJsonMsgCrypt

app = Flask(__name__)

corp_id = "ww1a53d7b005ccd4cf"
token = 'qvZWNNf'
EncodingAESKey = 'MxN7OjDOB2XFqZDGTHDH646YCN9DWHJKj5lxHNm9cYq'
ip = '124.220.52.35'


@app.route('/url_test', methods=['GET'])
def back():
    get_data = request.args.to_dict()
    msg = get_data.get('msg_signature')
    time = get_data.get('timestamp')
    nouce = get_data.get('nouce')
    echostr = get_data.get('echostr')

    wxcpt = WXBizJsonMsgCrypt.WXBizJsonMsgCrypt(token, EncodingAESKey, corp_id)

    ret, sEchoStr = wxcpt.VerifyURL(msg, time, nouce, echostr)
    if ret != 0:
        print("ERR: VerifyURL ret: " + str(ret))
        sys.exit(1)
    else:
        print("done VerifyURL")
        return sEchoStr


@app.route('/url_test', methods=['POST'])
def back():
    get_data = request.args.to_dict()
    msg = get_data.get('msg_signature')
    time = get_data.get('timestamp')
    nouce = get_data.get('nouce')

    wxcpt = WXBizJsonMsgCrypt.WXBizJsonMsgCrypt(token, EncodingAESKey, corp_id)

    ret, sMsg = wxcpt.DecryptMsg(get_data, msg, time, nouce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        sys.exit(1)
    else:
        print(sMsg)

    # 解密成功，sMsg即为json格式的明文
    # TODO: 对明文的处理
    # ...
    # ...


@app.route('/')
def hello_world():  # put application's code here
    test = search_api_info.search_api_info_money()
    return test


if __name__ == '__main__':
    print(sys.version)
    app.run()
