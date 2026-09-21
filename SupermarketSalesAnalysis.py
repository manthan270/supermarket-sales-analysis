#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Supermarket Sales Analysis — Data Analytics Project
# Author : Manthan
# Date   : September 2026
# Dataset: SUPER MARKET DATA.xlsx (500 transactions)
# =============================================================================

# %% [markdown]
# # 🛒 Supermarket Sales Analysis
# ## Data Analytics Project — by Manthan
#
# **Objective:** Analyze supermarket sales data to extract actionable insights
# about products, branches, categories, customers, payment methods, and ratings.

# %% [markdown]
# ---
# ## 1. Imports & Setup

# %%
# --- Core Libraries ---
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for chart saving
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# --- Visualization Style ---
sns.set_theme(style='darkgrid', palette='viridis')
plt.rcParams.update({
    'figure.figsize': (12, 6),
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'font.size': 11,
    'axes.titlesize': 15,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'figure.facecolor': '#f8f9fa',
    'axes.facecolor': '#ffffff',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.3,
})

# Color palette
COLORS = {
    'primary': '#4361ee',
    'secondary': '#3a0ca3',
    'accent': '#f72585',
    'success': '#06d6a0',
    'warning': '#ffd166',
    'info': '#118ab2',
    'dark': '#073b4c',
}
PALETTE_MAIN = ['#4361ee', '#f72585', '#06d6a0', '#ffd166', '#118ab2',
                '#3a0ca3', '#7209b7', '#e63946']
PALETTE_SEQ = 'coolwarm'

# Charts output directory
CHART_DIR = 'charts'
os.makedirs(CHART_DIR, exist_ok=True)

def save_chart(fig, name):
    """Save a chart to the charts directory."""
    path = os.path.join(CHART_DIR, f'{name}.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f'  ✅ Saved: {path}')
    return path

print('✅ Libraries imported & style configured.')

# %% [markdown]
# ---
# ## 2. Data Loading

# %%
# Load dataset
DATA_FILE = 'SUPER MARKET DATA.xlsx'
df = pd.read_excel(DATA_FILE)

print(f'📊 Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns\n')
print('--- First 5 Rows ---')
print(df.head().to_string())
print('\n--- Column Data Types ---')
print(df.dtypes)
print(f'\n--- Dataset Info ---')
print(f'Memory usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB')

# %% [markdown]
# ---
# ## 3. Data Cleaning & Preprocessing

# %%
print('🔍 DATA QUALITY CHECKS\n')

# 3.1 Missing values
print('--- Missing Values ---')
missing = df.isnull().sum()
print(missing)
print(f'\nTotal missing values: {missing.sum()}')

# 3.2 Duplicate rows
duplicates = df.duplicated().sum()
print(f'\n--- Duplicate Rows: {duplicates} ---')

# 3.3 Verify Sales = Quantity × Unit Price
df['Sales_Calculated'] = (df['Quantity'] * df['Unit Price']).round(2)
mismatch = df[df['Sales'] != df['Sales_Calculated']]
print(f'\n--- Sales Verification ---')
print(f'Mismatches between Sales and Quantity × Unit Price: {len(mismatch)}')
if len(mismatch) > 0:
    print('Fixing mismatched rows...')
    df['Sales'] = df['Sales_Calculated']
df.drop(columns=['Sales_Calculated'], inplace=True)

# 3.4 Data type checks
print('\n--- Data Type Validation ---')
print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
print(f"Quantity range: {df['Quantity'].min()} to {df['Quantity'].max()}")
print(f"Unit Price range: ₹{df['Unit Price'].min():.2f} to ₹{df['Unit Price'].max():.2f}")
print(f"Sales range: ₹{df['Sales'].min():.2f} to ₹{df['Sales'].max():.2f}")
print(f"Rating range: {df['Rating'].min()} to {df['Rating'].max()}")

# 3.5 Add derived columns for time-based analysis
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')
df['Day_of_Week'] = df['Date'].dt.day_name()

print('\n✅ Data cleaning complete. Added Month, Month_Name, Day_of_Week columns.')

# %% [markdown]
# ---
# ## 4. Descriptive Statistics

# %%
print('📈 DESCRIPTIVE STATISTICS\n')
print(df.describe().round(2).to_string())

print('\n--- Categorical Column Summary ---')
for col in ['Branch', 'City', 'Customer Type', 'Gender', 'Category', 'Payment']:
    print(f"\n{col}: {df[col].nunique()} unique → {df[col].value_counts().to_dict()}")

# %% [markdown]
# ---
# ## 5. EDA — Product Analysis
#
# *Which product generates the highest sales?*

# %%
print('🛍️  PRODUCT ANALYSIS\n')

# Total sales by product
product_sales = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).round(2)
print('--- Total Sales by Product (Top 10) ---')
print(product_sales.head(10).to_string())
print(f'\n🏆 Highest: {product_sales.index[0]} — ₹{product_sales.iloc[0]:,.2f}')
print(f'📉 Lowest : {product_sales.index[-1]} — ₹{product_sales.iloc[-1]:,.2f}')

