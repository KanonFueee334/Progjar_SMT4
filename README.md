<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Bebas+Neue&weight=500&size=24&duration=7500&pause=500&color=8AE1F7&center=true&random=false&width=435&lines=Welcome+!!;Kanon's+GitHub+Repository;%F0%9F%94%A5+FTP+Socket+Programming+%F0%9F%94%A5" alt="Typing SVG" /></a>
```
Nama : Ali Rafli Putra Hakiki
NIM : 1203220107
Kelas : IF-02-01
```

<hr>

SOAL

1. Buat sebuah program file transfer protocol menggunakan socket programming dengan beberapa perintah dari client seperti berikut:
- `ls` : ketika client menginputkan command tersebut, maka server akan menampilkan daftar folder dan file dalam folder.
- `rm {nama file}` : ketika client menginputkan command tersebut, maka server akan menghapus file.
- `download {nama file}` : ketika client menginputkan command tersebut, maka server akan memberikan dan menampilkan isi file.
- `upload {nama file}` : ketika client menginputkan command tersebut, maka server akan menerima dan menyimpan file.
- `size {nama file}` : ketika client menginputkan command tersebut, maka server akan memberikan informasi file dalam satuan MB (Mega bytes) sesuai nama file.
- `byebye` : ketika client menginputkan command tersebut, hubungan server-client akan diputus.

<br>

### Code Program : Server 
    import socket
    import os
    import configparser

    BUFFER_SIZE = 1024

    def handle_client(client_socket):
    while True:
        command = client_socket.recv(BUFFER_SIZE).decode()
        
        if not command:
            break
        
        if command == 'ls':
            file_list = os.listdir('.')
            response = "\n".join(file_list)
            client_socket.send(response.encode())
        
        elif command.startswith('size'):
            filename = command.split()[1]
            if os.path.exists(filename):
                file_size = os.path.getsize(filename) / (1024 * 1024)  # Convert to MB
                client_socket.send(f"File size of {filename}: {file_size:.2f} MB".encode())
            else:
                client_socket.send("File not found.".encode())
        
        elif command.startswith('upload'):
            filename = command.split()[1]
            data = client_socket.recv(BUFFER_SIZE)
            with open(filename, 'wb') as file:
                file.write(data)
            client_socket.send("File uploaded successfully.".encode())
        
        elif command.startswith('download'):
            filename = command.split()[1]
            if os.path.exists(filename):
                with open(filename, 'rb') as file:
                    while True:
                        data = file.read(BUFFER_SIZE)
                        if not data:
                            break
                        client_socket.send(data)
            else:
                client_socket.send("File not found.".encode())
        
        elif command.startswith('rm'):
            filename = command.split()[1]
            if os.path.exists(filename):
                os.remove(filename)
                client_socket.send("File deleted successfully.".encode())
            else:
                client_socket.send("File not found.".encode())
        
        elif command == 'byebye':
            client_socket.send("Goodbye! Closing connection.".encode())
            client_socket.close()
            break

    def main():
    config = configparser.ConfigParser()
    config.read('server_config.ini')

    host = config['SERVER']['Host']
    port = int(config['SERVER']['Port'])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[*] Listening for incoming connections on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

        handle_client(client_socket)

    server_socket.close()

    if __name__ == "__main__":
    main()
<br>

### Penjelasan :
    
- Import Library: Program ini mengimpor beberapa modul yang diperlukan, yaitu socket, os, dan configparser. 
<br>
    
- Variabel Konfigurasi: BUFFER_SIZE didefinisikan sebagai ukuran buffer yang digunakan untuk mengirim dan menerima data. Nilainya adalah 1024 byte.
<br>

