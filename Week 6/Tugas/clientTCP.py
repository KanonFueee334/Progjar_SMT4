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
