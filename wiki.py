

import pip._vendor.requests as requests
import json
import traceback
import xml
import copy
import re

def on_load(server,old_mouble):
    server.add_help_message('!!&wiki <页面名>', '查询中文Minecraft Wiki上的页面。')
    
def m(lang,str1):
    if lang =='en':
        metaurl = 'https://minecraft.gamepedia.com/api.php?action=query&format=json&prop=info&inprop=url&redirects&titles='
        l = 'https://minecraft.gamepedia.com/'
    else:
        metaurl = 'https://minecraft-'+lang+'.gamepedia.com/api.php?action=query&format=json&prop=info&inprop=url&redirects&titles='
        l = 'https://minecraft-'+lang+'.gamepedia.com/'
    try:
        pagename = str1
        url = metaurl+pagename
        metatext = requests.get(url,timeout=15)
        try:
            file = json.loads(metatext.text)
            x = file['query']['pages']
            y = sorted(x.keys())[0]
            if  int(y) == -1:
                if 'missing' in x['-1']:
                    try:
                        if lang =='en':
                            searchurl = 'https://minecraft.gamepedia.com/api.php?action=query&generator=search&gsrsearch='+str1+'&gsrsort=just_match&gsrenablerewrites&prop=info&gsrlimit=1&format=json'
                        else:
                            searchurl = 'https://minecraft-'+lang+'.gamepedia.com/api.php?action=query&generator=search&gsrsearch='+str1+'&gsrsort=just_match&gsrenablerewrites&prop=info&gsrlimit=1&format=json'
                        f = requests.get(searchurl)
                        g = json.loads(f.text)
                        j=g['query']['pages']
                        b = sorted(j.keys())[0]
                        m = j[b]['title']
                        return ('[{"text":"§4发生错误：§r找不到条目，您是否要找的是：' + m +'？"},\
                        {"text":"【是】","bold":true,"underlined":true,"clickEvent":\
                        {"action":"run_command","value":"!!&wiki ~'+l+' '+m+'"}}]')
                    except Exception:
                        return('找不到条目。')
                else:
#                    return ('您要的'+pagename+'：'+l+urllib.parse.quote(pagename.encode('UTF-8')))
                    return ('[{"text":"您要的' + pagename +'："},\
                        {"text":"'+l+urllib.parse.quote(pagename.encode('UTF-8'))+'",\
                        "bold":true,"underlined":true,"clickEvent":\
                        {"action":"open_url","value":"'+l+urllib.parse.quote(pagename.encode('UTF-8'))+'"}}]')
            else:
                try:
                    z = x[y]['fullurl']
                    if lang =='en':
                        h = re.match(r'https://minecraft.gamepedia.com/(.*)', z, re.M | re.I)
                        texturl = 'https://minecraft.gamepedia.com/api.php?action=query&prop=extracts&exsentences=1&&explaintext&exsectionformat=wiki&format=json&titles=' + h.group(1)
                    else:
                        h = re.match(r'https://minecraft-(.*).gamepedia.com/(.*)', z, re.M | re.I)
                        texturl = 'https://minecraft-'+h.group(1)+'.gamepedia.com/api.php?action=query&prop=extracts&exsentences=1&&explaintext&exsectionformat=wiki&format=json&titles='+h.group(2)
                    textt = requests.get(texturl,timeout=5)
                    e = json.loads(textt.text)
                    r = e['query']['pages'][y]['extract']
                    try:
                        s = re.match(r'.*(\#.*)',str1)
                        z = x[y]['fullurl'] + urllib.parse.quote(s.group(1).encode('UTF-8'))
                    except Exception:
                        z = x[y]['fullurl']
                    n = re.match(r'https://.*?/(.*)',z)
                    k = urllib.parse.unquote(n.group(1),encoding='UTF-8')
                    k = re.sub('_',' ',k)
                    if k == str1:
                        xx = re.sub('\n$', '', z + '\n' + r)
                    else:
                        xx = re.sub('\n$', '', '\n('+str1 +' -> '+k+')\n'+z + '\n' + r)
