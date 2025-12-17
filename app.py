# ==============================================================================
# BAGIAN 1: IMPORT LIBRARY (MEMANGGIL ALAT-ALAT YANG DIBUTUHKAN)
# ==============================================================================

import streamlit as st                  # Library utama untuk membuat tampilan Web App (UI/Antarmuka).
import fitz  # PyMuPDF                  # Library khusus untuk membuka dan membaca teks dari dalam file PDF.
import nltk                             # Natural Language Toolkit: Otak kecerdasan buatan untuk memproses bahasa manusia.
from nltk.corpus import stopwords       # Mengambil daftar "kata sampah" (seperti: dan, yang, di, ke) untuk dibuang.
from nltk.tokenize import word_tokenize # Alat untuk memotong kalimat panjang menjadi potongan kata-kata (token).
import pandas as pd                     # Library untuk membuat tabel data yang rapi dan bisa diurutkan (seperti Excel).
import networkx as nx                   # Library matematika untuk menghitung hubungan antar titik (Graph) dan algoritma PageRank.
from pyvis.network import Network       # Library untuk memvisualisasikan Graph agar bisa digerakkan/interaktif di web.
import tempfile                         # Library untuk membuat file sementara di sistem (karena PyMuPDF butuh file fisik, bukan di RAM).
import re                               # Regex (Regular Expression): Alat pencari pola teks (misal: mencari dan menghapus semua angka).
import streamlit.components.v1 as components # Komponen penghubung agar kode HTML (hasil graph) bisa muncul di dalam Streamlit.
import os                               # Library untuk berinteraksi dengan sistem operasi (seperti perintah menghapus file).

# ==============================================================================
# BAGIAN 2: KONFIGURASI HALAMAN WEB
# ==============================================================================

# Mengatur judul yang muncul di tab browser dan mengatur agar layout memenuhi layar (wide mode).
st.set_page_config(page_title="Analisis Paper Dinamis", layout="wide") 

# ==============================================================================
# BAGIAN 3: FUNGSI DOWNLOAD RESOURCE BAHASA (CACHE)
# ==============================================================================

# @st.cache_resource adalah perintah agar fungsi ini hanya dijalankan SEKALI saja saat aplikasi pertama dibuka.
# Tujuannya agar tidak download data bahasa berulang-ulang setiap kali user klik tombol (biar tidak lemot).
@st.cache_resource
def download_nltk_data():
    # Membuat daftar paket bahasa dasar NLTK yang wajib ada.
    resources = ['punkt', 'stopwords', 'punkt_tab']
    
    # Melakukan perulangan (loop) untuk mengecek satu per satu paket di atas.
    for res in resources:
        try:
            # Mencoba mencari: Apakah paket ini sudah ada di folder komputer server?
            nltk.data.find(f'tokenizers/{res}')
        except LookupError:
            # Jika komputer bilang "Error/Gak ketemu", maka download paketnya secara diam-diam (quiet=True).
            nltk.download(res, quiet=True)
            
    # Pengecekan ekstra khusus untuk folder 'stopwords' agar tidak error.
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        # Download stopwords jika belum ada.
        nltk.download('stopwords', quiet=True)

# ==============================================================================
# BAGIAN 4: FUNGSI EKSTRAKSI (MEMBACA) PDF
# ==============================================================================

# Fungsi ini menerima file PDF yang diupload user, lalu mengembalikan isinya dalam bentuk teks panjang.
def extract_text_from_pdf(uploaded_file):
    # Membuka blok 'tempfile' untuk membuat file sementara yang aman.
    # delete=False artinya file tidak langsung dihapus saat blok kode selesai (kita hapus manual nanti).
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        # Menulis/menyalin isi file yang ada di RAM (uploaded_file) ke dalam file sementara di hardisk.
        tmp_file.write(uploaded_file.getvalue()) 
        # Menyimpan alamat/lokasi file sementara tersebut (path) ke variabel tmp_path.
        tmp_path = tmp_file.name 
    
    # Membuka file PDF yang ada di alamat sementara tadi menggunakan library PyMuPDF (fitz).
    doc = fitz.open(tmp_path) 
    
    # Menyiapkan variabel string kosong untuk menampung hasil teks.
    text = ""                 
    
    # Melakukan loop untuk membaca setiap halaman yang ada di dalam PDF.
    for page in doc:          
        # Mengambil teks dari halaman tersebut dan menambahkannya ke variabel 'text'.
        text += page.get_text() 
    
    # Menutup file PDF agar tidak memakan memori.
    doc.close()               
    
    # Menghapus file sementara yang tadi kita buat dari sistem komputer.
    # Ini PENTING agar hardisk server tidak penuh dengan sampah file temp.
    os.remove(tmp_path)       
    
    # Mengembalikan hasil teks bersih ke pemanggil fungsi.
    return text               

