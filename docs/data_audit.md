# Data audit

## Verified from the dataset landing page
| Item | Value |
|---|---|
| Dataset | Retail Transactions and Stocks Data |
| Files | `retail_inventory_ml_apl.csv`; `retail_sales_ml_apl.csv` |
| File sizes | 95.4 MB; 37.3 MB |
| Frequency described | Daily |
| Stores | 40 |
| SKUs | 2,326 |
| Divisions | 3 |
| Product hierarchy | Division → Category → Subcategory → Segment |

## Pending CSV inspection
- Actual column names and data types
- Full date range and missing dates
- Sales and inventory units/definitions
- Store-SKU-date grain and duplicate keys
- Join coverage between sales and inventory
- Actual hierarchy values and category-level coverage
- Whether inventory values are end-of-day snapshots, point-in-time balances or another measure

Do not report these as verified until the two CSV files have been downloaded and profiled.
