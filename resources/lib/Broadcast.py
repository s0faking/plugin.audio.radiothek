#!/usr/bin/python
# -*- coding: utf-8 -*-

from resources.lib.helpers import *
from resources.lib.BroadcastItem import BroadcastItem


class Broadcast:
    images = []
    thumbnail = ""
    backdrop = ""
    items = []
    files = []
    loopStreamId = ""
    host = ""
    host_channel = ""
    station = ""
    program = ""
    subtitle = ""
    category = ""
    description = ""

    def __init__(self, json_data, api_reference):
        self.item_type = "Broadcast"
        if json_data and 'entity' in json_data and json_data['entity'] == self.item_type:
            self.id = json_data['id']
            if 'station' in json_data:
                self.station = json_data['station']
            if 'title' in json_data:
                self.title = json_data['title']
            if 'programTitle' in json_data:
                self.program = json_data['programTitle']
            if 'subtitle' in json_data:
                self.subtitle = clean_html(json_data['subtitle'])
            if 'ressort' in json_data:
                self.category = json_data['ressort']
            if 'description' in json_data:
                self.description = clean_html(json_data['description'])
            if 'images' in json_data and json_data['images']:
                self.thumbnail = get_images(json_data['images'][0]['versions'], True, True)
                self.images = get_images(json_data['images'][0]['versions'])
                if self.images and len(self.images) > 1:
                    self.backdrop = self.images[1]

            # Stream Infos
            self.broadcasted = get_time_format(json_data['scheduledStart'])
            self.start = json_data['scheduledStart']
            self.end = json_data['scheduledEnd']
            self.time = "%s - %s" % (get_time_format(self.start, False, True),get_time_format(self.end, False, True))
            self.loopStreamIds = json_data['streams']
            (self.loopStreamId, self.offset) = self.get_stream_base(json_data['start'])

            channel_infos = api_reference['stations'][self.station]
            self.host = channel_infos['loopstream']['host']
            self.host_channel = channel_infos['loopstream']['channel']

            parameters = {'channel': self.host_channel,
                          'id': self.loopStreamId,
                          'shoutcast': 1,
                          'player': 'radiothek_v1',
                          'referer': 'radiothek.orf.at',
                          'offset': self.offset}
            get_params = url_encoder(parameters)
            self.stream = "https://%s/?%s" % (self.host, get_params)
            self.files = [self.stream]

            if 'items' in json_data:
                self.items = []
                for item in json_data['items']:
                    bcast_item = BroadcastItem(item, self)
                    self.items.append(bcast_item)

    def get_stream_base(self, start):
        loopstream_path = ""
        loopstream_offset = 0
        for stream in self.loopStreamIds:
            if start >= stream['start']:
                loopstream_path = stream['loopStreamId']
                loopstream_offset = start - stream['start']
        return loopstream_path, loopstream_offset

    def print_debug(self):
        object_print(vars(self))
        print("----------------------------------")