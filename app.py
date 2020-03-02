from config import app, db
import json
from flask import request, jsonify
from table import User,Lecture
from spider import sp
# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.acs_exception.exceptions import ClientException
# from aliyunsdkcore.acs_exception.exceptions import ServerException
# from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
# from aliyunsdkecs.request.v20140526 import StopInstanceRequest
# # 创建AcsClient实例
# client = AcsClient(
#    "LTAIxJp2trqekdOL",
#    "yFb6EaJ635MeS7q4kEp2US4lFUU1i3",
#    "cn-hangzhou"
# )
# # 创建request，并设置参数
# request = DescribeInstancesRequest.DescribeInstancesRequest()
# request.set_PageSize(10)
# # 发起API请求并显示返回值
# response = client.do_action_with_exception(request)
SubjectDic ={1: "计算机", 2: "生命科学", 4: "理学院"}
subjson = ["computer", "biology", "Sciences"]
@app.route('/enter', methods=['POST'])
def enter():
    json_re = json.loads(request.get_data())
    wxId = json_re['wxId']
    user = User.query.filter_by(wxId=wxId).first()
    if user == None:
        return jsonify({
            "status": "200",
            "description": "初始用户"
        })
    else:
        return jsonify({
            "status": "200",
            "description": "已选择标签用户"
        })


@app.route('/option', methods=['POST'])
def option():
    try:
        json_re = json.loads(request.get_data())
        wxId = json_re['wxId']
        # 保留兴趣转换Int
        Interests = json_re['Interests']
        # MarkNum = json_re['MarkNum']
        user = User(wxId, Interests, 0)
        user.save()
        return jsonify({
            "status": "200",
            "description": "增加标签成功"
        })
    except Exception as e:
        return jsonify({
            "status": "404",
            "description": "未知错误"
        })


@app.route('/')
def hello():
    return "hello,world"


@app.route('/person', methods=['POST'])
def person():
    json_re = json.loads(request.get_data())
    wxId =json_re['wxId']
    user = User.query.filter_by(wxId=wxId).first()
    Interests = user.Interests
    data = []
    for i in SubjectDic:
        if Interests & i != 0:
            data.append(1)
        else:
            data.append(0)
    list_json = dict(zip(subjson,data))
    str_json =json.dumps(list_json,indent=2,ensure_ascii=False)
    return str_json


if __name__ == '__main__':
     db.drop_all()     #第一次使用时须更新
     db.create_all()
     sp()
     #updata()
     app.run(port=5000,debug=True)
     #sp()
