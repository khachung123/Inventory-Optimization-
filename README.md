# Forecast-Driven Inventory Optimization System

A portfolio case study linking retail demand forecasting with inventory policy design and simulation. The business context is **WinMart+ inspired**, but the public dataset is third-party retail data and is **not WinMart's proprietary data**.

## Project status
- [x] Candidate dataset selected: Mendeley Data, *Retail Transactions and Stocks Data*.
- [x] Dataset metadata checked: two CSV files, daily sales and on-hand inventory, 40 stores, 2,326 SKUs, three divisions, four-level product hierarchy.
- [ ] Download both CSV files and place them in `data/raw/`.
- [ ] Run schema profiling to create the actual data dictionary.
- [ ] Confirm date coverage, join grain, field meaning and product hierarchy values.
- [ ] Select a product group using observed coverage and demand quality.
- [ ] Build forecast, uncertainty simulation and inventory policy model.

**Do not assume column names, date range, units, or category values until the downloaded CSVs have been audited.**

## Dataset
Source: [Retail Transactions and Stocks Data — Mendeley Data](https://data.mendeley.com/datasets/27x8mjm8k4/1)  
DOI: `10.17632/27x8mjm8k4.1` · Licence: CC BY 4.0.

Download `retail_sales_ml_apl.csv` and `retail_inventory_ml_apl.csv` from the source page and place them in `data/raw/`. Raw data is excluded from Git because of file size and third-party licensing.

## Quick start
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/audit_dataset.py --sales data/raw/retail_sales_ml_apl.csv --inventory data/raw/retail_inventory_ml_apl.csv --out reports/data_audit
```

After reviewing the actual hierarchy column:
```bash
python src/select_product_group.py --sales data/raw/retail_sales_ml_apl.csv --group-col <actual_category_column> --out reports/product_group_candidates.csv
```

## Workflow
1. Audit CSV schemas, date coverage, key grain, duplicates and sales/inventory overlap.
2. Validate the store × SKU × date join semantics before merging.
3. Select a product group based on coverage, demand continuity and inventory observability.
4. Aggregate demand to weekly frequency and create time-based train/validation/test splits.
5. Compare Seasonal Naive and moving-average baselines; evaluate SARIMAX if justified.
6. Model forecast uncertainty and generate Monte Carlo demand paths.
7. Define lead-time and cost assumptions transparently; calculate safety stock, reorder point and order quantity/order-up-to level.
8. Validate inventory policies on held-out periods and report fill rate, stockout rate, average inventory and total cost.
9. Present decision-oriented results in Power BI.

## Important limitations
The public dataset description does not establish supplier lead times, purchase-order timing, unit costs, selling prices, replenishment constraints, or whether observed sales are censored by stockouts. These must be verified or introduced as clearly labelled scenario assumptions. A stock snapshot is not automatically equivalent to available-to-promise inventory.

This is an educational portfolio simulation, not a production replenishment system.
