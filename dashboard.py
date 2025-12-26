import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi
st.set_page_config(page_title="Dashboard Bike Sharing", layout="wide")
st.title("🚲 Dashboard Analisis Bike Sharing")
st.write("Analisis penyewaan sepeda berdasarkan waktu, musim, dan kondisi cuaca.")

st.markdown("""
Keadaan Data
- Duplikasi = 0 (tidak ada)
- Missing Value = 0 (Tidak ada)
- Tidak butuh Transformasi data (koreksi jika salah)

Penjelasan Kolom yang dimiliki beserta maksud dari setiap Kolom tersebut
- dteday = Tanggal
- season = Musim pada tanggal tersebut (1=Spring, 2=Summer, 3=Fall, 4=Winter)
- yr = Tahun (0=2011, 1=2012 data ini tersedia hanya dari tahun 2011 - 2012)
- mnth = Bulan (1–12) konteks nya sama kayak bulan januari - Desember
- holiday = Apakah hari libur pada tanggal tersebut (0=tidak, 1=ya)
- weekday = Hari tanggal tersebut (0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday)
- workingday = Hari kerja atau bukan (0=tidak, 1=ya)
- weathersit = Kondisi cuaca (1=cuaca bagus, 2=cuaca sedang, 3=cuaca buruk)
- temp = Suhu yang sudah di normalisasi menjadi celcius
- atemp = Suhu terasa (celcius)
- hum = Kelembapan udara (0 sampai 1)
- windspeed = Kecepatan angin
- casual = Penyewa non-member
- registered = Penyewa member
- cnt = Total peminjaman
""")