# --- Chart: Top 10 Products by Sales ---
fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(product_sales.index[::-1], product_sales.values[::-1],
               color=sns.color_palette('coolwarm_r', n_colors=len(product_sales)),
               edgecolor='white', linewidth=0.5)
# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 200, bar.get_y() + bar.get_height()/2,
            f'₹{width:,.0f}', ha='left', va='center', fontsize=9, fontweight='bold')
ax.set_xlabel('Total Sales (₹)')
ax.set_title('Total Sales by Product', fontsize=16, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
save_chart(fig, '01_product_sales')

# --- Chart: Average Sales per Transaction by Product ---
product_avg = df.groupby('Product')['Sales'].mean().sort_values(ascending=False).round(2)
fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(product_avg.index[::-1], product_avg.values[::-1],
               color=sns.color_palette('mako', n_colors=len(product_avg)),
               edgecolor='white', linewidth=0.5)
for bar in bars:
    width = bar.get_width()
    ax.text(width + 10, bar.get_y() + bar.get_height()/2,
            f'₹{width:,.0f}', ha='left', va='center', fontsize=9, fontweight='bold')
ax.set_xlabel('Average Sales per Transaction (₹)')
ax.set_title('Average Sales per Transaction by Product', fontsize=16, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
save_chart(fig, '02_product_avg_sales')

# %% [markdown]
# ---
# ## 6. EDA — Branch & City Analysis
#
# *Which branch performs best?*

# %%
print('🏢 BRANCH & CITY ANALYSIS\n')

# Sales by branch
branch_sales = df.groupby(['Branch', 'City'])['Sales'].agg(['sum', 'mean', 'count']).round(2)
branch_sales.columns = ['Total Sales', 'Avg Transaction', 'Transactions']
branch_sales = branch_sales.sort_values('Total Sales', ascending=False)
print('--- Sales by Branch & City ---')
print(branch_sales.to_string())

best_branch = branch_sales['Total Sales'].idxmax()
print(f'\n🏆 Best Branch: {best_branch[0]} ({best_branch[1]}) — ₹{branch_sales.loc[best_branch, "Total Sales"]:,.2f}')

# --- Chart: Branch Comparison ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Branch Performance Comparison', fontsize=18, fontweight='bold', y=1.02)

branch_data = df.groupby('Branch').agg(
    Total_Sales=('Sales', 'sum'),
    Avg_Transaction=('Sales', 'mean'),
    Transactions=('Sales', 'count')
).reset_index()
branch_data['City'] = branch_data['Branch'].map(
    df.groupby('Branch')['City'].first().to_dict()
)
branch_data['Label'] = branch_data['Branch'] + '\n(' + branch_data['City'] + ')'

# Total Sales
bars1 = axes[0].bar(branch_data['Label'], branch_data['Total_Sales'],
                     color=PALETTE_MAIN[:4], edgecolor='white', linewidth=1.5)
axes[0].set_title('Total Sales', fontweight='bold')
axes[0].set_ylabel('Sales (₹)')
axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
for bar in bars1:
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f'₹{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Avg Transaction
bars2 = axes[1].bar(branch_data['Label'], branch_data['Avg_Transaction'],
                     color=PALETTE_MAIN[:4], edgecolor='white', linewidth=1.5)
axes[1].set_title('Avg Transaction Value', fontweight='bold')
axes[1].set_ylabel('Avg Sales (₹)')
for bar in bars2:
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'₹{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Transaction Count
bars3 = axes[2].bar(branch_data['Label'], branch_data['Transactions'],
                     color=PALETTE_MAIN[:4], edgecolor='white', linewidth=1.5)
axes[2].set_title('Number of Transactions', fontweight='bold')
axes[2].set_ylabel('Count')
for bar in bars3:
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9, fontweight='bold')

for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
save_chart(fig, '03_branch_comparison')

# %% [markdown]
# ---
# ## 7. EDA — Category Analysis
#
# *Which category sells the most?*

# %%
print('📦 CATEGORY ANALYSIS\n')

# Sales by category
cat_sales = df.groupby('Category')['Sales'].agg(['sum', 'mean', 'count']).round(2)
cat_sales.columns = ['Total Sales', 'Avg Transaction', 'Transactions']
cat_sales = cat_sales.sort_values('Total Sales', ascending=False)
print('--- Sales by Category ---')
print(cat_sales.to_string())
print(f'\n🏆 Top Category: {cat_sales.index[0]} — ₹{cat_sales.iloc[0]["Total Sales"]:,.2f}')

# --- Chart: Category Sales ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Category Analysis', fontsize=18, fontweight='bold', y=1.02)

# Total sales
colors_cat = sns.color_palette('rocket', n_colors=len(cat_sales))
bars = axes[0].barh(cat_sales.index[::-1], cat_sales['Total Sales'].values[::-1],
                     color=colors_cat, edgecolor='white', linewidth=0.5)
for bar in bars:
    width = bar.get_width()
    axes[0].text(width + 300, bar.get_y() + bar.get_height()/2,
                 f'₹{width:,.0f}', ha='left', va='center', fontsize=9, fontweight='bold')
axes[0].set_title('Total Sales by Category', fontweight='bold')
axes[0].set_xlabel('Total Sales (₹)')
axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))

