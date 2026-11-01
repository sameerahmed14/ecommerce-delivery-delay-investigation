from pathlib import Path
import subprocess
import sys
import pandas as pd
import pytest
from delivery_investigation.pipeline import load_csvs, build_fact_orders
from delivery_investigation.analysis import analyze

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / 'data' / 'sample'


def _fixture():
    subprocess.check_call([sys.executable, str(ROOT / 'scripts' / 'create_demo_data.py')])
    return load_csvs(DEMO)


def test_one_order_grain_and_sla_clock_time_boundary():
    fact,audit=build_fact_orders(_fixture())
    assert len(fact)==6 and fact['order_id'].is_unique
    by=fact.set_index('order_id')
    # delivered at 20:30 on promised date: on time despite midnight promise timestamp
    assert by.loc['o1','is_late']==0 and by.loc['o1','is_on_time']==1
    assert by.loc['o2','is_late']==1 and by.loc['o2','late_days']==3
    assert by.loc['o4','seller_count']==2
    assert pd.isna(by.loc['o4','single_seller_id'])
    assert by.loc['o4','review_count']==2
    assert by.loc['o4','review_score_mean']==3
    assert by.loc['o5','eligible_sla']==0
    assert by.loc['o6','eligible_sla']==0  # timestamp impossibility
    assert audit['eligible_delivered_orders']==4
    assert audit['late_orders']==2
    assert audit['orders_with_bad_stage_sequence']>=1


def test_review_join_never_duplicates_orders():
    fact,_=build_fact_orders(_fixture())
    result=analyze(fact,min_group_size=1)
    assert result['summary']['eligible_delivered_orders']==4
    assert result['summary']['late_rate_pct']==50.0
    assert len(result['monthly'])==2
    assert result['reviews']['orders_with_reviews'].sum()==4


def test_missing_file_is_descriptive(tmp_path):
    with pytest.raises(FileNotFoundError, match='Missing Olist CSVs'):
        load_csvs(tmp_path)


def test_duplicate_order_key_rejected():
    frames=_fixture()
    frames['orders']=pd.concat([frames['orders'],frames['orders'].iloc[[0]]], ignore_index=True)
    # Main loading detects source duplicates. Data-joining also protects grain.
    with pytest.raises(Exception):
        build_fact_orders(frames)
