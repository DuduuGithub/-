import pickle
from pathlib import Path

from user import User 
from server import Server
from YourInformation import yourIPv4Addr,yourUsingPort,yourName
# 在下方填入正确的ip地址和选择使用的端口，这些都是作为server的内容，作为client无需addr与port
#yourIPv4Addr="10.7.61.136"



# 读取主机user
def loader(file_path):
    with open(file_path,'rb') as f:
        return pickle.load(f)

if __name__=="__main__":
    
    # 创建本地user
    file_path = Path('Me.pkl')
    if file_path.exists():
        Me=loader(file_path)
    else:
        Me=User(yourIPv4Addr,yourUsingPort,yourName)
    print("本地user已加载")
    
    #创建本地server
    myServer=Server(Me)
    print("本地server已搭建")
    
    #打开server
    myServer.open()

    with open(file_path, 'wb') as file:
        pickle.dump(Me, file)
    
    