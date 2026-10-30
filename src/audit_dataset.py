"""Profile retail sales and inventory CSVs without assuming their schema."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any
import pandas as pd

ALIASES={"date":["date","sales_date","transaction_date","business_date","snapshot_date","datetime","timestamp","day"],"store":["store","store_id","store_code","store_nbr","shop","shop_id","branch","branch_id","location_id"],"sku":["sku","sku_id","item","item_id","item_nbr","product_id","product_code","barcode","stock_keeping_unit"],"sales_qty":["sales_qty","sale_qty","quantity_sold","qty_sold","units_sold","unit_sales","sales_units","quantity","qty","units"],"on_hand":["on_hand","onhand","on_hand_qty","stock_on_hand","inventory","inventory_qty","stock_qty","closing_stock","quantity_on_hand","stock"]}
HIERARCHY_TERMS=["division","category","subcategory","sub_category","segment","family","product_group","department","class"]
def norm(v:Any)->str:return re.sub(r"[^a-z0-9]+","_",str(v).strip().lower()).strip("_")
def infer_field(cols:list[str],role:str)->str|None:
 n={norm(c):c for c in cols}
 for a in ALIASES[role]:
  if a in n:return n[a]
 tokens={"date":["date","datetime","timestamp"],"store":["store","shop","branch","location"],"sku":["sku","item","product","barcode"],"sales_qty":["sales","quantity","qty","units"],"on_hand":["onhand","inventory","stock"]}[role]
 m=[c for c in cols if any(t in norm(c).split("_") for t in tokens)]
 return m[0] if len(m)==1 else None
def scan_dates(path:Path,col:str)->tuple[str|None,str|None]:
 lo=hi=None
 for ch in pd.read_csv(path,usecols=[col],chunksize=250000,low_memory=False):
  d=pd.to_datetime(ch[col],errors="coerce").dropna()
  if not d.empty:
   a,b=d.min(),d.max();lo=a if lo is None else min(lo,a);hi=b if hi is None else max(hi,b)
 return (str(lo.date()) if lo is not None else None,str(hi.date()) if hi is not None else None)
def keys(path:Path,fields:dict[str,str|None]):
 roles=["date","store","sku"]
 if not all(fields.get(x) for x in roles):return {"available":False},None
 d=pd.read_csv(path,usecols=[fields[x] for x in roles],low_memory=False);d.columns=roles;d["date"]=pd.to_datetime(d.date,errors="coerce").dt.strftime("%Y-%m-%d")
 dup=int(d.duplicated(roles).sum());null=int(d.isna().any(axis=1).sum());u=d.dropna().drop_duplicates()
 return {"available":True,"key_columns":{x:fields[x] for x in roles},"rows":len(d),"null_key_rows":null,"duplicate_key_rows":dup,"unique_keys":len(u)},u
def profile(path:Path,label:str,out:Path)->dict[str,Any]:
 if not path.exists():raise FileNotFoundError(f"Missing {path}; download it from the Mendeley source page.")
 preview=pd.read_csv(path,nrows=20000,low_memory=False);rows=sum(len(c) for c in pd.read_csv(path,chunksize=250000,low_memory=False));fields={r:infer_field(list(preview.columns),r) for r in ALIASES}
 hierarchy=[c for c in preview.columns if any(t in norm(c).split("_") for t in HIERARCHY_TERMS)];records=[]
 for c in preview.columns:
  s=preview[c];records.append({"column":c,"sample_dtype":str(s.dtype),"sample_missing_pct":round(float(s.isna().mean()*100),2),"sample_unique_count":int(s.nunique()),"sample_values":" | ".join(s.dropna().astype(str).drop_duplicates().head(5)),"possible_role":next((r for r,v in fields.items() if v==c),"hierarchy" if c in hierarchy else "unclassified")})
 pd.DataFrame(records).to_csv(out/f"{label}_data_dictionary.csv",index=False);dmin,dmax=scan_dates(path,fields["date"]) if fields["date"] else (None,None);kp,_=keys(path,fields)
 r={"file":str(path),"size_mb":round(path.stat().st_size/1048576,2),"row_count":rows,"columns":list(preview.columns),"inferred_fields":fields,"hierarchy_candidates":hierarchy,"preview_rows":len(preview),"preview_missing_pct":{c:round(float(preview[c].isna().mean()*100),2) for c in preview.columns},"date_min":dmin,"date_max":dmax,"key_profile":kp}
 (out/f"{label}_profile.json").write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding="utf-8");return r
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--sales",type=Path,required=True);p.add_argument("--inventory",type=Path,required=True);p.add_argument("--out",type=Path,default=Path("reports/data_audit"));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 s=profile(a.sales,"sales",a.out);i=profile(a.inventory,"inventory",a.out);sk,sf=keys(a.sales,s["inferred_fields"]);ik,inf=keys(a.inventory,i["inferred_fields"]);j={"available":False}
 if sf is not None and inf is not None:
  m=sf.merge(inf,on=["date","store","sku"],how="inner");j={"available":True,"sales_unique_keys":len(sf),"inventory_unique_keys":len(inf),"matched_keys":len(m),"sales_match_pct":round(100*len(m)/max(len(sf),1),2)}
 lines=["# Automated data audit","","> Inferred fields are provisional; validate business meanings before modelling.","","## Sales",f"- Rows: {s['row_count']:,}",f"- Fields: {s['inferred_fields']}",f"- Date range: {s['date_min']} to {s['date_max']}","","## Inventory",f"- Rows: {i['row_count']:,}",f"- Fields: {i['inferred_fields']}",f"- Date range: {i['date_min']} to {i['date_max']}","","## Key and join check",f"- Sales: {sk}",f"- Inventory: {ik}",f"- Join: {j}","","Matching keys do not prove matching business semantics. Confirm date definitions and aggregate duplicate store-SKU-date rows before joining."]
 (a.out/"audit_summary.md").write_text("\n".join(lines),encoding="utf-8");print(f"Audit written to {a.out.resolve()}");print(j)
if __name__=="__main__":main()