# Transaction count pie
wedges, texts, autotexts = axes[1].pie(
    cat_sales['Transactions'], labels=cat_sales.index, autopct='%1.1f%%',
    colors=sns.color_palette('Set2', n_colors=len(cat_sales)),
    startangle=140, pctdistance=0.8,
    wedgeprops=dict(edgecolor='white', linewidth=2)
)
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')
axes[1].set_title('Transaction Share by Category', fontweight='bold')

for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
save_chart(fig, '04_category_analysis')

# %% [markdown]
# ---
# ## 8. EDA — Payment Method Analysis
#
# *What is the most popular payment method?*

# %%
print('💳 PAYMENT METHOD ANALYSIS\n')

# Payment analysis
payment_stats = df.groupby('Payment')['Sales'].agg(['count', 'sum', 'mean']).round(2)
payment_stats.columns = ['Transactions', 'Total Sales', 'Avg Transaction']
payment_stats = payment_stats.sort_values('Transactions', ascending=False)
print('--- Payment Method Statistics ---')
print(payment_stats.to_string())
print(f'\n🏆 Most Popular: {payment_stats.index[0]} — {payment_stats.iloc[0]["Transactions"]} transactions')

# --- Chart: Payment Methods ---
fig, axes = plt.subplots(1, 2, figsize=(15, 7))
fig.suptitle('Payment Method Analysis', fontsize=18, fontweight='bold', y=1.02)

# Transaction count — Donut chart
colors_pay = [COLORS['primary'], COLORS['accent'], COLORS['success'], COLORS['warning']]
wedges, texts, autotexts = axes[0].pie(
    payment_stats['Transactions'], labels=payment_stats.index,
    autopct='%1.1f%%', colors=colors_pay, startangle=90,
    pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)
)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')
axes[0].set_title('Transaction Count by Payment', fontweight='bold')
# Add center text
centre_circle = plt.Circle((0, 0), 0.30, fc='white')
axes[0].add_artist(centre_circle)
axes[0].text(0, 0, f'{payment_stats["Transactions"].sum()}\nTotal', ha='center',
             va='center', fontsize=13, fontweight='bold', color=COLORS['dark'])

# Total sales by payment
bars = axes[1].bar(payment_stats.index, payment_stats['Total Sales'],
                    color=colors_pay, edgecolor='white', linewidth=1.5)
for bar in bars:
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f'₹{bar.get_height():,.0f}', ha='center', va='bottom',
                 fontsize=10, fontweight='bold')
axes[1].set_title('Total Sales by Payment Method', fontweight='bold')
axes[1].set_ylabel('Total Sales (₹)')
axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.tight_layout()
save_chart(fig, '05_payment_analysis')

# %% [markdown]
# ---
# ## 9. EDA — Customer Type Analysis
#
# *Do Members spend more than Normal customers?*