# Load Data]
@st.cache_data
def load_day():
    df = pd.read_csv(r"day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["year"] = df["dteday"].dt.year
    df["month"] = df["dteday"].dt.month
    return df

@st.cache_data
def load_hour():
    return pd.read_csv(r"hour.csv")

FramePertama = load_day()
FrameKedua = load_hour()

# Mapping
month_map = {
    1: 'Januari', 
    2: 'Februari', 
    3: 'Maret', 
    4: 'April',
    5: 'Mei', 
    6: 'Juni', 
    7: 'Juli', 
    8: 'Agustus',
    9: 'September', 
    10: 'Oktober', 
    11: 'November', 
    12: 'Desember'
}

weather_category = {
    1: 'Baik',
    2: 'Sedang',
    3: 'Buruk',
    4: 'Buruk Sekali'
}

season_map = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

# Tambahan kolom
FramePertama['year'] = FramePertama['dteday'].dt.year
FramePertama['month'] = FramePertama['dteday'].dt.month
FramePertama['weather_category'] = FramePertama['weathersit'].map(weather_category)

# Prepare untuk Visual
perbulan_tahun = (FramePertama.groupby(['year', 'month'])['cnt'].sum().reset_index())

data_2011 = perbulan_tahun[perbulan_tahun['year'] == 2011]
data_2012 = perbulan_tahun[perbulan_tahun['year'] == 2012]

total_2011 = data_2011['cnt'].sum()
total_2012 = data_2012['cnt'].sum()

weather_full_2011 = (FramePertama[FramePertama['year'] == 2011].groupby(['season', 'month', 'weather_category']).agg(day_total=('cnt', 'size'),total_rental=('cnt', 'sum'),rata_perhari=('cnt', 'mean'),).reset_index())
weather_full_2011['season_name'] = weather_full_2011['season'].map(season_map)
weather_full_2011['bulan'] = weather_full_2011['month'].map(month_map)

weather_full_2012 = (FramePertama[FramePertama['year'] == 2012].groupby(['season', 'month', 'weather_category']).agg(day_total=('cnt', 'size'),total_rental=('cnt', 'sum'),rata_perhari=('cnt', 'mean'),).reset_index())
weather_full_2012['season_name'] = weather_full_2012['season'].map(season_map)
weather_full_2012['bulan'] = weather_full_2012['month'].map(month_map)

tahun2011 = FramePertama[FramePertama['year'] == 2011].groupby('month')['cnt'].sum().reset_index()
total_2011 = FramePertama[FramePertama['year'] == 2011]['cnt'].sum()
tahun2011['bulan'] = tahun2011['month'].map(month_map)

tahun2012 = FramePertama[FramePertama['year'] == 2012].groupby('month')['cnt'].sum().reset_index()
total_2012 = FramePertama[FramePertama['year'] == 2012]['cnt'].sum()
tahun2012['bulan'] = tahun2012['month'].map(month_map)

cuaca_tahun = (FramePertama.groupby(['year', 'weather_category'])['cnt'].sum().reset_index())
cuaca_2011 = cuaca_tahun[cuaca_tahun['year'] == 2011]
cuaca_2012 = cuaca_tahun[cuaca_tahun['year'] == 2012]

hari_cuaca = (FramePertama.groupby(['year', 'weather_category']).size().reset_index(name='total_hari'))
hari_2011 = hari_cuaca[hari_cuaca['year'] == 2011].set_index('weather_category')
hari_2012 = hari_cuaca[hari_cuaca['year'] == 2012].set_index('weather_category')

data_bulan_cuaca2011 = (weather_full_2011.groupby(['bulan', 'weather_category'])['day_total'].sum().reset_index())
data_bulan_cuaca2012 = (weather_full_2012.groupby(['bulan', 'weather_category'])['day_total'].sum().reset_index())

rata_bulan_cuaca2011 = (weather_full_2011.groupby(['bulan', 'weather_category'])['rata_perhari'].mean().reset_index())
rata_bulan_cuaca2012 = (weather_full_2012.groupby(['bulan', 'weather_category'])['rata_perhari'].mean().reset_index())

total_bulan_cuaca2011 = (weather_full_2011.groupby(['bulan', 'weather_category'])['total_rental'].sum().reset_index())
total_bulan_cuaca2012 = (weather_full_2012.groupby(['bulan', 'weather_category'])['total_rental'].sum().reset_index())

data_juli_2011 = FrameKedua[(FrameKedua['mnth'] == 7) & (FrameKedua['season'] == 3) & (FrameKedua['yr'] == 0)]
hourly_juli = data_juli_2011.groupby('hr')['cnt'].sum().reset_index()

data_juni_2012 = FrameKedua[(FrameKedua['mnth'] == 6) & (FrameKedua['season'] == 3) & (FrameKedua['yr'] == 1)]
hourly_juni = data_juni_2012.groupby('hr')['cnt'].sum().reset_index()

data_agustus_2011 = FrameKedua[(FrameKedua['mnth'] == 8) & (FrameKedua['season'] == 3) & (FrameKedua['yr'] == 0)]
hourly_agustus = data_agustus_2011.groupby('hr')['cnt'].sum().reset_index()

data_juli_2012 = FrameKedua[(FrameKedua['mnth'] == 7) & (FrameKedua['season'] == 3) & (FrameKedua['yr'] == 1)]
hourly_juli = data_juli_2012.groupby('hr')['cnt'].sum().reset_index()

total_2011 = FramePertama[FramePertama['year'] == 2011]['cnt'].sum()
total_2012 = FramePertama[FramePertama['year'] == 2012]['cnt'].sum()
growth = ((total_2012 - total_2011) / total_2011) * 100

bulan_puncak = (FramePertama.groupby('month')['cnt'].mean().idxmax())
cuaca_dominan = (FramePertama.groupby('weather_category')['cnt'].sum().idxmax())

# Data Summary
st.subheader("📌 Ringkasan Data")

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Total Hari", len(FramePertama))
with col2:
    st.metric("Rata-rata Penyewaan / Hari", int(FramePertama["cnt"].mean()))
with col3:
    st.metric("Total Penyewaan", f"{int(FramePertama['cnt'].sum()):,}")
with col4:
    st.metric("Pertumbuhan 2011 → 2012",f"{growth:.1f}%",delta=f"+{int(total_2012 - total_2011):,}")
with col5:
    st.metric("Bulan dengan Rata-rata Tertinggi",month_map[bulan_puncak])
with col6:
    st.metric("Kondisi Cuaca Paling Dominan",cuaca_dominan)

st.caption(
    f"📌 Bulan puncak penyewaan terjadi pada **{month_map[bulan_puncak]}**, "
    f"dengan kondisi cuaca paling dominan **{cuaca_dominan}**."
)

st.subheader("Pertanyaan 1: Bagaimana tren jumlah penyewaan sepeda dari tahun 2011 - 2012?")
# Visualisasi 1: Perbandingan Penyewaan setiap tahun
st.subheader("📊 Perbandingan Total Penyewaan Sepeda per Bulan (2011 vs 2012)")
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(data_2011['month'],data_2011['cnt'],marker='o',label='2011')
ax.plot(data_2012['month'],data_2012['cnt'],marker='o',label='2012')

ax.set_title("Perbandingan Total Penyewaan Sepeda per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")

ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_map.values(), rotation=0)

ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend()

