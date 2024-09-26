import sys
import socket
import selectors
import types
from user import User
import threading
# 过程：client首先通过一个套接字与server取得联系，第一次连接调用accept_wrapper，得到一个新的套接字用于之后的联系conn、和ip地址addr
# 通过sellector模块(self.sel)集合conn、events、key(套接字和定义的命名空间data(里面有addr，应用：可以用来收集这个接口发送的所有信息))在server中注册，关联
# 而后通过sellect()监听，识别出信号后，会有key和mask返回，如果已经注册过，使用key的fileobj(套接字)即可实现信息接收
# 当客户端发送数据到服务器时，触发 EVENT_READ，当服务器准备好发送数据回客户端时，触发 EVENT_WRITE
# 不同的客户端会触发不同的key
# 如果client断开了连接，会在server注销，key也会消失


# server连接关闭的依据：client连接的关闭会发送一个“结束”信号（FIN 包）到服务器，读取到空消息即可关闭连接
class Server:
    def __init__(self,Me:User) -> None:
        self.user= Me
        self.HOST = Me.addr  # 默认主机地址，如需修改需专门在runserver修改
        self.PORT = Me.port  # Port to listen on (non-privileged ports are > 1023)位于server上
        self.friend=None #如果不是friend,则就是none
        self.judge=False #True则表示是你的朋友
        self.sel = selectors.DefaultSelector()
        self.connectedClientIp={} #{ip:true} true表示是朋友
        self.running = True  # 控制服务器运行的标志
        
    def open(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.bind((self.HOST, self.PORT))
            s.listen()
            print("等待连接")
            s.setblocking(False)
            self.sel.register(s, selectors.EVENT_READ, data=None)
            
            
            try:
                while True:
                    if self.running==False:
                        break
                    events = self.sel.select(timeout=1)  # 添加超时以避免长时间阻塞
                    if self.running==False:
                        break
                    for key, mask in events:
                        if key.data is None:
                            self.accept_wrapper(key.fileobj) 
                        else:
                            self.service_connection(key, mask)
            except KeyboardInterrupt:
                    print("Caught keyboard interrupt, exiting")
 
            self.sel.close()

            
        
            
    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  
        print(f"A new connection from {addr} is set up")
        conn.setblocking(False)
        judge=self.user.findFriend_from_ip(addr)[0]
        self.connectedClientIp.update({addr:judge})
        
        
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") #使用命名空间对data进行封装
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data) 
        
    def service_connection(self,key, mask):
        conn = key.fileobj
        data = key.data
        addr=data.addr#获得该套接字的ip地址
        if mask & selectors.EVENT_READ:
            recv_data = conn.recv(1024).decode("utf-8")  # Should be ready to read
            if recv_data:
                self.showToSelf(addr,recv_data,conn)
            else:
                print(f"IP为{data.addr}的client断开了连接")
                self.sel.unregister(conn)
                conn.close()
        # if mask & selectors.EVENT_WRITE:
        #     self.responseToClient()
            
    # 运行该函数的前提是recv_data已经有内容
    def showToSelf(self,addr,text,conn):
        requestType=text.splitlines()[0]
        contentlist=text.splitlines()[1:]
        content = "\n".join(contentlist)
        print(1)
        print(requestType)
        print(123)
        if requestType=='message':  #发信息
            if self.connectedClientIp[addr]:
                print(f"Connected with friend {self.friend.name},IP is {addr}")
                print(f"{self.friend.name} : {content}")
                user=self.user.findFriend_from_ip(addr)[1]
                self.user.chat_history[user].append(user.name+':'+content)
            else :
                print(f"Connected with unknown,IP is {addr}")
                print(f"{addr} : {content}")
        elif requestType=='addFriendsRequest':   #加好友请求
            resume=text.splitlines()[1:4]
            #print(content)
            print("如果想同意好友请求，请输入y，如果不同意，请输入n")
            result=input()
            if result=='y':
                name=resume[0].split(':')[1]
                ip=resume[1].split(':')[1]
                port=int(resume[2].split(':')[1])
                newFriend=User(ip,port,name)
                self.user.friends.append(newFriend) #被申请者加好友
                
                self.responseFriendRequest(conn)
            if result=='n':
                refuseText="Sorry,I refuse"
                conn.sendall(refuseText)
        elif requestType=="responseFriendRequest": #接收到好友申请的返回
            secureKey=text.splitlines()[1]
            friendName=text.splitlines()[2]
            friendIP=text.splitlines()[3]
            friendPort=text.splitlines()[4]
            if secureKey==self.user.name:
                newFriend=User(friendIP,friendPort,friendName)
                self.user.friends.append(newFriend)
            else:
                print("He/She don't pass the secure test,please be cautious")
                print(f"And sender's IP is {addr}")
            
                
    # 加好友的response报文：
    # responseFriendRequest
    # secure:                      该项是用来让client验证是否有伪装,内容为申请者的姓名
    # name:
    # ip:
    # port:
    def responseFriendRequest(self,conn):
        responseText="responseFriendRequest\n"
        responseText+=self.user.getResumeText()
        conn.sendall(responseText.encode('utf-8'))
            
    def responseToClient(self,conn,text):
        pass
    
    def showConnectedClient(self):
        for ip in self.connectedClientIp:
            judge,user=self.user.findFriend_from_ip(ip)
            if judge:
                print(f"Friends: {user.name} IP={ip}")
            else:
                print(f"Unknown IP={ip}")
        print("All connected clients have been presented")
    
    