# %%
print('👥 CUSTOMER TYPE ANALYSIS\n')

# Customer type comparison
cust_stats = df.groupby('Customer Type')['Sales'].agg(['count', 'sum', 'mean']).round(2)
cust_stats.columns = ['Transactions', 'Total Sales', 'Avg Transaction']
print('--- Customer Type Comparison ---')
print(cust_stats.to_string())

member_avg = cust_stats.loc['Member', 'Avg Transaction']
normal_avg = cust_stats.loc['Normal', 'Avg Transaction']
print(f'\nMember Avg: ₹{member_avg:,.2f}  |  Normal Avg: ₹{normal_avg:,.2f}')
if member_avg > normal_avg:
    print('→ Members spend MORE per transaction.')
else:
    print('→ Normal customers spend MORE per transaction.')

# --- Chart: Customer Type ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Customer Type Analysis: Member vs Normal', fontsize=18, fontweight='bold', y=1.02)

cust_colors = [COLORS['primary'], COLORS['accent']]

# Transactions
bars1 = axes[0].bar(cust_stats.index, cust_stats['Transactions'], color=cust_colors,
                     edgecolor='white', linewidth=1.5)
axes[0].set_title('Transaction Count', fontweight='bold')
axes[0].set_ylabel('Count')
for bar in bars1:
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Total Sales
bars2 = axes[1].bar(cust_stats.index, cust_stats['Total Sales'], color=cust_colors,
                     edgecolor='white', linewidth=1.5)
axes[1].set_title('Total Sales', fontweight='bold')
axes[1].set_ylabel('Sales (₹)')
axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
for bar in bars2:
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f'₹{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Avg Transaction
bars3 = axes[2].bar(cust_stats.index, cust_stats['Avg Transaction'], color=cust_colors,
                     edgecolor='white', linewidth=1.5)
axes[2].set_title('Average Transaction Value', fontweight='bold')
axes[2].set_ylabel('Avg Sales (₹)')
for bar in bars3:
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                 f'₹{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
save_chart(fig, '06_customer_type_analysis')

# %% [markdown]
# ---
# ## 10. EDA — Gender Analysis

# %%
print('🧑‍🤝‍🧑 GENDER ANALYSIS\n')

# Gender breakdown
gender_stats = df.groupby('Gender')['Sales'].agg(['count', 'sum', 'mean']).round(2)
gender_stats.columns = ['Transactions', 'Total Sales', 'Avg Transaction']
print('--- Gender Comparison ---')
print(gender_stats.to_string())

# Gender × Category
gender_cat = df.groupby(['Gender', 'Category'])['Sales'].sum().unstack(fill_value=0).round(2)
print('\n--- Sales by Gender × Category ---')
print(gender_cat.to_string())

# --- Chart: Gender Analysis ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Gender-Based Sales Analysis', fontsize=18, fontweight='bold', y=1.02)

gender_colors = ['#4361ee', '#f72585']

# Total sales by gender
bars = axes[0].bar(gender_stats.index, gender_stats['Total Sales'], color=gender_colors,
                    edgecolor='white', linewidth=1.5, width=0.5)
for bar in bars:
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f'₹{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
axes[0].set_title('Total Sales by Gender', fontweight='bold')
axes[0].set_ylabel('Total Sales (₹)')
axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

# Gender × Category grouped bar
gender_cat.T.plot(kind='bar', ax=axes[1], color=gender_colors, edgecolor='white', linewidth=1)
axes[1].set_title('Sales by Category & Gender', fontweight='bold')
axes[1].set_ylabel('Total Sales (₹)')
axes[1].set_xlabel('Category')
axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
axes[1].legend(title='Gender')
axes[1].tick_params(axis='x', rotation=45)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.tight_layout()
save_chart(fig, '07_gender_analysis')

# %% [markdown]
# ---
# ## 11. EDA — Rating Analysis
#
# *What is the average customer rating?*

# %%
print('⭐ RATING ANALYSIS\n')

avg_rating = df['Rating'].mean()
print(f'Average Customer Rating: {avg_rating:.2f} / 5.0\n')

# Rating by branch
rating_branch = df.groupby('Branch')['Rating'].mean().round(2)
print('--- Average Rating by Branch ---')
print(rating_branch.to_string())

# Rating by category
rating_cat = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).round(2)
print('\n--- Average Rating by Category ---')
print(rating_cat.to_string())