info_text = (
    f"Total Penyewaan:\n"
    f"2011: {int(total_2011):,}\n"
    f"2012: {int(total_2012):,}"
)

ax.text(
    0.02, 0.95,
    info_text,
    transform=ax.transAxes,
    va='top',
    fontsize=10,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

st.pyplot(fig)

# Visualisasi 2: Jumlah Penyewaan setiap bulan pada tahun 2011
st.subheader("📊 Detail Total Penyewaan Sepeda per Bulan (2011)")

fig, ax = plt.subplots(figsize=(15, 5))

bars2011 = ax.bar(
    tahun2011['bulan'],
    tahun2011['cnt']
)

ax.set_title("Detail Total Penyewaan Sepeda per Bulan Tahun 2011")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(axis='y', linestyle='--', alpha=0.5)

# angka di atas bar
for bar in bars2011:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{int(height):,}',
        ha='center',
        va='bottom',
        fontsize=9
    )

st.pyplot(fig)

# Visualisasi 3: Jumlah Penyewaan setiap bulan pada tahun 2012
st.subheader("📊 Detail Total Penyewaan Sepeda per Bulan (2012)")

fig, ax = plt.subplots(figsize=(15, 5))

bars2012 = ax.bar(
    tahun2012['bulan'],
    tahun2012['cnt']
)

ax.set_title("Detail Total Penyewaan Sepeda per Bulan Tahun 2012")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(axis='y', linestyle='--', alpha=0.5)

# angka di atas bar
for bar in bars2012:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{int(height):,}',
        ha='center',
        va='bottom',
        fontsize=9
    )

st.pyplot(fig)

st.subheader("Insight")
st.markdown("""
Pertumbuhan signifikan dari 2011 ke 2012
- Total penyewaan 2011: 1.243.103 kali
- Total penyewaan 2012: 2.049.576 kali

Pola musiman konsisten di kedua tahun
- Penyewaan rendah di awal tahun pada bulan Januari - Februari. walaupun ditahun 2011 lonjakan nya terjadi pada bulan April dan naik ,lagi pada bulan mei (naik secara bertahap tapi tidak secara signifikan), beda dengan tahun 2012 dimana di bulan maret langsung terjadi lonjakan penyewaan. Hal ini dapat kita tahu kalau penyewaan mulai meningkat mulai pada Maret - Mei.
- Penyewaan Puncak penyewaan terjadi di pertengahan tahun (Juni - Juli (2011) & Agustus - September (2012)), Lalu kembali menurun kembali menjelang akhir tahun (Oktober - Desember). Ini menunjukkan pengaruh kuat faktor cuaca terhadap penggunaan sepeda yang nanti bakal kita bahas di next pertanyaan.

Tahun 2012 selalu lebih tinggi di setiap bulan
- Pada setiap bulan, jumlah penyewaan 2012 selalu di atas 2011.Ini menunjukkan peningkatan bukan hanya karena satu bulan tertentu,
""")

st.subheader("Pertanyaan 2: Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?")
# Visualisai 1: Perbandingan total penyewaan disetiap cuaca per tahun
st.subheader("🌦️ Total Penyewaan Sepeda berdasarkan Kondisi Cuaca (2011 vs 2012)")

label = cuaca_2011['weather_category']
x = np.arange(len(label))
width = 0.3

fig, ax = plt.subplots(figsize=(12, 5))

bars1 = ax.bar(x - width/2, cuaca_2011['cnt'], width, label='2011')
bars2 = ax.bar(x + width/2, cuaca_2012['cnt'], width, label='2012')

for bars in (bars1, bars2):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{int(height):,}',
            ha='center',
            va='bottom',
            fontsize=9
        )

info_text = (
    "Jumlah Hari per Kondisi Cuaca\n"
    "2011:\n"
    f"- Baik   : {hari_2011.loc['Baik','total_hari']} hari\n"
    f"- Sedang : {hari_2011.loc['Sedang','total_hari']} hari\n"
    f"- Buruk  : {hari_2011.loc['Buruk','total_hari']} hari\n\n"
    "2012:\n"
    f"- Baik   : {hari_2012.loc['Baik','total_hari']} hari\n"
    f"- Sedang : {hari_2012.loc['Sedang','total_hari']} hari\n"
    f"- Buruk  : {hari_2012.loc['Buruk','total_hari']} hari"
)

