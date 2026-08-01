
# Data Fetch Pipeline for HKInformation
#
# data.gov.hk status:
# - Main website: REACHABLE (200 OK)
# - API Gateway (api.data.gov.hk): REACHABLE (needs API key)
# - CKAN legacy API (api/3/action): DEPRECATED (404)
# - Direct RVD Excel: BLOCKED by WAF from this server
#
# How to set up:
# 1. Go to https://data.gov.hk/en/help/api
# 2. Register free account -> get API key
# 3. Store as GitHub Secret: DATA_GOV_HK_KEY
#
# API endpoints available:
# - Catalog search: GET /v1/catalog?q=xxx
# - Dataset detail: GET /v1/catalog/{id}
# - Data download: GET /v1/catalog/{id}/data
#
# Known dataset IDs to search:
# - hk-rvd-property-price-index (RVD)
# - hk-rvd-rental-indexes (RVD)
# - hk-censtatd-median-domestic-household-income (C&SD)
# - hk-housing-authority-public-rental-housing (HA)
#
# Google integrations (2026-08):
# - AdSense: ca-pub-0408433589148621, ads.txt served at https://hinfok.com/ads.txt
# - Analytics: site.googleAnalyticsId in src/data/config.json (398765735 -> UA-398765735-1)
# - Search Console: seo.googleSiteVerification = GgeGOetKECwe-jEZFjXPgZX1AMmV-ZlFTXDGkbLNiGs
#
# GitHub repos with HK gov data tools:
# - mcp-open-data-hk/mcp-open-data-hk (MCP server)
# - JMSCHKU/HKOpenGovData (HKU project)
# - DemChing/hkopendata (Python package)
