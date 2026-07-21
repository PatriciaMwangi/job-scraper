#!/bin/bash
cd /opt/lampp/htdocs/data-analysis
source /opt/lampp/htdocs/env/bin/activate
python scrape.py >> /opt/lampp/htdocs/data-analysis/scrape.log 2>&1

chmod +x /opt/lampp/htdocs/data-analysis/run_scrape.sh

