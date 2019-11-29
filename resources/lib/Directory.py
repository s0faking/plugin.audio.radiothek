#!/usr/bin/python
# -*- coding: utf-8 -*-


class Directory:
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

    def __init__(self, title, description, link, thumbnail, backdrop, station):
        self.title = title
        self.description = description
        self.link = link
        self.thumbnail = thumbnail
        self.backdrop = backdrop
        self.station = station
        if self.station in self.channel_icons:
            self.logo = self.channel_icons[self.station]

    def print_debug(self):
        print("Name: %s" % self.title)
        print("Description: %s" % self.description)
        print("Link: %s" % self.link)
        print("Image: %s" % self.thumbnail)
        print("Backdrop: %s" % self.backdrop)
        print("Station: %s" % self.station)
        print("----------------------------------")