# ==============================================================================
# BAGIAN 5: FUNGSI PRE-PROCESSING (BERSIH-BERSIH TEKS)
# ==============================================================================

# Fungsi ini menerima teks kotor, membersihkannya, dan mengembalikan daftar kata (list).
def process_text(text):
    # Menggunakan Regex untuk menghapus semua angka (0-9) dan menggantinya dengan kosong.
    text = re.sub(r'\d+', '', text)        
    # Menggunakan Regex untuk menghapus semua tanda baca (titik, koma, seru, dll).
    # [^\w\s] artinya: hapus apa pun yang BUKAN huruf dan BUKAN spasi.
    text = re.sub(r'[^\w\s]', '', text)    
    # Mengubah semua huruf menjadi huruf kecil (lowercase) agar seragam.
    text = text.lower()                    
    
    # Mencoba memotong kalimat menjadi kata-kata menggunakan alat pintar NLTK (word_tokenize).
    try:
        words = word_tokenize(text)        
    # Jika NLTK error (jarang terjadi), gunakan metode split spasi biasa sebagai cadangan.
    except:
        words = text.split()               
    
    # Mencoba mengambil daftar kata sambung (stopwords) Bahasa Indonesia dari NLTK.
    try:
        stop_words = set(stopwords.words('indonesian')) 
    # Jika gagal/belum terdownload, gunakan himpunan kosong (tidak ada filter).
    except:
        stop_words = set()                 
        
    # Membuat daftar kata sampah tambahan (Custom Stopwords) yang spesifik untuk paper/jurnal.
    custom_stopwords = [
        'dan', 'yang', 'di', 'ke', 'dari', 'ini', 'itu', 'pada', 'untuk', 'dengan', 'adalah', 
        'sebagai', 'juga', 'karena', 'oleh', 'dalam', 'akan', 'dapat', 'tersebut', 'saya', 'kita',
        'kami', 'anda', 'ia', 'dia', 'mereka', 'apa', 'siapa', 'bagaimana', 'mengapa', 'kapan',
        'dimana', 'kenapa', 'bisa', 'ada', 'tidak', 'ya', 'hal', 'maka', 'atau', 'jika', 'saat',
        'serta', 'setelah', 'sebelum', 'lalu', 'sedangkan', 'meskipun', 'sehingga', 'namun',
        'bagi', 'antara', 'selama', 'setiap', 'suatu', 'sudah', 'telah', 'agar', 'pun',
        'gambar', 'tabel', 'penelitian', 'metode', 'data', 'hasil', 'analisis', 'pembahasan',
        'kesimpulan', 'saran', 'daftar', 'pustaka', 'universitas', 'jurusan', 'fakultas',
        'skripsi', 'tesis', 'disertasi', 'jurnal', 'paper', 'makalah', 'bab', 'halaman',
        'berdasarkan', 'menggunakan', 'dilakukan', 'merupakan', 'terhadap', 'adanya', 
        'menunjukkan', 'terdiri', 'mengenai', 'dijelaskan', 'penerapan', 'penggunaan', 
        'perancangan', 'pengujian', 'implementasi', 'sistem', 'aplikasi', 'program', 'proses',
        'studi', 'kasus', 'abstract', 'abstrak', 'keyword', 'kata', 'kunci', 'latar', 'belakang'
    ]
    # Menggabungkan daftar stopwords bawaan dengan stopwords buatan sendiri.
    stop_words.update(custom_stopwords) 
    
    # Melakukan filter terakhir (List Comprehension).
    # Hanya ambil kata JIKA: 
    # 1. Isinya huruf (isalpha), 
    # 2. Tidak ada di daftar stopwords, 
    # 3. Panjang kata lebih dari 2 huruf.
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 2]
    
    # Mengembalikan hasil daftar kata bersih.
    return filtered_words

# ==============================================================================
# BAGIAN 6: FUNGSI MEMBUAT GRAPH (NETWORK)
# ==============================================================================

