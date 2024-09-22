"""convert csv files to stac"""

import argparse
import logging
from pathlib import Path

import pandas as pd
import pystac

from climate_stac import create_catalog, update_catalog_from_dataframe

if __name__ == '__main__':
    # set logger level
    logger = logging.getLogger("climate_stac")
    # logger.setLevel(logging.INFO) # by default, the logger level is set to WARNING

    # File paths
    output_dir = 'stac'
    hazard_path = 'csv/hazard.csv'
    exv_path = 'csv/expvul.csv' # can both be combined into one csv, but: some attributes are slightly different
    csv_paths = [hazard_path, exv_path]

    # Create the parser
    parser = argparse.ArgumentParser(description='Convert CSV files to STAC')
    # --stac_dir is the output directory for the STAC catalog
    parser.add_argument('--stac_dir', type=str, help='Output directory for the STAC catalog', default='stac')
    # --csv_paths are one or more paths to CSV files
    parser.add_argument('--csv_paths', type=str, nargs='+', help='One or more paths to CSV files', default=csv_paths)

    # Parse the arguments
    args = parser.parse_args()
    output_dir = Path(args.stac_dir)
    output_dir.mkdir(parents=True, exist_ok=True)  # Create the output directory if it doesn't exist
    csv_paths = [Path(path) for path in args.csv_paths]

    # Create catalogs from both hazard and exposure-vulnerability CSVs
    catalog_main = create_catalog()

    # Update the catalog with the data from the CSV files
    for csv_path in csv_paths:
        df = pd.read_csv(csv_path, encoding='utf-8')
        catalog_main = update_catalog_from_dataframe(catalog=catalog_main, dataframe=df)

    # validate catalog
    # pystac.Catalog.validate(catalog_main)
    
    # show full catalog structure
    # catalog_main.describe()

    # Normalize hrefs and save the catalog
    catalog_main.normalize_hrefs(output_dir.as_posix())
    catalog_main.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
    # catalog_main.save(catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)
