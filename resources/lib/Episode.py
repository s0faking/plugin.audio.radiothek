#!/usr/bin/python
# -*- coding: utf-8 -*-


class Episode:
    channel_icons = {
        'bgl': 'bgl.png',
        'vbg': 'vbg.png',
        'ooe': 'ooe.png',
        'noe': 'noe.png',
        'ktn': 'ktn.png',
        'sbg': 'sbg.png',
        'stm': 'stm.png',
        'tir': 'tir.png',
        'wie': 'wie.png',
        'fm4': 'fm4.png',
        'oe1': 'oe1.png',
        'oe3': 'oe3.png'
    }
    logo = ""

    def __init__(self, cms_id, title, description, files, item_type, thumbnail, backdrop, station):
        self.id = cms_id
        self.title = title
        self.description = description
        self.files = files
        self.thumbnail = thumbnail
        self.item_type = item_type
        self.backdrop = backdrop
        self.station = station
        if self.station in self.channel_icons:
            self.logo = self.channel_icons[self.station]

    def print_debug(self):
        print("Station: %s" % self.station)
        print("ID: %s" % self.id)
        print("Type: %s" % self.item_type)
        print("Name: %s" % self.title)
        print("Description: %s" % self.description)
        print("Files: %s" % self.files)
        print("Image: %s" % self.thumbnail)
        print("Backdrop: %s" % self.backdrop)
        print("----------------------------------")