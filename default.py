#!/usr/bin/python
# -*- coding: utf-8 -*-

from resources.lib.RadioThek import *
import os
import xbmcaddon
import xbmcgui
import xbmcplugin
import sys


def parameters_string_to_dict(parameters):
    param_dict = {}
    if parameters:
        param_pairs = parameters[1:].split("&")
        for param_pair in param_pairs:
            param_splits = param_pair.split('=')
            if (len(param_splits)) == 2:
                param_dict[param_splits[0]] = param_splits[1]
    return param_dict


def get_media_path():
    settings = xbmcaddon.Addon()
    basepath = settings.getAddonInfo('path')
    resource_path = os.path.join(basepath, "resources")
    return os.path.join(resource_path, "media")


def add_directory_item(directory, mode, pluginhandle):
    parameters = {"link": directory.link.encode('utf-8'), "mode": mode}
    u = sys.argv[0] + '?' + url_encoder(parameters)
    liz = xbmcgui.ListItem(directory.title)
    info_labels = {
        "Title": directory.title,
        "Plot": directory.description
    }
    liz.setInfo(type="Video", infoLabels=info_labels)

    print("Thumbnail: %s" % directory.thumbnail)

    if directory.logo:
        channel_icon_base = get_media_path()
        logo_path = os.path.join(channel_icon_base, directory.logo)
        if not directory.thumbnail:
            directory.thumbnail = logo_path
        liz.setArt({'thumb': logo_path, 'icon': logo_path, 'poster': directory.thumbnail, 'banner': directory.thumbnail})
    else:
        liz.setArt({'thumb': directory.thumbnail, 'icon': directory.thumbnail, 'poster': directory.thumbnail, 'banner': directory.thumbnail})
    liz.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=liz, isFolder=True)


def add_directory(title, banner, backdrop, logo, description, link, mode, pluginhandle):
    parameters = {"link": link.encode('utf-8'), "mode": mode}
    u = sys.argv[0] + '?' + url_encoder(parameters)
    liz = xbmcgui.ListItem(title)
    info_labels = {
        "Title": title,
        "Plot": description
    }
    liz.setInfo(type="Video", infoLabels=info_labels)

    print("Banner %s" % banner)
    if not banner:
        banner = logo
    if logo:
        channel_icon_base = get_media_path()
        logo_path = os.path.join(channel_icon_base, logo)
        liz.setArt({'thumb': logo_path, 'icon': logo_path, 'poster': banner, 'banner': banner, 'clearlogo': banner, 'clearart': banner})
    else:
        liz.setArt({'thumb': banner, 'icon': banner, 'poster': banner, 'banner': banner, 'clearlogo': banner, 'clearart': banner})
    liz.setProperty('IsPlayable', 'false')
    #xbmcplugin.setContent(pluginhandle, "songs")
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=liz, isFolder=True)


def add_episode(episode, pluginhandle):
    if episode.item_type == 'Broadcast' or episode.item_type == 'BroadcastItem':
        generated_title = "%s | %s" % (episode.time, episode.title)
    else:
        generated_title = episode.title

    parameters = {"link": episode.files[0], "mode": "play", "label": generated_title.encode('utf-8')}
    u = sys.argv[0] + '?' + url_encoder(parameters)
    liz = xbmcgui.ListItem(label=generated_title.encode('utf-8'))
    liz.setProperty('Music', 'true')
    liz.setProperty('mimetype', 'audio/mpeg')

    info_labels = {
        "Title": generated_title,
        "Plot": episode.description,
    }
    if episode.item_type == 'BroadcastItem' and episode.artist:
        info_labels['Plot'] = "[B]Artist:[/B] [COLOR blue]%s[/COLOR] \n[B]Track:[/B] [COLOR blue]%s[/COLOR]\n\n[LIGHT]%s[/LIGHT]" % (episode.artist, episode.trackname, info_labels['Plot'])

    liz.setInfo(type="Video", infoLabels=info_labels)
    liz.setArt({'thumb': episode.thumbnail, 'icon': episode.thumbnail})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addSortMethod(handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_FOLDERS )
    xbmcplugin.setContent(pluginhandle, "video")
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=liz, isFolder=False)


