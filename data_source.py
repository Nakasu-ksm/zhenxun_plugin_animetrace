import json
from utils.http_utils import AsyncHttpx
from hashlib import md5
import time
import random


async def getData(imageUrl, model="anime", mode=0):
    """
    :param imageUrl: input Image
    :param model: select Model [game, anime]
    :param mode: 0-1, 0 for single, 1 for multiple
    :return: result
    """
    save_name = md5(imageUrl.encode("utf-8")).hexdigest() + ".png"
    await AsyncHttpx.download_file(imageUrl, save_name)
    files = {
        'image': open(save_name, 'rb')
    }
    content = await AsyncHttpx.post(f"https://aiapiv2.animedb.cn/ai/api/detect?model={model}&force_one={mode}",
                                    data=None, files=files)
    content = json.loads(content.text)
    return content


def buildMessage(result, mode, Model):
    modelName = ""
    if Model == 'game':
        modelName = "游戏"
    else:
        modelName = "动漫"

    """
    :param Model: 
    :param result: result from AnimeTrace
    :param mode: mode
    :return: message_build
    """
    if mode == 0:
        char = ""
        for i in result['data']:
            message = "人物:" + i['name'] + f"--来自{modelName}《" + i['cartoonname'] + "》" + "\n"
            char += message
        return char

    else:
        char = ""
        count = 0
        message_list = []

        message_list.append(link(f"感谢使用AnimeTrace动漫查询引擎，这是您的{modelName}图片预测结果"))
        for i in result['data']:
            count += 1
            message = f"第{count}个人物:" + i['char'][0]['name'] + f"--来自{modelName}《" + i['char'][0][
                'cartoonname'] + "》" + "\n"
            if (len(i['char']) != 1):
                for idx, d in enumerate(i['char']):
                    if (idx == 0):
                        continue
                    message += "--其他可能性"
                    message += "-" + d['name'] + f"--来自{modelName}《" + d['cartoonname'] + "》" + "\n"
            char += message
            message_list.append(link(char, i['char'][0]['name']))
            char = ""
        message_list.append(link("共预测到" + str(len(result['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!"))
        return message_list


def link(string, name=None):
    if name == None:
        namearray = ['式宫 舞菜', '香风 智乃', "保登 心爱", "越谷 小鞠", "稻森 光香", "雪村 葵", "龙宫 礼奈", "北条 沙都子", "间宫 乃乃香"]
        name = random.choice(namearray)
    return {
        "type": "node",
        "data": {
            "name": f"{name}",
            "uin": f"1398087940",  # 这里可以自定义
            "content": string,
        },
    }
