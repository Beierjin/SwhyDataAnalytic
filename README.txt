部署生产环境：
修改 SwhyDataAnalytic.SwhyDataAnalytic.settings.py中
STATIC_ROOT = 'D:/Project/Python/SwhyDataAnalytic'为物理路径

如果修改static文件夹位置，需要修改vim /etc/nginx/nginx.conf中，static位置

