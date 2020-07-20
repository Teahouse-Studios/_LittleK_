# -*- coding: utf8 -*-
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
        mojira_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/10400')
        mojira = json.loads(mojira_raw.text)
        mojira_version = []
        for Version in mojira[:]:
            if Version['archived'] == False:
                mojira_version.append(Version['name'])
            else:
                pass
        pipe = '| '
        mojira_version_name = pipe.join(mojira_version)
        if manifest['latest']['release'] == mojira_version_name or manifest['latest']['snapshot'] == mojira_version_name:
            return "最新版：" + manifest['latest']['release'] + "，最新快照：" + manifest['latest']['snapshot'] + '\n'
        else:
            return "最新版：" + manifest['latest']['release'] + "，最新快照：" + manifest['latest']['snapshot'] + '\nMojira上的最新版本：'+ mojira_version_name + '\n'
    except Exception:
        return "发生错误：土豆熟了。\n"

# Bedrock
def bedrockVer():
    manifest_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/10200/versions')
    manifest = json.loads(manifest_raw.text)
    beta = []
    release = []
    for Version in manifest[:]:
        if Version['archived'] == False:
            try:
                findBeta = re.match(r'(.*)Beta$',Version['name'])
                beta.append(findBeta.group(1))
            except Exception:
                release.append(Version['name'])
        else:
            pass
    pipe = '| '
    beta_name = pipe.join(beta)
    release_name = pipe.join(release)
    return 'Beta: ' + beta_name + '\nRelease: ' + release_name + '\n'

# Dungeons
def dungeonsVer():
    manifest_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/10200/versions')
    manifest = json.loads(manifest_raw.text)
    release = []
    for Version in manifest[:]:
        if Version['archived'] == False:
            release.append(Version['name'])
        else:
            pass
    pipe = '| '
    release_name = pipe.join(release)
    return '最新版：' + release_name + '\n'

# Earth
def earthVer():
    manifest_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/11900')
    manifest = json.loads(manifest_raw.text)
    release = []
    for Version in manifest[:]:
        if Version['archived'] == False:
            release.append(Version['name'])
        else:
            pass
    pipe = '| '
    release_name = pipe.join(release)
    return '最新版：' + release_name + '\n'

# Final output
def on_user_info(server, info):
    # All
    if info.content.startswith("!!&version") or info.content.startswith("!!&mcv"):
        server.tell(info, "Java版：\n" + javaVer() + "基岩版（Mojira）：\n" + bedrockVer() + "Minecraft Dungeons（Mojira）：\n" + dungeonsVer() + "Minecraft Earth（Mojira）：\n" + earthVer())
    # Java
    if info.content.startswith("!!&version java") or info.content.startswith("!!&version je") or info.content.startswith("!!&mcv java") or info.content.startswith("!!&mcv je") or info.content.startswith("!!&mcjv"):
        server.tell(info, javaVer())
    # Bedrock
    if info.content.startswith("!!&version bedrock") or info.content.startswith("!!&version be") or info.content.startswith("!!&mcv bedrock") or info.content.startswith("!!&mcv be") or info.content.startswith("!!&mcbv"):
        server.tell(info, bedrockVer())
    # Dungeons
    if info.content.startswith("!!&version dungeons") or info.content.startswith("!!&version mcd") or info.content.startswith("!!&mcv dungeons") or info.content.startswith("!!&mcv mcd") or info.content.startswith("!!&mcdv"):
        server.tell(info, dungeonsVer())
    # Earth
    if info.content.startswith("!!&version earth") or info.content.startswith("!!&version mce") or info.content.startswith("!!&mcv earth") or info.content.startswith("!!&mcv mce") or info.content.startswith("!!&mcev"):
        server.tell(info, earthVer())
