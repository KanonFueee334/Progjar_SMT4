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