#                    return('您要的'+pagename+"："+xx)
                    return ('[{"text":"您要的' + pagename +'："},\
                        {"text":"'+xx+'",\
                        "bold":true,"underlined":true,"clickEvent":\
                        {"action":"open_url","value":"'+xx+'"}}]')
                except Exception:
                    try:
                        s = re.match(r'.*(\#.*)',str1)
                        z = x[y]['fullurl'] + urllib.parse.quote(s.group(1).encode('UTF-8'))
                    except Exception:
                        z = x[y]['fullurl']
                    n = re.match(r'https://.*?/(.*)',z)
                    k = urllib.parse.unquote(n.group(1),encoding='UTF-8')
                    k = re.sub('_',' ',k)
                    if k == str1:
                        zz = z
                    else:
                        zz = ('\n('+str1 +' -> '+k+')\n'+z)
#                    return('您要的'+pagename+"："+zz)
                    return ('[{"text":"您要的' + pagename +'："},\
                        {"text":"'+zz+'",\
                        "bold":true,"underlined":true,"clickEvent":\
                        {"action":"open_url","value":"'+zz+'"}}]')
        except Exception:
            return('§4发生错误：§r内容非法。')
    except Exception as e:
        return('§4发生错误：§r'+str(e))

def Wiki(path1,pagename):
    metaurl = path1 +'/api.php?action=query&format=json&prop=info&inprop=url&redirects&titles=' + pagename
    metatext = requests.get(metaurl, timeout=15)
    file = json.loads(metatext.text)
    try:
        x = file['query']['pages']
        y = sorted(x.keys())[0]
        if int(y) == -1:
            if 'missing' in x['-1']:
                try:                
                    searchurl = path1+'/api.php?action=query&generator=search&gsrsearch=' + pagename + '&gsrsort=just_match&gsrenablerewrites&prop=info&gsrlimit=1&format=json'
                    f = requests.get(searchurl,timeout=15)
                    g = json.loads(f.text)
                    j = g['query']['pages']
                    b = sorted(j.keys())[0]
                    m = j[b]['title']
                    return ('[{"text":"§4发生错误：§r找不到条目，您是否要找的是：' + m +'？"},\
                        {"text":"【是】","bold":true,"underlined":true,"clickEvent":\
                        {"action":"run_command","value":"!!&wiki ~'+path1+' '+m+'"}}]')
                except Exception:
                    return ('§4发生错误：§r找不到条目。')
            else:
#                return ('您要的'+pagename+'：'+path1+'/'+urllib.parse.quote(pagename.encode('UTF-8')))
                return ('[{"text":"您要的' + pagename +'："},\
                        {"text":"'+path1+'/'+urllib.parse.quote(pagename.encode('UTF-8'))+'",\
                        "bold":true,"underlined":true,"clickEvent":\
                        {"action":"open_url","value":"'+path1+'/'+urllib.parse.quote(pagename.encode('UTF-8'))+'"}}]')
        else:
            try:
                z = x[y]['fullurl']
                h = re.match(r'https://.*/(.*)', z, re.M | re.I)
                texturl = metaurl + '/api.php?action=query&prop=extracts&exsentences=1&&explaintext&exsectionformat=wiki&format=json&titles=' + h.group(1)
                gettext = requests.get(texturl, timeout=10)
                loadtext = json.loads(gettext.text)
                v = loadtext['query']['pages'][y]['extract']
                try:
                    s = re.match(r'.*(\#.*)',pagename)
                    z = x[y]['fullurl'] + urllib.parse.quote(s.group(1).encode('UTF-8'))
                except Exception:
                    z = x[y]['fullurl']
                n = re.match(r'https://.*?/(.*)',z)
                k = urllib.parse.unquote(n.group(1),encoding='UTF-8')
                k = re.sub('_',' ',k)
                if k == pagename:
                    xx = re.sub('\n$', '', z + '\n' + v)
                else:
                    xx = re.sub('\n$', '', '\n('+pagename +' -> '+k+')\n'+z + '\n' + v)
