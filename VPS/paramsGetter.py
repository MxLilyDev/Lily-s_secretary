import json
import os


s = os.path.realpath(__file__)
currentFolder = s[:s.rindex('/') + 1] if '/' in s else './'

def getParams():
    params = {}
    try:
        with open(currentFolder + 'params.json', 'r', encoding='utf-8') as f:
            params = json.load(f)
    except IOError as error:
        print(error)
    except Exception as error:
        print(error)
    return params


async def getGuildId():
    params = getParams()
    try:
        return params['discordGuildId']
    except KeyError as error:
        print(error)
    return 0
