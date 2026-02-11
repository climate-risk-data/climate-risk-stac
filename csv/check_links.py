"""Check validity of URLs in CSV files."""

import logging
import sys
from pathlib import Path
import pandas as pd
import urllib.request
import urllib.error

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("link_checker")

def check_url(url: str) -> tuple[bool, str | int]:
    """Check if a URL is reachable."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as response:
            return True, response.status
    except urllib.error.HTTPError:
        try:
            get_headers = headers.copy()
            get_headers['Range'] = 'bytes=0-10'
            req = urllib.request.Request(url, headers=get_headers, method='GET')
            with urllib.request.urlopen(req, timeout=10) as response:
                return True, response.status
        except urllib.error.HTTPError as e:
            return False, e.code
        except Exception as e:
            return False, str(e)
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
            links = [link.strip() for link in str(asset_links).split(' ')]
            
            for link in links:
                if not link:
                    continue
                    
                success, status = check_url(link)
                item_title = row.get('title_item', f'Row {idx + 2}')

                if not success:
                    has_errors = True
                    logger.error(f"Broken link in '{item_title}': {link} (Status: {status})")
                
                link_report.append({
                    'file': str(path),
                    'row_number': idx + 2,
                    'title_item': item_title,
                    'link': link,
                    'status': str(status),
                    'success': success
                })

    if link_report:
        pd.DataFrame(link_report).to_csv("link_report.csv", index=False)
        logger.info("Full link report saved to 'link_report.csv'.")

    if has_errors:
        sys.exit(1)
    else:
        logger.info("All links checked successfully.")

if __name__ == "__main__":
    # Default paths based on project structure
    paths = ['csv/hazard.csv', 'csv/expvul.csv']
    check_links(paths)
