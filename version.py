import requests
import json
import re

// Java
def javaVer():
    url = 'http://launchermeta.mojang.com/mc/game/version_manifest.json'
    try:
        version_manifest = requests.get(url)
        file = json.loads(version_manifest.text)
        return("最新版：" + file['latest']['release'] + "，最新快照：" + file['latest']['snapshot'] + '\n')
    except Exception:
        return("发生错误：土豆熟了。\n")

// Bedrock
def bedrockVer():
    url = 'https://bugs.mojang.com/rest/api/2/project/10200/versions'
    q = requests.get(url)
    w = json.loads(q.text)
    f = []
    z = []
    for x in w[:]:
        if x['archived'] == False:
            try:
                e = re.match(r'(.*)Beta$',x['name'])
                f.append(e.group(1))
            except Exception:
                z.append(x['name'])
        else:
            pass
    h = '| '
    d = h.join(f)
    u = h.join(z)
    return('Beta: '+str(d)+'\nRelease: '+u+'\n')

// Dungeons
def dungeonsVer():
    url = 'https://bugs.mojang.com/rest/api/2/project/11901/versions'
    q = requests.get(url)
    w = json.loads(q.text)
    f = []
    for x in w[:]:
        if x['archived'] == False:
            s = x['name']
        else:
            pass
    return('最新版：'+s+'\n')

def on_user_info(server, info):
    if info.content.startswith("!!&version") or info.content.startswith("!!&mcv"):
        server.tell(info, "Java版：\n" + javaVer() + "基岩版：\n" + bedrockVer() + "Minecraft Dungeons：\n")

    if info.content.startswith("!!&version java") or info.content.startswith("!!&version je") or info.content.startswith("!!&mcv java") or info.content.startswith("!!&mcv je") or info.content.startswith("!!&mcjv")
        server.tell(info, javaVer())

    if info.content.startswith("!!&version bedrock") or info.content.startswith("!!&version be") or info.content.startswith("!!&mcv bedrock") or info.content.startswith("!!&mcv be") or info.content.startswith("!!&mcbv")
        server.tell(info, bedrockVer())

    if info.content.startswith("!!&version dungeons") or info.content.startswith("!!&version mcd") or info.content.startswith("!!&mcv dungeons") or info.content.startswith("!!&mcv mcd") or info.content.startswith("!!&mcdv")
        server.tell(info, dungeonsVer())
