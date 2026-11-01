"""Create TINY SYNTHETIC data to verify pipeline functionality - NOT real Olist observations."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1] / "data" / "sample"
BASE.mkdir(parents=True, exist_ok=True)

# Six orders: on-time, late, date-time boundary, multi-seller, canceled, and invalid chronology.
orders = [
 ("o1","c1","delivered","2018-01-01 12:00:00","2018-01-01 13:00:00","2018-01-02 10:00:00","2018-01-05 20:30:00","2018-01-05 00:00:00"),
 ("o2","c2","delivered","2018-01-03 09:00:00","2018-01-03 10:00:00","2018-01-04 10:00:00","2018-01-12 18:00:00","2018-01-09 00:00:00"),
 ("o3","c3","delivered","2018-02-01 09:00:00","2018-02-01 11:00:00","2018-02-02 10:00:00","2018-02-05 11:00:00","2018-02-06 00:00:00"),
 ("o4","c4","delivered","2018-02-02 09:00:00","2018-02-02 10:00:00","2018-02-04 10:00:00","2018-02-10 18:00:00","2018-02-08 00:00:00"),
 ("o5","c5","canceled","2018-03-02 09:00:00",None,None,None,"2018-03-08 00:00:00"),
 ("o6","c6","delivered","2018-03-05 09:00:00","2018-03-05 10:00:00","2018-03-04 10:00:00","2018-03-03 10:00:00","2018-03-10 00:00:00"),
]
ordercols = ["order_id","customer_id","order_status","order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]
pd.DataFrame(orders,columns=ordercols).to_csv(BASE/'olist_orders_dataset.csv',index=False)
pd.DataFrame([(f'c{i}',f'u{i}','01001','City','SP' if i<4 else 'RJ') for i in range(1,7)],
 columns=['customer_id','customer_unique_id','customer_zip_code_prefix','customer_city','customer_state']).to_csv(BASE/'olist_customers_dataset.csv',index=False)
pd.DataFrame([
 ('o1',1,'p1','s1','2018-01-03',30,5),('o2',1,'p2','s1','2018-01-04',55,6),
 ('o3',1,'p3','s2','2018-02-03',10,3),('o4',1,'p4','s1','2018-02-05',35,5),
 ('o4',2,'p5','s2','2018-02-05',40,4),('o5',1,'p6','s1','2018-03-04',21,7),
 ('o6',1,'p7','s2','2018-03-06',22,3)],
 columns=['order_id','order_item_id','product_id','seller_id','shipping_limit_date','price','freight_value']).to_csv(BASE/'olist_order_items_dataset.csv',index=False)
pd.DataFrame([('s1','01001','City','SP'),('s2','01002','City','RJ')],
 columns=['seller_id','seller_zip_code_prefix','seller_city','seller_state']).to_csv(BASE/'olist_sellers_dataset.csv',index=False)
pd.DataFrame([
 ('r1','o1',5),('r2','o2',1),('r3','o3',4),('r4','o4',2),('r5','o4',4),('r6','o6',5)],
 columns=['review_id','order_id','review_score']).to_csv(BASE/'olist_order_reviews_dataset.csv',index=False)
(BASE/'README_DEMO_DATA.txt').write_text('SYNTHETIC DEMONSTRATION ONLY. Six invented orders to exercise testing and CLI. Never report these metrics as Olist findings.\n')
print('Created synthetic test fixture in',BASE)
