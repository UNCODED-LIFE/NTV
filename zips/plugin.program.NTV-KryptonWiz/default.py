import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, binascii
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import zipfile
import ntpath


AddonID = "plugin.program.NTV-KryptonWiz"
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='https://www.facebook.com/groups/1417431028282425/'
ADDON=xbmcaddon.Addon(id='plugin.program.NTV-KryptonWiz')
dialog = xbmcgui.Dialog()    
VERSION = "1.6.0"
PATH = "NTV-KryptonWiz"
ICON = "http://notorious-tv.com/wizimg/ntvicon.png"
UICON = "http://notorious-tv.com/wizimg/Update-icon.png"
FANART = "http://i.imgsafe.org/01ccc6c.jpg"       
WizTitle = "NTV-KryptonWiz"
home         =  xbmc.translatePath('special://home/')
dp = xbmcgui.DialogProgress()
ES = '5b277265706f7369746f72792e4e5456272c27706c7567696e2e70726f6772616d2e4e54562d4b727970746f6e57697a272c277061636b61676573275d'
EXCLUDES = binascii.unhexlify(ES)
UES = '5b274d794e7476272c276d657461646174612e7468656d6f76696564622e6f7267272c276d657461646174612e747664622e636f6d272c277265706f7369746f72792e4e5456272c277061636b61676573272c27706c7567696e2e70726f6772616d2e4e54562d4b727970746f6e57697a272c27706c7567696e2e766964656f2e65786f647573272c27706c7567696e2e766964656f2e626f787365746b696e6773272c27706c7567696e2e766964656f2e626f622e756e6c656173686564272c27706c7567696e2e766964656f2e62656e6e75272c27706c7567696e2e766964656f2e6d6574616c6c6971272c27706c7567696e2e766964656f2e73616c7473272c27706c7567696e2e766964656f2e626c616d6f272c27706c7567696e2e766964656f2e636f76656e616e74272c27706c7567696e2e766964656f2e656c797369756d272c27706c7567696e2e766964656f2e706f736569646f6e272c277363726970742e6d6f64756c652e75726c7265736f6c766572272c277363726970742e7472616b74272c277363726970742e70736575646f74762e6c697665272c274461746162617365272c277363726970742e6d6f64756c652e73696d706c656a736f6e272c277363726970742e6d6f64756c652e7472616b74272c277363726970742e6d6f64756c652e646174657574696c272c277363726970742e6d6f64756c652e6164646f6e2e7369676e616c73272c27706c7567696e2e617564696f2e6d75736963626f78275d'
UEXCLUDES = binascii.unhexlify(UES)
    
def CATEGORIES():
    link = OPEN_URL('http://notorious-tv.com/krypton/wiz.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,1,iconimage,fanart,description)
    addDir('Update',url,2,UICON,FANART,'')

    setView('movies', 'MAIN')
	
def UCATEGORIES():
    link = OPEN_URL('http://notorious-tv.com/Update/wiz.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:

        addDir(name,url,3,iconimage,fanart,description)

    setView('movies', 'MAIN')	
        
    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    sure2 = xbmcgui.Dialog().yesno("[COLOR=green]NTV-KryptonWiz[/COLOR]", 'Are you absolutely certain you want to proceed?', '', 'All addons and personal settings will be completely wiped!', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
    if sure2 == 0:
        return
    elif sure2 == 1:
		dp.create("[COLOR=green]NTV-KryptonWiz[/COLOR]","[COLOR=orange]Wiping any previous installation[/COLOR]",'[COLOR=orange]Please Wait[/COLOR]')
    Fresh(params)
    time.sleep(2)
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
 
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    killxbmc()

def Uwizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    sure2 = xbmcgui.Dialog().yesno("[COLOR=green]NTV-KryptonWiz[/COLOR]", 'Are you absolutely certain you want to proceed?', '', 'All addons and personal settings will be completely wiped retaining The MyNtv Library And Trakt/Debrid Details', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
    if sure2 == 0:
        return
    elif sure2 == 1:

		dp.create("[COLOR=green]NTV-UpdateWiz[/COLOR]","[COLOR=orange]Wiping previous Installation[/COLOR]",'[COLOR=orange]Please Wait[/COLOR]')
    UFresh(params)
    time.sleep(2)
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
 
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    killxbmc()	
        
def Fresh(params):
    addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
    xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("freshstart.main_list xbmcPath="+xbmcPath); failed=False
    for root, dirs, files in os.walk(xbmcPath,topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDES]
        for name in files:
            try: os.remove(os.path.join(root,name))
            except:
                if name not in ["kodi.log"]: failed=False
                plugintools.log("Error removing "+root+" "+name)
        for name in dirs:
            try: os.rmdir(os.path.join(root,name))
            except:
                if name not in ["MyNtvBackup"]: failed=False
                plugintools.log("Error removing "+root+" "+name)
	else:
	    pass
		
def UFresh(params):
    addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
    xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("freshstart.main_list xbmcPath="+xbmcPath); failed=False
    for root, dirs, files in os.walk(xbmcPath,topdown=True):
        dirs[:] = [d for d in dirs if d not in UEXCLUDES]
        for name in files:
            try: os.remove(os.path.join(root,name))
            except:
                if name not in ["kodi.log","MyVideos107.db","kodiSHITE.log"]: failed=False
                plugintools.log("Error removing "+root+" "+name)
        for name in dirs:
            try: os.rmdir(os.path.join(root,name))
            except:
                if name not in ["MyNtv","metadata.themoviedb.org","metadata.tvdb.com","repository.NTV","packages","plugin.program.NTV-KryptonWiz","plugin.video.exodus","plugin.video.boxsetkings","plugin.video.bob.unleashed","plugin.video.bennu","plugin.video.metalliq","plugin.video.salts","plugin.video.blamo","plugin.video.covenant","plugin.video.elysium","plugin.video.poseidon","script.module.urlresolver","script.trakt","script.pseudotv.live","Database","script.module.simplejson","script.module.trakt","script.module.dateutil","script.module.addon.signals","plugin.audio.musicbox"]: failed=False
                plugintools.log("Error removing "+root+" "+name)
	else:
	    pass		
		
		
 
		
def Remove(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "Sorry we were not able to remove Package Files", "[COLOR red]Contact us for support[/COLOR]")
	print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass        
	killxbmc1()
	

	
def killxbmc():
    choice = xbmcgui.Dialog().yesno('[COLOR=green]DOWNLOAD COMPLETE[/COLOR]', 'Please force close kodi to continue.', 'Click "Close" to force Kodi to close.',yeslabel='Close')
    if choice == 1:
        
        os._exit(1)
		
def killxbmc1():
    choice = xbmcgui.Dialog().yesno('[COLOR=green]FORCE CLOSE[/COLOR]', 'Please force close kodi to continue.', 'Click "Close" to force Kodi to close.',yeslabel='Close')
    if choice == 1:
        
        os._exit(1)		
		


		
		

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        wizard(name,url,description)

elif mode==2:
        Remove(url)
		


if mode==None or url==None or len(url)<3:
        UCATEGORIES()
       
elif mode==3:
        Uwizard(name,url,description)
		



			
        

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))