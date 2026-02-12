"""
Check validity of URLs in CSV files.
This script should be run before building the new catalog.
It results in a CSV output file ('csv/link_report.csv') containing broken links.
"""

import logging
import sys
from pathlib import Path
import pandas as pd
import urllib.request
import urllib.error
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("link_checker")

def check_url(url: str) -> tuple[bool, str | int]:
    """Check if a URL is reachable."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Create SSL context that ignores certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        # 1. Try HEAD first
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            return True, response.status
    except Exception:
        try:
            # 2. Fallback to GET with Range (to avoid downloading large files)
            get_headers = headers.copy()
            get_headers['Range'] = 'bytes=0-10'
            req = urllib.request.Request(url, headers=get_headers, method='GET')
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                return True, response.status
        except Exception:
            try:
                # 3. Fallback to GET without Range (some servers reject Range)
                req = urllib.request.Request(url, headers=headers, method='GET')
                with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                    return True, response.status
            except urllib.error.HTTPError as e:
                # Accept 401/403 as valid (resource exists but is protected/login required)
                if e.code in [401, 403]:
                    return True, e.code
                return False, e.code
            except Exception as e:
                return False, str(e)

def check_links(csv_paths: list[str]):
    """Check links in the provided CSV files."""
    has_errors = False
    link_report = []
    
    for path in csv_paths:
        file_path = Path(path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            continue
            
        logger.info(f"Checking file: {file_path}")
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            continue
        
        if 'asset_links' not in df.columns:
            logger.warning(f"'asset_links' column missing in {file_path}")
            continue
            
        for idx, row in df.iterrows():
            asset_links = row['asset_links']
            
            # Skip if empty or NaN
            if pd.isna(asset_links) or str(asset_links).strip() == "":
                continue
                
            # Handle space separator
            links = str(asset_links).split()
            
            for link in links:
                if not link:
                    continue
                    
                success, status = check_url(link)
                item_title = row.get('title_item', f'Row {idx + 2}')
                data_overview = row.get('data_overview_link', None)

                if success:
                    continue

                has_errors = True
                logger.error(f"Broken link in '{item_title}': {link} (Status: {status})")
                link_report.append({
                    'file': str(path),
                    'row_number': idx + 2,
                    'title_item': item_title,
                    'data_overview_link': data_overview,
                    'link': link,
                    'status': str(status),
                    'success': success
                    })

    num_broken_links = sum(not item['success'] for item in link_report)
    if num_broken_links > 0:
        pd.DataFrame(link_report).to_csv("csv/link_report.csv", index=False)
        logger.info("Full link report saved to 'csv/link_report.csv'.")
        logger.info(f"Number of broken links: {num_broken_links}")
    else:
        logger.info("All CSVs are valid: no broken links found.")

    if has_errors:
        sys.exit(1)

if __name__ == "__main__":
    # Default paths based on project structure 
    paths = ['csv/hazard.csv', 'csv/expvul.csv']
    check_links(paths)