def add_stream(episode, pluginhandle):
    if episode.item_type == 'Broadcast' or episode.item_type == 'BroadcastItem':
        generated_title = "%s | %s" % (episode.time, episode.title)
    else:
        generated_title = episode.title

    parameters = {"link": episode.files[0], "mode": "play", "label": generated_title.encode('utf-8')}
    u = sys.argv[0] + '?' + url_encoder(parameters)
    liz = xbmcgui.ListItem(label=generated_title.encode('utf-8'))

    if episode.logo:
        channel_icon_base = get_media_path()
        logo_path = os.path.join(channel_icon_base, episode.logo)
        liz.setArt({'thumb': logo_path, 'icon': logo_path, 'poster': episode.thumbnail, 'banner': episode.thumbnail, 'clearlogo': episode.thumbnail, 'clearart': episode.thumbnail})
    else:
        liz.setArt({'thumb': episode.thumbnail, 'icon': episode.thumbnail, 'poster': episode.thumbnail, 'banner': episode.thumbnail, 'clearlogo': episode.thumbnail, 'clearart': episode.thumbnail})

    liz.setProperty('Music', 'true')
    liz.setProperty('mimetype', 'audio/mpeg')

    info_labels = {
        "Title": generated_title,
        "Plot": episode.description,
    }
    if episode.item_type == 'BroadcastItem' and episode.artist:
        info_labels['Plot'] = "[B]Artist:[/B] [COLOR blue]%s[/COLOR] \n[B]Track:[/B] [COLOR blue]%s[/COLOR]\n\n[LIGHT]%s[/LIGHT]" % (episode.artist, episode.trackname, info_labels['Plot'])

    liz.setInfo(type="Video", infoLabels=info_labels)
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=liz, isFolder=False)


def get_navigation():
    add_directory("Highlights", "", "", "", "", "", "highlights", pluginhandle)
    add_directory("Broadcasts", "", "", "", "", "", "broadcast", pluginhandle)
    add_directory("Podcasts", "", "", "", "", "", "podcasts", pluginhandle)
    add_directory("Topics", "", "", "", "", "", "tags", pluginhandle)
    add_directory("Archive", "", "", "", "", "", "archive", pluginhandle)
    add_directory("Live", "", "", "", "", "", "live", pluginhandle)
    xbmcplugin.endOfDirectory(pluginhandle)


def main():
    params = parameters_string_to_dict(sys.argv[2])
    mode = params.get('mode')
    link = unquote_url(params.get('link'))
    print("MODE %s" % mode)
    print("LINK %s" % link)

    if mode is None:
        get_navigation()
    elif mode == 'broadcast':
        list_items = api.get_broadcast()
        for list_item in list_items:
            add_directory_item(list_item, "broadcast_detail", pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'podcasts':
        list_items = api.get_podcasts()
        for list_item in list_items:
            add_directory_item(list_item,  "podcast_detail", pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'highlights':
        list_items = api.get_highlights()
        for list_item in list_items:
            add_directory_item(list_item, "broadcast_detail", pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'live':
        episodes = api.get_livestream()
        for episode in episodes:
            add_stream(episode, pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'tags':
        list_items = api.get_tags()
        for list_item in list_items:
            add_directory_item(list_item,  "tags_detail", pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'archive':
        list_items = api.get_archive()
        for list_item in list_items:
            add_directory_item(list_item, "podcast_detail", pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'podcast_detail':
        episodes = api.get_podcast_details(link)
        for episode in episodes:
            add_episode(episode, pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'tags_detail':
        list_items = api.get_tag_items(link)
        for list_item in list_items:
            add_directory_item(list_item, "broadcast_detail", pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'broadcast_detail':
        print("----------    Broadcast Details Called width %s" % link)
        api.get_api_reference()
        broadcast = api.get_broadcast_details(link)
        add_episode(broadcast, pluginhandle)
        for broadcast_item in broadcast.items:
            if not broadcast_item.hidden:
                add_episode(broadcast_item, pluginhandle)
        xbmcplugin.endOfDirectory(pluginhandle)
    elif mode == 'play':
        play_link = "%s|User-Agent=%s" % (link, api.user_agent)
        title = params.get('label')
        play_item = xbmcgui.ListItem(label=title, path=play_link)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem=play_item)
        xbmcplugin.setContent(pluginhandle, "album")
        xbmcplugin.endOfDirectory(pluginhandle)


if __name__ == '__main__':
    pluginhandle = int(sys.argv[1])
    api = RadioThek()
    main()