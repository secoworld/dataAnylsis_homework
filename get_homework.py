import requests
import os
import json

# 设置请求头部信息
header = {
    'cookie': "UM_distinctid=1707a831af22d0-09b52444af64bf-6701b35-100200-1707a831af3111; _log_user_id=67ef3219e9957a4aee072714715f8afa; sharesessionid=f8bdf594f9c4e0eab3b634f32704743f; login_type=WX; csrftoken=hm6AJZrTZP70b8ROqT8K7RvO6onwnwMR; sessionid=fz2n3to0zbqn7szpkg5it93vh5gu7dza; k=46887; django_language=zh",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    'referer': "https://next.xuetangx.com/learn/tjnu08091002372/tjnu08091002372/1516372/exercise/1392904",
    'x-csrftoken': "QLdw3KKDQOLPWIVVvOsJyXKI2wq97GZr",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': 'zh-CN,zh;q=0.9'
}

url = 'https://next.xuetangx.com/api/v1/lms/exercise/get_exercise_list/'


def get_json(url):
    response = requests.get(url, headers=header)
    data = json.loads(response.content, encoding=response.encoding)
    return data


def save_json(path, data):
    with open(path, 'w', encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # 第一章作业id是235660，每一章的作业id都增1，一共是九章作业
    for i in range(9):
        url_id = url + str(235660 + i) + '/'
        data = get_json(url_id)
        print(data)
        path = "./html/homework/" + str(235660 + i) + ".json"
        if not os.path.exists("./html/homework/"):
            os.mkdir("./html/homework/")
        save_json(path, data)

