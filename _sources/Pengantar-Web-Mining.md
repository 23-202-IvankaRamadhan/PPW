# Pengantar Web Mining

Taksonomi Web Mining
Secara umum, Web Mining dibagi menjadi tiga sub-bidang utama berdasarkan jenis data yang dianalisis:
1. Web Content Mining (Penambangan Isi Web)
Web Content Mining adalah proses mengekstraksi informasi berguna dari dokumen web, dengan fokus pada konten halaman itu sendiri. Konten ini bisa berupa teks, gambar, audio, atau video. Salah satu aplikasi utamanya adalah Text Mining, yaitu proses mendapatkan informasi berkualitas dari data teks.
Aplikasi utama dari Text Mining meliputi:
•	Ekstraksi Informasi: Mengambil informasi terstruktur dari teks yang tidak terstruktur atau semi-terstruktur.
•	Topic Modelling: Mengidentifikasi topik utama dalam sekumpulan dokumen.
•	Peringkasan Dokumen: Membuat ringkasan singkat dari dokumen yang panjang.
•	Klasifikasi Dokumen: Mengkategorikan dokumen ke dalam kelas-kelas yang telah ditentukan (contoh: deteksi spam, kategorisasi berita). Metode yang digunakan termasuk Naive Bayes, Support Vector Machines (SVM), Jaringan Saraf Tiruan, dan Transformers.
•	Pengelompokan Dokumen (Clustering): Mengelompokkan dokumen yang serupa tanpa label kategori sebelumnya. Teknik yang digunakan antara lain K-Means dan Hierarchical Clustering.
•	Analisis Sentimen: Mengklasifikasikan polaritas suatu teks (positif, netral, atau negatif). Ini sangat berguna untuk menganalisis ulasan produk atau pendapat publik.
________________________________________
2. Web Usage Mining (Penambangan Penggunaan Web)
Web Usage Mining berfokus pada ekstraksi informasi dari data yang dihasilkan oleh perilaku pengguna saat berinteraksi dengan sebuah situs web. Data ini biasanya berasal dari log akses server, log agen, dan clickstream (urutan klik pengguna).
Proses ini bertujuan untuk memahami karakteristik dan profil penggunaan pengguna. Aplikasi penting dari Web Usage Mining meliputi:
•	Sistem Rekomendasi Produk: Menyarankan produk yang paling mungkin diminati oleh pengguna berdasarkan perilakunya di masa lalu.
•	Personalisasi Pencarian (Personalized Search): Menyesuaikan hasil pencarian agar lebih relevan dengan preferensi dan konteks pengguna individu.
________________________________________
3. Web Structure Mining (Penambangan Struktur Web)
Web Structure Mining adalah proses penemuan dan interpretasi pola dalam struktur hyperlink di Internet. Tujuannya adalah untuk menganalisis hubungan antar halaman web atau antar pengguna di jaringan sosial.
Aplikasi utama dari Web Structure Mining adalah:
•	Analisis Graf Web (Web Graph): Merepresentasikan halaman web sebagai simpul (node) dan hyperlink sebagai sisi (edge) untuk menganalisis struktur.
•	Identifikasi Simpul Penting (Centrality): Menemukan halaman atau aktor yang memiliki pengaruh besar dalam jaringan, contohnya melalui algoritma PageRank yang digunakan oleh Google untuk menentukan peringkat hasil pencarian.
•	Deteksi Komunitas: Mengidentifikasi kelompok-kelompok simpul (aktor) yang berinteraksi lebih sering satu sama lain dibandingkan dengan simpul di luar kelompok tersebut. Ini berguna untuk sistem rekomendasi atau visualisasi jaringan sosial.
________________________________________
Proses Web Mining
Proses Web Mining mengikuti tahapan yang mirip dengan Data Mining, tetapi dengan fokus khusus pada data web. Tahapan-tahapan tersebut adalah:
1. Gathering and Exploration (Pengumpulan dan Eksplorasi Data) Tahap ini meliputi pengumpulan data dari web melalui Web Crawling atau Web API. Setelah data terkumpul, dilakukan eksplorasi untuk memahami karakteristiknya, seperti ringkasan statistik dan visualisasi data.
2. Preprocessing and Transformation (Praporses dan Transformasi) Tahap ini adalah yang paling memakan waktu, seringkali 70-80% dari total proyek. Tujuannya adalah mengubah data mentah menjadi format yang siap untuk dianalisis. Ini termasuk:
•	Reduksi Dimensi dan Seleksi Fitur.
•	Transformasi Teks menjadi vektor atau embedding untuk pemrosesan oleh model machine learning.
•	Mengintegrasikan berbagai sumber data.
3. Actual Data Mining (Penambangan Data Aktual) Pada tahap ini, model atau pola diekstraksi dari data yang sudah diproses. Prosesnya bersifat iteratif, di mana eksperimen dilakukan dengan berbagai metode dan hyperparameter untuk mendapatkan hasil terbaik. Jika model tidak valid, maka akan kembali ke tahap praporses atau pengumpulan data untuk perbaikan.
