import pystac
import json
import os

catalog = pystac.Catalog.from_file("stac/catalog.json")

a = list(catalog.get_links())

catalog1 = pystac.Catalog.from_file(a[0].get_target_str())

# # Parse the JSON data
# catalog_dict = json.loads("../stac/catalog.json")

# # Create a PySTAC Catalog
# catalog = pystac.Catalog.from_dict(catalog_dict)

def process_links(catalog, links_dict, parent_folder):
    for link in catalog.links:
        if link.rel == 'child':
            print(link.target.replace('./', f'{parent_folder}/'))
            if 'collection' in link.target:
                linked_catalog = pystac.Collection.from_file(link.target.replace('./', f'{parent_folder}/'))
                links_dict[linked_catalog.id] = {"href": f"{parent_folder}/{linked_catalog.id}"}
            elif 'catalog' in link.target:
                linked_catalog = pystac.Catalog.from_file(link.target.replace('./', f'{parent_folder}/'))
                # Include the parent folder in the href for sub-catalogs
                links_dict[linked_catalog.id] = {"href": f"{parent_folder}/{linked_catalog.id}"}
                process_links(linked_catalog, links_dict[linked_catalog.id], os.path.join( parent_folder, os.path.split(link.target[2:])[0]))


# Initialize the dictionary to store links
links_dict = {}

# Manually include the parent folder for the main catalog
parent_folder = "stac"
links_dict[parent_folder] = {"href": f"./{parent_folder}/catalog.json"}

# Process links recursively
process_links(catalog, links_dict[parent_folder], parent_folder)

# Print the resulting dictionary
print(links_dict)