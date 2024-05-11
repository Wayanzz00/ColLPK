import pandas as pd
import streamlit as st
import numpy as np

col1, col2, col3 = st.columns([1, 2, 0.5])
with col3:
    st.markdown=st.page_link("Home.py", label="Home")

with col2:
    st.title ("Alkalimetri")
    
# Fungsi untuk menghitung konsentrasi
def konsentrasi(gram, volume, BE):
    try:
        result = gram / (volume * BE)
        return result
    except ZeroDivisionError:
        return "Error: Silakan masukkan nilai yang valid (Kolom tidak boleh nol)."

# Fungsi untuk menghasilkan jawaban dari input pengguna
def materi_utama(materi):
    options = {
        "Pengertian Alkalimetri": "Alkalimetri adalah titrasi yang dilakukan dengan menggunakan larutan titran yang bersifat basa dan menggunakan larutan baku primer yang bersifat asam. Dari volume larutan baku asam yang diperlukan untuk mencapai titik akhir titrasi, konsentrasi larutan basa dapat dihitung menggunakan stoikiometri reaksi titrasi yang terjadi.",
        "Pemilihan Indikator": "Indikator yang ideal untuk titrasi alkalimetri adalah indicator dengan perubahan warna di sekitar pH titik ekivalensi ( pH di mana jumlah ekivalen asam dan basa dalam larutan menjadi sama). Contoh titik ekivalensi dalam titrasi NaOH dengan asam oksalat terjadi ketika asam oksalat sepenuhnya bereaksi dengan NaOH membentuk garam oksalat dan air. Salah satu pilihan yang umum digunakan adalah fenolftalein. Yang merupakan indikator yang berubah warna dari semula tidak berwarna menjadi merah muda seulas di kisaran pH 8,2 - 10, sehingga sesuai untuk menandai titik akhir titrasi NaOH dengan asam oksalat.",
        "Reaksi Umum": """Reaksi umum yang terjadi dalam standardisasi larutan NaOH dengan Asam Oksalat adalah :

    2 NaOH (aq) + H2C2O4 (aq) -> Na2C2O4 (aq) + 2 H2O (l)

    Dengan Natrium Hidroksida bereaksi dengan Asam Oksalat (H2C2O4) menghasilkan Natrium Oksalat (Na2C2O4).""",
        "Rumus Perhitungan Normalitas": """Rumus untuk menghitung normalitas (N) adalah :
        
    N(titran) = massa titrat(mg)/(BE(titrat) x Volume Akhir(mL))
        
    Notes : 
        ~ N adalah Normalitas (mgrek/mL)
        ~ BE adalah Berat ekuivalen titrat(mg/mgrek)
        ~ V adalah Volume akhir titrasi (mL)"""
    }

    return options.get(materi)

# Fungsi untuk menghitung mean dan standard deviation
def data_pengamatan(df, nama_column, mean, std_dev):
    # Ekstrak Spesifik Kolom
    column_data = df[nama_column]

    # Fungsi untuk menghitung Mean, Standar Deviasi dan %RSD
    hasil_mean = np.mean(column_data)
    hasil_std_dev = np.std(column_data)
    hasil_rsd = (hasil_std_dev / hasil_mean) * 100 if hasil_mean != 0 else 0
    
     # Desimal Hasil Akhir
    hasil_mean = round(hasil_mean, 4)
    hasil_rsd = round(hasil_rsd, 2)
    hasil_std_dev = round(hasil_std_dev, 6)

    # Menampilkan Hasil Kalkulasi
    st.success(f"Rata-rata dari {nama_column}: {hasil_mean}")
    st.success(f"Standar Deviasi dari {nama_column}: {hasil_std_dev}")
    st.success(f"%RSD dari {nama_column}: {hasil_rsd}%")
    
def main():
    
    # Pilihan konten menggunakan selection box
    selected_content = st.radio(
        "Pilih konten :",
        ["Materi Utama", "Kalkulator Konsentrasi", "Kalkulasi %RSD"],
        horizontal=True,
    )

    # Tampilk konten terkait
    if selected_content == "Kalkulator Konsentrasi":
        st.header("Kalkulator Konsentrasi")
        gram = st.number_input("Masukkan jumlah massa (mg):", min_value=0.00)
        volume = st.number_input("Masukkan volume (mL):", min_value=0.00)
        BE = st.number_input("Masukkan nilai BE Titrat:", min_value=0.00)
        if st.button("Kalkulasi"):
            if gram == 0 or volume == 0 or BE == 0:
                st.error("Pastikan untuk mengisi semua nilai.")
            else:
                result = konsentrasi(gram, volume, BE)
                result_rounded = round(result, 4)
                st.success(f"Hasil perhitungan Normalitas : {result_rounded} N")
            
    elif selected_content == "Materi Utama":
        st.header("Materi Utama")
        user_input = st.selectbox("Pilih topik : ", ["Pengertian Alkalimetri", "Pemilihan Indikator", "Reaksi Umum", "Rumus Perhitungan Normalitas"])
        if st.button("Kirim"):
            response = materi_utama(user_input)
            text_area_height = min(max(len(response.split('\n')) * 20, 200), 600)  # Adjust height dynamically
            st.text_area("💸 Penjawab", value=response, height=text_area_height, disabled=True)
        
      
    elif selected_content == "Kalkulasi %RSD":
        st.header("Kalkulasi %RSD")

        # Table Data Pengamatan
        data = {
            "Sample (mg)": [0.00, 0.00, 0.00],
            "Volume Titran (mL)": [0.00, 0.00, 0.00],
            "Normalitas Titran (N)": [0.00, 0.00, 0.00]
        }
        df = pd.DataFrame(data)

        # Definisi dari fungsi
        mean = st.write()
        std_dev = st.write()

        # Input judul kolom untuk dikalkulasi
        column_index = st.selectbox("Pilih kolom untuk dikalkulasi :", df.columns)

        # Edit Spesifik Kolom
        st.sidebar.header("Edit Specific Column")
        selected_columns = []
        for column in df.columns:
            if st.sidebar.checkbox(f"Edit {column}", value=True, key=column):
                selected_columns.append(column)

        updated_df = df.copy()
        if len(selected_columns) > 0:
            df_edit = df[selected_columns]
            edited_df = st.data_editor(df_edit)
            if st.button("Kalkulasi"):
                for column in selected_columns:
                    updated_df[column] = edited_df[column]

                # Kalkulasi melalui fungsi data_pengamatan
                data_pengamatan(updated_df, column_index, mean, std_dev)

if __name__ == "__main__":
    main()