ax.text(
    0.75, 0.95,
    info_text,
    transform=ax.transAxes,
    va='top',
    fontsize=9,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

ax.set_xticks(x)
ax.set_xticklabels(label)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Total Penyewaan Sepeda berdasarkan Kondisi Cuaca")
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend()

st.pyplot(fig)

# Visualisasi 2: Total hari berdasarkan cuaca per bulan pada tahun 2011
st.subheader("🌦️ Jumlah Hari Berdasarkan Kondisi Cuaca per Bulan (2011)")
bulan_order = list(month_map.values())
data_bulan_cuaca2011['bulan'] = pd.Categorical(data_bulan_cuaca2011['bulan'],categories=bulan_order,ordered=True)
pivot_bulan = (data_bulan_cuaca2011.pivot(index='bulan', columns='weather_category', values='day_total').fillna(0))

x = np.arange(len(pivot_bulan.index))
width = 0.2

fig, ax = plt.subplots(figsize=(16, 6))

for i, cuaca in enumerate(pivot_bulan.columns):
    bars = ax.bar(
        x + (i - (len(pivot_bulan.columns)-1)/2) * width,
        pivot_bulan[cuaca],
        width,
        label=cuaca
    )

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                h + 0.3,
                int(h),
                ha='center',
                va='bottom',
                fontsize=9
            )

ax.set_title("Jumlah Hari Berdasarkan Kondisi Cuaca per Bulan (2011)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Hari")

ax.set_xticks(x)
ax.set_xticklabels(pivot_bulan.index)

ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(title="Kondisi Cuaca")

season_info2011 = (
    "Keterangan Musim (2011):\n"
    "- Spring  : Januari, Februari, Maret & Desember\n"
    "- Summer  : Maret, April, Mei & Juni\n"
    "- Fall    : Juli, Agustus & September\n"
    "- Winter  : September, Oktober, November & Desember"
)

ax.text(
    0.66, 0.95,
    season_info2011,
    transform=ax.transAxes,
    va='top',
    fontsize=10,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

st.pyplot(fig)

# Visualisasi 3: Rata rata penyewaan berdasarkan cuaca per bulan pada tahun 2011
st.subheader("🌦️ Rata-rata Penyewaan Sepeda per Hari berdasarkan Kondisi Cuaca per Bulan (2011)")

rata_bulan_cuaca2011['bulan'] = pd.Categorical(rata_bulan_cuaca2011['bulan'],categories=bulan_order,ordered=True)
pivot_avg = (rata_bulan_cuaca2011.pivot(index='bulan', columns='weather_category', values='rata_perhari').fillna(0))

for c in label:
    if c not in pivot_avg.columns:
        pivot_avg[c] = 0
pivot_avg = pivot_avg[label]

x = np.arange(len(pivot_avg.index))
width = 0.15

fig, ax = plt.subplots(figsize=(20, 8))

for i, cuaca in enumerate(label):
    bars = ax.bar(
        x + (i - (len(label)-1)/2) * width,
        pivot_avg[cuaca],
        width,
        label=cuaca
    )

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                h + (0.02 * h),
                f'{int(h):,}',
                ha='center',
                va='bottom',
                fontsize=9
            )

ax.set_title(
    "Rata-rata Penyewaan Sepeda per Hari\n"
    "berdasarkan Kondisi Cuaca per Bulan (2011)"
)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan per Hari")

ax.set_xticks(x)
ax.set_xticklabels(pivot_avg.index)

ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(title="Kondisi Cuaca")

ax.text(
    0.01, 0.95,
    season_info2011,
    transform=ax.transAxes,
    va='top',
    fontsize=13,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

st.pyplot(fig)

# Visualisasi 4: Total Penyewaan berdasarkan cuaca per bulan pada tahun 2011
st.subheader("🌦️ Total Penyewaan Sepeda per Bulan berdasarkan Kondisi Cuaca (2011)")
total_bulan_cuaca2011['bulan'] = pd.Categorical(total_bulan_cuaca2011['bulan'],categories=bulan_order,ordered=True)
pivot_total = (total_bulan_cuaca2011.pivot(index='bulan', columns='weather_category', values='total_rental').fillna(0))

for c in label:
    if c not in pivot_total.columns:
        pivot_total[c] = 0
pivot_total = pivot_total[label]

x = np.arange(len(pivot_total.index))
width = 0.25

fig, ax = plt.subplots(figsize=(16, 6))

for i, cuaca in enumerate(label):
    bars = ax.bar(
        x + (i - (len(label)-1)/2) * width,
        pivot_total[cuaca],
        width,
        label=cuaca
    )

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                h + (0.01 * h),
                f'{int(h):,}',
                ha='center',
                va='bottom',
                fontsize=9
            )

