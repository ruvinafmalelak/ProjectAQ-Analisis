import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('dashboard/main_data.csv')


# Set page configuration
st.set_page_config(page_title="Air Quality Analysis Dashboard - Guanyuan", layout="wide")

# Header
st.title("Air Quality Analysis Dashboard - Guanyuan")
st.markdown("""
Dashboard ini menyajikan analisis kualitas udara di Guanyuan, termasuk tren polusi berdasarkan musim, bulan, hari, dan hubungannya dengan variabel cuaca.
""")

# Sidebar for filters
st.sidebar.header("Filter Data")
year = st.sidebar.multiselect("Pilih Tahun", options=df["year"].unique(), default=df["year"].unique())
month = st.sidebar.multiselect("Pilih Bulan", options=df["month"].unique(), default=df["month"].unique())
pollutant = st.sidebar.selectbox("Pilih Jenis Polutan", options=["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"])

# Filter data based on selection
filtered_df = df[(df["year"].isin(year)) & (df["month"].isin(month))]

# Section 1: Monthly and Seasonal Analysis
st.subheader("Analisis Polusi Berdasarkan Bulan dan Musim")

# Monthly Analysis
# Mengambil kolom numerik saja untuk menghindari peringatan
monthly_avg = filtered_df.groupby('month').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_avg.index, monthly_avg[pollutant], marker='o', color='b')
ax.set_title(f'Rata-Rata Konsentrasi {pollutant} Berdasarkan Bulan di Guanyuan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Konsentrasi (µg/m³)')
st.pyplot(fig)

# Seasonal Analysis
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

# Gunakan .loc untuk menghindari SettingWithCopyWarning
filtered_df.loc[:, 'season'] = filtered_df['month'].map(get_season)
# Hanya gunakan kolom numerik untuk rata-rata musiman
seasonal_avg = filtered_df.groupby('season').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(10, 6))
seasonal_avg[[pollutant]].plot(kind='bar', ax=ax, color='skyblue')
ax.set_title(f'Rata-Rata Konsentrasi {pollutant} Berdasarkan Musim di Guanyuan')
ax.set_xlabel('Musim')
ax.set_ylabel('Konsentrasi (µg/m³)')
st.pyplot(fig)

# Section 2: Daily Analysis
st.subheader("Tren Harian Polusi Udara di Guanyuan")
daily_avg = filtered_df.groupby('day').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_avg.index, daily_avg[pollutant], marker='o', color='green')
ax.set_title(f'Rata-Rata Konsentrasi {pollutant} Berdasarkan Hari dalam Sebulan di Guanyuan')
ax.set_xlabel('Hari dalam Sebulan')
ax.set_ylabel('Konsentrasi (µg/m³)')
st.pyplot(fig)

# Section 3: Correlation Analysis
st.subheader("Analisis Korelasi antara Polutan dan Variabel Cuaca")
# Pilih kolom numerik untuk korelasi
correlation_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
correlation_matrix = filtered_df[correlation_columns].corr()

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='RdBu', vmin=-1, vmax=1, ax=ax)
ax.set_title('Korelasi antara Polutan dan Variabel Cuaca di Guanyuan')
st.pyplot(fig)

# Section 4: Data Table
st.subheader("Data Lengkap: Guanyuan Air Quality")
st.dataframe(filtered_df)
