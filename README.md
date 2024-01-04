# 项目名称

cupyraylab-docker

## 开始

这些说明将指导你如何获取此项目的副本并在本地运行。

### 构建Docker镜像

使用以下命令构建Docker镜像：

```bash
docker build -f ./Dockerfile -t cupyraylab:v1 . 
```

### 运行Docker容器

使用以下命令运行Docker容器：

```bash
docker run -it --shm-size=1.10gb -p 6379:6379 -p 8265:8265 -p 8080:8080 -p 8888:8888 -v D:\dev\raydocker\workspace:/workspace -v D:\dev\raydocker\hf_cache:/hf_cache cupyraylab:v1 /bin/bash
```

### 启动Jupyter Lab

首先，设置Jupyter Lab的密码，然后启动Jupyter Lab：

```bash
jupyter-lab password && jupyter-lab --allow-root --ip 0.0.0.0 --port 8080 --no-browser
```

## 其他