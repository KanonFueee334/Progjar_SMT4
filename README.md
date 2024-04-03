<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Bebas+Neue&weight=500&size=24&duration=7500&pause=500&color=8AE1F7&center=true&random=false&width=435&lines=Welcome+!!;Kanon's+GitHub+Repository;%F0%9F%94%A5+FTP+Socket+Programming+%F0%9F%94%A5" alt="Typing SVG" /></a>
```
Nama : Ali Rafli Putra Hakiki
NIM : 1203220107
Kelas : IF-02-01
```

<hr>
# SOAL

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


