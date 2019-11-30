from resources.lib.RadioThek import RadioThek

api = RadioThek("./")
search_items = api.get_search('HALLO')
for search in search_items:
    search.print_debug()