#                return('您要的'+pagename+"："+xx)
                return ('[{"text":"您要的' + pagename +'："},\
                        {"text":"'+xx+'",\
                        "bold":true,"underlined":true,"clickEvent":\
                        {"action":"open_url","value":"'+xx+'"}}]')
            except Exception:
                try:
                    s = re.match(r'.*(\#.*)',pagename)
                    z = x[y]['fullurl'] + urllib.parse.quote(s.group(1).encode('UTF-8'))
                except Exception:
                    z = x[y]['fullurl']
                n = re.match(r'https://.*?/(.*)',z)
                k = urllib.parse.unquote(n.group(1),encoding='UTF-8')
                k = re.sub('_',' ',k)
                if k == pagename:
                    zz = z
                else:
                    zz = '\n('+pagename+' -> '+k+')\n'+z
#                return('您要的' + pagename + "：" + zz)
                return ('[{"text":"您要的' + pagename +'："},\
                        {"text":"'+zz+'",\
                        "bold":true,"underlined":true,"clickEvent":\
                        {"action":"open_url","value":"'+zz+'"}}]')
    except Exception:
        try:
            w = re.match(r'https://.*-(.*).gamepedia.com',path1)
            u = re.sub(w.group(1) + r':', "", pagename)
            i = re.sub(r':.*', "", u)
            print(u)
            print(i)
            if (i == "ftb" or i == "aether" or i == "cs" or i == "de" or i == "el" or i == "en" or i == "es" or i == "fr" or i == "hu" or i == "it" or i == "ja" or i == "ko" or i == "nl" or i == "pl" or i == "pt" or i == "ru" or i == "th" or i == "tr" or i == "uk" or i == "zh"):
                return('§4发生错误：§r检测到多重Interwiki，暂不支持多重Interwiki。')
            else:
                return('§4发生错误：§r内容非法。')
        except Exception as e:
            return('§4发生错误：§r'+str(e))


def wikilookup(info):
    str1=info.content[3:]
    try:
        b = re.sub(r'^Wiki','wiki',str1)
    except:
        b = str1
    try:
        q = re.match(r'^wiki-(.*?) (.*)',b)
        w = q.group(1)
        print(w)
        if (w == "cs" or w == "de" or w == "el" or w == "en" or w == "es" or w == "fr" or w == "hu" or w == "it" or w == "ja" or w == "ko" or w == "nl" or w == "pl" or w == "pt" or w == "ru" or w == "th" or w == "tr" or w == "uk" or w == "zh"):
            return(m(q.group(1),q.group(2)))
        else:
            return('§4发生错误：§r未知语言。')
    except:
        q = re.match(r'^wiki (.*)',b)
        try:
            s = re.match(r'~(.*) (.*)',q.group(1))
            metaurl = 'https://' + s.group(1) + '.gamepedia.com'
            return (Wiki(metaurl,s.group(2)))
        except:
            try:
                d = re.sub(r':.*','',q.group(1))
                x = re.sub(r'^'+d+':','',q.group(1))
                w = d
                if (w == "cs" or w == "de" or w == "el" or w == "en" or w == "es" or w == "fr" or w == "hu" or w == "it" or w == "ja" or w == "ko" or w == "nl" or w == "pl" or w == "pt" or w == "ru" or w == "th" or w == "tr" or w == "uk" or w == "zh"):
                    try:
                        metaurl = 'https://minecraft-' + w + '.gamepedia.com'
                        return (Wiki(metaurl, x))
                    except  Exception as e:
                        return ('§4发生错误：§r' + str(e))
                elif w == 'Wikipedia' or w == 'wikipedia':
                        return('§4发生错误：§r暂不支持Wikipedia查询。')
                elif w == 'Moegirl' or w == 'moegirl':
                    try:
                        metaurl = 'https://zh.moegirl.org'
                        return (Wiki(metaurl, x))
                    except Exception as e:
                        return ('§4发生错误：§r' + str(e))
                else:
                    try:
                        metaurl = 'https://minecraft.gamepedia.com'
                        return (Wiki(metaurl, q.group(1)))
                    except  Exception as e:
                        return ('§4发生错误：§r' + str(e))
            except Exception:
                return(m('en',q.group(1)))


def on_user_info(server, info):
    if info.content.startswith("!!&wiki"):
        server.reply(info,wikilookup(server, info))
