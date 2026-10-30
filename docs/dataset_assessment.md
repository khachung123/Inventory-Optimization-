# Dataset assessment

## Selected source
- Title: Retail Transactions and Stocks Data
- Publisher: Mendeley Data
- DOI: `10.17632/27x8mjm8k4.1`
- Version 1; published 27 April 2026
- Files listed: `retail_inventory_ml_apl.csv` (95.4 MB), `retail_sales_ml_apl.csv` (37.3 MB)
- Description: daily transaction-level sales and SKU on-hand inventory from 40 retail storefronts and 2,326 SKUs across three divisions.
- Product hierarchy: Division → Category → Subcategory → Segment
- Licence shown: CC BY 4.0

Source page: https://data.mendeley.com/datasets/27x8mjm8k4/1

## Why selected
It is a better fit for an end-to-end forecasting-to-inventory project than a sales-only dataset because the description explicitly includes on-hand inventory. Corporación Favorita is a useful forecasting benchmark, but its core competition tables do not provide observed daily on-hand stock.

## Unknowns
The landing page does not expose CSV headers, a separate data dictionary, date range, units, exact join keys, category labels or inventory snapshot semantics. It also does not establish lead times, unit costs, order quantities or stockout flags. Verify these from the downloaded files before modelling.
