#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pandas scikit-learn psycopg2-binary


# In[2]:


import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


# In[3]:


DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "marketing_analytics"   # change if yours is different
DB_USER = "postgres"              # your Postgres user
DB_PASSWORD = "postgres"     # your Postgres password


# In[4]:


def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# In[5]:


conn = get_conn()

query = """
SELECT
    id,
    amount_spent_usd,
    impressions,
    reach,
    ctr,
    cpc,
    cpm,
    frequency,
    link_clicks,
    adds_to_cart,
    views,
    thruplays,
    video_plays_50,
    video_plays_100,
    purchases_conversion_value
FROM ad_performance
WHERE amount_spent_usd IS NOT NULL
  AND purchases_conversion_value IS NOT NULL
"""

df = pd.read_sql(query, conn)
conn.close()

df.head(10)


# In[6]:


feature_cols = [
    "amount_spent_usd",
    "impressions",
    "reach",
    "ctr",
    "cpc",
    "cpm",
    "frequency",
    "link_clicks",
    "adds_to_cart",
    "views",
    "thruplays",
    "video_plays_50",
    "video_plays_100",
]

X = df[feature_cols].fillna(0)
y = df["purchases_conversion_value"]


# In[7]:


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# In[8]:


model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, X_train.index.to_series()*0 + y_train)  # or simply model.fit(X_train, y_train)


# In[9]:


y_pred = model.predict(X_test)

print("R²:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))


# In[10]:


df["predicted_purchases_value"] = model.predict(X)
df["predicted_roas"] = df["predicted_purchases_value"] / df["amount_spent_usd"].replace(0, 1)


# In[11]:


conn = get_conn()
cur = conn.cursor()

rows = list(
    zip(
        df["predicted_purchases_value"].astype(float),
        df["predicted_roas"].astype(float),
        df["id"].astype(int),
    )
)

sql = """
UPDATE ad_performance
SET predicted_purchases_value = %s,
    predicted_roas = %s
WHERE id = %s
"""

execute_batch(cur, sql, rows, page_size=1000)

conn.commit()
cur.close()
conn.close()


# In[ ]:




