

import pip._vendor.requests as requests
import json
import traceback
import xml
import copy
import re
import urllib

def on_load(server,old_mouble):
    server.add_help_message('!!&wiki[-<语言>] <页面名>', '查询指定语言（默认为英文）的Minecraft Wiki上的页面。')
    server.add_help_message('!!&wiki ~<site> <页面名>', '查询指定Gamepedia Wiki上的页面。')
    server.add_help_message('!!&wiki <语言>:<页面名>', '查询指定语言的Minecraft Wiki上的页面。')
    
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
                        return ('[{"text":"发生错误:","color":"red"},{"text":"找不到条目，您是否要找的是：","color":"reset"},{"text":"'+m+'","bold":true,"underlined":true,"color":"white","clickEvent":{"action":"run_command","value":"!!&wiki-'+lang+' '+m+'"}},{"text":"？","color":"reset"}]')
                    except Exception:
                        return('[{"text":"发生错误：","color":"red"},{"text":"找不到条目。","color":"reset"}]')
                else:
#                    return ('您要的'+pagename+'：'+l+urllib.parse.quote(pagename.encode('UTF-8')))
                    return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+l+urllib.parse.quote(pagename.encode('UTF-8'))+'"}}]')
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
#                    if k == str1:
#                        xx = re.sub('\n$', '', z + '\n' + r)
#                    else:
#                        xx = re.sub('\n$', '', '\n('+str1 +' -> '+k+')\n'+z + '\n' + r)
#                    return('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}}'+pagename+"："+xx)
                    if k == str1:
                        return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}},{"text":"："},{"text":"'+r+'"}]')
                    else:
                        return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}},{"text":"('+str1+'->'+k+')："},{"text":"'+r+'"}]')
                except Exception:
                    try:
                        s = re.match(r'.*(\#.*)',str1)
                        z = x[y]['fullurl'] + urllib.parse.quote(s.group(1).encode('UTF-8'))
                    except Exception:
                        z = x[y]['fullurl']
                    n = re.match(r'https://.*?/(.*)',z)
                    k = urllib.parse.unquote(n.group(1),encoding='UTF-8')
                    k = re.sub('_',' ',k)
#                    if k == str1:
#                        zz = z
#                    else:
#                        zz = ('\n('+str1 +' -> '+k+')\n'+z)
#                    return('您要的'+pagename+"："+zz)
                    if k == str1:
                        return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}}]')
                    else:
                        return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}},{"text":"('+str1+'->'+k+')"}]')
        except Exception as e:
            print(str(e))
            return('[{"text":"发生错误：","color":"red"},{"text":"内容非法。","color":"reset"}]')
    except Exception as e:
        return('[{"text":"发生错误：","color":"red"},{"text":"'+str(e)+'","color":"reset"}]')

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
                    return ('[{"text":"发生错误:","color":"red"},{"text":"找不到条目，您是否要找的是：","color":"reset"},{"text":"'+m+'","bold":true,"underlined":true,"color":"white","clickEvent":{"action":"run_command","value":"!!&wiki ~'+path1+' '+m+'"}},{"text":"？","color":"reset"}]')
                except Exception:
                    return ('[{"text":"发生错误：","color":"red"},{"text":"找不到条目。","color":"reset"}]')
            else:
#                return ('您要的'+pagename+'：'+path1+'/'+urllib.parse.quote(pagename.encode('UTF-8')))
                return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+path1+'/'+urllib.parse.quote(pagename.encode('UTF-8'))+'"}}]')
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
#                if k == pagename:
#                    xx = re.sub('\n$', '', z + '\n' + v)
#                else:
#                    xx = re.sub('\n$', '', '\n('+pagename +' -> '+k+')\n'+z + '\n' + v)
#                return('您要的'+pagename+"："+xx)
                if k == pagename:
                    return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}},{"text":"："},{"text":"'+v+'"}]')
                else:
                    return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}},{"text":"('+pagename+'->'+k+')："},{"text":"'+v+'"}]')
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
                if k == pagename:
                        return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}}]')
                    else:
                        return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+z+'"}},{"text":"('+pagename+'->'+k+')"}]')
    except Exception as e:
        print(str(e))
        try:
            w = re.match(r'https://.*-(.*).gamepedia.com',path1)
            u = re.sub(w.group(1) + r':', "", pagename)
            i = re.sub(r':.*', "", u)
            print(u)
            print(i)
            if (i == "ftb" or i == "aether" or i == "cs" or i == "de" or i == "el" or i == "en" or i == "es" or i == "fr" or i == "hu" or i == "it" or i == "ja" or i == "ko" or i == "nl" or i == "pl" or i == "pt" or i == "ru" or i == "th" or i == "tr" or i == "uk" or i == "zh"):
                return('[{"text":"发生错误：","color":"red"},{"text":"检测到多重Interwiki，暂不支持多重Interwiki。","color":"reset"}]')
            else:
                return('[{"text":"发生错误：","color":"red"},{"text":"内容非法。","color":"reset"}]')
        except Exception as e:
            return('[{"text":"发生错误：","color":"red"},{"text":"'+str(e)+'","color":"reset"}]')


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
            return('[{"text":"发生错误：","color":"red"},{"text":"未知语言。","color":"reset"}]')
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
                        return ('[{"text":"发生错误：","color":"red"},{"text":"'+str(e)+'","color":"reset"}]')
                elif w == 'Wikipedia' or w == 'wikipedia':
                        return('[{"text":"发生错误：","color":"red"},{"text":"暂不支持Wikipedia查询。","color":"reset"}]')
                elif w == 'Moegirl' or w == 'moegirl':
                    try:
                        metaurl = 'https://zh.moegirl.org'
                        return (Wiki(metaurl, x))
                    except Exception as e:
                        return ('[{"text":"发生错误：","color":"red"},{"text":"'+str(e)+'","color":"reset"}]')
                else:
                    try:
                        metaurl = 'https://minecraft.gamepedia.com'
                        return (Wiki(metaurl, q.group(1)))
                    except  Exception as e:
                        return ('[{"text":"发生错误：","color":"red"},{"text":"'+str(e)+'","color":"reset"}]')
            except Exception:
                return(m('en',q.group(1)))

def tellraw(server,info,player):
    server.execute("tellraw "+player+" "+info)


def on_user_info(server, info):
    if info.content.startswith("!!&wiki"):
        a=wikilookup(info)
        print(a)
        tellraw(server,a,info.player)
