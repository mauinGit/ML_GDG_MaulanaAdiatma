# 🚲 Dashboard Analisis Bike Sharing

## 📌 Deskripsi Proyek
Tugas ini dilakukan untuk memenuhi assignment pada tugas Machine Learning GDG Batch 2025/2026 disini saya membuat sebuah  dashboard analisis berdasarkan data **Bike Sharing** yang dibangun menggunakan **Streamlit**.  Dashboard ini bertujuan untuk menyajikan hasil analisis data penyewaan sepeda secara visual namun tidak sampai ke tahap machine learning. Tapi disini saya berfokus pada **tren waktu**, **pengaruh kondisi cuaca**, serta **pola penggunaan per jam**. Hasil analisis diharapkan dapat membantu memahami faktor-faktor yang memengaruhi tingkat penyewaan sepeda.

## 📊 Dataset yang Digunakan
Dataset yang digunakan merupakan **Bike Sharing Dataset** yang terdiri dari dua file utama:
1. **`day.csv`**  
   Berisi data penyewaan sepeda harian, termasuk:
   - tanggal (`dteday`)
   - tahun (`year`)
   - bulan (`month`)
   - kondisi cuaca (`weathersit`)
   - total penyewaan (`cnt`)

2. **`hour.csv`**  
   Berisi data penyewaan sepeda per jam, termasuk:
   - jam (`hr`)
   - bulan (`mnth`)
   - musim (`season`)
   - total penyewaan (`cnt`)

note: detail penjelasan tiap kolom bisa ditelusuri di hasil yang sudah di deploy atau melihat di code nya langsung

## ⚙️ Cara Menjalankan Proyek
### 1️⃣ Menjalankan Notebook (Opsional)
Jika ingin menjalankan analisis awal menggunakan notebook:

```bash
pip install -r requirements.txt
```
```bash
streamlit run dashboard.py
```
```bash
http://localhost:8501
```

Akses Dashboard Online
Dashboard ini juga telah dideploy menggunakan Streamlit Cloud sehingga dapat diakses secara online melalui tautan berikut:
```bash
https://explore-7zafjtjstappkcmopr4qd9p.streamlit.app/
```

Beberapa insight utama yang diperoleh dari analisis data antara lain:
1. Terjadi peningkatan signifikan jumlah penyewaan sepeda dari tahun 2011 ke 2012.
2. Pola penyewaan menunjukkan tren musiman, dengan peningkatan pada pertengahan tahun dan penurunan di awal serta akhir tahun.
3. Kondisi cuaca memiliki pengaruh besar terhadap jumlah penyewaan, di mana cuaca Baik menghasilkan penyewaan tertinggi.
4. Analisis per jam menunjukkan adanya jam sibuk pada pagi dan sore hari, yang mengindikasikan penggunaan sepeda untuk aktivitas rutin.
Dari hasil insight yang ditemukan saya memberikan beberapa rekomendasi dan strategi untuk lebih memaksimalkan bisnis sepeda tersebut dengan keadaan yang ada saat ini

## 🖼️ Screenshot Dashboard
Tampilan awal (detail lebih lanjut bisa lihat di streamlit yang sudah di Deploy
![Preview Dashboard](img/home description.png)
![Preview Dashboard](img/down description.png)
