# ai-marketing-analytics-dashboard

## Overview
This project is my high school passion project where I built an AI-powered marketing analytics dashboard. I take real ad campaign data from a CSV file, store it in a PostgreSQL database, analyze it in a Metabase dashboard, and use a Python machine learning model to predict how well ads will perform (revenue and ROAS).

## What this project does
- Stores ad performance data in a proper database (PostgreSQL) instead of just a spreadsheet.
- Shows key marketing metrics like spend, impressions, CTR, CPC, CPM, and ROAS in an interactive dashboard.
- Uses a machine learning model (scikit-learn) to predict future purchases conversion value and ROAS.
- Saves the predictions back into the database so the dashboard can show actual vs predicted results together.

## Tech Stack
- **Database:** PostgreSQL (hosted on a free cloud service)
- **Dashboard:** Metabase
- **Language:** Python 3
- **Libraries:** pandas, scikit-learn, psycopg2
- **Data:** CSV export of ad performance (campaigns, ad sets, and ads)

## Data (example columns)
The main table is called `ad_performance` and includes columns like:

- `campaign_name`, `ad_set_name`, `ad_name`
- `amount_spent_usd`, `purchase_roas`
- `ctr`, `cpc`, `cpm`
- `impressions`, `reach`, `link_clicks`
- `adds_to_cart`, `purchases_conversion_value`
- Video metrics such as `video_plays_50`, `video_plays_100`, `thruplays`
- Prediction columns: `predicted_purchases_value`, `predicted_roas`

(I converted the original CSV headers to snake_case for the database.)

## How it works (high-level)

1. **Load data into PostgreSQL**
   - I start with a CSV file that has ad performance data.
   - I create a table called `ad_performance` in PostgreSQL and import the CSV so I can query it with SQL.

2. **Build the dashboard in Metabase**
   - I connect Metabase to the PostgreSQL database.
   - I create questions and dashboards that show:
     - Overall KPIs: total spend, total purchases conversion value, overall ROAS, CTR.
     - Charts by campaign and ad: ROAS, CPC, CPM, CTR, frequency, etc.
     - Tables where I can compare different ads and campaigns.

3. **Train the machine learning model in Python**
   - I use Python and pandas to read the data from PostgreSQL.
   - I pick features like spend, impressions, reach, CTR, CPC, CPM, link clicks, and video plays.
   - I train a regression model (for example, RandomForestRegressor from scikit-learn) to predict `purchases_conversion_value`.
   - I then calculate `predicted_roas = predicted_purchases_value / amount_spent_usd`.

4. **Write predictions back to the database**
   - After the model makes predictions for each row, I update the `ad_performance` table with the new columns `predicted_purchases_value` and `predicted_roas`.
   - This lets the dashboard display actual vs predicted performance.

5. **Visualize actual vs predicted**
   - In Metabase, I create charts that compare actual ROAS to predicted ROAS by campaign or ad.
   - I also build tables that show the difference between actual and predicted values so I can see how well the model is doing.

## Project structure (planned)
- `sql/schema.sql` – SQL to create the `ad_performance` table (and add prediction columns).
- `train_and_update_predictions.py` – Python script to train the model and update predictions in the database.
- `requirements.txt` – Python dependencies.
- `screenshots/` – Dashboard screenshots (for documentation and college apps).
- `notebooks/` (optional) – Jupyter notebooks for experiments.

## Why I built this
I’m a 10th grade student interested in data science, machine learning, and marketing. I wanted to create a project that feels like something used in a real company: collecting data, storing it in a database, analyzing it in a dashboard, and using AI to make predictions that can help with decisions like ad budget allocation.
