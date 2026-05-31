import subprocess
import sys

# ───────────────────────────────────────୨ৎ───────────────────────────────────
# AUTO INSTALLER PIL
# ───────────────────────────────────────୨ৎ───────────────────────────────────
# Coba import PIL, jika gagal maka install otomatis menggunakan pip
try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    print("Library 'Pillow' tidak ditemukan. Sedang menginstal otomatis...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageTk
        print("Instalasi sukses!")
    except Exception as e:
        print(f"Gagal menginstal otomatis: {e}")

import tkinter as tk
from tkinter import ttk
import heapq

# ───────────────────────────────────────୨ৎ───────────────────────────────────
# DATA PASIEN (20 Pasien)
# ───────────────────────────────────────୨ৎ───────────────────────────────────
data_pasien_mentah = [
    {"id": "P01", "prioritas": 3, "waktu_masuk": "07:00", "ambulance": "Tidak", "komorbid": "Hipertensi", "usia": 24, "jenis_kelamin": "P"},
    {"id": "P02", "prioritas": 4, "waktu_masuk": "07:08", "ambulance": "Tidak", "komorbid": "Tidak Ada", "usia": 19, "jenis_kelamin": "L"},
    {"id": "P03", "prioritas": 2, "waktu_masuk": "07:15", "ambulance": "Ya", "komorbid": "PPOK", "usia": 61, "jenis_kelamin": "P"},
    {"id": "P04", "prioritas": 5, "waktu_masuk": "07:22", "ambulance": "Tidak", "komorbid": "Tidak Ada", "usia": 17, "jenis_kelamin": "L"},
    {"id": "P05", "prioritas": 3, "waktu_masuk": "07:30", "ambulance": "Tidak", "komorbid": "Diabetes", "usia": 42, "jenis_kelamin": "P"},
    {"id": "P06", "prioritas": 1, "waktu_masuk": "07:37", "ambulance": "Ya", "komorbid": "Penyakit Jantung", "usia": 70, "jenis_kelamin": "L"},
    {"id": "P07", "prioritas": 4, "waktu_masuk": "07:45", "ambulance": "Tidak", "komorbid": "Migrain Kronis", "usia": 21, "jenis_kelamin": "P"},
    {"id": "P08", "prioritas": 2, "waktu_masuk": "07:53", "ambulance": "Tidak", "komorbid": "Hipertensi", "usia": 58, "jenis_kelamin": "L"},
    {"id": "P09", "prioritas": 3, "waktu_masuk": "08:00", "ambulance": "Tidak", "komorbid": "Gastritis", "usia": 33, "jenis_kelamin": "P"},
    {"id": "P10", "prioritas": 5, "waktu_masuk": "08:07", "ambulance": "Tidak", "komorbid": "Tidak Ada", "usia": 15, "jenis_kelamin": "L"},
    {"id": "P11", "prioritas": 1, "waktu_masuk": "08:15", "ambulance": "Ya", "komorbid": "Trauma Multipel", "usia": 49, "jenis_kelamin": "L"},
    {"id": "P12", "prioritas": 3, "waktu_masuk": "08:24", "ambulance": "Tidak", "komorbid": "Dehidrasi", "usia": 28, "jenis_kelamin": "P"},
    {"id": "P13", "prioritas": 4, "waktu_masuk": "08:33", "ambulance": "Tidak", "komorbid": "Tidak Ada", "usia": 20, "jenis_kelamin": "P"},
    {"id": "P14", "prioritas": 2, "waktu_masuk": "08:41", "ambulance": "Ya", "komorbid": "Asma", "usia": 55, "jenis_kelamin": "L"},
    {"id": "P15", "prioritas": 3, "waktu_masuk": "08:50", "ambulance": "Tidak", "komorbid": "Vertigo", "usia": 37, "jenis_kelamin": "P"},
    {"id": "P16", "prioritas": 4, "waktu_masuk": "09:00", "ambulance": "Tidak", "komorbid": "Tidak Ada", "usia": 31, "jenis_kelamin": "L"},
    {"id": "P17", "prioritas": 1, "waktu_masuk": "09:12", "ambulance": "Ya", "komorbid": "Penyakit Jantung", "usia": 63, "jenis_kelamin": "P"},
    {"id": "P18", "prioritas": 3, "waktu_masuk": "09:25", "ambulance": "Tidak", "komorbid": "Maag Kronis", "usia": 46, "jenis_kelamin": "L"},
    {"id": "P19", "prioritas": 4, "waktu_masuk": "09:37", "ambulance": "Tidak", "komorbid": "Alergi", "usia": 26, "jenis_kelamin": "P"},
    {"id": "P20", "prioritas": 2, "waktu_masuk": "09:50", "ambulance": "Ya", "komorbid": "Demam Berdarah", "usia": 39, "jenis_kelamin": "L"}
]

# Fungsi untuk mengubah waktu dari format jam:menit ke total menit
def ubah_ke_menit(waktu_str):
    jam, menit = map(int, waktu_str.split(':'))
    return jam * 60 + menit

# Fungsi untuk mengubah menit kembali ke format jam:menit
def ubah_ke_jam(total_menit):
    jam = total_menit // 60
    menit = total_menit % 60
    return f"{jam:02d}:{menit:02d}"

# ───────────────────────────────────────୨ৎ───────────────────────────────────
# STATE MANAGEMENT & ENGINE SIMULASI
# ───────────────────────────────────────୨ৎ───────────────────────────────────
# Variabel global untuk menyimpan hasil simulasi dan indeks langkah saat ini
hasil_simulasi_global = []
current_step_idx = 0

# Fungsi utama untuk menjalankan simulasi engine berdasarkan data pasien dan aturan prioritas
def jalankan_simulasi_engine():
    global hasil_simulasi_global, current_step_idx
    
    for row in tabel_hasil.get_children():
        tabel_hasil.delete(row)

    beds = {1: None, 2: None, 3: None, 4: None, 5: None} 
    perawat_tersedia = ["Perawat 1", "Perawat 2", "Perawat 3"]
    # Gunakan heapq untuk mengelola antrian perawat agar selalu mendapatkan perawat
    heapq.heapify(perawat_tersedia) 
    
    # Antrian pasien yang belum mendapat bed, diprioritaskan berdasarkan tingkat keparahan (prioritas) dan waktu masuk
    pq_kritis = [] 
    pq_umum = [] 
    # Antrian pasien yang sudah mendapat bed tapi masih menunggu perawat  
    pq_nunggu_perawat = [] 

    # Antrian event untuk simulasi, diurutkan berdasarkan waktu kejadian (arrival/departure)
    events = []
    event_counter = 0
    pasien_counter = 0

    # Inisialisasi event kedatangan pasien ke dalam antrian event
    for p in data_pasien_mentah:
        w_menit = ubah_ke_menit(p['waktu_masuk'])
        p['w_masuk_mnt'] = w_menit
        event_counter += 1
        heapq.heappush(events, (w_menit, 1, event_counter, 'arrival', p))
    
    # List sementara untuk menyimpan hasil simulasi sebelum ditampilkan langkah demi langkah
    hasil_simulasi_sementara = []

    # Fungsi untuk memproses pasien yang sudah mendapat bed dan menunggu perawat, berdasarkan prioritas dan waktu masuk
    def proses_perawat(current_time):
        nonlocal event_counter
        while perawat_tersedia and pq_nunggu_perawat:
            _, _, _, p_data, b_id = heapq.heappop(pq_nunggu_perawat)
            nama_perawat = heapq.heappop(perawat_tersedia) 
            
            durasi = {1: 180, 2: 60, 3: 45, 4: 30, 5: 15}[p_data['prioritas']]
            w_selesai = current_time + durasi
            w_tunggu_total = current_time - p_data['w_masuk_mnt']

            hasil_simulasi_sementara.append({
                'id': p_data['id'], 'prioritas': p_data['prioritas'],
                'masuk': p_data['waktu_masuk'], 'ambulance': p_data['ambulance'],
                'komorbid': p_data['komorbid'], 'usia': p_data['usia'], 'jenis_kelamin': p_data['jenis_kelamin'],
                'bed': f"Bed {b_id}", 'perawat': nama_perawat, 
                'tunggu': f"{w_tunggu_total} mnt", 'mulai': ubah_ke_jam(current_time), 'selesai': ubah_ke_jam(w_selesai)
            })

            # Tambahkan event departure untuk pasien yang sedang diproses, sehingga saat waktunya tiba, bed dan perawat bisa dibebaskan
            event_counter += 1
            heapq.heappush(events, (w_selesai, 0, event_counter, 'departure', (b_id, nama_perawat)))

    # Proses event simulasi satu per satu berdasarkan kedatangan pasien hingga keberangkatan pasien setelah selesai diproses
    while events:
        curr_time, _, _, ev_type, data = heapq.heappop(events)

        # Saat pasien tiba (arrival), cek prioritasnya dan coba tempatkan di bed yang sesuai, jika tidak ada bed yang sesuai maka masukkan ke antrian sesuai prioritasnya
        if ev_type == 'arrival':
            p = data
            if p['prioritas'] == 1:
                target_beds = [4, 5]
                queue = pq_kritis
            else:
                target_beds = [1, 2, 3]
                queue = pq_umum
            
            # Cek apakah ada bed yang sesuai dengan prioritas pasien yang masih kosong, jika ada langsung tempatkan pasien di bed tersebut, jika tidak maka masukkan ke antrian sesuai
            free_beds = [b for b in target_beds if beds[b] is None]
            if free_beds:
                b_id = free_beds[0]
                beds[b_id] = p['id']
                pasien_counter += 1
                heapq.heappush(pq_nunggu_perawat, (p['prioritas'], p['w_masuk_mnt'], pasien_counter, p, b_id))
            else:
                pasien_counter += 1
                heapq.heappush(queue, (p['prioritas'], p['w_masuk_mnt'], pasien_counter, p))
            
            proses_perawat(curr_time)

        # Saat pasien selesai diproses (departure), bed dan perawat yang digunakan akan dibebaskan, kemudian cek apakah ada pasien yang menunggu untuk mendapatkan bed dan perawat, jika ada maka proses pasien tersebut
        elif ev_type == 'departure':
            b_id, nama_perawat = data
            beds[b_id] = None 
            heapq.heappush(perawat_tersedia, nama_perawat)

            # Cek antrian pasien yang menunggu untuk mendapatkan bed dan perawat, prioritaskan pasien dengan prioritas lebih tinggi (kritis) terlebih dahulu, jika tidak ada pasien kritis yang menunggu maka proses pasien umum
            if b_id in [4, 5] and pq_kritis:
                _, _, _, p_next = heapq.heappop(pq_kritis)
                beds[b_id] = p_next['id']
                pasien_counter += 1
                heapq.heappush(pq_nunggu_perawat, (p_next['prioritas'], p_next['w_masuk_mnt'], pasien_counter, p_next, b_id))
            elif b_id in [1, 2, 3] and pq_umum:
                _, _, _, p_next = heapq.heappop(pq_umum)
                beds[b_id] = p_next['id']
                pasien_counter += 1
                heapq.heappush(pq_nunggu_perawat, (p_next['prioritas'], p_next['w_masuk_mnt'], pasien_counter, p_next, b_id))

            proses_perawat(curr_time)

    # Setelah semua event diproses, simpan hasil simulasi ke variabel global untuk ditampilkan langkah demi langkah
    hasil_simulasi_global = hasil_simulasi_sementara
    current_step_idx = 0

# Fungsi untuk menampilkan langkah selanjutnya dari hasil simulasi ke dalam tabel hasil di halaman simulasi
def tampilkan_step_selanjutnya():
    global current_step_idx
    if current_step_idx < len(hasil_simulasi_global):
        h = hasil_simulasi_global[current_step_idx]
        status = {1:"Kritis", 2:"Emergen", 3:"Urgen", 4:"Semi-Ur", 5:"Non-Ur"}[h['prioritas']]
        
        tabel_hasil.insert("", "end", values=(
            h['id'], f"{h['prioritas']} ({status})", h['masuk'], h['ambulance'],
            h['komorbid'], h['usia'], h['jenis_kelamin'], h['bed'], 
            h['perawat'], h['tunggu'], h['mulai'], h['selesai']
        ))
        tabel_hasil.yview_moveto(1)
        current_step_idx += 1

# ───────────────────────────────────────୨ৎ───────────────────────────────────
# HELPER DESIGN
# ───────────────────────────────────────୨ৎ───────────────────────────────────
# Fungsi untuk menggambar rectangle dengan sudut melengkung pada tombol
def draw_rounded_rect(canvas_obj, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
        x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
        x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
        x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
    ]
    return canvas_obj.create_polygon(points, **kwargs, smooth=True)

# ───────────────────────────────────────୨ৎ───────────────────────────────────
# ALUR PERPINDAHAN HALAMAN
# ───────────────────────────────────────୨ৎ───────────────────────────────────
# Fungsi untuk berpindah dari halaman cover ke halaman simulasi utama
def pindah_ke_simulasi():
    canvas_cover.pack_forget()
    tampilkan_halaman_simulasi()

# ───────────────────────────────────────୨ৎ───────────────────────────────────
# COVER PERKENALAN
# ───────────────────────────────────────୨ৎ───────────────────────────────────
root = tk.Tk()
root.title("Sistem Simulasi Antrean IGD - Universitas Negeri Surabaya")
root.geometry("1366x768")
root.resizable(False, False)

# Coba load gambar background, jika gagal maka gunakan warna solid sebagai background
try:
    bg_img = Image.open("Background SDA.jpeg").resize((1366, 768), Image.Resampling.LANCZOS)
    ph_img = ImageTk.PhotoImage(bg_img)
except Exception:
    ph_img = None

canvas_cover = tk.Canvas(root, width=1366, height=768, bd=0, highlightthickness=0)
canvas_cover.pack(fill="both", expand=True)

if ph_img:
    canvas_cover.create_image(0, 0, image=ph_img, anchor="nw")
else:
    canvas_cover.create_rectangle(0, 0, 1366, 768, fill="#75b7df")

canvas_cover.create_rectangle(0, 0, 1366, 65, fill="#073a6a", outline="")
canvas_cover.create_text(683, 32, text="IMPLEMENTASI PRIORITY QUEUE UNTUK PENENTUAN PRIORITAS PASIEN IGD BERDASARKAN TINGKAT KEPARAHAN", 
                         font=("Arial", 14, "bold"), fill="white", justify="center")

box_kelompok = tk.Frame(canvas_cover, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
canvas_cover.create_window(333, 180, window=box_kelompok, width=700, height=320, anchor="nw")

lbl_judul_box = tk.Label(box_kelompok, text="ANGGOTA KELOMPOK :", font=("Arial", 16, "bold"), bg="white", fg="#073a6a")
lbl_judul_box.pack(pady=(35, 20))

anggota = [
    "AMMALYA KHOIRUN NIZAK (25031554036)",
    "KANE MATTHEW PRASTERSEN (25031554141)",
    "NAYLA SALSABILA AZ-ZAHRA (25031554268)"
]

for mhs in anggota:
    tk.Label(box_kelompok, text=mhs, font=("Arial", 14, "bold"), bg="white", fg="#222222").pack(pady=8)

# Button Mulai Simulasi
btn_bg = draw_rounded_rect(canvas_cover, 533, 560, 833, 615, radius=25, fill="#a8d63a", outline="", tags="btn_mulai")
btn_txt = canvas_cover.create_text(683, 587, text="MULAI SIMULASI", font=("Arial", 13, "bold"), fill="white", tags="btn_mulai")

# Event hover dan click pada tombol mulai simulasi
def on_hover_cover(event):
    canvas_cover.itemconfig(btn_bg, fill="#94c032")

def on_leave_cover(event):
    canvas_cover.itemconfig(btn_bg, fill="#a8d63a")

canvas_cover.tag_bind("btn_mulai", "<Enter>", on_hover_cover)
canvas_cover.tag_bind("btn_mulai", "<Leave>", on_leave_cover)
# Klik tombol mulai simulasi akan memanggil fungsi untuk berpindah ke halaman simulasi utama
canvas_cover.tag_bind("btn_mulai", "<Button-1>", lambda e: pindah_ke_simulasi())


# ───────────────────────────────────────୨ৎ───────────────────────────────────
# SIMULASI UTAMA
# ───────────────────────────────────────୨ৎ───────────────────────────────────
tabel_hasil = None

def tampilkan_halaman_simulasi():
    global tabel_hasil
    
    # Coba load gambar background, jika gagal maka gunakan warna solid sebagai background
    canvas_sim = tk.Canvas(root, width=1366, height=768, bd=0, highlightthickness=0)
    canvas_sim.pack(fill="both", expand=True)
    
    if ph_img:
        canvas_sim.create_image(0, 0, image=ph_img, anchor="nw")
    else:
        canvas_sim.create_rectangle(0, 0, 1366, 768, fill="#75b7df")

    canvas_sim.create_rectangle(0, 0, 1366, 65, fill="#073a6a", outline="")
    canvas_sim.create_text(683, 32, text="SISTEM SIMULASI ANTREAN IGD", font=("Arial", 22, "bold"), fill="white")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="white", fieldbackground="white", foreground="#333333", rowheight=28, font=("Arial", 9), borderwidth=0)
    style.configure("Treeview.Heading", background="#90a4ae", foreground="#111111", font=("Arial", 9, "bold"), borderwidth=0)
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    # Bagian kiri untuk menampilkan jadwal kedatangan pasien
    frame_kiri = tk.Frame(root, bg="white", bd=0, highlightthickness=0)
    canvas_sim.create_window(40, 110, window=frame_kiri, anchor="nw", width=490, height=500)

    lbl_kiri = tk.Label(frame_kiri, text="JADWAL KEDATANGAN", font=("Arial", 12, "bold"), bg="#073a6a", fg="white", pady=10)
    lbl_kiri.pack(fill="x")

    kolom_kiri = ("ID", "Pri", "Jam", "Amb", "Komorbid", "Usia", "JK")
    header_kiri = ["ID", "PRIORITAS", "JAM MASUK", "AMBULAN", "KOMORBID", "USIA", "JK"]
    lebar_kiri = [35, 75, 75, 65, 130, 45, 35]

    t_awal = ttk.Treeview(frame_kiri, columns=kolom_kiri, show="headings")
    for i in range(len(kolom_kiri)):
        t_awal.heading(kolom_kiri[i], text=header_kiri[i])
        t_awal.column(kolom_kiri[i], width=lebar_kiri[i], anchor="center")
    t_awal.pack(fill="both", expand=True)

    for p in data_pasien_mentah:
        t_awal.insert("", "end", values=(p['id'], p['prioritas'], p['waktu_masuk'], p['ambulance'], p['komorbid'], p['usia'], p['jenis_kelamin']))

    # Bagian kanan untuk menampilkan hasil simulasi kedatangan pasien secara realtime
    frame_kanan = tk.Frame(root, bg="white", bd=0, highlightthickness=0)
    canvas_sim.create_window(550, 110, window=frame_kanan, anchor="nw", width=775, height=500)

    lbl_kanan = tk.Label(frame_kanan, text="PROSES KEDATANGAN REALTIME", font=("Arial", 12, "bold"), bg="#073a6a", fg="white", pady=10)
    lbl_kanan.pack(fill="x")

    kolom_hasil = ("ID", "Pri", "Msk", "Amb", "Komorbid", "Usia", "JK", "Bed", "Perawat", "Wait", "Start", "End")
    header_teks = ["ID", "PRIORITAS", "JAM MASUK", "AMBULAN", "KOMORBID", "USIA", "JK", "BED", "PERAWAT", "TUNGGU", "MULAI", "SELESAI"]
    lebar_kolom = [35, 75, 75, 65, 105, 35, 25, 45, 65, 55, 45, 50]

    tabel_hasil = ttk.Treeview(frame_kanan, columns=kolom_hasil, show="headings")
    for i in range(len(kolom_hasil)):
        tabel_hasil.heading(kolom_hasil[i], text=header_teks[i])
        tabel_hasil.column(kolom_hasil[i], width=lebar_kolom[i], anchor="center")
    tabel_hasil.pack(fill="both", expand=True)

    # Tombol untuk menjalankan simulasi dan menampilkan langkah selanjutnya
    btn1 = draw_rounded_rect(canvas_sim, 400, 640, 630, 690, radius=25, fill="#cd3e2b", outline="", tags="btn_sim_start")
    canvas_sim.create_text(515, 665, text="Reset Simulasi", font=("Arial", 11, "bold"), fill="white", tags="btn_sim_start")
    
    btn2 = draw_rounded_rect(canvas_sim, 660, 640, 940, 690, radius=25, fill="#043b6b", outline="", tags="btn_sim_next")
    canvas_sim.create_text(800, 665, text="Langkah Selanjutnya", font=("Arial", 11, "bold"), fill="white", tags="btn_sim_next")

    # Event hover dan click pada tombol simulasi
    def on_click_sim(event):
        clicked_tags = canvas_sim.gettags(canvas_sim.find_withtag("current"))
        if "btn_sim_start" in clicked_tags:
            jalankan_simulasi_engine()
        elif "btn_sim_next" in clicked_tags:
            if not hasil_simulasi_global:
                jalankan_simulasi_engine()
            tampilkan_step_selanjutnya()

    # Klik tombol simulasi akan memanggil fungsi untuk menjalankan simulasi engine atau menampilkan langkah selanjutnya dari hasil simulasi
    canvas_sim.bind("<Button-1>", on_click_sim)
    
    # Event hover untuk tombol simulasi
    canvas_sim.tag_bind("btn_sim_start", "<Enter>", lambda e: canvas_sim.itemconfig(btn1, fill="#d72316"))
    canvas_sim.tag_bind("btn_sim_start", "<Leave>", lambda e: canvas_sim.itemconfig(btn1, fill="#cd3e2b"))
    
    canvas_sim.tag_bind("btn_sim_next", "<Enter>", lambda e: canvas_sim.itemconfig(btn2, fill="#032c52"))
    canvas_sim.tag_bind("btn_sim_next", "<Leave>", lambda e: canvas_sim.itemconfig(btn2, fill="#043b6b"))

# Jalankan aplikasi
root.mainloop()