- Fungsi handle_client: Ini adalah fungsi yang menangani koneksi dari klien. Ini menerima perintah dari klien, memprosesnya, dan memberikan respons sesuai. Struktur if-elif-else digunakan untuk menangani beberapa jenis perintah yang berbeda:
        ls: Membaca daftar file di direktori saat ini dan mengirimkan daftar tersebut kembali ke klien.
        size [filename]: Mengembalikan ukuran file yang diminta kepada klien.
        upload [filename]: Menerima data file dari klien dan menyimpannya di server dengan nama file yang diberikan.
        download [filename]: Mengirimkan file yang diminta kepada klien.
        rm [filename]: Menghapus file yang diminta dari server.
        byebye: Menutup koneksi dengan klien.
<br>

- Fungsi main :
      Ini adalah fungsi utama dari program server. Ini membaca konfigurasi server dari file server_config.ini, mengikat socket server ke alamat dan port yang ditentukan, dan mulai mendengarkan koneksi masuk. Ketika koneksi diterima, ia menerima klien baru dan menangani permintaan klien dengan memanggil fungsi handle_client.
<br>

- Baca Konfigurasi Server :
      Konfigurasi server dibaca dari file server_config.ini menggunakan configparser. Konfigurasi mencakup host dan port yang digunakan oleh server.
<br>

- Membuat Socket Server :
  Server membuat socket menggunakan socket.socket() dengan alamat IPv4 dan jenis socket TCP (socket.AF_INET dan socket.SOCK_STREAM). Kemudian socket 
  tersebut diikat ke alamat dan port yang diberikan.
<br>

- Mendengarkan Koneksi Masuk :
  Server memulai mendengarkan koneksi masuk dengan memanggil server_socket.listen(). Ini menunggu dan menerima koneksi dari klien dengan server_socket.accept().
<br>

- Mengelola Koneksi:
  Ketika koneksi diterima, server memanggil handle_client untuk menangani koneksi dari klien tersebut. Setelah selesai, server kembali ke tahap mendengarkan koneksi masuk.
<br>

### Code Program : Client
    import socket
    import sys

    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345
    BUFFER_SIZE = 1024

    def main():
    print("\n------------------------------------")
    print("Python FTP Socket Programming")
    print("-------------------------------------")
    print("Choose Command:")
    print("ls                    : List of files")
    print("size <file_path>      : file sizes")
    print("upload <file_path>    : Upload files")
    print("download <file_path>  : Download files")
    print("rm <file_path>        : Remove files")
    print("byebye                : Disconnect.")
    print("-------------------------------------")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[*] Connected to server {SERVER_HOST}:{SERVER_PORT}")

        while True:
            command = input("\nEnter Command : ").strip()
            client_socket.send(command.encode())

            if command == 'byebye':
                print("[*] Disconnecting from server...")
                print(client_socket.recv(BUFFER_SIZE).decode())
                break

            data = client_socket.recv(BUFFER_SIZE).decode()
            if data == "Command not found":
                print("[!] Command not found. Please enter a valid command.")
            else:
                print(data)

    if __name__ == "__main__":
    main()
<br>

### Penjelasan :
- Variabel Konfigurasi :
        SERVER_HOST: Alamat IP server yang akan dikoneksikan oleh klien. Dalam contoh ini, diatur ke '127.0.0.1', yang merupakan localhost.
        SERVER_PORT: Port yang digunakan oleh server untuk menerima koneksi dari klien. Dalam contoh ini, diatur ke 12345.
        BUFFER_SIZE: Ukuran buffer untuk mengirim dan menerima data antara klien dan server.
<br>

- Fungsi main :
        Fungsi utama program yang akan dieksekusi saat menjalankan program.
        Mencetak pesan selamat datang dan daftar perintah yang dapat digunakan oleh pengguna.
        Membuat socket klien menggunakan socket.socket() dengan alamat IPv4 dan jenis socket TCP (socket.AF_INET dan socket.SOCK_STREAM).
        Menghubungkan klien ke server menggunakan client_socket.connect((SERVER_HOST, SERVER_PORT)).

<br>