# Fungsi ini menerima daftar kata dan ukuran jendela (window_size) untuk menentukan hubungan antar kata.
def build_graph(words, window_size=2):
    # Membuat dictionary kosong untuk mencatat pasangan kata yang muncul bersamaan.
    co_occurrences = {} 
    
    # Melakukan loop dari kata pertama sampai kata (akhir dikurangi window_size).
    for i in range(len(words) - window_size):
        # Menentukan kata pusat (target).
        target = words[i] 
        # Mengambil potongan kata-kata di sebelah kanannya sebagai konteks/tetangga.
        context = words[i+1 : i+1+window_size] 
        
        # Loop setiap kata tetangga di dalam konteks.
        for neighbor in context:
            # Jika kata target sama dengan tetangga (misal: "data data"), lewati/skip.
            if target == neighbor: continue 
            
            # Membuat pasangan kata. Fungsi 'sorted' memastikan urutan abjad.
            # Jadi ("ibu", "ayah") dianggap SAMA dengan ("ayah", "ibu").
            pair = tuple(sorted((target, neighbor))) 
            
            # Jika pasangan ini sudah pernah dicatat di buku (dictionary):
            if pair in co_occurrences:
                # Tambahkan skor frekuensinya +1.
                co_occurrences[pair] += 1
            # Jika belum pernah dicatat:
            else:
                # Tulis baru dengan skor awal 1.
                co_occurrences[pair] = 1
                
    # Membuat objek Graph kosong menggunakan library NetworkX.
    G = nx.Graph() 
    
    # Loop isi dictionary co_occurrences untuk dimasukkan ke dalam Graph.
    # u = kata pertama, v = kata kedua, weight = jumlah kemunculan bersama.
    for (u, v), weight in co_occurrences.items():
        # Menambahkan garis (edge) penghubung antara u dan v dengan bobot tertentu.
        G.add_edge(u, v, weight=weight)
        
    # Mengembalikan objek Graph yang sudah jadi.
    return G

# ==============================================================================
# BAGIAN 7: PROGRAM UTAMA (MAIN LOOP)
# ==============================================================================

