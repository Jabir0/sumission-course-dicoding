import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set Seaborn style and configure default fonts
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.family'] = 'sans-serif'

# Load data
day_df = pd.read_csv('day_data_bersih.csv')
hour_df = pd.read_csv('hour_data_bersih.csv')

# Define mappings for categorical data
season_map = {1: 'Spring/Semi', 2: 'Summer/Panas', 3: 'Fall/Gugur', 4: 'Winter/Dingin'}
month_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
day_map = {0:'Minggu', 1:'Senin', 2:'Selasa', 3:'Rabu', 4:'Kamis', 5:'Jumat', 6:'Sabtu'}
holiday_map = {0: 'Holiday/Weekend/Hari Libur', 1: 'Working Day/Non-Holiday/Hari Kerja'}

# Map the categorical columns in the DataFrame
day_df['season_name'] = day_df['season'].map(season_map)
day_df['weekday_name'] = day_df['weekday'].map(day_map)
day_df['holiday_name'] = day_df['workingday'].map(holiday_map)

# --- Dashboard Header ---
st.title('🚴‍♂️ Bike Sharing Data Dashboard')
st.markdown('### Jelajahi pola penyewaan sepeda di berbagai waktu dan kondisi cuaca.')
st.markdown('#### Dibuat Oleh :')
st.markdown('#### JABIR MUKTABIR M206B4KY2033')

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Filter Data")
    selected_season = st.multiselect("Select Season", options=day_df['season_name'].unique(), default=day_df['season_name'].unique())
    selected_day = st.multiselect("Select Day of Week", options=day_df['weekday_name'].unique(), default=day_df['weekday_name'].unique())

    # Apply filters
    filtered_data = day_df[(day_df['season_name'].isin(selected_season)) & (day_df['weekday_name'].isin(selected_day))]

# --- Visualization 1: Total Rentals by Season ---
st.subheader("1. Total Penyewaan Sepeda Berdasarkan Musim")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', data=filtered_data, palette='coolwarm', ax=ax1)
ax1.set_title('Jumlah Penyewaan Sepeda per Musim', fontsize=16, fontweight='bold')
ax1.set_xlabel('Musim', fontsize=12)
ax1.set_ylabel('Total Rental', fontsize=12)
st.pyplot(fig1)

# --- Visualization 2: Monthly Bike Rental Trend ---
st.subheader("2. Tren Penyewaan Sepeda Bulanan")
monthly_data = day_df.groupby('mnth')['cnt'].mean().reset_index()
monthly_data['month_name'] = monthly_data['mnth'].map(month_map)
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(x='month_name', y='cnt', data=monthly_data, marker='o', linewidth=2, markersize=8, ax=ax2)
ax2.set_title('Tren Bulanan Penyewaan Sepeda', fontsize=16, fontweight='bold')
ax2.set_xlabel('Bulan', fontsize=12)
ax2.set_ylabel('Rata-rata Rental', fontsize=12)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

# --- Visualization 3: Bike Rentals by Day of Week ---
st.subheader("3. Penyewaan Sepeda Berdasarkan Hari")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday_name', y='cnt', data=filtered_data, palette='coolwarm', ax=ax3)
ax3.set_title('Penyewaan Berdasarkan Hari dalam Seminggu', fontsize=16, fontweight='bold')
ax3.set_xlabel('Hari', fontsize=12)
ax3.set_ylabel('Total Rental', fontsize=12)
st.pyplot(fig3)

# --- Visualization 4: Rentals on Holidays vs Working Days ---
st.subheader("4. Perbandingan Penyewaan: Hari Libur vs Hari Kerja")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x='holiday_name', y='cnt', data=filtered_data, palette='coolwarm', ax=ax4)
ax4.set_title('Penyewaan pada Hari Kerja dan Hari Libur', fontsize=16, fontweight='bold')
ax4.set_xlabel('Tipe Hari', fontsize=12)
ax4.set_ylabel('Total Rental', fontsize=12)
st.pyplot(fig4)

# --- Visualization 5: Hourly Bike Rentals ---
st.subheader("5. Jumlah Penyewaan Sepeda Berdasarkan Jam")
hourly_data = hour_df.groupby('hr')['cnt'].mean().reset_index()
fig5, ax5 = plt.subplots(figsize=(14, 7))
sns.lineplot(x='hr', y='cnt', data=hourly_data, marker='o', linewidth=2, markersize=8, ax=ax5)
ax5.set_title('Penyewaan Berdasarkan Jam dalam Sehari', fontsize=16, fontweight='bold')
ax5.set_xlabel('Jam', fontsize=12)
ax5.set_ylabel('Rata-rata Rental', fontsize=12)
ax5.set_xticks(range(0, 24))
st.pyplot(fig5)

# --- Manual Clustering: Temperature vs Rentals ---
st.subheader("6. Clustering Manual: Suhu vs Jumlah Rental")
def temp_cluster(temp):
    if temp < 0.3:
        return 'Dingin'
    elif temp < 0.6:
        return 'Sejuk'
    else:
        return 'Panas'

def rental_cluster(cnt):
    if cnt < 1000:
        return 'Rendah'
    elif cnt < 3000:
        return 'Sedang'
    else:
        return 'Tinggi'

# Apply the clustering functions
day_df['temp_cluster'] = day_df['temp'].apply(temp_cluster)
day_df['rental_cluster'] = day_df['cnt'].apply(rental_cluster)

# Plot scatterplot with clusters
fig6, ax6 = plt.subplots(figsize=(12, 6))
sns.scatterplot(x='temp', y='cnt', hue='temp_cluster', style='rental_cluster', data=day_df, palette='coolwarm', ax=ax6)
ax6.set_title('Clustering Manual: Temperatur vs Total Rental', fontsize=16, fontweight='bold')
ax6.set_xlabel('Temperatur (Normalized)', fontsize=12)
ax6.set_ylabel('Total Rental', fontsize=12)
st.pyplot(fig6)

# --- Footer ---
st.markdown("---")
st.caption("© 2024 Bike Sharing Data Analysis - Powered by Streamlit and Seaborn")
st.caption("Jabir Muktabir")
