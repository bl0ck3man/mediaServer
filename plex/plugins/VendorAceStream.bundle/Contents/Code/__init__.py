import os
import sys
import urllib
import hashlib

TITLE = 'Ace Stream'
PREFIX = '/video/acestream'

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.jpg')
    
@handler(PREFIX, TITLE)
def MainMenu():
    categories = LoadCategories()
    
    oc = ObjectContainer()
    for category in categories:
        oc.add(DirectoryObject(
            key = Callback(ListItems, category=category),
            title = category
        ))
    oc.add(PrefsObject(title = L('Preferences'), thumb = R('icon-prefs.png')))
    return oc

@route(PREFIX + '/listitems')
def ListItems(category, subcategory=None):
    if subcategory is None:
        oc = ObjectContainer(title1 = L(category))
    else:
        if isinstance(subcategory, str):
            subcategory = subcategory.decode("utf-8")
        oc = ObjectContainer(title1 = subcategory)
    
    if subcategory is None:
        # we're inside category, show subcategories
        subcategories = LoadSubcategories(category)
        for s in subcategories:
            oc.add(DirectoryObject(
                key = Callback(ListItems, category=category, subcategory=s),
                title = s
            ))
            
    items = LoadPlaylist(category, subcategory)
    for item in items:
        # Simply adding VideoClipObject does not work on some clients (like LG SmartTV),
        # so there is an endless recursion - function CreateVideoClipObject calling itself -
        # and I have no idea why and how it works...
        oc.add(CreateVideoClipObject(
            url = item['url'],
            title = item['title'],
            thumb = item['thumb'],
            protocol = item['protocol'],
            media_container = item.get('mediainfo_container'),
            video_codec = item.get('mediainfo_video_codec'),
            audio_codec = item.get('mediainfo_audio_codec')
        ))
    return oc

@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, protocol, media_container, video_codec, audio_codec, container=False):
    if protocol == "hls":
        part_key = HTTPLiveStreamURL(url=url)
    else:
        part_key = url
        
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url=url, title=title, thumb=thumb, protocol=protocol, media_container=media_container, video_codec=video_codec, audio_codec=audio_codec, container=True),
        url = url,
        title = title,
        thumb = GetThumb(thumb),
        items = [
            MediaObject(
                container = GetPlexMediaContainer(media_container),
                video_codec = GetPlexVideoCodec(video_codec),
                audio_codec = GetPlexAudioCodec(audio_codec),
                parts = [
                    PartObject(
                        key = part_key
                    )
                ],
                optimized_for_streaming = True
            )
        ]
    )

    if container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
    return vco
    
def GetPlaylistURL():
    if Prefs['playlist'] and (Prefs['playlist'].startswith('http://') or Prefs['playlist'].startswith('https://')):
        return Prefs['playlist']
    return None
    
def LoadCategories():
    playlist_url = GetPlaylistURL()
    if not playlist_url:
        return []
    
    url = playlist_url + "?cmd=get_categories&format=json"    
    return JSON.ObjectFromURL(url)
    
def LoadSubcategories(category):
    if not category:
        return []
    playlist_url = GetPlaylistURL()
    if not playlist_url:
        return []
        
    if isinstance(category, unicode):
        category = category.encode("utf-8")
    
    url = playlist_url + "?cmd=get_subcategories&format=json&category=%s" % (category)    
    return JSON.ObjectFromURL(url)
    
def LoadPlaylist(category, subcategory):
    playlist_url = GetPlaylistURL()
    if not playlist_url:
        return []
        
    if 'Host' in Request.Headers:
        host = Request.Headers['Host']
    else:
        host = None
        
    url = playlist_url + "?cmd=get_playlist&format=json&transcode_audio=1&transcode_mp3=0"
    if host:
        url += "&host=" + str(host)
    if category is not None:
        if isinstance(category, unicode):
            category = category.encode("utf-8")
        url += "&category=" + str(category)
    
    if subcategory is None:
        subcategory = ""
    if isinstance(subcategory, unicode):
        subcategory = subcategory.encode("utf-8")
    url += "&subcategory=" + str(subcategory)
    data = JSON.ObjectFromURL(url)
    
    return data
    
def GetThumb(thumb):
    if thumb and thumb.startswith('http'):
        return thumb
    elif thumb and thumb <> '':
        return R(thumb)
    else:
        return R('icon-default.png')

def GetAttribute(text, attribute, delimiter1 = '="', delimiter2 = '"'):
    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip())
    else:
        return ''
        
# map mediainfo to plex values
def GetPlexMediaContainer(value):
    if not value:
        return None

    valuemap = {
        'mpeg-4': 'mp4',
        'avi': 'avi',
        'mkv': 'mkv',
        'mpegts': 'mpegts',
    }
    
    value = value.lower()
    if value in valuemap:
        Log.Debug("GetPlexMediaContainer: %s -> %s" % (value, valuemap[value]))
        return valuemap[value]
        
    Log.Debug("GetPlexMediaContainer: not found: %s" % (value,))
    return None

def GetPlexVideoCodec(value):
    if not value:
        return None

    valuemap = {
        'avc': 'h264',
        'xvid': 'xvid',
        'h264': 'h264',
    }
    
    value = value.lower()
    if value in valuemap:
        Log.Debug("GetPlexVideoCodec: %s -> %s", value, valuemap[value])
        return valuemap[value]
        
    Log.Debug("GetPlexVideoCodec: not found: %s", value)
    return None

def GetPlexAudioCodec(value):
    if not value:
        return None

    valuemap = {
        'aac': 'aac',
        'aac lc': 'aac',
        'ac3': 'ac3',
        'mp3': 'mp3',
        'mp2': 'mp2',
    }
    
    value = value.lower()
    if value in valuemap:
        Log.Debug("GetPlexAudioCodec: %s -> %s", value, valuemap[value])
        return valuemap[value]
        
    Log.Debug("GetPlexAudioCodec: not found: %s", value)
    return None

