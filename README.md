# product_collection-
Data Pipeline from KoboToolbox to PostgreSQL using Python

Analyst Sale Performance of Khmer Beverages – Project Overview
1. Project Objective

The primary goal of this project is to analyze and evaluate the sales performance of Khmer beverages across different outlets and provinces. The analysis aims to provide insights into product performance, market trends, stock management, pricing, and customer satisfaction. These insights can help businesses make data-driven decisions to increase sales, optimize inventory, and enhance customer satisfaction.

2. Data Source

The data is collected via surveys conducted on KoboToolbox.

KoboToolbox is a robust platform for collecting field data through mobile and web forms.

Data input was done manually by the project owner during field surveys.

The dataset includes detailed product-level information from various retail outlets across Cambodia.

3. Key Metrics Analyzed

The project focuses on analyzing key metrics that determine sales performance:

Total Sales: Overall revenue generated per product and per province.

Stock Management: Inventory levels and stock movement trends.

Product Availability: Assessment of products’ presence in outlets.

Pricing Analysis: Comparison of pricing between products and competitors.

Customer Satisfaction: Average satisfaction score per product to understand customer preferences.

Competitor Insights: Promotions and pricing strategies to evaluate market competitiveness.

4. Methodology

The analysis is performed using Python with the following steps:

Data Extraction: Connect to PostgreSQL database to retrieve the product_data table.

Data Cleaning: Convert numeric fields to correct types, handle missing values, and standardize text fields.

Data Aggregation: Summarize sales by product, province, and outlet type.

Visualization: Generate charts for better understanding of trends, including:

Bar charts for top products and provinces

Pie charts for sales proportion

Column charts for satisfaction score comparison

Area charts for stock vs sales trends

Insights Generation: Identify top-performing products, provinces with high sales, underperforming outlets, and stock-related issues.

5. Expected Outcomes

By completing this analysis, the project provides:

Identification of top-selling products and their contribution to overall revenue.

Recognition of key provinces or regions driving sales.

Insights into stock and inventory management for better supply planning.

Understanding of customer preferences through satisfaction scores.

Competitive intelligence on pricing and promotions.

6. Tools & Technologies

Database: PostgreSQL for storing and querying sales data.

Data Analysis: Python (Pandas, NumPy) for data manipulation.

Visualization: Matplotlib and Seaborn for generating charts and graphs.

Environment: Jupyter Notebook for interactive analysis and reporting.

7. Conclusion

This project provides a comprehensive overview of the sales performance of Khmer beverages, enabling decision-makers to optimize product placement, pricing, and inventory. The visualizations and metrics generated serve as actionable insights to improve sales efficiency and market competitiveness.

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