ax.set_title("Total Penyewaan Sepeda per Bulan berdasarkan Kondisi Cuaca (2011)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")

ax.set_xticks(x)
ax.set_xticklabels(pivot_total.index)

ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(title="Kondisi Cuaca")

ax.text(
    0.99, 0.95,
    season_info2011,
    transform=ax.transAxes,
    va='top',
    ha='right',
    fontsize=10,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

st.pyplot(fig)

# Visualisasi 5: Total hari berdasarkan cuaca per bulan pada tahun 2012
st.subheader("🌦️ Jumlah Hari Berdasarkan Kondisi Cuaca per Bulan (2012)")
bulan_order = list(month_map.values())
data_bulan_cuaca2012['bulan'] = pd.Categorical(data_bulan_cuaca2012['bulan'],categories=bulan_order,ordered=True)
pivot_bulan = (data_bulan_cuaca2012.pivot(index='bulan', columns='weather_category', values='day_total').fillna(0))

x = np.arange(len(pivot_bulan.index))
width = 0.2

fig, ax = plt.subplots(figsize=(16, 6))

for i, cuaca in enumerate(pivot_bulan.columns):
    bars = ax.bar(
        x + (i - (len(pivot_bulan.columns)-1)/2) * width,
        pivot_bulan[cuaca],
        width,
        label=cuaca
    )

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                h + 0.3,
                int(h),
                ha='center',
                va='bottom',
                fontsize=9
            )

ax.set_title("Jumlah Hari Berdasarkan Kondisi Cuaca per Bulan (2012)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Hari")

ax.set_xticks(x)
ax.set_xticklabels(pivot_bulan.index)

ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(title="Kondisi Cuaca")

season_info2012 = (
    "Keterangan Musim (2012):\n"
    "- Spring  : Januari, Februari, Maret & Desember\n"
    "- Summer  : Maret, April, Mei & Juni\n"
    "- Fall    : Juni, Juli, Agustus & September\n"
    "- Winter  : September, Oktober, November & Desember"
)

ax.text(
    0.03, 0.95,
    season_info2012,
    transform=plt.gca().transAxes,
    va='top',
    fontsize=7,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

st.pyplot(fig)

# Visualisasi 6: Rata rata penyewaan berdasarkan cuaca per bulan pada tahun 2012
st.subheader("🌦️ Rata-rata Penyewaan Sepeda per Hari berdasarkan Kondisi Cuaca per Bulan (2012)")

rata_bulan_cuaca2012['bulan'] = pd.Categorical(rata_bulan_cuaca2012['bulan'],categories=bulan_order,ordered=True)
pivot_avg = (rata_bulan_cuaca2012.pivot(index='bulan', columns='weather_category', values='rata_perhari').fillna(0))

for c in label:
    if c not in pivot_avg.columns:
        pivot_avg[c] = 0
pivot_avg = pivot_avg[label]

x = np.arange(len(pivot_avg.index))
width = 0.15

fig, ax = plt.subplots(figsize=(20, 8))

for i, cuaca in enumerate(label):
    bars = ax.bar(
        x + (i - (len(label)-1)/2) * width,
        pivot_avg[cuaca],
        width,
        label=cuaca
    )

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                h + (0.02 * h),
                f'{int(h):,}',
                ha='center',
                va='bottom',
                fontsize=9
            )

ax.set_title(
    "Rata-rata Penyewaan Sepeda per Hari\n"
    "berdasarkan Kondisi Cuaca per Bulan (2012)"
)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan per Hari")

ax.set_xticks(x)
ax.set_xticklabels(pivot_avg.index)

ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(title="Kondisi Cuaca")

ax.text(
    0.01, 0.95,
    season_info2012,
    transform=plt.gca().transAxes,
    va='top',
    fontsize=10,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

st.pyplot(fig)

# Visualisasi 7: Total penyewaan berdasarkan cuaca per bulan pada tahun 2012
st.subheader("🌦️ Total Penyewaan Sepeda per Bulan berdasarkan Kondisi Cuaca (2011)")
total_bulan_cuaca2011['bulan'] = pd.Categorical(total_bulan_cuaca2011['bulan'],categories=bulan_order,ordered=True)
pivot_total = (total_bulan_cuaca2011.pivot(index='bulan', columns='weather_category', values='total_rental').fillna(0))

for c in label:
    if c not in pivot_total.columns:
        pivot_total[c] = 0
pivot_total = pivot_total[label]

x = np.arange(len(pivot_total.index))
width = 0.25

fig, ax = plt.subplots(figsize=(16, 6))

for i, cuaca in enumerate(label):
    bars = ax.bar(
        x + (i - (len(label)-1)/2) * width,
        pivot_total[cuaca],
        width,
        label=cuaca
    )

    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                h + (0.01 * h),
                f'{int(h):,}',
                ha='center',
                va='bottom',
                fontsize=9
            )

