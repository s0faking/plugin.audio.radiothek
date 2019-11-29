from resources.lib.RadioThek import RadioThek
from resources.lib.Broadcast import Broadcast

import pprint

api = RadioThek()
api.get_api_reference()
print(api.api_reference)
podcasts = api.get_broadcast()
for podcast in podcasts:
    print(podcast.link)
    broadcast = api.get_broadcast_details(podcast.link)
    #broadcast.print_debug()
    #for episode in episodes:
    #    print("Loading %s" % episode.link)
    #    audio_info = api.get_episode_detail(episode.link)
    #    audio_info.print_debug()
    break

#print(api.get_api_reference())