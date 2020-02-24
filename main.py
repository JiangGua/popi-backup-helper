import os
import time
import json
import re
import requests

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

class Question():
    def __init__(self, question_id):
        self.question_id = question_id

    def get_answer(self):
        r = requests.get('https://apiv3.popiask.cn/unuser/question/{}'.format(self.question_id))
        r = json.loads(r.text)
        self.data = r
        obj = {
            "question": r['content']['title'],
            "answer": r['content']['answer']['txt_content'],
            "created": r['content']['created_at'] 
        }
        return obj

    def get_user_name(self):
        if not hasattr(self, 'data'):
            self.get_answer()
        return self.data['content']['userInfo']['nickName']
    
class User():
    def __init__(self, sharecode):
        self.sharecode = sharecode

    def get_questions_from_user(self):
        r = requests.get('https://apiv3.popiask.cn/unuser/getQuestionFromUser/{}?pageSize=100'.format(self.sharecode))
        r = json.loads(r.text)
        questions = []
        for item in r['content']['data']:
            q = Question(item['id'])
            questions.append(q)
        self.questions = questions

    def format(self):
        self.get_questions_from_user()
        l = [item.get_answer() for item in self.questions]
        return l

    def get_user_name(self):
        return self.questions[0].get_user_name()

if __name__ == "__main__":
    sharecode = input('请输入Popi提问箱分享码：')
    user = User(sharecode)
    result = user.format()
    file_name = validateTitle(user.get_user_name())
    with open('{}.json'.format(file_name), 'w', encoding='utf-8') as f:
        f.write(json.dumps(result))
    print("Success")