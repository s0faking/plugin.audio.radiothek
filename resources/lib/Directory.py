#!/usr/bin/python
# -*- coding: utf-8 -*-


class Directory:
    def __init__(self, title, description, link, thumbnail, backdrop, station, logo):
        self.title = title
        self.description = description.strip()
        self.link = link
        self.thumbnail = thumbnail
        self.backdrop = backdrop
        self.station = station
        self.logo = logo

    def print_debug(self):
        print("----------  DIRECTORY  -------------")
        print("Name: %s" % self.title)
        print("Description: %s" % self.description)
        print("Link: %s" % self.link)
        print("Image: %s" % self.thumbnail)
        print("Backdrop: %s" % self.backdrop)
        print("Station: %s" % self.station)
        print("Logo: %s" % self.logo)
        print("----------------------------------")

