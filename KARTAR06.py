from datetime import datetime
import io
import pandas as pd
import pytz
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Konfigurasi halaman
st.set_page_config(
    page_title="Aplikasi Toko Sembako - Karang Taruna", layout="wide"
)

# Fitur Auto-Refresh setiap 1 detik agar jam digital berjalan real-time
st_autorefresh(interval=1000, key="datetimerefresh")

# Zona Waktu Indonesia Barat (WIB)
wib_tz = pytz.timezone("Asia/Jakarta")

# Konversi hari ke Bahasa Indonesia
days_indo = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu",
}

# Inisialisasi Data Stok Produk Sembako Gen Z Karang Taruna
if "stok" not in st.session_state:
  st.session_state.stok = {
      "Telur Horn": {
          "kategori": "Telur",
          "satuan": "Kg",
          "harga_beli": 21000,
          "harga_jual": 24000,
          "stok": 100,
      },
      "Telur Omega": {
          "kategori": "Telur",
          "satuan": "Kg",
          "harga_beli": 23000,
          "harga_jual": 26000,
          "stok": 80,
      },
      "Minyak Fortune 2L": {
          "kategori": "Minyak",
          "satuan": "Pouch",
          "harga_beli": 38000,
          "harga_jual": 42000,
          "stok": 50,
      },
      "Minyak Sania 2L": {
          "kategori": "Minyak",
          "satuan": "Pouch",
          "harga_beli": 38000,
          "harga_jual": 42000,
          "stok": 50,
      },
      "Minyak Tropical 2L": {
          "kategori": "Minyak",
          "satuan": "Pouch",
          "harga_beli": 39000,
          "harga_jual": 43000,
          "stok": 40,
      },
      "Minyak Sunco 2L": {
          "kategori": "Minyak",
          "satuan": "Pouch",
          "harga_beli": 40000,
          "harga_jual": 44000,
          "stok": 30,
      },
      "Beras Punokawan 10kg": {
          "kategori": "Beras",
          "satuan": "Sak",
          "harga_beli": 145000,
          "harga_jual": 155000,
          "stok": 25,
      },
      "Beras Lahap 5kg": {
          "kategori": "Beras",
          "satuan": "Sak",
          "harga_beli": 72000,
          "harga_jual": 78000,
          "stok": 30,
      },
      "Beras Lahap 10kg": {
          "kategori": "Beras",
          "satuan": "Sak",
          "harga_beli": 145000,
          "harga_jual": 155000,
          "stok": 25,
      },
  }

if "riwayat" not in st.session_state:
  st.session_state.riwayat = []

st.title("🛒 Aplikasi Manajemen & Penjualan - GEN Z KARANG TARUNA")

# --- JAM DIGITAL & HARI BERJALAN (AKURAT SESUAI WIB) ---
st.sidebar.header("🕒 Waktu Sistem")
now_wib = datetime.now(wib_tz)
hari_eng = now_wib.strftime("%A")
hari_id = days_indo.get(hari_eng, hari_eng)
tanggal_str = now_wib.strftime("%Y-%m-%d")
jam_str = now_wib.strftime("%H:%M:%S")

st.sidebar.markdown(f"**📅 {hari_id}, {tanggal_str}**")
st.sidebar.markdown(f"**⏰ Jam: {jam_str} WIB**")

st.sidebar.markdown("---")
st.sidebar.header("Navigasi Menu")
menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Dashboard & Stok", "Catat Transaksi (Masuk/Keluar)", "Laporan & Analisis"],
)

if menu == "Dashboard & Stok":
  st.header("📦 Status Stok & Harga Barang")
  data_tabel = []
  for nama, info in st.session_state.stok.items():
    data_tabel.append({
        "Nama Produk": nama,
        "Kategori": info["kategori"],
        "Satuan": info["satuan"],
        "Harga Beli (Rp)": info["harga_beli"],
        "Harga Jual (Rp)": info["harga_jual"],
        "Stok Tersedia": info["stok"],
    })
  df_stok = pd.DataFrame(data_tabel)
  st.dataframe(df_stok, use_container_width=True)

  # Tombol Download Stok ke Excel
  buffer_stok = io.BytesIO()
  with pd.ExcelWriter(buffer_stok, engine="openpyxl") as writer:
    df_stok.to_excel(writer, index=False, sheet_name="Data Stok")

  st.download_button(
      label="📥 Ekspor Stok (.xlsx)",
      data=buffer_stok.getvalue(),
      file_name="Laporan_Stok_GenZ_KarangTaruna.xlsx",
      mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  )

elif menu == "Catat Transaksi (Masuk/Keluar)":
  st.header("📝 Catat Barang Masuk & Keluar")
  jenis = st.radio(
      "Jenis Transaksi", ["Barang Masuk (Restock)", "Barang Keluar (Penjualan)"]
  )
  produk = st.selectbox("Pilih Produk", list(st.session_state.stok.keys()))
  jumlah = st.number_input("Jumlah", min_value=1, step=1)
  ket = st.text_input("Keterangan (Opsional)")

  if st.button("Simpan Transaksi"):
    waktu_wib = datetime.now(wib_tz)
    nama_hari = days_indo[waktu_wib.strftime("%A")]
    waktu = (
        f"{nama_hari}, "
        + waktu_wib.strftime("%Y-%m-%d")
        + " "
        + waktu_wib.strftime("%H:%M:%S")
    )

    if jenis == "Barang Masuk (Restock)":
      st.session_state.stok[produk]["stok"] += jumlah
      st.session_state.riwayat.append({
          "Waktu & Hari": waktu,
          "Jenis": "Masuk",
          "Produk": produk,
          "Jumlah": jumlah,
          "Total": jumlah * st.session_state.stok[produk]["harga_beli"],
          "Ket": ket,
      })
      st.success("Stok berhasil ditambahkan!")
      st.rerun()
    else:
      if jumlah > st.session_state.stok[produk]["stok"]:
        st.error("Stok tidak mencukupi!")
      else:
        st.session_state.stok[produk]["stok"] -= jumlah
        st.session_state.riwayat.append({
            "Waktu & Hari": waktu,
            "Jenis": "Keluar",
            "Produk": produk,
            "Jumlah": jumlah,
            "Total": jumlah * st.session_state.stok[produk]["harga_jual"],
            "Ket": ket,
        })
        st.success("Penjualan berhasil dicatat!")
        st.rerun()

elif menu == "Laporan & Analisis":
  st.header("📊 Laporan Penjualan & Riwayat Stok")
  if st.session_state.riwayat:
    df_riwayat = pd.DataFrame(st.session_state.riwayat)
    st.dataframe(df_riwayat, use_container_width=True)

    # Tombol Download Riwayat Transaksi ke Excel
    buffer_riwayat = io.BytesIO()
    with pd.ExcelWriter(buffer_riwayat, engine="openpyxl") as writer:
      df_riwayat.to_excel(writer, index=False, sheet_name="Riwayat Transaksi")

    st.download_button(
        label="📥 Ekspor Riwayat (.xlsx)",
        data=buffer_riwayat.getvalue(),
        file_name="Riwayat_Transaksi_GenZ_KarangTaruna.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
  else:
    st.info(
        "Belum ada riwayat transaksi. Silakan catat transaksi terlebih dahulu."
    )