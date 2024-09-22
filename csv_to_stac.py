"""convert csv files to stac"""

import os
from pathlib import Path
import pandas as pd
import pystac
import logging

from climate_stac import update_catalog_from_dataframe, create_catalog


if __name__ == '__main__':
    # set logger level
    logger = logging.getLogger("climate_stac")
    # logger.setLevel(logging.INFO) # by default, the logger level is set to WARNING

    # File paths
    output_dir = Path('stac')
    haz = Path('csv/hazard.csv')
    exv = Path('csv/expvul.csv') # can both be combined into one csv, but: some attributes are slightly different

    # Read data sheets
    hazard_df = pd.read_csv(haz, encoding='utf-8')
    expvul_df = pd.read_csv(exv, encoding='utf-8')

    # Create catalogs from both hazard and exposure-vulnerability CSVs
    catalog_main = create_catalog()
    catalog_main = update_catalog_from_dataframe(catalog=catalog_main, dataframe=hazard_df)
    catalog_main = update_catalog_from_dataframe(catalog=catalog_main, dataframe=expvul_df)

    # validate catalog
    # pystac.Catalog.validate(catalog_main)
    
    # show full catalog structure
    # catalog_main.describe()

    # Normalize hrefs and save the catalog
    catalog_main.normalize_hrefs(output_dir.as_posix())
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
    # catalog_main.save(catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)