# --- Chart: Rating Distribution & Analysis ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Customer Rating Analysis', fontsize=18, fontweight='bold', y=1.01)

# Distribution histogram
axes[0, 0].hist(df['Rating'], bins=20, color=COLORS['primary'], edgecolor='white',
                linewidth=0.8, alpha=0.85)
axes[0, 0].axvline(avg_rating, color=COLORS['accent'], linestyle='--', linewidth=2,
                    label=f'Mean: {avg_rating:.2f}')
axes[0, 0].set_title('Rating Distribution', fontweight='bold')
axes[0, 0].set_xlabel('Rating')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].legend()

# Rating by branch
bars = axes[0, 1].bar(rating_branch.index, rating_branch.values, color=PALETTE_MAIN[:4],
                       edgecolor='white', linewidth=1.5)
for bar in bars:
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                     f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
axes[0, 1].set_title('Avg Rating by Branch', fontweight='bold')
axes[0, 1].set_ylabel('Average Rating')
axes[0, 1].set_ylim(0, 5.5)

# Rating by category
bars = axes[1, 0].barh(rating_cat.index[::-1], rating_cat.values[::-1],
                        color=sns.color_palette('viridis', n_colors=len(rating_cat)),
                        edgecolor='white', linewidth=0.5)
for bar in bars:
    axes[1, 0].text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                     f'{bar.get_width():.2f}', ha='left', va='center', fontsize=9, fontweight='bold')
axes[1, 0].set_title('Avg Rating by Category', fontweight='bold')
axes[1, 0].set_xlabel('Average Rating')
axes[1, 0].set_xlim(0, 5.5)

# Rating vs Sales scatter
scatter = axes[1, 1].scatter(df['Rating'], df['Sales'], alpha=0.5,
                              c=df['Rating'], cmap='coolwarm', edgecolors='white',
                              linewidth=0.3, s=50)
axes[1, 1].set_title('Rating vs Sales', fontweight='bold')
axes[1, 1].set_xlabel('Rating')
axes[1, 1].set_ylabel('Sales (₹)')
plt.colorbar(scatter, ax=axes[1, 1], label='Rating')

for ax in axes.flat:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
save_chart(fig, '08_rating_analysis')

# %% [markdown]
# ---
# ## 12. EDA — Time / Monthly Trend Analysis

# %%
print('📅 MONTHLY TREND ANALYSIS\n')

# Monthly sales
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
monthly = df.groupby('Month_Name')['Sales'].agg(['sum', 'mean', 'count']).round(2)
monthly.columns = ['Total Sales', 'Avg Transaction', 'Transactions']
monthly = monthly.reindex(month_order)
print('--- Monthly Sales Summary ---')
print(monthly.to_string())

# --- Chart: Monthly Trends ---
fig, ax1 = plt.subplots(figsize=(14, 7))

# Line plot — total sales
color1 = COLORS['primary']
ax1.plot(monthly.index, monthly['Total Sales'], marker='o', linewidth=2.5,
         color=color1, markersize=8, markerfacecolor='white',
         markeredgecolor=color1, markeredgewidth=2, label='Total Sales', zorder=5)
ax1.fill_between(monthly.index, monthly['Total Sales'], alpha=0.15, color=color1)
ax1.set_xlabel('Month', fontsize=12)
ax1.set_ylabel('Total Sales (₹)', color=color1, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))

# Annotate values
for i, (month, row) in enumerate(monthly.iterrows()):
    ax1.annotate(f'₹{row["Total Sales"]:,.0f}', (month, row['Total Sales']),
                 textcoords="offset points", xytext=(0, 15), ha='center',
                 fontsize=9, fontweight='bold', color=color1)

# Secondary axis — transaction count
ax2 = ax1.twinx()
color2 = COLORS['accent']
ax2.bar(monthly.index, monthly['Transactions'], alpha=0.3, color=color2,
        edgecolor=color2, linewidth=1, label='Transactions', width=0.4)
ax2.set_ylabel('Number of Transactions', color=color2, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color2)

ax1.set_title('Monthly Sales Trend (Jan–Jul 2026)', fontsize=16, fontweight='bold', pad=15)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
plt.tight_layout()
save_chart(fig, '09_monthly_trend')

# --- Chart: Day of Week Analysis ---
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily = df.groupby('Day_of_Week')['Sales'].agg(['sum', 'count']).reindex(day_order)
daily.columns = ['Total Sales', 'Transactions']

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(daily.index, daily['Total Sales'], color=sns.color_palette('husl', 7),
              edgecolor='white', linewidth=1.5)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
            f'₹{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Sales by Day of Week', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Total Sales (₹)')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
