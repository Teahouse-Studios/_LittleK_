import pip._vendor.requests as requests
import json
import re
import urllib
def on_load(server,old_mouble):
    server.add_help_message('!!&wiki[-<语言>] <页面名>', '查询指定语言（默认为英文）的Minecraft Wiki上的页面。')
    server.add_help_message('!!&wiki ~<site> <页面名>', '查询指定Gamepedia Wiki上的页面。')
    server.add_help_message('!!&wiki <语言>:<页面名>', '查询指定语言的Minecraft Wiki上的页面。')
    
def m(lang,str1):
    if lang =='en':
        jsonUrl = 'https://minecraft.gamepedia.com/api.php?action=query&format=json&prop=info&inprop=url&redirects&titles='
        metaUrl = 'https://minecraft.gamepedia.com/'
    else:
        jsonUrl = 'https://minecraft-'+lang+'.gamepedia.com/api.php?action=query&format=json&prop=info&inprop=url&redirects&titles='
        metaUrl = 'https://minecraft-'+lang+'.gamepedia.com/'
    try:
        pageName = str1
        getUrl = jsonUrl+pageName
        metaText = requests.get(getUrl,timeout=15)
        try:
            file = json.loads(metaText.text)
            pages = file['query']['pages']
            pageID = sorted(pages.keys())[0]
            if  int(pageID) == -1:
                if 'missing' in pages['-1']:
                    try:
                        if lang =='en':
                            searchUrl = 'https://minecraft.gamepedia.com/api.php?action=query&generator=search&gsrsearch='+str1+'&gsrsort=just_match&gsrenablerewrites&prop=info&gsrlimit=1&format=json'
                        else:
                            searchUrl = 'https://minecraft-'+lang+'.gamepedia.com/api.php?action=query&generator=search&gsrsearch='+str1+'&gsrsort=just_match&gsrenablerewrites&prop=info&gsrlimit=1&format=json'
                        getSearch = requests.get(searchUrl)
                        parseSearch = json.loads(getSearch.text)
                        searchPage = parseSearch['query']['pages']
                        searchPageID = sorted(searchPage.keys())[0]
                        searchTitle = searchPage[searchPageID]['title']
                        return ('[{"text":"发生错误:","color":"red"},{"text":"找不到条目，您是否要找的是：","color":"reset"},{"text":"'+searchTitle+'","bold":true,"underlined":true,"color":"white","clickEvent":{"action":"run_command","value":"!!&wiki-'+lang+' '+searchTitle+'"}},{"text":"？","color":"reset"}]')
                    except Exception:
                        return('[{"text":"发生错误：","color":"red"},{"text":"找不到条目。","color":"reset"}]')
                else:
                    return ('[{"text":"您要的"},{"text":"'+pageName+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+metaUrl+urllib.parse.quote(pageName.encode('UTF-8'))+'"}}]')
#                    return ('您要的'+pagename+'：'+l+urllib.parse.quote(pagename.encode('UTF-8')))
            else:
                try:
                    pageUrl = pages[pageID]['fullurl']
                    if lang =='en':
                        result = re.match(r'https://minecraft\.gamepedia.com/(.*)', pageUrl, re.M | re.I)
                        descUrl = 'https://minecraft.gamepedia.com/api.php?action=query&prop=extracts&exsentences=1&&explaintext&exsectionformat=wiki&format=json&titles=' + result.group(1)
                    else:
                        result = re.match(r'https://minecraft-(.*)\.gamepedia.com/(.*)', pageUrl, re.M | re.I)
                        descUrl = 'https://minecraft-'+result.group(1)+'.gamepedia.com/api.php?action=query&prop=extracts&exsentences=1&&explaintext&exsectionformat=wiki&format=json&titles='+result.group(2)
                    getDesc = requests.get(descUrl,timeout=5)
                    parseDesc = json.loads(getDesc.text)
                    descText = parseDesc['query']['pages'][pageID]['extract']
                    try:
                        paraGraph = re.match(r'.*(\#.*)',str1)
                        page = pages[pageID]['fullurl'] + urllib.parse.quote(paraGraph.group(1).encode('UTF-8'))
                    except Exception:
                        page = pages[pageID]['fullurl']
                    resultName = re.match(r'https://.*?/(.*)',Page)
                    unquoteName = re.sub('_',' ',unquoteName)
                    if unquoteName == str1:
                        return ('[{"text":"您要的"},{"text":"'+pageName+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+page+'"}},{"text":"："},{"text":"'+descText+'"}]')
                    else:
                        return ('[{"text":"您要的"},{"text":"'+pageName+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+page+'"}},{"text":"('+str1+'->'+unquoteName+')："},{"text":"'+descText+'"}]')