ax.set_title("Total Penyewaan Sepeda per Bulan berdasarkan Kondisi Cuaca (2011)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")

ax.set_xticks(x)
ax.set_xticklabels(pivot_total.index)

ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(title="Kondisi Cuaca")

ax.text(
    0.03, 0.95,
    season_info2012,
    transform=plt.gca().transAxes,
    va='top',
    fontsize=7,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        edgecolor='red'
    )
)

st.pyplot(fig)

st.subheader("Insight")
st.markdown("""
Dominasi Cuaca terletak pada Cuaca Baik
- Di kedua tahun (2011 & 2012), penyewaan menunjukan bahwa Cuaca Baik menempati posisi tertinggi, disusul oleh Cuaca Sedang, dan Cuaca Buruk di posisi terendah. Kondisi cuaca buruk menyebabkan penurunan drastis, di mana rata rata penyewaan bisa kehilangan 40% hingga 75% potensi penyewaan dibandingkan saat cuaca baik dan sedang. kita dari sini tahu bahwa pengaruh cuaca yang buruk memungkinkan individu lebih memilih transportasi lain untuk menghindari terjadinya hal yang tidak baik

Titik Puncak Musim Terbaik
- Titik penyewaan tertinggi terjadi pada rentang Juni - Juli (2011) dan Agustus - September (2012).
- Pada rentang bulan tersebut ini cuaca buruk tidak ditemukan (0 hari). Ketiadaan risiko hujan/salju pada bulan-bulan tersebut menjadi pendorong utama masyarakat untuk memilih melakukan penyewaan sepeda
- Musim Summer dan Fall adalah musim yang sangat mendukung para individu untuk melakuakn penyewaans sepeda dimana, dengan musim Fall (Gugur) menjadi periode yang paling dominan karena kondisi udara yang lebih mendukung untuk aktivitas luar ruangan secara berkelanjutan.

Pengaruh Cuaca pada Rata-Rata Harian Penyewaan
- Tahun 2011: Memasuki Mei hingga Oktober, rata-rata penyewaan harian pada kondisi cuaca baik secara konsisten melampaui angka 4.000 unit/hari.
- Tahun 2012: Terjadi peningkatan lebih signifikasn dari Maret hingga November rata-rata harian meningkat ke angka 5.000 unit/hari dengan periode yang lebih panjang.
- Simpel nya pada tahun 2012 menunjukkan adanya peningkatan kepercayaan dan kebiasaan pengguna (user behavior) yang semakin kuat.

Karakteristik Musim Transisi & Ekstrem
- Musim Summer & Fall Pada musim Summer dan terutama Fall menjadi yang paling dominan karena kombinasi cuaca baik dengan suhu yang sejuk (tidak terlalu panas seperti Summer), sehingga rata-rata penyewaan harian tetap tinggi meskipun langit sedang mendung (Cuaca Sedang). Di musim ini, meskipun terjadi cuaca "Sedang", masyarakat tetap antusias bersepeda karena risiko hujan mendadak sangat kecil
- Frekuensi cuaca buruk berada pada Musim Winter Selain cuaca buruk, suhu ekstrem di musim dingin membuat cuaca "Baik" sekalipun tetap tidak menarik bagi pengguna. Akibatnya, saat cuaca buruk tiba, penyewaan bisa menurun.
- Musim Spring adalah masa transisi. Angka penyewaan di musim ini mulai naik dibandingkan Winter seiring munculnya lebih banyak hari dengan cuaca "Baik", namun belum bisa menyamai Summer/Fall karena masih berada pada posisi pemulihan dari winter.

Pengaruh Kondisi Cuaca Per Musim
- Pada Musim Puncak (Summer/Fall): Cuaca "Sedang" (mendung) tidak terlalu menurunkan minat orang. Data menunjukkan rata-rata harian pada cuaca sedang di musim ini masih sangat tinggi (bahkan menembus 6.000+ di Sept 2012).
- Pada Musim Rendah (Winter/Spring): Cuaca "Sedang" atau "Buruk" berdampak double hit. Pengguna sudah enggan karena suhu dingin, ditambah lagi dengan kondisi langit yang tidak cerah, sehingga mereka lebih memilih moda transportasi tertutup.
""")

