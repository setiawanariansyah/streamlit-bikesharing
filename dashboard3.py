import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from sklearn.cluster import KMeans
import random

sns.set(style='whitegrid')

# Load cleaned data
data_gabung = pd.read_csv("data_gabung.csv")

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://static.sehatq.com/content/review/product/image/650120220322171147.png")

    # Menambahkan judul
    st.header("Proyek Analisis Data")

    # Menambahkan teks
    st.markdown("""
    Proyek ini adalah proyek analisis data bike sharing. Analisis dimulai dari persiapan hingga kesimpulan yang didapatkan dari data disajikan dalam proyek ini.

    **Nama  : Setiawan Ariansyah**  
    **Email : ariansyahsetiawan818@gmail.com**
    """)

# Menyiapkan berbagai dataframe
## Berdasarkan musim
def create_byseason_daily_df(df):
    byseason_daily_df = df.groupby(by="season_daily").cnt_daily.sum().reset_index()
    return byseason_daily_df

def create_byseason_hourly_df(df):
    byseason_hourly_df = df.groupby(by="season_hourly").cnt_hourly.sum().reset_index()
    return byseason_hourly_df

def create_byseason_hum_daily_df(df):
    byseason_hum_daily = df.groupby(by="season_daily").hum_daily.mean().reset_index()
    return byseason_hum_daily

byseason_daily_df = create_byseason_daily_df(data_gabung)
byseason_hourly_df = create_byseason_hourly_df(data_gabung)
byseason_hum_daily = create_byseason_hum_daily_df(data_gabung)

# plot
st.header('Bike Sharing :sparkles:')
st.subheader('Jumlah Penyewaan Harian')

col1, col2 = st.columns(2)

with col1:
    total_sewaharian = data_gabung.instant_daily.nunique()
    st.metric("Total Sewa Harian dalam 2 Tahun", value=total_sewaharian)

with col2:
    total_pengguna = data_gabung.cnt_daily.sum() 
    st.metric("Total Pengguna dalam 2 tahun", value=total_pengguna)


# Penyewaan sepeda berdasarkan musim
st.subheader("Penyewaan berdasarkan musim (harian dan jam)")
colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="cnt_daily", 
        x="season_daily",
        data=byseason_daily_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Sewa per Musim (Harian)", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        y="cnt_hourly", 
        x="season_hourly",
        data=byseason_hourly_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Sewa per Musim (Jam)", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="season_daily", 
    y="hum_daily",
    data=byseason_hum_daily,
    palette=colors,
    ax=ax
)
ax.set_title("Grafik Kelembapan Udara Harian per Musim", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.markdown("""Dari grafik diatas terlihat bahwa pengguna lebih banyak melakukan peminjaman sepeda pada musim gugur dan musim panas. Sedangkan jumlah peminjaman sepeda terendah di musim gugur. Musim panas dan musim gugur memiliki rentang nilai kelembapan yang normal sehingga pada sebagian besar orang akan nyaman untuk melakukan aktivitas diluar rumah. Dibandingkan dengan musim dingin dengan humiditas yg tinggi akan berbahaya untuk bersepeda dikarenakan jalanan yang licin. Hal ini jug berlaku untuk musim semi dengan humiditas yg kurang menandakan suasana yg kering. Jika dilihat dari suhu, maka secara rata-rata suhu cukup tinggi.""")

# Pola Penyewaan Berdasarkan Bulan dan Jam
st.subheader("Pola Penyewaan Harian dan Jam")
colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.lineplot(
        y="cnt_daily", 
        x="mnth_daily",
        data=data_gabung,
        palette=colors,
        ax=ax
    )
    ax.set_title("Pola Penyewaan Bulan", loc="center", fontsize=50)
    ax.set_ylabel("Jumlah sewa Bulan")
    ax.set_xlabel("Bulan")
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.lineplot(
        y="cnt_hourly", 
        x="hr",
        data=data_gabung,
        palette=colors,
        ax=ax
    )
    ax.set_title("Pola Penyewaan dalam Jam", loc="center", fontsize=50)
    ax.set_ylabel("Jumlah sewa dalam jam")
    ax.set_xlabel("Jam")
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.text("Berdasarkan bulan, jumlah sepeda harian terjadi kenaikan pada bulan keenam hingga kesepuluh. Setelah itu terjadi penurunan jumlah sewa sepeda harian. Hal ini sejalan dengan temuan di tujuan pertama bahwa pada musim dingin orang-orang menghindari kegiatan diluar karena keadaan.")
st.text("Berdasarkan jam, jumlah sepeda harian lebih banyak dilakukan pada pagi hari dan sore hari.")

# Gambaran Penyewaan dalam Beragam Kondisi Cuaca
st.subheader("Penyewaan dalam Beragam Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.boxplot(
    x="weathersit_daily", 
    y="hum_daily",
    data=data_gabung,
    palette=colors,
    ax=ax
)
ax.set_title("Pengaruh Kondisi Cuaca Terhadap Jumlah Sewa Sepeda Harian", loc="center", fontsize=30)
ax.set_ylabel("Jumlah Sewa Sepeda Harian")
ax.set_xlabel("Kondisi Cuaca")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.text("Penyewaan sepeda lebih banyak dilakukan pada saat cuaca cerah, sedikit berawan, dan berawan sebagian. Serta tidak ada penyewaan sepeda pada saat kondisi ekstrem.")

# Gambaran Penyewaan dalam Kondisi Libur dan Kerja
st.subheader("Penyewaan dalam Kondisi Libur dan Kerja")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.boxplot(
    x="workingday_daily", 
    y="cnt_daily",
    data=data_gabung,
    palette=colors,
    ax=ax
)
ax.set_title("Perbedaan Antara Hari Kerja dan Hari Libur dalam Jumlah Sewa Sepeda Harian", loc="center", fontsize=30)
ax.set_ylabel("Jumlah Sewa Sepeda Harian")
ax.set_xlabel("Workingday")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.text("Tidak ada perbedaan signifikan antara rata-rata peminjaman pada saat hari kerja dibandingkan dengan hari libur sedangkan secara jumlah lebih banyak saat hari kerja. Hal ini dapat disebabkan karena penyewaan sepeda dilakukan untuk mobilitas ke tempat kerja.")

# Clustering dengan K-Means
clustering = pd.DataFrame()
clustering["kelembapan"] = data_gabung["hum_daily"]
clustering["temperatur"] =  data_gabung["temp_daily"]

# Menjalankan K-means dengan 2 kelompok
kmeans = KMeans(n_clusters=2, random_state=42)
clustering['Cluster'] = kmeans.fit_predict(clustering)

st.subheader("Clustering Kelompok Penyewaan Berdasarkan Humiditas dan Temperatur")
fig, ax = plt.subplots(figsize=(20, 10))
sns.scatterplot(
    x="kelembapan", 
    y="temperatur",
    data=clustering,
    ax=ax, 
    hue="Cluster"
)
ax.set_title("Pengelompokan Data Perjalanan Sepeda", loc="center", fontsize=30)
ax.set_ylabel("Temperatur")
ax.set_xlabel("Kelembapan")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.text("Terlihat terdapat dua kelompok besar dalam pengelompokan penyewaan sepeda berdasarkan kriteria kelembapan dan temperatur dengan metode K-Means.")