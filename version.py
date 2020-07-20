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
        manifest = json.loads(manifest_raw.text)
        mojira_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/10400/versions')
        mojira = json.loads(mojira_raw.text)
        mojira_version = []
        for Version in mojira[:]:
            if Version['archived'] == False:
                mojira_version.append(Version['name'])
            else:
                pass
        pipe = ' | '
        mojira_version_name = pipe.join(mojira_version)
        if manifest['latest']['release'] == mojira_version_name or manifest['latest']['snapshot'] == mojira_version_name:
            return "最新版：" + manifest['latest']['release'] + "，最新快照：" + manifest['latest']['snapshot']
        else:
            return "最新版：" + manifest['latest']['release'] + "，最新快照：" + manifest['latest']['snapshot'] + '\nMojira上的最新版本：'+ mojira_version_name
    except Exception as e:
        return "发生错误："+str(e)

# Bedrock
def bedrockVer():
    manifest_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/10200/versions')
    manifest = json.loads(manifest_raw.text)
    beta = []
    release = []
    for Version in manifest[:]:
        if Version['archived'] == False:
            try:
                findBeta = re.match(r'(.*Beta)$',Version['name'])
                beta.append(findBeta.group(1))
            except Exception:
                release.append(Version['name'])
        else:
            pass
    pipe = ' | '
    beta_name = pipe.join(beta)
    release_name = pipe.join(release)
    return 'Beta: ' + beta_name + '\nRelease: ' + release_name

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
    pipe = ' | '
    release_name = pipe.join(release)
    return '最新版：' + release_name

# Earth
def earthVer():
    manifest_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/11900/versions')
    manifest = json.loads(manifest_raw.text)
    release = []
    for Version in manifest[:]:
        if Version['archived'] == False:
            release.append(Version['name'])
        else:
            pass
    pipe = ' | '
    release_name = pipe.join(release)
    return '最新版：' + release_name

# Final output
def on_user_info(server, info):
    # All
    if info.content.startswith("!!&version") or info.content.startswith("!!&mcv"):
        server.reply(info, "Java版：\n" + javaVer() + "\n基岩版（Mojira）：\n" + bedrockVer() + "\nMinecraft Dungeons（Mojira）：\n" + dungeonsVer() + "\nMinecraft Earth（Mojira）：\n" + earthVer())
    # Java
    if info.content.startswith("!!&version java") or info.content.startswith("!!&version je") or info.content.startswith("!!&mcv java") or info.content.startswith("!!&mcv je") or info.content.startswith("!!&mcjv"):
        server.reply(info, javaVer())
    # Bedrock
    if info.content.startswith("!!&version bedrock") or info.content.startswith("!!&version be") or info.content.startswith("!!&mcv bedrock") or info.content.startswith("!!&mcv be") or info.content.startswith("!!&mcbv"):
        server.reply(info, bedrockVer())
    # Dungeons
    if info.content.startswith("!!&version dungeons") or info.content.startswith("!!&version mcd") or info.content.startswith("!!&mcv dungeons") or info.content.startswith("!!&mcv mcd") or info.content.startswith("!!&mcdv"):
        server.reply(info, dungeonsVer())
    # Earth
    if info.content.startswith("!!&version earth") or info.content.startswith("!!&version mce") or info.content.startswith("!!&mcv earth") or info.content.startswith("!!&mcv mce") or info.content.startswith("!!&mcev"):
        server.reply(info, earthVer())
