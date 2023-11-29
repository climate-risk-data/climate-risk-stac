import pystac


catalog = pystac.Catalog.from_file("../stac/catalog.json")

a = list(catalog.get_links())