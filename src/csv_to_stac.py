import pystac


catalog = pystac.Catalog.from_file("../stac/catalog.json")

a = list(catalog.get_links())

catalog1 = pystac.Catalog.from_file(a[0].get_target_str())