- Loop Utama :
        Program masuk ke dalam loop utama yang berjalan selama koneksi dengan server aktif.
        Pengguna diminta untuk memasukkan perintah menggunakan input().
        Perintah yang dimasukkan oleh pengguna dikirimkan ke server menggunakan client_socket.send(command.encode()).

<br>

- Penanganan Perintah "byebye" :
        Jika pengguna memasukkan perintah "byebye", klien mengirimkan perintah ke server dan mencetak pesan sebelum memutus koneksi.
        Klien menerima respons dari server dan mencetak pesan penutupan sebelum keluar dari loop dan menutup koneksi dengan server.
<br>

- Menerima Respons dari Server:
        Setelah mengirim perintah ke server, klien menerima respons dari server menggunakan client_socket.recv(BUFFER_SIZE).
        Data yang diterima kemudian didekode dari byte menjadi string menggunakan .decode() untuk membaca pesan respons dari server.
        Jika respons adalah "Command not found", klien mencetak pesan kesalahan.
        Jika respons adalah respons dari perintah yang dijalankan, klien mencetak respons tersebut.
<br>

### Cara Kerja Program :

- Server Program:
        Program server membuat sebuah socket dan mulai mendengarkan koneksi masuk.
        Ketika koneksi diterima dari klien, server menerima perintah dari klien.
        Server memproses perintah tersebut dan memberikan respons yang sesuai kepada klien.
        Koneksi antara klien dan server tetap terbuka sampai klien mengirimkan perintah "byebye" untuk menutup koneksi.

<br>

- Klien Program:
        Program klien membuat sebuah socket dan terhubung ke alamat dan port yang telah ditentukan oleh server.
        Pengguna diminta untuk memasukkan perintah dari daftar perintah yang tersedia.
        Klien mengirimkan perintah yang dimasukkan oleh pengguna ke server melalui socket.
        Klien menerima respons dari server dan mencetaknya.
        Loop ini berlanjut sampai pengguna memasukkan perintah "byebye" untuk keluar dari program.

<br>


### Kesimpulan : 

- Fungsionalitas dasar kedua program diatas adalah untuk berkomunikasi antara klien dan server melalui protokol FTP menggunakan socket. program diatas memberikan pengguna           antarmuka sederhana untuk melakukan operasi dasar pada file di server, seperti melihat daftar file, mengunduh, mengunggah, menghapus, dan menghitung ukuran file.
<br>

### COMMAND LIST :

**1. Ls**
```
Enter Command : ls
```

Perintah `ls` digunakan untuk mengetahui folder dan file yang ada di direktori. Output : 
`client.py`

![alt text](Assets/ls.png)


**2. Size**
```
Enter Command : size <nama_file>
```

Perintah `size` digunakan untuk mengetahui ukuran file yang diinginkan dengan menambahkan parameter nama file. Output : 

![alt text](Assets/size.png)


**3. Upload**
```
Enter Command : upload <nama_file>
```

Perintah `upload` digunakan untuk mengunggah file yang diinginkan `client` dengan menambahkan nama file, misalnya `DreamAI.py`. File yang diunggah ini akan diterima dan disimpan oleh `server` ke direktori server.

**4. Download**
```
Enter Command : download <nama_file>
```

Perintah `download` digunakan untuk mengunduh file yang diinginkan `client` dengan menambahkan nama file, misalnya `DreamAI.py`. File yang diunduh ini akan berada di `client` dan `client` akan menampilkannya. Output : 

![alt text](Assets/down.png)


**5. Rm**
```
Enter Command : rm <nama_file>
```

Perintah `rm` digunakan untuk menghapus file yang diinginkan `client`. Output :

![alt text](Assets/rm.png)

**6. Byebye**
```
Enter Command : byebye
```

Perintah `byebye` digunakan untuk memutuskan koneksi antara `client` dengan `server`. Output :

![alt text](Assets/bye.png)


<hr>



