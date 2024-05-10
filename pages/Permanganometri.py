import pandas as pd
import streamlit as st
import numpy as np

col1, col2 = st.columns([10, 1])
with col2:
    st.markdown=st.page_link("Home.py", label="Home")


st.title ("Permanganometri")

# Fungsi untuk menghitung konsentrasi
def konsentrasi(gram, volume, BE):
    try:
        result = gram / (volume * BE)
        return result
    except ZeroDivisionError:
        return "Error: BE tidak boleh nol. Silakan masukkan nilai yang valid."

# Fungsi untuk menghasilkan jawaban dari input pengguna
def materi_utama(materi):
    options = {
        "Pengertian Permanganometri": "Permanganometri adalah metode analisis kimia yang menggunakan reaksi redoks antara ion permanganat (MnO₄⁻) dan senyawa kimia lainnya dalam larutan. Reaksi ini sering digunakan untuk menentukan kadar senyawa reduktor dalam sampel, di mana permanganat bertindak sebagai agen pengoksidasi. KMnO4 bersifat oksidator kuat akan mengalami reduksi menjadi Mn2+ + H2O dan sampel akan mengalami reaksi oksidasi.",
        "Pemilihan Indikator": "Pada titrasi metode permanganometri KMno4 bersifat sebagai auto indikator. Karena kelebihan satu tetes KMnO4 akan terjadi perubahan warna larutan menjadi merah muda seulas. Perubahan warna ini ditetapkan sebagai warna titik akhir titrasi.",
        "Reaksi Umum": """Reaksi umum yang terjadi dalam standardisasi larutan KMnO4 dengan Asam Oksalat (H2C2O4) adalah :

    2 MnO4^- (aq) + 5 H2C2O4 (aq) + 6 H^+ -> 2 Mn^2+ (aq) + 10 CO2 (aq) + 8 H2O (l)

    Dengan Kalium Permanganat bereaksi dengan Asam Oksalat (H2C2O4) menghasilkan ion Mn^2+."""    ,
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
    # Extract the specified column
    column_data = df[nama_column]

    # Evaluate the mean and standard deviation functions
    hasil_mean = eval(mean)(column_data)
    hasil_std_dev = eval(std_dev)(column_data)
    hasil_rsd = (hasil_std_dev / hasil_mean) * 100 if hasil_mean != 0 else 0
    
     # Round the results to four decimal places
    hasil_mean = round(hasil_mean, 4)
    hasil_rsd = round(hasil_rsd, 2)
    hasil_std_dev = round(hasil_std_dev, 6)

    # Display the results
    st.write(f"Rata-rata dari {nama_column}: {hasil_mean}")
    st.write(f"Standar Deviasi dari {nama_column}: {hasil_std_dev}")
    st.write(f"%RSD dari {nama_column}: {hasil_rsd}%")
    
def main():
    
    # Pilihan konten menggunakan selection box
    selected_content = st.radio(
        "Pilih konten:",
        ["Materi Utama", "Kalkulator Konsentrasi", "Data Pengamatan"],
        horizontal=True,
    )

    # Tampilkan konten terkait
    if selected_content == "Kalkulator Konsentrasi":
        st.header("Kalkulator Konsentrasi")
        gram = st.number_input("Masukkan jumlah massa (mg):", min_value=0.0)
        volume = st.number_input("Masukkan volume (mL):", min_value=0.0)
        BE = st.number_input("Masukkan nilai BE Titrat:", min_value=0.00)
        if st.button("Kalkulasi"):
            result = konsentrasi(gram, volume, BE)
            result_rounded = round(result, 4)
            st.write(f"Hasil perhitungan Normalitas : {result_rounded} N")
            
    elif selected_content == "Materi Utama":
        st.header("Materi Utama")
        user_input = st.selectbox("Pilih topik : ", ["Pengertian Permanganometri", "Pemilihan Indikator", "Reaksi Umum", "Rumus Perhitungan Normalitas"])
        if st.button("Kirim"):
            response = materi_utama(user_input)
            text_area_height = min(max(len(response.split('\n')) * 25, 200), 600)  # Adjust height dynamically
            st.text_area("Penjawab:", value=response, height=text_area_height, disabled=True)
      
    elif selected_content == "Data Pengamatan":
        st.title("Data Pengamatan")

        # Sample DataFrame
        data = {
            "Sample (mg)": [0.01, 0.02, 0.03],
            "Volume Titran (mL)": [0.00, 0.00, 0.00],
            "Normalitas Titran (N)": [0.00, 0.00, 0.00]
        }
        df = pd.DataFrame(data)

        # Allow users to input the column index
        column_index = st.sidebar.selectbox("Pilih kolom untuk dikalkulasi :", df.columns)

        # Allow users to input functions for mean and standard deviation
        st.sidebar.header("Kalkulasi Data Statistik")
        mean = st.sidebar.text_input("Fungsi Rata - rata :", value="np.mean")
        std_dev = st.sidebar.text_input("Fungsi Standar Deviasi :", value="np.std")

        # Allow users to edit a specific column
        st.sidebar.header("Edit Column")
        selected_columns = []
        for column in df.columns:
            if st.sidebar.checkbox(f"Edit '{column}'", value=True, key=column):
                selected_columns.append(column)

        updated_df = df.copy()
        if len(selected_columns) > 0:
            df_edit = df[selected_columns]
            edited_df = st.data_editor(df_edit)
            if st.sidebar.button("Kalkulasi"):
                for column in selected_columns:
                    updated_df[column] = edited_df[column]

                # Calculate and display mean and standard deviation
                data_pengamatan(updated_df, column_index, mean, std_dev)

if __name__ == "__main__":
    main()
