import json
import math

from flask import request, jsonify
from sqlalchemy import or_

from config import app, db
from spider import sp, update
from table import User, userToLec, Lecture, userToLecLike
import datetime

SubjectDic = {1: "计算机", 2: "管理学院", 4: "经济学院", 8: "土木工程", 16: "生命科学学院"}
subjson = ["computer", "business", "finance", "building", "biology"]
tot = 0
date = str(1999) + '-' + str(4) + '-' + str(25)
now = datetime.date(1999,4,25)


@app.route('/enter', methods=['POST'])
def enter():
    json_re = json.loads(request.get_data())
    wxId = json_re['wxId']
    print(wxId, type(wxId))
    user = User.query.filter_by(wxId=wxId).first()
    print(user)
    if user is None:
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
        print(wxId, type(wxId))
        tot = 1
        Interests = 0
        for i in subjson:
            tmp = json_re[i]
            print(i, tmp, type(tmp))
            Interests += tmp * tot
            tot *= 2
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


@app.route('/bookmark', methods=['POST'])
def bookmark():
    try:
        json_re = json.loads(request.get_data())
        wxId = json_re['wxId']
        user = User.query.filter_by(wxId=wxId).first()
        relationship = userToLec.query.filter_by(userId=user.id).all()
        response = {'data': [], 'description': 'get lecturelist success'}
        for relation in relationship:
            lecture = Lecture.query.filter_by(id=relation.LecId).first()
            response['data'].append({
                "id": lecture.id,
                "Subject": lecture.Subject,
                "Title": lecture.Title,
                "Lecturer": lecture.Lecturer,
                "Year": lecture.Year,
                "Month": lecture.Month,
                "Day": lecture.Day,
                "Location": lecture.Location,
                "Content": lecture.Content
            })
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "status": "404",
            "description": "未知错误"
        })


@app.route('/home', methods=['POST'])
def home():
    try:
        json_re = json.loads(request.get_data())
        wxId = json_re['wxId']
        user = User.query.filter_by(wxId=wxId).first()
        Interests = user.Interests
        data = []
        for i in SubjectDic:
            if Interests & i != 0:
                data.append(1)
            else:
                data.append(0)
        rule = or_(*[Lecture.Subject.like(int(math.pow(2, i) * data[i])) for i in range(3)])
        lectures = Lecture.query.filter(rule).order_by(Lecture.Year, Lecture.Month, Lecture.Day).all()
        response = {'data': [], 'description': 'get lecturelist success'}
        for lecture in lectures:
            response['data'].append({
                "id": lecture.id,
                "Subject": lecture.Subject,
                "Title": lecture.Title,
                "Lecturer": lecture.Lecturer,
                "Year": lecture.Year,
                "Month": lecture.Month,
                "Day": lecture.Day
            })
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "status": "404",
            "description": "未知错误"
        })


@app.route('/details', methods=['POST'])
def details():
    try:
        json_re = json.loads(request.get_data())
        id = json_re['id']
        wxId = json_re['wxId']
        IsShow = json_re['IsShow']
        lecture = Lecture.query.filter_by(id=id).first()
        user = User.query.filter_by(wxId=wxId).first()
        relationship = userToLec.query.filter_by(userId=user.id, LecId=id).first()
        relationshiplike = userToLecLike.query.filter_by(userId=user.id, LecId=id).first()
        if relationship is None:
            IsBookMark = 0
        else:
            IsBookMark = 1
        if relationshiplike is None:
            IsLike = 0
        else:
            IsLike = 1
        if IsShow == 1:
            response = {'data': [], 'description': 'get lecturelist success'}
            response['data'].append({
                "id": lecture.id,
                "Subject": lecture.Subject,
                "Title": lecture.Title,
                "Lecturer": lecture.Lecturer,
                "Year": lecture.Year,
                "Month": lecture.Month,
                "Day": lecture.Day,
                "Location": lecture.Location,
                "Content": lecture.Content,
                "IsBookMark": IsBookMark,
                "LikeNum": lecture.like,
                "IsLike": IsLike
            })
            return jsonify(response)
        elif IsShow == 0:
            IsBookMark = json_re['IsBookMark']
            if IsBookMark == 1:
                relationship = userToLec(user.id, lecture.id)
                relationship.save()
                return jsonify({
                    "status": "200",
                    "description": "收藏成功"
                })
            else:
                relationship = userToLec.query.filter_by(userId=user.id, LecId=lecture.id).first()
                relationship.remove()
                return jsonify({
                    "status": "200",
                    "description": "取消收藏成功"
                })
        elif IsShow == 2:
            IsLike = json_re['IsLike']
            if IsLike == 1:
                relationshiplike = userToLecLike(user.id, lecture.id)
                relationd = userToLecLike.query.filter_by(userId=user.id, LecId=lecture.id).first()
                if relationd is None:
                    lecture.like += 1
                    relationshiplike.save()
                    lecture.save()
                    return jsonify({
                        "status": "200",
                        "description": "点赞成功"
                    })
                else:
                    return jsonify({
                        "status": "410",
                        "description": "已点赞，请勿重复点赞"
                    })
            else:
                relationshiplike = userToLecLike.query.filter_by(userId=user.id, LecId=lecture.id).first()
                relationshiplike.remove()
                lecture.like -= 1
                lecture.save()
                return jsonify({
                    "status": "200",
                    "description": "取消点赞成功"
                })

    except Exception as e:
        return jsonify({
            "status": "404",
            "description": "未知错误"
        })


@app.route('/us')
def us():
    n_date = datetime.datetime.now().date()
    global tot
    global now
    print(tot)
    if n_date.__gt__(now):
        tot = 0
        now = n_date
    print(tot)
    if tot < 1:
        tot += 1
        update()
        sp()
        return jsonify({
            "status": 200,
            "description": "spider成功"
        })
    else:
        return jsonify({
            "status":200,
            "description": "今日已spider"
        })


@app.route('/')
def hello():
    return "hello,world"


@app.route('/label', methods=['POST'])
def label():
    try:
        json_re = json.loads(request.get_data())
        wxId = json_re['wxId']
        user = User.query.filter_by(wxId=wxId).first()
        IsShow = json_re['IsShow']
        # print(user.Interests)
        if IsShow == 1:
            Interests = user.Interests
            data = []
            for i in SubjectDic:
                if Interests & i != 0:
                    data.append(1)
                else:
                    data.append(0)
            list_json = dict(zip(subjson, data))
            str_json = json.dumps(list_json, indent=2, ensure_ascii=False)
            return str_json
        else:
            tot = 1
            Interests = 0
            for i in subjson:
                tmp = json_re[i]
                Interests += tmp * tot
                tot *= 2
            user.Interests = Interests
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



if __name__ == '__main__':
    # db.drop_all()     #第一次使用时须更新
    # db.create_all()
    # update()
    # sp()
    app.run(port=5000, host='0.0.0.0')
