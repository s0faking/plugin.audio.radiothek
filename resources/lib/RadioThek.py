#!/usr/bin/python
# -*- coding: utf-8 -*-

from resources.lib.helpers import *
from resources.lib.Directory import Directory
from resources.lib.Episode import Episode
from resources.lib.Broadcast import Broadcast

import json
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
    from urllib import urlencode


class RadioThek:
    api_ref = "https://radiothek.orf.at/js/app.769b3884.js"
    api_base = "https://audioapi.orf.at"
    tag_url = "/radiothek/api/tags/%s"
    staple_url = "/radiothek/stapled.json?_o=radiothek.orf.at"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    api_reference = False
    stapled_content = False
    station_nice = {'sbg': 'Radio Salzburg',
                    'ooe': 'Radio Oberösterreich',
                    'wie': 'Radio Wien',
                    'vgrp': 'ORF Volksgruppen',
                    'vbg': 'Radio Vorarlberg',
                    'oe3': 'Hitradio Ö3',
                    'fm4': 'FM4',
                    'stm': 'Radio Steiermark',
                    'sbg': 'Radio Salzburg',
                    'noe': 'Radio Niederösterreich',
                    'oe1': 'Ö1',
                    'ktn': 'Radio Kärnten',
                    'bgl': 'Radio Burgenland',
                    'slo': 'Slovenski spored',
                    'campus': 'Ö1 Campus',
                    'tir': 'Radio Tirol'
                    }

    def __init__(self):
        self.log("RadioThek API loaded")

    def get_livestream(self):
        self.get_api_reference()
        list_items = []

        for station in self.api_reference['stations']:
            item = self.api_reference['stations'][station]
            title = item['title']
            description = ""

            if 'livestream' in item:
                link = item['livestream']
                thumbnail = ""
                backdrop = ""
                print(link)
                if link:
                    episode = Episode(station, title, description, [link], 'Livestream', thumbnail, backdrop, station)
                    list_items.append(episode)
        return list_items


    def get_tags(self):
        staple = self.get_stapled()
        list_items = []
        if 'tags' in staple:
            for tag_item in staple['tags']:
                title = clean_html(tag_item['title'])
                subtitle = clean_html(tag_item['subtitle'])
                thumbnail = get_images(tag_item['image']['versions'], True)
                backdrop = ""
                images = get_images(tag_item['image']['versions'])
                rel_link = self.tag_url % tag_item['key']
                abs_link = "%s%s" % (self.api_base, rel_link)
                list_items.append(Directory(title, subtitle, abs_link, thumbnail, images[0], backdrop))
                self.log("-----------   Tags   -------------")
                self.log("Title: %s" % title)
                self.log("Subtitle: %s" % subtitle)
                self.log("Thumbnail: %s" % thumbnail)
                self.log("Link: %s" % abs_link)
                for image in images:
                    self.log("Images: %s" % image)
        return list_items

    def get_episode_detail(self, cms_id, items_json, loop_stream_id, start):
        for item in items_json['items']:
            if item['id'] == cms_id:
                station = clean_html(item['station'])

                title = clean_html(item['title'])
                episode_title = "%s %s" % (station, title)
                item_type = clean_html(item['entity'])
                description = clean_html(item['description'])
                thumbnail = ""
                if 'images' in item and len(item['images']):
                    thumbnail = get_images(item['images'][0]['versions'])[0]

                station_infos = self.api_reference['stations'][item['station']]
                host = station_infos['loopstream']['host']
                host_station = station_infos['loopstream']['channel']
                offset = item['start'] - start

                parameters = self.build_stream_url(host_station, loop_stream_id, offset)
                get_params = urlencode(parameters)
                base_stream = "https://%s/?%s" % (host, get_params)

                return Episode(cms_id, episode_title, description, [base_stream], item_type, thumbnail, "", station)

    @staticmethod
    def build_stream_url(host_station, loop_stream_id, offset):
        return {'channel': host_station,
                'id': loop_stream_id,
                'shoutcast': 1,
                'player': 'radiothek_v1',
                'referer': 'radiothek.orf.at',
                'offset': offset}

    def get_broadcast_details(self, url):
        detail_json = self.request_url(url, True)
        return Broadcast(detail_json, self.api_reference)

    def get_podcast_details(self, url):
        episodes = []
        self.log("Getting Podcast Details from %s" % url)
        detail_json = self.request_url(url, True)
        item_type = 'Podcast'
        if 'data' in detail_json and 'episodes' in detail_json['data']:
            data_json = detail_json['data']
            for episode_json in data_json['episodes']:
                cms_id = detail_json['slug']

                station = clean_html(data_json['author'])
                title = clean_html(episode_json['title'])
                episode_title = "%s %s" % (station, title)

                description = clean_html(episode_json['description'])

                thumbnail = data_json['image']
                files = []
                for audio_file in episode_json['enclosures']:
                    files.append(audio_file['url'])
                backdrop = ""

                episode = Episode(cms_id, episode_title, description, files, item_type, thumbnail, backdrop, station)
                episodes.append(episode)
        return episodes

    def get_tag_items(self, url):
        items = []
        self.log("Getting Tag Details from %s" % url)
        data_json = self.request_url(url, True)
        if data_json['items']:
            for item_json in data_json['items']:
                try:
                    station = clean_html(item_json['station'])

                    title = clean_html(item_json['title'])
                    broadcasted = get_time_format(item_json['start'])
                    directory_title = "%s (%s)" % (title, broadcasted)

                    subtitle = clean_html(item_json['subtitle'])
                    description = clean_html(item_json['description'])

                    if station in self.station_nice:
                        directory_description = "[COLOR blue]%s[/COLOR]\n%s\n\n%s" % (self.station_nice[station], subtitle, description)
                    else:
                        directory_description = "%s\n\n%s" % (subtitle, description)

                    thumbnail = ""
                    if 'images' in item_json:
                        if len(item_json['images']):
                            thumbnail = get_images(item_json['images'][0]['versions'], True, True)

                    link = item_json['href']
                    backdrop = ""

                    tag_directory = Directory(directory_title, directory_description, link, thumbnail, backdrop, station)
                    items.append(tag_directory)
                    #self.log("-----------   Items   -------------")
                    #self.log("Station: %s" % station)
                    #self.log("Title: %s" % title)
                    #self.log("Subtitle: %s" % subtitle)
                    #self.log("Description: %s" % description)
                    #self.log("Thumbnail: %s" % thumbnail)
                    #self.log("Broadcasted: %s" % broadcasted)
                    #self.log("Link: %s" % link)
                except Exception as e:
                    self.log(str(e))
                    self.log("[ERROR] Request Url: %s" % url)
                    print(item_json)
        return items

    def get_broadcast(self):
        staple = self.get_stapled()
        list_items = []
        if 'stations' in staple:
            for station in staple['stations']:
                if 'broadcast' in staple['stations'][station]['data']:
                    broadcast_item = staple['stations'][station]['data']['broadcast']

                    station = clean_html(broadcast_item['station'])
                    title = clean_html(broadcast_item['title'])
                    broadcasted = get_time_format(broadcast_item['scheduledStart'], False, True)
                    broadcastedUntil = get_time_format(broadcast_item['scheduledEnd'], False, True)
                    directory_title = "%s (%s-%s)" % (title, broadcasted, broadcastedUntil)

                    subtitle = clean_html(broadcast_item['subtitle'])
                    description = clean_html(broadcast_item['description'])

                    if station in self.station_nice:
                        directory_description = "[COLOR blue]%s[/COLOR]\n%s\n\n%s" % (self.station_nice[str(station)].decode('utf-8'), subtitle, description)
                    else:
                        directory_description = "%s\n\n%s" % (subtitle, description)

                    if broadcast_item["images"]:
                        thumbnail = get_images(broadcast_item['images'][0]['versions'], True)
                    else:
                        thumbnail = ""
                    backdrop = ""
                    link = broadcast_item['href']

                    broadcast_directory = Directory(directory_title, directory_description, link, thumbnail, backdrop, station)
                    list_items.append(broadcast_directory)
                    #self.log("-----------   Broadcast   -------------")
                    #self.log("Station: %s" % station)
                    #self.log("Title: %s" % title)
                    #self.log("Subtitle: %s" % subtitle)
                    #self.log("Description: %s" % description)
                    #self.log("Thumbnail: %s" % thumbnail)
                    #self.log("Broadcasted: %s" % get_time_format(broadcast_item['scheduledStart']))
                    #self.log("Link: %s" % link)
        return list_items

    def get_highlights(self):
        staple = self.get_stapled()
        list_items = []
        if 'stations' in staple:
            for station in staple['stations']:
                if 'highlights' in staple['stations'][station]['data']:
                    broadcast_items = staple['stations'][station]['data']['highlights']
                    for broadcast_item in broadcast_items:
                        title = clean_html(broadcast_item['title'])
                        if 'broadcastDay' in broadcast_item and broadcast_item['broadcastDay'] is not None:
                            broadcasted = get_date_format(broadcast_item['broadcastDay'])
                            directory_title = "%s - %s" % (title, broadcasted)
                        else:
                            directory_title = station, title
                        description = ""

                        if station in self.station_nice:
                            station_name = self.station_nice[str(station)].decode('utf-8')
                        else:
                            station_name = station

                        if 'text' in broadcast_item:
                            description = clean_html(broadcast_item['text'])
                        directory_description = "[COLOR blue]%s[/COLOR] \n%s" % (station_name, description)

                        if broadcast_item["images"]:
                            thumbnail = get_images(broadcast_item['images'][0]['versions'], True)
                        else:
                            thumbnail = ""
                        backdrop = ""
                        link = broadcast_item['target']

                        broadcast_directory = Directory(directory_title, directory_description, link, thumbnail, backdrop, station)
                        list_items.append(broadcast_directory)
                        #self.log("-----------   Broadcast   -------------")
                        #self.log("Station: %s" % station)
                        #self.log("Title: %s" % title)
                        #self.log("Subtitle: %s" % subtitle)
                        #self.log("Description: %s" % description)
                        #self.log("Thumbnail: %s" % thumbnail)
                        #self.log("Broadcasted: %s" % get_time_format(broadcast_item['scheduledStart']))
                        #self.log("Link: %s" % link)
        return list_items

    def get_archive(self):
        staple = self.get_stapled()
        list_items = []
        if 'archive' in staple:
            for archive_item in staple['archive']:
                station = clean_html(archive_item['data']['author'])
                title = clean_html(archive_item['data']['title'])
                broadcasted = get_time_format(archive_item['data']['published'])
                directory_title = "[%s] %s (%s)" % (station, title, broadcasted)

                subtitle = clean_html(archive_item['data']['subtitle'])
                description = clean_html(archive_item['data']['description'])
                directory_description = "%s\n\n%s" % (subtitle, description)

                thumbnail = archive_item['data']['image']
                backdrop = ""
                link = archive_item['href']

                archive_directory = Directory(directory_title, directory_description, link, thumbnail, backdrop, station)
                list_items.append(archive_directory)
                #self.log("-----------   Archive   -------------")
                #self.log("Station: %s" % station)
                #self.log("Title: %s" % title)
                #self.log("Subtitle: %s" % subtitle)
                #self.log("Description: %s" % description)
                #self.log("Thumbnail: %s" % thumbnail)
                #self.log("Broadcasted: %s" % broadcasted)
                #self.log("Link: %s" % link)
        return list_items

    def get_podcasts(self):
        staple = self.get_stapled()
        list_items = []
        if 'podcasts' in staple:
            for station in staple['podcasts']:
                for podcast_item in staple['podcasts'][station]:
                    station = clean_html(podcast_item['data']['author'])

                    broadcasted = get_time_format(podcast_item['data']['published'])
                    title = clean_html(podcast_item['data']['title'])
                    directory_title = "%s (%s)" % (title, broadcasted)

                    subtitle = clean_html(podcast_item['data']['subtitle'])
                    description = clean_html(podcast_item['data']['description'])
                    directory_description = "[B]%s[/B]\n%s\n\n%s" % (station, subtitle, description)

                    thumbnail = podcast_item['data']['image']

                    link = podcast_item['href']
                    podcast_directory = Directory(directory_title, directory_description, link, thumbnail, "", station)
                    list_items.append(podcast_directory)
                    #self.log("-----------   Podcast   -------------")
                    #self.log("Station: %s" % station)
                    #self.log("Title: %s" % title)
                    #self.log("Subtitle: %s" % subtitle)
                    #self.log("Description: %s" % description)
                    #self.log("Thumbnail: %s" % thumbnail)
                    #self.log("Broadcasted: %s" % broadcasted)
                    #self.log("Link: %s" % link)
        return list_items

    def get_api_reference(self):
        if not self.api_reference:
            content = self.request_url(self.api_ref, True, False)
            self.api_reference = get_js_json(content)
        return self.api_reference

    # gets the station list
    def get_stapled(self):
        if not self.stapled_content:
            self.stapled_content = self.request_url(self.staple_url)
        return self.stapled_content

    # request external url, returns the url content
    def request_url(self, url, absolute_url=False, parse_json=True):
        if not absolute_url:
            request_url = "%s%s" % (self.api_base, url)
        else:
            request_url = url
        self.log("Loading from %s" % request_url)
        request = urlopen(Request(request_url, headers={'User-Agent': self.user_agent}))
        request_data = request.read()
        if parse_json:
            return json.loads(request_data)
        else:
            return request_data

    @staticmethod
    def log(msg):
        try:
            print(msg)
        except Exception as e:
            print(msg.encode('utf-8'))