# Fungsi utama yang akan dijalankan oleh Streamlit.
def main():
    # Menjalankan fungsi download data bahasa (yang di-cache di atas).
    download_nltk_data() 
    
    # --- SETUP MEMORI (SESSION STATE) ---
    # Bagian ini penting untuk menyimpan data antar-klik (state management).
    
    # Cek: Apakah laci 'paper_data' sudah ada di memori?
    if 'paper_data' not in st.session_state:
        # Jika belum, buat dictionary kosong untuk menyimpan data setiap paper secara terpisah.
        st.session_state.paper_data = {}
        
    # Cek: Apakah variabel 'active_file_key' sudah ada?
    # Variabel ini gunanya untuk mencatat: "File mana yang sedang dilihat user sekarang?"
    if 'active_file_key' not in st.session_state:
        # Jika belum, set ke None (belum ada yang dilihat).
        st.session_state.active_file_key = None

    # Menampilkan Judul Aplikasi di layar utama.
    st.title("Analisis Paper PDF Dinamis")
    # Menampilkan deskripsi singkat.
    st.markdown("Upload file -> Geser Slider -> Graph berubah otomatis.")

    # --- SIDEBAR (PANEL KIRI) ---
    with st.sidebar:
        # Menampilkan Header di sidebar.
        st.header("1. Upload & Settings")
        
        # Membuat tombol Upload File.
        # accept_multiple_files=True membolehkan user upload banyak PDF sekaligus.
        uploaded_files = st.file_uploader(
            "Upload PDF Disini", 
            type="pdf", 
            accept_multiple_files=True
        )
        
        # Membuat garis pemisah visual.
        st.divider()
        
        # Membuat Slider untuk mengatur Window Size.
        # Jika user menggeser slider ini, Streamlit akan me-rerun kode dari atas.
        # MODIFIKASI: Default value diubah dari 2 menjadi 1
        window_size = st.slider("Jarak Hubungan Kata (Window Size)", 1, 5, 1)
        # Menampilkan info kecil.
        st.info("Geser slider untuk melihat perubahan graph.")

    # --- LOGIKA UTAMA: MEMPROSES DATA ---
    
    # Jika user sudah mengupload minimal satu file:
    if uploaded_files:
        # Lakukan loop untuk setiap file yang ada di uploader.
        for uploaded_file in uploaded_files:
            # Ambil nama filenya (misal: "JurnalA.pdf").
            file_name = uploaded_file.name 
            
            # --- TAHAP PENENTUAN: APAKAH FILE INI PERLU DIPROSES? ---
            # Kita buat variabel penanda (flag), awalnya False (jangan proses).
            process_now = False 

            # KONDISI 1: Cek apakah file ini belum pernah ada di memori 'paper_data'?
            if file_name not in st.session_state.paper_data:
                # Jika belum ada (file baru), maka WAJIB DIPROSES.
                process_now = True
            else:
                # KONDISI 2: File sudah ada, tapi apakah settingan Window Size berubah?
                # Kita ambil window_size yang DULU disimpan saat pemrosesan terakhir.
                saved_window = st.session_state.paper_data[file_name].get('window_size', 0)
                
                # Bandingkan: Apakah window_size slider (sekarang) BEDA dengan simpanan (lama)?
                if saved_window != window_size:
                    # Jika beda, berarti user minta update graph. WAJIB PROSES ULANG.
                    process_now = True 

            # --- EKSEKUSI PEMROSESAN (JIKA process_now ADALAH TRUE) ---
            if process_now:
                # Tampilkan animasi loading dengan pesan yang sesuai.
                with st.spinner(f"Memproses {file_name} (Window Size: {window_size})..."):
                    
                    # --- OPTIMASI: MENGHINDARI BACA ULANG PDF ---
                    # Cek: Apakah teks mentah (raw_text) file ini sudah ada di memori?
                    if file_name in st.session_state.paper_data and 'raw_text' in st.session_state.paper_data[file_name]:
                        # Jika sudah ada (karena file lama yang cuma digeser slidernya), pakai teks dari RAM.
                        raw_text = st.session_state.paper_data[file_name]['raw_text']
                    else:
                        # Jika ini benar-benar file baru, ekstrak teks dari PDF fisik.
                        raw_text = extract_text_from_pdf(uploaded_file)
                    
                    # 1. Jalankan fungsi pembersihan teks.
                    words = process_text(raw_text)
                    
                    # Validasi: Pastikan hasil kata lebih dari 5 (bukan PDF kosong/gambar).
                    if len(words) > 5:
                        # 2. Jalankan fungsi buat Graph (menggunakan window_size TERBARU dari slider).
                        G = build_graph(words, window_size)
                        
                        # Validasi: Pastikan Graph punya node/titik.
                        if len(G.nodes) > 0:
                            # 3. Hitung algoritma PageRank untuk mencari kata terpenting.
                            pr = nx.pagerank(G, alpha=0.85)
                            
                            # 4. Buat DataFrame (Tabel) dari hasil PageRank.
                            df = pd.DataFrame(list(pr.items()), columns=['Kata', 'PageRank'])
                            # Urutkan dari nilai tertinggi ke terendah.
                            df = df.sort_values(by='PageRank', ascending=False).reset_index(drop=True)
                            # Tambahkan kolom nomor urut (ID) di depan.
                            df.insert(0, 'ID', range(1, 1 + len(df))) 
                            
                            # 5. SIMPAN SEMUA HASIL KE MEMORI (SESSION STATE)
                            # Kita update isi laci dengan data terbaru.
                            st.session_state.paper_data[file_name] = {
                                'graph': G,                 # Simpan objek Graph.
                                'pagerank': pr,             # Simpan skor PageRank.
                                'df': df,                   # Simpan Tabel.
                                'count': len(words),        # Simpan jumlah kata.
                                'raw_text': raw_text,       # Simpan teks mentah (cache) biar hemat waktu nanti.
                                'window_size': window_size  # PENTING: Simpan angka slider yang dipakai saat ini.
                            }
                            
                            # 6. AUTO SWITCH FITUR
                            # Paksa tampilan aplikasi untuk langsung pindah ke file yang baru saja diproses ini.
                            st.session_state.active_file_key = file_name
                            
                        else:
                            # Tampilkan warning jika graph gagal dibuat.
                            st.warning(f"File {file_name} kurang relasi kata.")
                    else:
                        # Tampilkan warning jika teks terlalu sedikit.
                        st.warning(f"File {file_name} teksnya kosong.")

        # --- LOGIKA TAMPILAN (VIEW) ---
        
        # Ambil daftar semua nama file yang datanya sudah siap di memori.
        processed_files = list(st.session_state.paper_data.keys())
        
        # Jika daftar file tidak kosong (ada data):
        if processed_files:
            # Tampilkan pemisah dan judul di sidebar.
            st.sidebar.divider()
            st.sidebar.header("2. Pilih File")
            
            # Safety Check:
            # Jika file yang sedang aktif tiba-tiba hilang (misal user hapus di uploader),
            # maka reset pilihan ke file pertama yang tersedia agar tidak error.
            if st.session_state.active_file_key not in processed_files:
                st.session_state.active_file_key = processed_files[0]

            # MEMBUAT MENU DROPDOWN (SELECTBOX)
            # key='active_file_key' membuat menu ini terikat dua arah dengan variabel session state.
            # Jika session_state berubah (karena auto-switch), menu berubah.
            # Jika menu diklik user, session_state berubah.
            selected_file = st.sidebar.selectbox(
                "Tampilkan Analisis Paper Yang Sudah Diproses:",
                options=processed_files,
                key='active_file_key' 
            )
            
            # Jika ada file yang dipilih:
            if selected_file:
                # Ambil data SPESIFIK milik file tersebut dari laci memori.
                data = st.session_state.paper_data[selected_file]
                
                # Bongkar (unpack) data ke variabel masing-masing agar mudah dipakai.
                G = data['graph']
                pr = data['pagerank']
                df = data['df']
                count = data['count']
                current_win = data.get('window_size', '?') # Ambil info window size.

                # Menampilkan Header Nama File di area utama.
                st.subheader(f"📄 File: {selected_file}")
                # Menampilkan caption untuk konfirmasi ke user bahwa settingan slider berfungsi.
                st.caption(f"Graph ini dibuat dengan Jarak Hubungan Kata (Window Size): {current_win}")
                # Menampilkan kotak sukses berisi statistik singkat.
                st.success(f"Total Kata: {count} | Node Graph: {len(G.nodes())}")

                # Membagi layar utama menjadi 2 kolom (Kiri 3 bagian, Kanan 2 bagian).
                col_graph, col_stats = st.columns([3, 2])

                # --- VISUALISASI GRAPH (KOLOM KIRI) ---
                with col_graph:
                    st.subheader("🕸️ Word Graph")
                    
                    # Menghitung posisi (x, y) setiap titik agar menyebar rapi (spring layout).
                    pos = nx.spring_layout(G, k=0.5, seed=42)
                    
                    # Membuat kanvas visualisasi menggunakan PyVis.
                    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
                    # Memasukkan data dari NetworkX ke PyVis.
                    net.from_nx(G)

                    # Melakukan loop untuk mempercantik setiap node (titik).
                    for node in net.nodes:
                        word = node['id']               # Ambil kata (id node).
                        node['x'] = pos[word][0] * 1000 # Set koordinat X (dikali 1000 biar luas).
                        node['y'] = pos[word][1] * 1000 # Set koordinat Y.
                        node['physics'] = False         # Matikan simulasi fisika (biar graph diam/stabil).
                        
                        # Ambil skor PageRank kata tersebut.
                        score = pr.get(word, 0.01)
                        # Set ukuran node berdasarkan skor (makin penting makin besar).
                        node['size'] = score * 1000 
                        # Set tulisan tooltip yang muncul saat mouse diarahkan ke node.
                        node['title'] = f"Kata: {word}\nRank: {df[df['Kata']==word].index[0]+1}"

                    # Pastikan fisika mati total.
                    net.toggle_physics(False)

                    # Blok try-except untuk merender HTML.
                    try:
                        path_html = "graph.html"
                        # Simpan hasil graph ke file HTML sementara.
                        net.save_graph(path_html)
                        # Buka file HTML tersebut sebagai teks string.
                        with open(path_html, 'r', encoding='utf-8') as f:
                            html_source = f.read()
                        # Tampilkan string HTML tersebut ke dalam Streamlit.
                        components.html(html_source, height=620)
                    except Exception as e:
                        # Tampilkan error jika gagal render.
                        st.error(f"Error: {e}")

                # --- VISUALISASI STATISTIK (KOLOM KANAN) ---
                with col_stats:
                    st.subheader("📊 Top Ranking")
                    # Ambil 20 kata teratas dari dataframe.
                    top_df = df.head(20)
                    # Tampilkan Bar Chart (Grafik Batang).
                    st.bar_chart(top_df.set_index('Kata')['PageRank'])
                    
                    st.divider()
                    st.subheader("📋 PageRank")
                    # Tampilkan tabel data lengkap yang bisa di-scroll.
                    st.dataframe(df, use_container_width=True, height=300, hide_index=True)
        else:
            # Pesan jika belum ada file yang diproses.
            st.info("Belum ada file yang berhasil diproses.")

    else:
        # --- KONDISI JIKA USER MENGHAPUS SEMUA FILE (KLIK X DI UPLOADER) ---
        # Reset memori paper data jadi kosong.
        st.session_state.paper_data = {}
        # Reset pilihan file aktif jadi None.
        st.session_state.active_file_key = None
        # Tampilkan pesan instruksi awal.
        st.info("Silakan upload file PDF di sidebar.")

# ==============================================================================
# ENTRY POINT (TITIK MULAI PROGRAM)
# ==============================================================================

# Kode standar Python untuk memastikan fungsi main() hanya jalan jika file ini dijalankan langsung.
if __name__ == "__main__":
    main()