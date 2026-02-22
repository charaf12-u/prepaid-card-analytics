# 🍔 Prepaid Card Analytics & Restaurant Performance System

## 📌 Project Overview
This project is an end-to-end data analytics system designed for a fast-food chain that uses prepaid customer cards.

The objective is to transform raw transaction data into actionable business insights to support strategic decision-making, operational optimization, and risk detection.

The system covers the full analytics lifecycle:

- Data cleaning and preprocessing
- Feature engineering
- KPI and trend analysis
- Customer behavior analysis
- Restaurant performance evaluation
- Anomaly detection
- Automated reporting

---

## 🎯 Business Objectives

- Identify revenue trends and seasonality
- Detect high-value customers and risky accounts
- Evaluate restaurant and cashier performance
- Detect abnormal transactions and potential fraud
- Optimize staffing during peak hours
- Support data-driven decision-making for management

---

## ⚙️ Data Processing & Preparation

Key preprocessing steps include:

- Date and time standardization
- Missing value handling
- Duplicate removal
- Numeric conversion of transaction amounts
- Feature extraction (year, month, week, hour)
- Data consistency checks

These steps ensure reliable and accurate analytics.

---

## 📊 Analytics & KPIs

### Revenue Analysis
- Daily revenue
- Weekly revenue
- Monthly revenue
- Transaction volume trends

### Prepaid Card Balance Analysis
- Average daily card balance
- Customer recharge behavior insights

### Customer Analytics
- Top 10 highest-spending customers
- Average transaction value per customer
- Customers with remaining unpaid balances

### Restaurant Performance
- Revenue per restaurant
- Restaurant ranking
- Operational insights

### Peak Hours Analysis
- Transaction distribution by hour
- Identification of high-demand periods

### Cashier Performance
- Total processed amount
- Number of transactions handled

---

## 🚨 Anomaly Detection

Anomaly detection is performed using statistical methods (IQR):

- Abnormally high transactions
- Suspicious customer activity
- Restaurant-level anomalies
- Time-based irregularities

This helps prevent fraud and detect operational errors.

---

## 📈 Correlation Analysis

Analysis between:

- Prepaid card balance (Solde_CPP)
- Transaction amount (Montant_Rgl)

Provides insights into customer spending behavior.

---

## 🤖 Automation Pipeline

Automated workflow:

1. Raw transaction file received
2. Data cleaning and transformation
3. KPI computation
4. Anomaly detection
5. Report generation
6. Delivery to decision-makers

This reduces manual effort and ensures continuous monitoring.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 📁 Project Structure

```
prepaid-card-analytics/
│
├── REGLEMENTS_CARTES_PREPAYEES_FAST_FOOD.xlsx
├── logic.py
├── main.py
├── report.py
├── documents_rapport/
└── README.md
```

---

## 🚀 Business Impact

This system enables:

- Better operational efficiency
- Improved customer targeting
- Fraud risk reduction
- Revenue optimization
- Data-driven strategic planning

---

## 👤 Author

**Charaf Soubi**  
Data Analyst  

---

## ⭐ Project Status

Completed — Ready for production adaptation and dashboard integration.
