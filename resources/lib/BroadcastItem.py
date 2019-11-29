#!/usr/bin/python
# -*- coding: utf-8 -*-

from resources.lib.helpers import *


class BroadcastItem:
    images = []
    thumbnail = ""
    backdrop = ""
    title = ""
    artist = ""
    time = ""
    trackname = ""
    subtitle = ""
    station = ""
    description = ""
    duration = 0
    hidden = False

    def __init__(self, json_item_data, parent):
        self.item_type = "BroadcastItem"
        if json_item_data and 'entity' in json_item_data and json_item_data['entity'] == self.item_type:
            self.id = json_item_data['id']
            self.parent_title = parent.title
            if 'title' in json_item_data and json_item_data['title']:
                self.title = json_item_data['title']
            else:
                self.title = " -- %s" % parent.title
                self.hidden = True
            if 'interpreter' in json_item_data:
                self.artist = json_item_data['interpreter']
                self.trackname = self.title
                self.title = "%s - %s" % (self.artist, self.trackname)
            if 'subtitle' in json_item_data:
                self.subtitle = clean_html(json_item_data['subtitle'])
            else:
                self.subtitle = parent.subtitle
            if 'description' in json_item_data:
                self.description = clean_html(json_item_data['description'])
            else:
                self.description = parent.description
            if 'duration' in json_item_data:
                self.duration = json_item_data['duration']
            if 'images' in json_item_data and json_item_data['images']:
                self.thumbnail = get_images(json_item_data['images'][0]['versions'], True)
                self.images = get_images(json_item_data['images'][0]['versions'])
                if self.images and len(self.images) and not len(self.thumbnail):
                    self.thumbnail = get_images(json_item_data['images'][0]['versions'], True)
                if self.images and len(self.images) > 1:
                    self.backdrop = self.images[1]
            else:
                self.thumbnail = parent.thumbnail
                self.backdrop = parent.backdrop

            # Stream Infos
            self.station = parent.station
            self.broadcasted = get_time_format(json_item_data['start'])
            self.time = get_time_format(json_item_data['start'], False, True)
            self.start = json_item_data['start']
            self.end = json_item_data['end']
            self.offset = self.start - parent.start
            (self.loopStreamId, self.offset) = parent.get_stream_base(self.start)

            parameters = {'channel': parent.host_channel,
                          'id': self.loopStreamId,
                          'shoutcast': 1,
                          'player': 'radiothek_v1',
                          'referer': 'radiothek.orf.at',
                          'offset': self.offset}
            get_params = url_encoder(parameters)
            self.stream = "https://%s/?%s" % (parent.host, get_params)

            self.files = [self.stream]

    def print_debug(self):
        object_print(vars(self))
        print("----------------------------------")