st.subheader("Analisis pola penyewaan jam")
# Visualisasi 1: Perbandingan penyewaan di bulan puncak tertinggi penyewaan (Musim Fall) Juli (2011) & Juni (2012)
st.subheader("⏰ Total Penyewaan per Jam di Awal Bulan pada Musim Fall")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hourly_juli['hr'],hourly_juli['cnt'],marker='o',label='Juli 2011 (Awal Musim Fall)',color='blue')
ax.plot(hourly_juni['hr'],hourly_juni['cnt'],marker='o',label='Juni 2012 (Awal Musim Fall)',color='orange')

for x, y in zip(hourly_juli['hr'], hourly_juli['cnt']):
    ax.text(
        x,
        y + 150,
        f'{int(y):,}',
        ha='center',
        va='bottom',
        fontsize=8,
        color='blue'
    )

for x, y in zip(hourly_juni['hr'], hourly_juni['cnt']):
    ax.text(
        x,
        y + 150,
        f'{int(y):,}',
        ha='center',
        va='bottom',
        fontsize=8,
        color='orange'
    )

ax.set_title("Total Penyewaan per Jam di Awal Bulan pada Musim Fall", fontsize=14)
ax.set_xlabel("Jam (0–23)", fontsize=12)
ax.set_ylabel("Total Penyewaan (cnt)", fontsize=12)

ax.set_xticks(range(0, 24))
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)

st.pyplot(fig)

# Visualisasi 2: Perbandingan 1 bulan kemudian penyewaan (Musim Fall) Agustus (2011) & Juli (2012)
st.subheader("⏰ Total Penyewaan per Jam di Awal Bulan pada Musim Fall (Agustus 2011 vs Juli 2012)")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hourly_agustus['hr'],hourly_agustus['cnt'],marker='o',label='Agustus 2011',color='blue')
ax.plot(hourly_juli['hr'],hourly_juli['cnt'],marker='o',label='Juli 2012',color='orange')

for x, y in zip(hourly_agustus['hr'], hourly_agustus['cnt']):
    ax.text(
        x,
        y + 150,
        f'{int(y):,}',
        ha='center',
        va='bottom',
        fontsize=8,
        color='blue'
    )


for x, y in zip(hourly_juli['hr'], hourly_juli['cnt']):
    ax.text(
        x,
        y + 150,
        f'{int(y):,}',
        ha='center',
        va='bottom',
        fontsize=8,
        color='orange'
    )

ax.set_title("Total Penyewaan per Jam di Awal Bulan pada Musim Fall", fontsize=14)
ax.set_xlabel("Jam (0–23)", fontsize=12)
ax.set_ylabel("Total Penyewaan (cnt)", fontsize=12)

ax.set_xticks(range(0, 24))
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)

st.pyplot(fig)

st.subheader("Insight")
st.markdown("""
Pola Waktu penyewaan
- Lonjakan Penyewaan Terjadi tajam pada pukul 08:00. Hal ini mengindikasikan bahwa sepeda menjadi pilihan transportasi utama bagi masyarakat sekitar untuk berangkat beraktivitas atau bekerja diawal pagi mereka
- Aktivitas Jam Kerja Setelah pukul 08:00 hingga sore hari, angka penyewaan cenderung stabil di bawah level jam sibuk. Ini menunjukkan bahwa mayoritas pengguna sedang berada dalam durasi kerja tetap, sehingga mobilitas di luar ruangan berkurang secara signifikan.
- Puncak Tertinggi pada saat Tren mencapai titik maksimalnya pada pukul 17:00 hingga 18:00. Tingginya angka pada jam ini kemungkinan besar disebabkan oleh perilaku pengguna yang menghindari kepadatan transportasi umum dan kemacetan jalan raya saat jam pulang kantor dengan memilih bersepeda.
- Setelah pukul 19:00 tingkat penyewaan menurun secara bertahap seiring dengan jam kerja pulang kerja
""")