save_chart(fig, '10_day_of_week')

# %% [markdown]
# ---
# ## 13. Correlation Analysis

# %%
print('🔗 CORRELATION ANALYSIS\n')

# Correlation matrix for numeric columns
numeric_cols = ['Quantity', 'Unit Price', 'Rating', 'Sales']
corr_matrix = df[numeric_cols].corr().round(3)
print('--- Correlation Matrix ---')
print(corr_matrix.to_string())

# --- Chart: Correlation Heatmap ---
fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=2, linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Correlation'},
            annot_kws={'size': 13, 'fontweight': 'bold'},
            ax=ax)
ax.set_title('Correlation Heatmap — Numeric Variables', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
save_chart(fig, '11_correlation_heatmap')

# %% [markdown]
# ---
# ## 14. Advanced Analysis — Branch × Category Heatmap

# %%
# Branch × Category sales heatmap
branch_cat = df.pivot_table(values='Sales', index='Category', columns='Branch',
                             aggfunc='sum').round(2)
print('--- Branch × Category Sales Matrix ---')
print(branch_cat.to_string())

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(branch_cat, annot=True, fmt=',.0f', cmap='YlOrRd',
            linewidths=2, linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Sales (₹)'},
            annot_kws={'size': 11, 'fontweight': 'bold'}, ax=ax)
ax.set_title('Sales Heatmap: Branch × Category', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Branch')
ax.set_ylabel('Category')
plt.tight_layout()
save_chart(fig, '12_branch_category_heatmap')

# %% [markdown]
# ---
# ## 15. Top & Bottom Performers Summary

# %%
print('\n' + '='*60)
print('   📊 KEY FINDINGS SUMMARY')
print('='*60)

# Top product
print(f'\n🏆 Highest-Selling Product : {product_sales.index[0]} — ₹{product_sales.iloc[0]:,.2f}')
print(f'📉 Lowest-Selling Product  : {product_sales.index[-1]} — ₹{product_sales.iloc[-1]:,.2f}')

# Best branch
best_b = df.groupby(['Branch', 'City'])['Sales'].sum().sort_values(ascending=False)
print(f'\n🏆 Best Branch : {best_b.index[0][0]} ({best_b.index[0][1]}) — ₹{best_b.iloc[0]:,.2f}')

# Top category
print(f'\n🏆 Top Category : {cat_sales.index[0]} — ₹{cat_sales.iloc[0]["Total Sales"]:,.2f}')

# Most popular payment
print(f'\n🏆 Most Popular Payment : {payment_stats.index[0]} — {int(payment_stats.iloc[0]["Transactions"])} transactions')

# Member vs Normal
print(f'\n👥 Member Avg Transaction  : ₹{member_avg:,.2f}')
print(f'👥 Normal Avg Transaction  : ₹{normal_avg:,.2f}')

# Rating
print(f'\n⭐ Average Customer Rating : {avg_rating:.2f} / 5.0')

# %% [markdown]
# ---
# ## 16. Business Recommendations
#
# Based on the analysis, the following business recommendations are proposed:
#
# 1. **Stock Optimization:** Increase stock for high-selling products (Cheese, Cooking Oil, Coffee)
#    and top categories (Beverages, Grocery).
#
# 2. **Branch Strategy:** Study Branch C (Mumbai) to understand why it outperforms other branches
#    and replicate successful practices across all locations.
#
# 3. **Payment Infrastructure:** Continue investing in UPI payment infrastructure as it is the
#    most popular payment method. Ensure smooth UPI transactions.
#
# 4. **Customer Programs:** Since Normal customers spend slightly more per transaction than Members,
#    redesign membership benefits to incentivize higher spending among Members.
#
# 5. **Rating Improvement:** The average rating of 3.99/5 indicates room for improvement.
#    Focus on customer service training and feedback mechanisms.
#
# 6. **Seasonal Planning:** Use monthly trend data to plan promotions and inventory for
#    high-sales and low-sales months.

# %%
print('\n✅ Analysis Complete! All charts saved to the "charts/" folder.')
print(f'   Total charts generated: {len(os.listdir(CHART_DIR))}')
print(f'   Charts: {sorted(os.listdir(CHART_DIR))}')
