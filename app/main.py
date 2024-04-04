# Uncomment this to pass the first stage
import socket


class decodeData(object): 
    def __init__(self,request): 
        request = request.decode()
        lines = request.split('\r\n')
        method , path,reponse= lines[0].split()
        self.method = method 
        self.path = path 
        self.response = reponse



def main():

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("listening on port 4221:")

    while True:

        conn,addr = server_socket.accept()

        with conn:
            data = conn.recv(1024)
            request = decodeData(data)
            if request.path == '/':
                conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                conn.send(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")

            if not data:
                break   




if __name__ == "__main__":
    main()

