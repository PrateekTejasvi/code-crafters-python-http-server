# Uncomment this to pass the first stage
import socket


class decodeData(object): 
    def __init__(self,request): 
        request = request.decode()
        lines = request.split('\r\n')
        method , path,reponse= lines[0].split()
        userAgent = lines[2]
        self.method = method 
        self.path = path 
        self.response = reponse
        self.userAgent = userAgent

    

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("listening on port 4221:")



    while True:

        conn,addr = server_socket.accept()

        with conn:
            data = conn.recv(1024)
            request = decodeData(data)
            if request.path == '/':
                response = f"HTTP/1.1 200 OK\r\n\r\n"
            elif request.path.startswith("/echo/"):
                echo_data = request.path[6:]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_data)}\r\n\r\n{echo_data}"
            elif request.path.startswith("/user-agent"):
                parsedData = request.userAgent.strip().split(": ")[1]
                print(parsedData)
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(parsedData)}\r\n\r\n{parsedData}"
            else:
                response = f"HTTP/1.1 404 NOT FOUND\r\n\r\n" 
            
            conn.send(response.encode('utf-8'))
            

        if not data:
            break  





if __name__ == "__main__":
    main()

