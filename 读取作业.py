import json
import re
import requests
# import docx
# from docx import Document


# 首先尝试读取一个json文件，并且读取里边中的内容
def first_test():
    path = "./json/chapter01.json"
    with open(path, 'r') as f:
        data = json.load(f)

    problems = data['data']['problems']
    for problem in problems:
        print(problem['content']['Body'])
        for op in problem['content']['Options']:
            print(op)
    print(type(data))


def read_fromJson(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


# 获取问题
def get_problems(data):
    problems = data['data']['problems']
    new_problems = []
    for problem in problems:
        content = problem['content']
        pr = {}
        pr['type'] = content['Type']
        pr['typeText'] = content['TypeText']
        pr['content'] = content
        pr['user'] = problem['user']
        new_problems.append(pr)
    return problems, new_problems


# 处理各种问题
def deal_problems_types(pros):
    for index, problem in enumerate(pros):
        ptype = problem['type']
        if ptype == 'SingleChoice':
            deal_singleChoice(index, problem)
        elif ptype == 'MultipleChoice':
            deal_MultipleChoice(index, problem)
        elif ptype == 'FillBlank':
            deal_FillBlank(index, problem)
        elif ptype == 'Judgement':
            deal_Judgement(index, problem)
        else:
            print("该问题属于未知分类！")


# 处理单选题
def deal_singleChoice(index, problem):
    data = ""
    question = problem['content']['Body']
    options = problem['content']['Options']
    try:
        answer = problem['user']['answer'][0]
    except KeyError:
        print(problem['user'])
    type = "[单选题]"
    data += str(index+1)+"、" + type
    data += clear_str(question) + "\r\n"
    for option in options:
        data += option['key'] +" "+ clear_str(option['value'])
        data += "\r\n"
    data += "【答案】" + answer + "\r\n"

    print(data)
    return data


# 处理多选题
def deal_MultipleChoice(index, problem):
    data = ""
    """
    处理多选题
    :param index:
    :param problem:
    :return:
    """
    question = problem['content']['Body']
    options = problem['content']['Options']
    answers = problem['user']['answer']
    type = "[多选题]"
    data += str(index + 1) + "、" + type
    data += clear_str(question) + "\r\n"
    for option in options:
        data += option['key'] + " " + clear_str(option['value'])
        data += "\r\n"
    data += "【答案】"
    for answer in answers:
        data += answer
    data += "\r\n"
    print(data)
    return data



# 处理判断题
def deal_Judgement(index, problem):
    """
    处理判断题
    :param index:
    :param problem:
    :return:
    """
    data = ""
    question = problem['content']['Body']
    options = problem['content']['Options']
    answer = problem['user']['answer']
    type = "[判断题]"
    data += str(index + 1) + "、" + type
    data += clear_str(question) + "\r\n"
    data += "【答案】 "
    if answer[0] == "true":
        data += "对"
    else:
        data += "错"
    data += "\r\n"
    print(data)
    return data


# 处理填空题
def deal_FillBlank(index, problem):
    """
    处理填空题
    :param index:
    :param problem:
    :return:
    """
    data = ""
    question = problem['content']['Body']
    answers = problem['user']['answers']
    type = "[填空题]"
    data += str(index + 1) + "、" + type
    data += clear_str(question) + "\r\n"
    data += "【答案】"
    for answer in answers:
        for an in answers[answer]:
            data += an + "  "
    data += "\r\n"
    print(data)
    return data
    pass


def clear_str(str):
    """
    用来匹配选项和问题中的html标签
    :param str:
    :return:
    """
    rdata = ""
    p_tag = r'</?p.*?>'
    blank = r'&nbsp;'
    underline = r'<span.*?</span>'
    img = r'<img.*?src="(.*?)".*?/>'
    br = r'<br.*?/>'

    rdata = re.sub(p_tag, "", str)
    rdata = re.sub(blank, " ", rdata)
    rdata = re.sub(br, " ", rdata)
    rdata = re.sub(underline, "__", rdata)
    rdata = re.sub(img, "（这是一个图片）", rdata)

    return rdata

def get_img(url):
    respones = requests.get(url)
    fname = url.split("/")[-1]
    with open('./img/'+fname, 'wb') as f:
        f.write(respones.content)


def json_to_write(path):
    with open(path, 'r') as f:
        jsdata = json.load(f)
    fname = path.replace("chapter", "homework")
    with open(fname, 'w', encoding='utf8') as f:
        # f.write(json.dump(jsdata))
        json.dump(jsdata, f, indent=4, ensure_ascii=False)

    pass

if __name__ == '__main__':
    # for i in range(1, 8):
    #     print("开始读取第%d个文件"%i)
    #     path = "./json/chapter0"+str(i)+".json"
    #     data = read_fromJson(path)
    #     problems, new_problems = get_problems(data)
    #     deal_problems_types(new_problems)
    for i in range(1, 9):
        path = "./json/chapter0" + str(i) + ".json"
        json_to_write(path)