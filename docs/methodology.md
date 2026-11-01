# Analytical Methodology

## Dataset
Olist Brazilian E-Commerce Public Dataset:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Tools
- Python and pandas for data preparation
- SQLite and SQL for analytical queries
- Power BI for planned reporting
- pytest for automated pipeline testing
- Git and GitHub for version control

## Unit of Analysis
One order, represented by order_id.

## Eligibility
The pipeline defines eligible_sla. KPI denominators include only eligible delivered orders with valid dates.

## Core Metrics
Late rate = late eligible orders / eligible delivered orders * 100.

An order is late if its actual delivery calendar date is after its estimated delivery calendar date.

Severe delay = more than seven calendar days after the estimated delivery date.

Order month refers to purchase month, not delivery month.

## Statistical Approach
- Counts and percentages
- Median delivery-stage durations
- Monthly and regional segmentation
- 90th percentile of actual delivery duration
- Comparisons of promised and actual delivery windows

## Quality Checks
- Four automated tests passed.
- Late classification independently validated.
- 6,534 late records matched with zero mismatches.

## Interpretation
Associations must not be presented as proven causes.
Sample sizes, missing timestamps and data quality exclusions must be disclosed.

## Reproducibility
Raw CSV files are downloaded separately from Kaggle.
Run the project's existing pipeline to generate analytical outputs.
