# Business case: WinMart+ inspired retail replenishment

## Context
Use a convenience-store / small-format grocery retailer as the operating context. The case is inspired by WinMart+, but the analysis uses a third-party public retail dataset. Do not describe it as WinMart internal data.

## Decision problem
A retail operations planner must decide when and how much to replenish a product group across stores. Excess ordering raises average inventory and holding cost; insufficient ordering increases stockout exposure and lost-sales risk. A forecast is useful only when translated into inventory decisions and tested against service and cost outcomes.

## Objective
Build an auditable forecasting-to-replenishment workflow, represent demand uncertainty, and test inventory policies against an initial target service level of 95%. This target is a project design choice, not a claim about WinMart's actual KPI.

## Assumptions to validate
- Analyse demand at store × SKU × day before aggregating to product group/week.
- Treat on-hand inventory as a stock snapshot only after confirming its timestamp and definition.
- Supplier lead time, ordering cost, holding cost and shortage cost are scenario parameters unless found in source data.
- Sales are not automatically equal to unconstrained demand; sales can be censored when inventory is unavailable.
- Tune policies on training/validation data and evaluate on held-out periods.

## Intended output
A product-group policy table with demand profile, forecast, forecast error, lead-time demand distribution, safety stock, reorder point, order quantity/order-up-to level, simulated fill rate, average inventory and estimated total cost.