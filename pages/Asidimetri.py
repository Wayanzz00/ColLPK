import pandas as pd
import streamlit as st
import numpy as np

col1, col2 = st.columns([10, 1])
with col2:
    st.markdown=st.page_link("Home.py", label="Home")


st.title ("Asidimetri")

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
        "Pengertian Asidimetri": "Asidimetri adalah sebuah metode analisis kimia yang digunakan untuk menentukan konsentrasi suatu larutan asam dengan menggunakan larutan baku basa. Dalam proses asidimetri, larutan asam yang konsentrasinya tidak diketahui dititrasi dengan larutan baku basa yang konsentrasinya diketahui. Titik akhir titrasi ditentukan dengan menggunakan indikator atau dengan menggunakan metode potensiometri. Dari volume larutan baku basa yang diperlukan untuk mencapai titik akhir titrasi, konsentrasi larutan asam dapat dihitung menggunakan stoikiometri reaksi titrasi yang terjadi. ",
        "Pemilihan Indikator": "Dalam standardisasi Asidimetri, indikator yang sering dipilih adalah Metil Merah(MM) karena memberikan perubahan warna sekitar pH 4,2 - 6,3. Metil Merah juga mudah kompatibel dengan kedua komponen dalam titrasi, dan memudahkan pengamatan perubahan warna, sehingga memastikan penentuan titik akhir titrasi dengan akurasi yang tinggi untuk mengukur konsentrasi asam.",
        "Reaksi Umum": """Reaksi umum yang terjadi dalam standardisasi larutan HCl dengan boraks (Na2B4O7) adalah :

    HCl (aq) + Na2B4O7 (aq) -> NaCl (aq) + H2B4O7 (aq)

    Dengan asam klorida (HCl) bereaksi dengan boraks (Na2B4O7) menghasilkan natrium klorida (NaCl) dan asam tetraborat (H2B4O7).""",
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
        volume = st.number_input("Masukkan volume titran(mL):", min_value=0.0)
        BE = st.number_input("Masukkan nilai BE Titrat:", min_value=0.00)
        if st.button("Kalkulasi"):
            result = konsentrasi(gram, volume, BE)
            result_rounded = round(result, 4)
            st.write(f"Hasil perhitungan Normalitas : {result_rounded} N")
            
    elif selected_content == "Materi Utama":
        st.header("Materi Utama")
        user_input = st.selectbox("Pilih topik : ", ["Pengertian Asidimetri", "Pemilihan Indikator", "Reaksi Umum", "Rumus Perhitungan Normalitas"])
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
