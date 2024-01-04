import socket
import ray
from PIL import Image
from pix2tex.cli import LatexOCR

#pip3 install torch pyperclip pillow "pix2tex[gui]" 

ray.init()
model = LatexOCR()
model_ind = ray.put(model)

def start_server():
    # 创建一个TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定IP地址和端口号
    server_address = ('0.0.0.0', 8888)
    server_socket.bind(server_address)

    # 监听连接请求
    server_socket.listen(1)

    while True:
        print('等待客户端连接...')
        client_socket, client_address = server_socket.accept()
        print('客户端已连接:', client_address)

        # 处理客户端请求
        handle_request(client_socket)

def handle_request(client_socket):
    try:
        # 接收客户端上传的图片文件
        image_data = client_socket.recv(1024 * 500)

        # 保存图片文件到指定目录
        save_image(image_data)

        # 获取图片文件
        imgfile = Image.open('/workspace/image.jpg')
        img_ind = ray.put(imgfile)
        # 对接收到的图片进行处理
        text = ray.get(process_image.remote(img_ind))

        # 返回处理后的结果给客户端
        send_response(client_socket, text)
    except Exception as e:
        print(e)
        print('关闭与客户端的连接')
        client_socket.close()
        

def save_image(image_data):
    # 保存图片文件到指定目录
    with open('/workspace/image.jpg', 'wb') as file:
        file.write(image_data)
#(num_gpus=1)
@ray.remote
def process_image(img):
    if img != None:
        text = str(ray.get(model_ind)(img))
        return text
    else: return 'error'
        # print(text)
        # pyperclip.copy('\\begin{align}' + text + '\\end{align}')

def send_response(client_socket, message):
    # 返回处理后的结果给客户端
    client_socket.send(message.encode())

if __name__ == '__main__':
    start_server()
