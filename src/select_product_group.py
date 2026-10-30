"""Rank product groups using observed sales coverage; verify inventory coverage separately."""
from __future__ import annotations
import argparse,re
from pathlib import Path
import pandas as pd
def norm(x:str)->str:return re.sub(r"[^a-z0-9]+","_",x.lower()).strip("_")
def find_col(cols:list[str],aliases:list[str])->str|None:
 d={norm(c):c for c in cols};return next((d[a] for a in aliases if a in d),None)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--sales",type=Path,required=True);p.add_argument("--group-col",required=True);p.add_argument("--out",type=Path,default=Path("reports/product_group_candidates.csv"));a=p.parse_args()
 if not a.sales.exists():raise FileNotFoundError(a.sales)
 cols=list(pd.read_csv(a.sales,nrows=0).columns)
 if a.group_col not in cols:raise ValueError(f"{a.group_col!r} not found; available columns: {cols}")
 sku=find_col(cols,["sku","sku_id","item","item_id","item_nbr","product_id","barcode"]);store=find_col(cols,["store","store_id","store_code","store_nbr","shop_id","branch_id"]);date=find_col(cols,["date","sales_date","transaction_date","business_date","datetime","timestamp"]);qty=find_col(cols,["sales_qty","quantity_sold","qty_sold","units_sold","unit_sales","quantity","qty","units"])
 use=[a.group_col]+[c for c in [sku,store,date,qty] if c and c!=a.group_col];df=pd.read_csv(a.sales,usecols=use,low_memory=False)
 if date:df[date]=pd.to_datetime(df[date],errors="coerce")
 if qty:df[qty]=pd.to_numeric(df[qty],errors="coerce")
 ag={"records":(a.group_col,"size")}
 if sku:ag["unique_skus"]=(sku,"nunique")
 if store:ag["unique_stores"]=(store,"nunique")
 if date:ag["unique_dates"]=(date,"nunique")
 if qty:ag["total_sales_qty"]=(qty,"sum");ag["mean_sales_qty"]=(qty,"mean");ag["zero_or_negative_qty_share"]=(qty,lambda x:float((x.fillna(0)<=0).mean()))
 out=df.groupby(a.group_col,dropna=False).agg(**ag).reset_index();terms=[out[c].rank(pct=True) for c in ["unique_dates","unique_stores","unique_skus"] if c in out]
 if terms:out["coverage_score"]=sum(terms)/len(terms);out=out.sort_values(["coverage_score","records"],ascending=False)
 a.out.parent.mkdir(parents=True,exist_ok=True);out.to_csv(a.out,index=False);print(out.head(15).to_string(index=False));print(f"Saved: {a.out.resolve()}");print("Validate inventory coverage and stock field semantics before selecting a group.")
if __name__=="__main__":main()
