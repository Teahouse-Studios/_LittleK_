import requests
import json
import time
import os,sys

def versionLoop(mojira):
    try:
        os.remove('version_loop/version_cache.txt')
    except Exception:
        pass
    manifest_raw = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json')
    file = json.loads(version_manifest.text)
    server.tell(info, "最新快照:" + file['latest']['snapshot'] + "，每15秒侦测一次。")
    if mojira == True:
        mojira_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/10400')
        mojira_json = json.loads(mojira_raw.text)
        mojira_version = []
        for Version in mojira_json[:]:
            if Version['archived'] == False:
                mojira_version.append(Version['name'])
            else:
                pass
        pipe = '| '
        mojira_version_name = pipe.join(mojira_version)
        launched = [manifest['latest']['snapshot'], manifest['latest']['release'], mojira_version_name]
    else:
        launched = [manifest['latest']['snapshot'], manifest['latest']['release']]
    cache_write = open('version_loop/version_cache.txt',mode='a',encoding='utf-8')
    cache_write.write(launched)
    cache_write.close()
    running_times = 0
    error_times = 0
    while True:
        running_times += 1
        if error_times / running_times > 0.5
            server.tell(info, "版本侦测运行异常，请检查网络状况。")
        try:
            cache_read = open('version_loop/version_cache.txt',mode='r',encoding='utf-8')
            cache_readed = open('version_loop/version_cache.txt',mode='r',encoding='utf-8').read()
            manifest_raw = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json',timeout=20)
            manifest = json.loads(version_manifest.text)
            if manifest['latest']['snapshot'] == cache_readed[0]:
                print("没有侦测到新快照。")
                cache_read.close()
            else:
                server.tell(info, "新快照:"+file['latest']['snapshot']+"。")
                cache_read.close()
                os.remove('version_loop/version_cache.txt')
            if file['latest']['release'] == cache_readed[1]:
                print("没有侦测到新正式版。")
                cache_read.close()
            else:
                server.tell(info, "新正式版:" + file['latest']['release'] + "。")
                cache_read.close()
                os.remove('version_loop/version_cache.txt')
            if mojira == True
                mojira_raw = requests.get('https://bugs.mojang.com/rest/api/2/project/10400')
                mojira_json = json.loads(mojira_raw.text)
                mojira_version = []
                for Version in mojira_json[:]:
                    if Version['archived'] == False:
                        mojira_version.append(Version['name'])
                    else:
                        pass
                pipe = '| '
                mojira_version_name = pipe.join(mojira_version)
                if mojira_version_name == cache_readed[2]:
                    print("没有在Mojira上侦测到新版本。")
                    cache_read.close()
                else:
                    server.tell(info, "在Mojira上的新版本:" + file['latest']['snapshot'] + "。")
                    cache_read.close()
            cache_write.write(launched)
            time.sleep(15)
            except requests.exceptions.RequestException:
                print("发生错误：无法获取信息。")
                time.sleep(15)
                error_times += 1
                continue
            except requests.exceptions.Timeout:
                print("发生错误：超时。")
                error_times += 1
                continue
