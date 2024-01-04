import socket
import time
import pyperclip
import argparse
from PIL import ImageGrab
from tempfile import TemporaryFile
#pip3 install pyperclip pillow

#     img = ImageGrab.grabclipboard()
#     if img != None:
#         text = str(model(img))
#         # pyperclip.copy('\\begin{align}' + text + '\\end{align}')
#         pyperclip.copy(text)
#         print(text)

def start_client(addr='localhost', port=8888):
    # 创建一个socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    server_address = (addr, port)
    client_socket.connect(server_address)

    # 打开图片文件
    img = ImageGrab.grabclipboard()
    if img == None:
        print('No image in clipboard')
        return
    with TemporaryFile('w+b') as f:
        print(img)
        img.save(f, format='JPEG')
        f.seek(0)
        # 将图片文件的内容发送到服务器
        client_socket.send(f.read())

    # 接收服务器返回的消息
    message = client_socket.recv(1024*10).decode()
    pyperclip.copy(message)
    # 打印服务器返回的消息
    print('服务器返回的消息:', message)

    # 关闭socket连接
    client_socket.close()
    #time.sleep(0.5)
    #start_client(addr, port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get LaTeX from image in clipboard')
    parser.add_argument('--addr', default='localhost', help='Server address')
    parser.add_argument('--port', default=8888, help='Server port')
    start_client(**vars(parser.parse_args()))