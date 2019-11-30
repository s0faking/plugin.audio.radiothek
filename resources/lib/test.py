from resources.lib.RadioThek import RadioThek

api = RadioThek("./")
api.get_livestream()
