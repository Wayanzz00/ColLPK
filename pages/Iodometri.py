import pandas as pd
import streamlit as st
import numpy as np

col1, col2, col3 = st.columns([1, 2, 0.5])
with col3:
    st.markdown=st.page_link("Home.py", label="Home")

with col2:
    st.title ("Iodometri")
    
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
        "Pengertian Iodometri": "Iodometri adalah metode analisis kimia yang menggunakan reaksi redoks antara ion iodin (I⁻) dan senyawa kimia lainnya dalam larutan. Reaksi ini umumnya digunakan untuk menentukan kadar senyawa oksidator atau reduktor dalam larutan, di mana iodin bertindak sebagai agen pengoksidasi atau penurun. Metode iodometri dapat dilakukan dengan menggunakan titrasi iodimetri, di mana larutan iodin dengan konsentrasi yang diketahui dititrasi dengan larutan yang mengandung senyawa yang akan ditentukan konsentrasinya.",
        "Pemilihan Indikator": "Pada standardisasi metode iodometri indikator yang biasanya digunakan adalah kanji. Penambahan indikator pada titrasi ini sesaat sebelum mendekati titik akhir agar kanji tidak bereaksi terlebih dahulu dengan KI sehingga mengganggu kesetimbangan reaksi.",
        "Reaksi Umum": """Reaksi umum yang terjadi dalam standardisasi larutan Natrium Tiosulfat (Na2SO3) dengan Kalium Dikromat (K2Cr2O7) adalah :

    K2Cr2O7 (aq) + 6 KI (aq) + 14 HCl (aq) -> 8 KCl (aq) + 2 CrCl3 (aq) + 7 H2O (l) + 3 I2
    2 NaS2O3 (aq) + I2 -> Na2S4O6 (aq) 2 NaI

    Dengan Kalium dikromat bereaksi dengan larutan KI menghasilkan I2 dan dilanjutkan titrasi dengan larutan Natrium Tiosulfat akan menghasilkan Natrium Tetrationat (Na2S4O6).""",
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
        user_input = st.selectbox("Pilih topik : ", ["Pengertian Iodometri", "Pemilihan Indikator", "Reaksi Umum", "Rumus Perhitungan Normalitas"])
        if st.button("Kirim"):
            response = materi_utama(user_input)
            text_area_height = min(max(len(response.split('\n')) * 20, 200), 600)  # Adjust height dynamically
            st.text_area("Penjawab:", value=response, height=text_area_height, disabled=True)
        
      
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
