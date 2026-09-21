# 🛒 Supermarket Sales Analysis

**A Data Analytics project** that analyzes 500 supermarket sales transactions to extract useful information about products, branches, categories, customers, payment methods, and ratings.

---

## 📋 Project Description

This project performs an end-to-end Exploratory Data Analysis (EDA) on supermarket sales data collected across 4 branches in Indian cities (Jaipur, Delhi, Mumbai, Bengaluru). The analysis covers:

- **Product Performance**: Top and bottom-selling products
- **Branch Comparison**: Branch-level sales and performance
- **Category Analysis**: Which product categories drive revenue
- **Payment Methods**: Customer payment preferences
- **Customer Segmentation**: Member vs Normal customer spending
- **Gender Analysis**: Sales patterns across genders
- **Rating Analysis**: Customer satisfaction across branches and categories
- **Time Trends**: Monthly and day-of-week sales patterns
- **Correlation Analysis**: Relationships between numeric variables

---

## 📊 Dataset

- **Dataset:** Supermarket Sales Dataset
- **Source:** [SUPER MARKET DATA.xlsx](./SUPER%20MARKET%20DATA.xlsx)
- **Project brief:** [Supermarket Sales Analysis DA project (Google Doc)](https://docs.google.com/document/d/1DVCIE1WCNGpbBrVBIfEkqaN6Qw9lJkCS_p-P5zeQV7Q/edit?tab=t.0)
- **Records:** 500 sales transactions
- **Period:** January 2026 – July 2026
- **Columns (13):**

| Column | Description |
|---|---|
| Invoice ID | Unique transaction identifier |
| Date | Transaction date |
| Branch | Branch code (A, B, C, D) |
| City | City name (Jaipur, Delhi, Mumbai, Bengaluru) |
| Customer Type | Member or Normal |
| Gender | Male or Female |
| Product | Product name (20 products) |
| Category | Product category (8 categories) |
| Quantity | Quantity purchased (1–10) |
| Unit Price | Price per unit (₹) |
| Payment | Payment method (UPI, Card, Cash, Net Banking) |
| Rating | Customer rating (3.0–5.0) |
| Sales | Total sale amount (₹) |

---

## 📍 Key Findings

| Metric | Result |
|---|---|
| 🏆 Highest-Selling Product | Cheese (₹27,906.30) |
| 🏢 Best Performing Branch | C, Mumbai (₹72,469.45) |
| 📦 Top Category | Beverages (₹56,108.24) |
| 💳 Most Popular Payment | UPI (127 transactions) |
| 👥 Member vs Normal Avg | ₹483.14 vs ₹497.07 |
| ⭐ Average Rating | 3.99 / 5.0 |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Programming language |
| Pandas | Data manipulation & analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualizations |
| OpenPyXL | Excel file reading |
| python-docx | Word document generation |
| Jupyter Notebook | Interactive analysis environment |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Steps

1. **Clone / Download** the project folder.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis** (choose one):

   **Option A — Jupyter Notebook:**
   ```bash
   jupyter notebook SupermarketSalesAnalysis.ipynb
   ```

   **Option B — Python Script:**
   ```bash
   python SupermarketSalesAnalysis.py
   ```

4. **View results:**
   - All 12 charts are saved to the `charts/` folder
   - Key findings are printed in the console output

---

## 📁 Project Structure

```text
PRO!/
├── SupermarketSalesAnalysis.ipynb           # Jupyter Notebook version (Main Code)
├── SupermarketSalesAnalysis.py              # Python Script version
├── ProjectReport.docx                       # Project report document
├── requirements.txt                         # Python dependencies
├── README.md                                # This file
├── SUPER MARKET DATA.xlsx                   # Source dataset
└── charts/                                  # Generated visualizations (12 charts)
```

---

## 👤 Author

**Manthan**

---

## 📄 License

This project is for educational purposes as part of a Data Analytics course project.