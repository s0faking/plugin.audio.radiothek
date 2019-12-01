from resources.lib.RadioThek import RadioThek

api = RadioThek("./")
search_items = api.get_day_selection('fm4')