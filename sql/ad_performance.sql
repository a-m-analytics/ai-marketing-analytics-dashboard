if exists drop table ad_performance ;

CREATE TABLE ad_performance (
  campaign_name TEXT,
  ad_set_name TEXT,
  ad_name TEXT,
  amount_spent_usd NUMERIC,
  purchase_roas NUMERIC,
  hold_rate NUMERIC,
  hook TEXT,
  ctr NUMERIC,
  attribution_setting TEXT,
  result_type TEXT,
  results NUMERIC,
  impressions NUMERIC,
  reach NUMERIC,
  cost_per_result NUMERIC,
  frequency NUMERIC,
  link_clicks NUMERIC,
  cpc NUMERIC,
  cpm NUMERIC,
  views NUMERIC,
  thruplays NUMERIC,
  adds_to_cart NUMERIC,
  cost_per_add_to_cart NUMERIC,
  avg_purchases_conversion_value NUMERIC,
  purchases_conversion_value NUMERIC,
  cost_per_1000_accounts_reached NUMERIC,
  video_plays_50 NUMERIC,
  video_plays_100 NUMERIC,
  reporting_starts DATE,
  reporting_ends DATE
);

-- import data into table from csv using import wizard

-- explore data
select count(*) from ad_performance ap ;

SELECT campaign_name, amount_spent_usd, purchases_conversion_value
FROM ad_performance
LIMIT 10;

select * from ad_performance ;

-- clean up rows where ad_name and ad_set_name = 'All'
delete from ad_performance where ad_set_name ='All';
delete from ad_performance where ad_name ='All';

-- create a id column as a unique identifier to match the machine learning predictions from the py code
-- Add ID column if it doesn't exist (running numbers 1, 2, 3...)
ALTER TABLE ad_performance 
ADD COLUMN IF NOT EXISTS id INTEGER;

-- Update the table to fill ID column with sequential numbers 1-N
WITH numbered_rows AS (
  SELECT 
    ctid,
    row_number() OVER (ORDER BY (SELECT NULL)) as row_num
  FROM ad_performance
)
UPDATE ad_performance 
SET id = nr.row_num
FROM numbered_rows nr
WHERE ad_performance.ctid = nr.ctid;
