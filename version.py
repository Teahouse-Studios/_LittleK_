import requests
import json
import re

def on_load(server,old_mouble):
    server.add_help_message('!!&version [java|je|bedrock|be|dungeons|mcd|earth|mce]','查询Mojira上的bug。')

# Java
def javaVer():
    try:
        manifest_raw = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json')
        manifest = json.loads(version_manifest.text)
        return("最新版：" + manifest['latest']['release'] + "，最新快照：" + manifest['latest']['snapshot'] + '\n')
    except Exception:
        return("发生错误：土豆熟了。\n")

# Bedrock
def bedrockVer():
    q = requests.get('https://bugs.mojang.com/rest/api/2/project/10200/versions')
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

# Dungeons
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

# Final output
def on_user_info(server, info):
    # All
    if info.content.startswith("!!&version") or info.content.startswith("!!&mcv"):
        server.tell(info, "Java版：\n" + javaVer() + "基岩版：\n" + bedrockVer() + "Minecraft Dungeons：\n")
    # Java
    if info.content.startswith("!!&version java") or info.content.startswith("!!&version je") or info.content.startswith("!!&mcv java") or info.content.startswith("!!&mcv je") or info.content.startswith("!!&mcjv")
        server.tell(info, javaVer())
    # Bedrock
    if info.content.startswith("!!&version bedrock") or info.content.startswith("!!&version be") or info.content.startswith("!!&mcv bedrock") or info.content.startswith("!!&mcv be") or info.content.startswith("!!&mcbv")
        server.tell(info, bedrockVer())
    # Dungeons
    if info.content.startswith("!!&version dungeons") or info.content.startswith("!!&version mcd") or info.content.startswith("!!&mcv dungeons") or info.content.startswith("!!&mcv mcd") or info.content.startswith("!!&mcdv")
        server.tell(info, dungeonsVer())
