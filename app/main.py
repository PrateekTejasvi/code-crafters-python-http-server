# Uncomment this to pass the first stage
import socket
import threading
import os
import sys

server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
print("listening on port 4221:")        

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

def postFile(path,request):
    #get the file contents 
    decoded = request.decode()
    lines = decoded.split('\r\n')
    content = lines[len(lines)-1]
    with open(path,"w") as f: 
        f.write(content)
    response = "HTTP/1.1 201 OK\r\nContent-length: 0\r\n\r\n".encode()
    return response

def getDir():
    args = sys.argv 
    dir = ""
    for i in range(len(args)):
        if args[i] == "--directory":
            dir = args[i+1]
    return dir





def handleConnections(conn):
    HTTPOK =  f"HTTP/1.1 200 OK\r\n\r\n".encode('utf-8')
    def sendValidResponse(data,type):
        send_resp = f"HTTP/1.1 200 OK\r\nContent-Type: {type}\r\nContent-Length: {len(data)}\r\n\r\n{data}".encode('utf-8')
        return send_resp
    def GetFile(dir):
        response = b"HTTP/1.1 404 NOT FOUND\r\n\r\n"
        if os.path.exists(dir):
            with open(dir) as f:
                content = f.read()
                response=sendValidResponse(content,"application/octet-stream")
        return response

    with conn:
        data = conn.recv(1024)
        request = decodeData(data)
        print(request.method)
        if request.path == '/':
            response = HTTPOK
        elif request.path.startswith("/echo/"):
            echo_data = request.path[6:]
            response = sendValidResponse(echo_data,"text/plain")
        elif request.path.startswith("/user-agent"):
            parsedData = request.userAgent.strip().split(": ")[1]
            response = sendValidResponse(parsedData,"text/plain")
        elif request.path.startswith("/file") and request.method == "GET":
            file_name = request.path[7:]
            dir = getDir()
            path = f"{dir[:len(dir)-1]}/{file_name}"
            response= GetFile(path)
        elif request.path.startswith("/file") and request.method=="POST":
            file_name = request.path[7:]
            dir = getDir()
            print(file_name)
            path = f"{dir[:len(dir)-1]}/{file_name}"
            response = postFile(path,data)
        else:
            response = f"HTTP/1.1 404 NOT FOUND\r\n\r\n".encode('utf-8')
        conn.send(response)

def main():
    try: 
        while True:
            conn, addr = server_socket.accept()  # wait for client
            client_thread = threading.Thread(target=handleConnections, args=(conn,))
            client_thread.start()
    finally:
        server_socket.close()
    

if __name__ == "__main__":
    main()

