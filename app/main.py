# Uncomment this to pass the first stage
import socket


def main():

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept() # wait for client
    print("listening on port 4221:")
    conn,addr = server_socket.accept()

    while conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")







if __name__ == "__main__":
    main()
