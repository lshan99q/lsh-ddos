import asyncio  # 导入asyncio库，用于处理异步任务
import aiohttp  # 导入aiohttp库，用于发送HTTP请求

# 定义全局变量
tt = 0  # 记录总成功次数

# 定义一个异步函数，用于发送HTTP请求
async def send_request(session, url):
    global tt  # 使用全局变量
    try:
        async with session.get(url) as response:
            print(f"Status: {response.status}")  # 打印响应的状态码
            tt += 1  # 成功次数加1
            return await response.text()  # 返回响应的文本内容
    except aiohttp.ClientConnectionResetError:
        print("连接被重置，重试中...")
        return None
    except Exception as e:
        print(f"Error: {e}")  # 如果发生异常，打印错误信息
        return None  # 返回None表示请求失败

# 定义一个异步主函数，用于并发发送多个请求
async def main(url, num_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

# 程序入口
if __name__ == "__main__":
    url = input("目标的IP或域名: ")  # 获取目标URL
    port = input("端口: ")  # 获取端口号
    num_requests = int(input("你想要并发的请求数量: "))  # 获取并发请求数量
    time = int(input("循环并发次数: "))  # 获取循环并发次数

    # 构造完整的URL（假设是HTTP协议）
    url = f"http://{url}:{port}"

    # 创建单个事件循环
    loop = asyncio.get_event_loop()

    # 循环执行压力测试
    for i in range(time):
        print(f"第{i + 1}轮并发开始...")
        try:
            # 设置超时机制，避免无限等待
            loop.run_until_complete(asyncio.wait_for(main(url, num_requests), timeout=30))  # 超时时间为30秒
        except asyncio.TimeoutError:
            print(f"第{i + 1}轮并发超时，跳过本轮...")
        except Exception as e:
            print(f"第{i + 1}轮并发失败: {e}")
        else:
            print(f"第{i + 1}轮并发完成，当前总成功次数: {tt}")

    # 关闭事件循环
    loop.close()

    # 运行结束后打印总结信息
    print(f"运行结束，总成功次数: {tt}")
