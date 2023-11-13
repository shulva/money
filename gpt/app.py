from flask import Flask
import search_api_info

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    test = search_api_info.search_api_info_money()
    return test


if __name__ == '__main__':
    app.run(host='124.220.52.35')
