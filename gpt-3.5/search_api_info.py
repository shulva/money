import subprocess
import json

api_key = "sk-2fGS2KVZyjdYpALZ4c22F1146eD847A88071EeB277F247Bc"
args = ['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d',
        '{{"api_key":"{name}"}}'.format(name=api_key),
        'https://billing.openkey.cloud/api/token']


def search_api_info_money():
    info = subprocess.Popen(args, stdout=subprocess.PIPE)
    info.wait()
    output = json.loads(info.communicate()[0])

    #print("余额为:"+str(output['Remaining']))
    #print("总额为:"+str(output['Total']))
    #print("已用额度为:"+str(output['Used']))

    if output['Status'] == 0:
        print("error")

    print(output)

    return "余额为:{},总额为:{},已用额度为:{}".format(str(output['Remaining']),str(output['Total']),str(output['Used']))
