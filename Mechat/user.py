
class User:
    # user实例的name=ip
    #只有好友才能记录聊天记录
    def __init__(self,addr,port,name):
        self.addr=addr #指主机地址，在本机作为server时应用
        self.port=port #主机使用的端口
        self.name=name # 不考虑name的改变
        self.friends=[]  # 会确保存储的friends只有可见内容，对于存储的friends设置为空(否则同时也会有无限循环情况的发生)，这部分内容在addFriend函数中实现
        self.chat_history={} #键为user实例
        
    def Default():
        return User()
    def findFriend_from_ip(self,addr):
        for f in self.friends:
            if f.addr==addr :
                return True,f
        
        return False,None
        
    def findFriend_from_name(self,name):
        for f in self.friends:
            if f.name==name :
                print("f")
                return True,f
        
        return False,None
        
    def getResumeText(self): #这个涉及到加好友对方对你信息的保存，要保证精准
        message="name:"+self.name+'\n'
        message+="ip:"+self.addr+'\n'
        message+="port:"+str(self.port)+'\n'
        return message
        
    def addFriendRequest(requestAddr,requestText):    
        #该函数在client实现，因为加好友的过程分解了请求和同意两种情况，故各在client和server上实现
        pass
    def showChatHistory(self,name):
        judge,user=self.findFriend_from_name(name)
        if judge:
            for text in self.chat_history[user]:
                    print(text)
        else:
            print("没有找到此friend")
                
        