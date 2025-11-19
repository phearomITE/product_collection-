# product_collection-
Data Pipeline from KoboToolbox to PostgreSQL using Python

# Khmer Beverages Sales Performance Pipeline

This project automates the collection, cleaning, and loading of **Khmer beverages sales and stock data** from KoboToolbox into PostgreSQL for performance analysis. It is designed to support data-driven decision-making for sales, distribution, and market intelligence.

---

## **Project Overview**

**Goal:**  
To build an automated pipeline that extracts sales and product data from KoboToolbox, cleans and processes the data, and stores it in a PostgreSQL database for analysis and reporting.

**Scope:**  
- Data collection from multiple retail outlets and distributors of Khmer beverages (Chip Mong company products).  
- Data includes outlet information, product stock, price, sales trends, and promotional information.  
- Clean numeric and textual data to ensure accuracy in PostgreSQL.  
- Support dashboards or reports for sales performance, stock levels, and trends.

---

## **Technologies Used**

- Python 3.x  
- Pandas for data manipulation  
- Requests for fetching KoboToolbox CSV data  
- Psycopg2 for PostgreSQL integration  
- PostgreSQL as the database  
- dotenv for managing credentials  
- Git & GitHub for version control

---

## **Data Pipeline Process**

### 1. Fetch Data from KoboToolbox
- Connects to the KoboToolbox API using credentials stored in `.env`.
- Downloads CSV export of Khmer beverages product data.
- Detects CSV separator automatically (comma or semicolon).

### 2. Clean & Normalize Data
- Normalizes column names (lowercase, remove spaces/special characters).
- Removes duplicate columns.
- Cleans numeric columns (`stock_on_hand`, `price`, `estimated_weekly_sales`, etc.) using `clean_numeric` function.
- Converts floats and integers safely for PostgreSQL.
- Converts `date` fields to datetime format.
- Handles phone numbers, ensuring consistent formatting.

### 3. Transform Data
- Calculates **Total Sales** per product:  
  `Total_Sales = Price * Estimated_Weekly_Sales`
- Ensures integer fields are correctly converted and do not store `NULL` incorrectly.

### 4. Load into PostgreSQL
- Connects to PostgreSQL using credentials in `.env`.
- Creates a dedicated schema: `product_collection`.
- Creates a table `product_data` with columns for all collected data.
- Inserts cleaned data row by row.
- Commits the transaction and closes the connection.

### 5. Output
- Data stored in PostgreSQL for further analysis.
- Tables include all key performance metrics: stock, sales, prices, and trends.

---

## **Database Table Structure**

| Column                     | Type      | Description                                      |
|----------------------------|-----------|-------------------------------------------------|
| id                         | SERIAL    | Primary key                                     |
| start, end_time            | TIMESTAMP | Kobo survey timestamps                          |
| date                       | DATE      | Survey date                                     |
| outlet_code, outlet_name   | TEXT      | Outlet identification                           |
| province, outlet_type      | TEXT      | Location and type of outlet                     |
| contact_name, phone        | TEXT      | Contact information                             |
| product, sku_code          | TEXT      | Product identification                          |
| availability, price        | FLOAT     | Product availability and price                  |
| stock_on_hand              | INT       | Product stock at the outlet                     |
| facing_count               | INT       | Number of facings (shelves)                    |
| posm_available, posm_condition | TEXT | POS materials availability and condition       |
| competitor, competitor_price, competitor_promotion | TEXT/FLOAT | Competitor product info |
| sales_trend                | TEXT      | Trend of product sales                          |
| estimated_weekly_sales     | FLOAT     | Estimated weekly sales                          |
| satisfaction_score         | INT       | Customer satisfaction score (1-10)             |
| issue_flag, feedback       | TEXT      | Observed issues and feedback                    |
| total_sales                | FLOAT     | Calculated total sales                          |

---
