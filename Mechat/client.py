#某一时刻只会与一个主机进行联系
# 规定，发送信息的第一行表示该请求的命令名称
import socket
import pickle
from pathlib import Path
from user import User
import time


serverConnecting={} #存储正在连接的主机的地址和端口，两个组合形成一个str，由:连接，值为conn和上一次操作的时间组成的列表

# 使用方法：只需要根据需求执行send函数就行
def show_serverConnecting():
    for addrport in serverConnecting.keys():
        print(addrport)

def Connect(serverHost="127.0.0.1",serverPort=65432):
    
    #HOST、PORT指的都是server的主机与端口号
    HOST =  serverHost # 默认主机地址，如需修改需专门在此修改
    
    PORT = serverPort  # server的端口号

    # 当with块结束时，s会自动关闭，进而引发与之相连的server的conn会收到空字符，引发server的conn关闭
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.sendall(b"Hello, world")
    #     data = s.recv(1024)
    #     print(f"Received {data!r}")
    
    #需要手动关闭

    serverConnecting[serverHost+':'+str(serverPort)][0].connect((HOST, PORT))
    
def connect_if_not_exisits(serverHost,serverPort):
    if (serverHost+':'+str(serverPort)) not in serverConnecting:#
                connectTime=time.perf_counter()
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverConnecting.update({serverHost+':'+str(serverPort):[s,connectTime]})
                Connect(serverHost,serverPort)
        
def Close(serverHost="127.0.0.1",serverPort=65432):
    serverConnecting[serverHost+':'+str(serverPort)][0].close()
  
#TCP允许持续连接，使用持续连接，以实现低延迟的通信,设定5min无操作的话断开连接 
def sendByIp(serverHost,serverPort,text):
    
    message=text
    # Connect(serverHost,serverPort)
    serverConnecting[serverHost+':'+str(serverPort)][0].sendall(str.encode(message))
    # Close(serverHost,serverPort)
        
def helloToUSer():
    text="Hi~Welcome to Mechat Client"
    print(text)
    
# 接下来需要再server中写出接受好友请求函数，需要在kongzhitai输入y\n，并返回给client结果，client再依次进行好友添加
# 好友请求报文的格式：
# addFriendsRequest
# name:
# ip:
# port:
# {申请语}
# n请求添加你为好友
def addFriendRequest(requestAddr,requestPort,requestTextAdd):
    connect_if_not_exisits(requestAddr,requestPort)
    requestText="addFriendsRequest\n" #命令名
    requestText+=requestTextAdd
    requestText+='\n请求添加你为好友'
    sendByIp(requestAddr,requestPort,requestText)
    print("好友申请已发送")
    pass
    
def help():
    pass
def changeName(Me,newName):
    Me.name=newName

def selectToClose():
    for addrport,mylist in serverConnecting.items():
        lastTime=mylist[1]
        timeNow=time.perf_counter()
        if timeNow-lastTime>60*10:
            serverHost=addrport.split(':')[0]
            serverPort=int(addrport.split(':')[1])
            Close(serverHost,serverPort) 
    pass

def runClient(Me:User):  #新学写法，指定函数形参的类型
    helloToUSer()
    print(Me.getResumeText())
    while True:
        selectToClose() # 在此关闭连接
        command=input("请输入指令(输入help可以获得指令介绍)").lower() #会整行输入,Lower之后大小写不敏感
        if command=="help":
            help()
        elif (command=="message with stranger")|(command=="message by ip"):
            serverHost=input("输入server的IP地址:")
            serverPort=int(input("输入想要连接的对应server的端口号:"))
            # 连接
            connect_if_not_exisits(serverHost,serverPort)
            
            message="message\n"  #命令名
            message+=input(Me.name+':')
            sendByIp(serverHost,serverPort,message)
            print("已发送")
        elif (command=="message with friend")|(command=="message with a friend")|(command=="message with friends"):
            FriendName=input("输入您想要连接的friend的name:")
            judge,targetFriend=Me.findFriend_from_name(FriendName)
            if judge==False:
                print("您没有这样的好友，请重新输入指令")
                
            else:
                print("找到了好友")
                message=input(Me.name+':')
                print(FriendName)
                print(targetFriend.name)
                Me.chat_history[FriendName].append(Me.name+message) # 聊天记录client端的记录
                sendByIp(targetFriend.addr,targetFriend.port,message)
                print("已发送")
        elif (command=="add friends")|(command=="add friend"):
            requestAddr=input("输入对方的IP地址:")
            requestPort=int(input("输入对方的端口号:"))
           
            requestTextAdd=Me.getResumeText()+'\n'
            requestTextAdd+=input("输入申请语:")
            addFriendRequest(requestAddr,requestPort,requestTextAdd)
            
        elif (command=="exit")|(command=="quit"):
            break
        elif command=="history":
            name=input("请输入要查看聊天的朋友name:")
            
            Me.showChatHistory(name)
        else:
            print("unknown command")     