st.subheader("Conclusion")
st.markdown("""
Conclution pertanyaan 1
- Peningkatan total penyewaan dari 1,24 juta menjadi 2,05 juta (kenaikan sekitar 65%) menunjukkan bahwa layanan bike sharing ini sedang dalam fase pertumbuhan yang sangat sehat. Kenaikan yang konsisten di setiap bulan (di mana 2012 selalu lebih tinggi dari 2011) membuktikan bahwa ini bukan sekadar tren sesaat, melainkan adanya peningkatan basis pengguna aktif atau loyalitas pelanggan yang kuat.
-Pola Musiman yang Terprediksi
Meskipun ada perbedaan titik lonjakan dimana awal Tahun: Masa persiapan/transisi, tengah Tahun: Masa puncak operasional (Peak Season) dan Akhir Tahun: Masa penurunan. Konklusi ini sangat penting untuk perencanaan stok sepeda, jadwal perawatan (maintenance), dan alokasi staf lapangan.

Conclution pertanyaan 2
- Cuaca adalah "Penentu Utama" penyewaan, Kondisi cuaca bukan sekadar faktor pendukung, melainkan penentu kelangsungan operasional. Cuaca buruk menyebabkan kehilangan potensi pendapatan. Hal ini menunjukkan bahwa bisnis penyewaan sepeda sangat rentan terhadap risiko eksternal iklim, di mana pengguna secara sadar memprioritaskan keamanan dan kenyamanan transportasi tertutup saat kondisi tidak kondusif.
- The Golden Pendapatan berada pada Musim Fall dan Musim Panas Summer dimana Musim Fall adalah periode emas bagi bisnis ini. Kesimpulan unik yang bisa diambil adalah kenyamanan suhu lebih penting daripada sekadar langit cerah. Pada Musim Gugur, udara yang sejuk membuat pengguna tetap mau bersepeda meskipun cuaca sedang mendung (Cuaca Sedang). Sebaliknya, pada Musim Dingin (Winter), langit cerah sekalipun tidak cukup untuk menarik minat karena faktor suhu ekstrem. Ini membuktikan adanya ambang batas toleransi fisik pengguna terhadap cuaca.
- Efek pada Musim Transisi dimana Musim dingin dan musim semi membawa resiko pada bisnis dimana secara psikologis pengguna yang masih dalam fase "pemulihan" dari suhu ekstrem membuat sensitivitas terhadap cuaca menjadi sangat tinggi. Satu hari cuaca buruk di musim dingin berdampak jauh lebih fatal bagi total pendapatan bulanan dibandingkan satu hari cuaca buruk di musim panas.

Conclution tambahan
- Penggunaan Sepeda disini berfungsi sebagai transportasi yang bukan sekadar alat rekreasi. Pola penyewaan yang dimiliki pada jam 08:00 dan 17:00 - 18:00 adalah karakteristik khas pergerakan pekerja atau pelajar menjadikan sepeda sebagai pilihan transportasi.
- Stabilitas angka penyewaan di bawah level jam sibuk antara pukul 09:00 hingga 16:00 memberikan informasi operasional yang pentin dimana tim lapangan dapat memindahkan sepeda dari stasiun yang penuh ke stasiun yang kosong tanpa mengganggu mayoritas pengguna yang sedang bekerja.
- Penurunan Bertahap setelah Jam 19:00 Penggunaan setelah jam ini kemungkinan besar bersifat opsional atau rekreasi ringan.
""")

st.subheader("Recomendation & Strategy")
st.markdown("""
Rekomendasi & Strategi pada layanan ini
- Optimasi Maintenance, Lakukan perawatan besar-besaran pada sepeda di bulan Januari - Februari (saat permintaan rendah) agar seluruh sepeda siap saat lonjakan mulai terjadi di bulan Maret.
- Manajemen Kapasitas & Optimalisasi, memastikan ketersediaan sepeda di stasiun-stasiun populer mencapai titik maksimal pada bulan Agustus - September untuk menghindari hilangnya potensi individu akibat kehabisan sepeda.
- Loyalty Program di Musim Winter, Untuk mengatasi efek Double Hit di musim winter atau summer, perusahaan bisa memberikan diskon khusus kayak "Pejuang Musim Dingin" bagi pengguna rutin agar angka penyewaan tidak jatuh terlalu drastis.
- Optimalisasi Stok di Jam Kritis, Memastikan pada pukul 07:30 stasiun di area pemukiman memiliki ketersediaan sepeda maksimal, dan pada pukul 16:30 stasiun di area perkantoran/pusat bisnis sudah terisi penuh untuk menyambut lonjakan pulang kantor.
- Pembuatan atau Perbaikan Infrastruktur Jalur Sepeda, Hasil ini bisa digunakan untuk memberi masukan kepada pengelola kota bahwa jalur sepeda sangat krusial pada rute-rute perkantoran karena terbukti mampu memecah kepadatan transportasi umum di jam sibuk.
""")

st.title("""
Mengenai dokumentasi lain bisa dilihat pada .ipynb, laporan singkat .pdf, .txt dan readme yang sudah dibuat
""")