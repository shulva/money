import requests

api_key = "sk-2fGS2KVZyjdYpALZ4c22F1146eD847A88071EeB277F247Bc"

def query_text(text):
    # url = "https://api.openai.com/v1/chat/completions"
    url = "https://openkey.cloud/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',

        # 填写OpenKEY生成的令牌/KEY，注意前面的 Bearer 要保留，并且和 KEY 中间有一个空格。
        'Authorization': 'Bearer {api}'.format(api=api_key)
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}]
    }

    response = requests.post(url, headers=headers, json=data)

    res_json = response.json()

    print(res_json)
    return res_json['choices'][0]['message']['content']
