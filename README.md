# Python CLI Shell

Aplikasi **Python CLI Shell** adalah aplikasi Command-Line Interface (CLI) sederhana yang dapat meniru fungsi dasar shell atau terminal pada sistem Linux. Selain itu, aplikasi ini menyediakan beberapa fitur tambahan untuk meningkatkan fungsionalitasnya.

## Fitur Utama

- **Fungsi Shell Dasar**:
  - `ls`: Menampilkan isi direktori.
  - `pwd`: Menampilkan direktori kerja saat ini.
  - `cd`: Mengganti direktori.
  - `mkdir`: Membuat direktori baru.
  - `rmdir`: Menghapus direktori kosong.
  - `touch`: Membuat file kosong.
  - `rm`: Menghapus file.
  - `cp`: Menyalin file.
  - `mv`: Memindahkan atau mengganti nama file/direktori.
  - `help`: Menampilkan daftar perintah yang tersedia.
  - `clear`: Membersihkan layar.
  - `exit`: Keluar dari aplikasi CLI.

- **Fitur Tambahan**:
  - `fileinfo`: Menampilkan informasi lengkap tentang sebuah file.
  - `recent`: Menampilkan file yang baru saja dimodifikasi di direktori saat ini.
  - `tree`: Menampilkan struktur direktori dalam format pohon.
  - `heil`: Menampilkan banner ASCII art yang spesial.
  - `bagi_angpao`: Menampilkan banner ASCII art yang unik dan meriah.

## Cara Menggunakan

### 1. Menjalankan Aplikasi
1. Clone repositori atau salin skrip project_final.py ke direktori lokal.
2. Buka terminal atau command prompt dan navigasikan ke direktori yang berisi file project_final.py.
3. Jalankan aplikasi dengan menjalankan file Python:```bash
python project_final.py
```
### 2. Menggunakan Perintah
Setelah aplikasi berjalan, Anda dapat memasukkan perintah berikut untuk menjalankan fungsinya:

#### Fungsi Shell Dasar
- **Menampilkan isi direktori**:
  ```bash
  ls
  ```
- **Menampilkan direktori saat ini**:
  ```bash
  pwd
  ```
- **Mengganti direktori**:
  ```bash
  cd <path>
  ```
- **Membuat direktori**:
  ```bash
  mkdir <nama_direktori>
  ```
- **Menghapus direktori kosong**:
  ```bash
  rmdir <nama_direktori>
  ```
- **Membuat file kosong**:
  ```bash
  touch <nama_file>
  ```
- **Menghapus file**:
  ```bash
  rm <nama_file>
  ```
- **Menyalin file**:
  ```bash
  cp <source> <destination>
  ```
- **Memindahkan/mengganti nama file/direktori**:
  ```bash
  mv <source> <destination>
  ```
- **Menampilkan daftar perintah yang tersedia**:
  ```bash
  help
  ```
- **Membersihkan layar**:
  ```bash
  clear
  ```
- **Keluar dari aplikasi**:
  ```bash
  exit
  ```

#### Fungsi Tambahan
- **Menampilkan informasi file**:
  ```bash
  fileinfo <nama_file>
  ```
- **Menampilkan file yang baru dimodifikasi**:
  ```bash
  recent
  ```
- **Menampilkan struktur direktori sebagai pohon**:
  ```bash
  tree [path]
  ```
- **Menampilkan banner ASCII art**:
  ```bash
  heil
  ```
- **Menampilkan QR ASCII**:
  ```bash
  bagi_angpao
  ```
