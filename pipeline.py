import pandas as pd
import requests
import io
import psycopg2
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kobo credentials
KUBO_USERNAME = os.getenv("KUBO_USERNAME")
KUBO_PASSWORD = os.getenv("KUBO_PASSWORD")
KUBO_CSV_URL = "https://kf.kobotoolbox.org/api/v2/assets/aCEjw8JUqyzrEZW4Vhhv85/export-settings/esE9u8dmcv6QSHFSRkeajGH/data.csv"

# PostgreSQL credentials
PG_HOST = os.getenv("PG_HOST")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = os.getenv("PG_PORT")

SCHEMA_NAME = "product_collection"
TABLE_NAME = "product_data"

print("Fetching data from Kobo...")

# Fetch CSV
response = requests.get(KUBO_CSV_URL, auth=HTTPBasicAuth(KUBO_USERNAME, KUBO_PASSWORD))

if response.status_code == 200:
    print("✅ Data fetched successfully.")

    csv_data = io.StringIO(response.text)

    # Detect separator
    sample = response.text[:1000]
    sep = ";" if sample.count(";") > sample.count(",") else ","

    df = pd.read_csv(csv_data, sep=sep, on_bad_lines="skip")

    # Normalize columns: lowercase + safe names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("&", "and")
        .str.replace("-", "_")
    )

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # ---- Force phone numbers as string and preserve leading zeros ----
    if "phone" in df.columns:
        df["phone"] = df["phone"].astype(str).str.strip()
        df["phone"] = df["phone"].apply(lambda x: x.zfill(9) if x.isdigit() else x)
    else:
        df["phone"] = ""

    print("Cleaned columns:", df.columns.tolist())

    # ---- Handle dynamic column names ----
    if "stock_on_hand" not in df.columns:
        for col in df.columns:
            if col.startswith("stock_on_hand"):
                df.rename(columns={col: "stock_on_hand"}, inplace=True)
                break
        if "stock_on_hand" not in df.columns:
            df["stock_on_hand"] = 0

    if "price" not in df.columns:
        for col in df.columns:
            if col.startswith("price") or "unit_price" in col:
                df.rename(columns={col: "price"}, inplace=True)
                break
        if "price" not in df.columns:
            df["price"] = 0

    if "estimated_weekly_sales" not in df.columns:
        for col in df.columns:
            if col.startswith("estimated_weekly_sales"):
                df.rename(columns={col: "estimated_weekly_sales"}, inplace=True)
                break
        if "estimated_weekly_sales" not in df.columns:
            df["estimated_weekly_sales"] = 0

    # Force numeric conversions
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["estimated_weekly_sales"] = pd.to_numeric(df["estimated_weekly_sales"], errors="coerce").fillna(0)
    df["stock_on_hand"] = pd.to_numeric(df["stock_on_hand"], errors="coerce").fillna(0).astype(int)

    # Calculate total sales
    df["total_sales"] = df["price"] * df["estimated_weekly_sales"]

    # Fix date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    print("Loading data into PostgreSQL...")

    conn = psycopg2.connect(
        host=PG_HOST,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        port=PG_PORT
    )
    cur = conn.cursor()

    # Create schema/table
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
    cur.execute(f"DROP TABLE IF EXISTS {SCHEMA_NAME}.{TABLE_NAME};")

    cur.execute(f"""
    CREATE TABLE {SCHEMA_NAME}.{TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        start TIMESTAMP,
        end_time TIMESTAMP,
        date DATE,
        outlet_code TEXT,
        outlet_name TEXT,
        province TEXT,
        outlet_type TEXT,
        contact_name TEXT,
        phone TEXT,
        product TEXT,
        address TEXT,
        sku_code TEXT,
        availability TEXT,
        price FLOAT,
        stock_on_hand INT,
        facing_count INT,
        posm_available TEXT,
        posm_condition TEXT,
        competitor TEXT,
        competitor_price FLOAT,
        competitor_promotion TEXT,
        sales_trend TEXT,
        estimated_weekly_sales FLOAT,
        satisfaction_score INT,
        issue_flag TEXT,
        feedback TEXT,
        total_sales FLOAT
    );
    """)

    insert_query = f"""
    INSERT INTO {SCHEMA_NAME}.{TABLE_NAME} (
        start, end_time, date, outlet_code, outlet_name, province, outlet_type,
        contact_name, phone, product, address, sku_code, availability,
        price, stock_on_hand, facing_count, posm_available, posm_condition,
        competitor, competitor_price, competitor_promotion, sales_trend,
        estimated_weekly_sales, satisfaction_score, issue_flag, feedback,
        total_sales
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """

    for _, row in df.iterrows():
        cur.execute(insert_query, (
            row.get("start"),
            row.get("end"),
            row.get("date"),
            row.get("outlet_code"),
            row.get("outlet_name"),
            row.get("province"),
            row.get("outlet_type"),
            row.get("contact_name"),
            row.get("phone"),
            row.get("product"),
            row.get("address"),
            row.get("sku_code"),
            row.get("availability"),
            row.get("price"),
            row.get("stock_on_hand"),
            row.get("facing_count"),
            row.get("posm_available"),
            row.get("posm_condition"),
            row.get("competitor"),
            row.get("competitor_price"),
            row.get("competitor_promotion"),
            row.get("sales_trend"),
            row.get("estimated_weekly_sales"),
            row.get("satisfaction_score"),
            row.get("issue_flag"),
            row.get("feedback"),
            row.get("total_sales")
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Data loaded into PostgreSQL successfully!")

else:
    print(f"❌ Error fetching data: {response.status_code}")