#                    return('您要的'+pagename+"："+xx)
                except Exception as e:
                    try:
                        paraGraph = re.match(r'.*(\#.*)',str1)
                        page = pages[pageID]['fullurl'] + urllib.parse.quote(paraGraph.group(1).encode('UTF-8'))
                    except Exception:
                        page = pages[pageID]['fullurl']
                    resultName = re.match(r'https://.*?/(.*)',page)
                    unquoteName = urllib.parse.unquote(resultName.group(1),encoding='UTF-8')
                    unquoteName = re.sub('_',' ',unquoteName)
                    if unquoteName == str1:
                        return ('[{"text":"您要的"},{"text":"'+pageName+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+page+'"}}]')
                    else:
                        return ('[{"text":"您要的"},{"text":"'+pageName+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+Page+'"}},{"text":"('+str1+'->'+unquoteName+')"}]')
        except Exception as e:
            print(str(e))
            return('[{"text":"发生错误：","color":"red"},{"text":"内容非法。","color":"reset"}]')
    except Exception as e:
        return('[{"text":"发生错误：","color":"red"},{"text":"'+str(e)+'","color":"reset"}]')

def Wiki(path1,pagename):
    JSONurl = path1 +'/api.php?action=query&format=json&prop=info&inprop=url&redirects&titles=' + pagename
    metatext = requests.get(JSONurl, timeout=15)
    file = json.loads(metatext.text)
    try:
        pages = file['query']['pages']
        pageID = sorted(pages.keys())[0]
        if int(pageID) == -1:
            if 'missing' in pages['-1']:
                try:                
                    Searchurl = path1+'/api.php?action=query&generator=search&gsrsearch=' + pagename + '&gsrsort=just_match&gsrenablerewrites&prop=info&gsrlimit=1&format=json'
                    GETSearch = requests.get(Searchurl,timeout=15)
                    ParseSearch = json.loads(GETSearch.text)
                    SearchPages = ParseSearch['query']['pages']
                    SearchPageID = sorted(SearchPages.keys())[0]
                    SearchTitle = SearchPages[SearchPageID]['title']
                    return ('[{"text":"发生错误:","color":"red"},{"text":"找不到条目，您是否要找的是：","color":"reset"},{"text":"'+SearchTitle+'","bold":true,"underlined":true,"color":"white","clickEvent":{"action":"run_command","value":"!!&wiki ~'+path1+' '+SearchTitle+'"}},{"text":"？","color":"reset"}]')
                except Exception:
                    return ('[{"text":"发生错误：","color":"red"},{"text":"找不到条目。","color":"reset"}]')
            else:
#                return ('您要的'+pagename+'：'+path1+'/'+urllib.parse.quote(pagename.encode('UTF-8')))
                return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+path1+'/'+urllib.parse.quote(pagename.encode('UTF-8'))+'"}}]')
        else:
            try:
                Pageurl = pages[pageID]['fullurl']
                result = re.match(r'https://.*?/(.*)', Pageurl, re.M | re.I)
                descriptionurl = JSONurl + '/api.php?action=query&prop=extracts&exsentences=1&&explaintext&exsectionformat=wiki&format=json&titles=' + result.group(1)
                GETdescription = requests.get(descriptionurl, timeout=10)
                Parsedescription = json.loads(GETdescription.text)
                description = Parsedescription['query']['pages'][pageID]['extract']
                try:
                    paragraph = re.match(r'.*(\#.*)',pagename)
                    Page = pages[pageID]['fullurl'] + urllib.parse.quote(paragraph.group(1).encode('UTF-8'))
                except Exception:
                    Page = pages[pageID]['fullurl']
                Resultname = re.match(r'https://.*?/(.*)',Page)
                unquotename = urllib.parse.unquote(Resultname.group(1),encoding='UTF-8')
                unquotename = re.sub('_',' ',unquotename)
                if unquotename == pagename:
                    return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+Page+'"}},{"text":"："},{"text":"'+description+'"}]')
                else:
                    return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+Page+'"}},{"text":"('+pagename+'->'+unquotename+')："},{"text":"'+description+'"}]')
            except Exception:
                try:
                    paragraph = re.match(r'.*(\#.*)',pagename)
                    Page = pages[pageID]['fullurl'] + urllib.parse.quote(paragraph.group(1).encode('UTF-8'))
                except Exception:
                    Page = pages[pageID]['fullurl']
                Resultname = re.match(r'https://.*?/(.*)',Page)
                unquotename = urllib.parse.unquote(Resultname.group(1),encoding='UTF-8')
                unquotename = re.sub('_',' ',k)
                if unquotename == pagename:
                    return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+Page+'"}}]')
                else:
                    return ('[{"text":"您要的"},{"text":"'+pagename+'","bold":true,"underlined":true,"clickEvent":{"action":"open_url","value":"'+Page+'"}},{"text":"('+pagename+'->'+unquotename+')"}]')
    except Exception as e:
        print(str(e))
        try:
            Check = re.match(r'https://.*-(.*)\.gamepedia.com',path1)
            Check1 = re.sub(Check.group(1) + r':', "", pagename)
            Check2 = re.sub(r':.*', "", Check1)
            print(Check1)
            print(Check2)
            i = Check2
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
            metaurl = s.group(1)
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
