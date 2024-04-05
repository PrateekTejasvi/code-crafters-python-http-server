# Uncomment this to pass the first stage
import socket
import threading

server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
print("listening on port 4221:")        
conn,addr = server_socket.accept()

HTTPNotFound =  f"HTTP/1.1 404 NOT FOUND\r\n\r\n".encode('utf-8')
HTTPOK =  f"HTTP/1.1 200 OK\r\n\r\n".encode('utf-8')

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


def sendValidResponse(data):
    send_resp = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(data)}\r\n\r\n{data}".encode('utf-8')
    return send_resp

def handleConnections():
     while True:
        with conn:
            data = conn.recv(1024)
            request = decodeData(data)
            if request.path == '/':
                response = HTTPOK
            elif request.path.startswith("/echo/"):
                echo_data = request.path[6:]
                response = sendValidResponse(echo_data)
            elif request.path.startswith("/user-agent"):
                parsedData = request.userAgent.strip().split(": ")[1]
                response = sendValidResponse(parsedData)
            else:
                response = HTTPNotFound
            conn.send(response)
            

        if not data:
            break  

def main():
    threading.Thread(target=handleConnections,args=(server_socket,),daemon=True).start()



   


if __name__ == "__main__":
    main()

