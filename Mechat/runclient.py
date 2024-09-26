import pickle
from pathlib import Path
from user import User
from client import runClient
from YourInformation import yourIPv4Addr,yourUsingPort,yourName

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
    runClient(Me)
    
    with open(file_path, 'wb') as file:
        pickle.dump(Me, file)