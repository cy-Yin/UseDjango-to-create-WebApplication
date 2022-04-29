# 用 Django 创建“学习笔记”Web应用程序

编写一个名为“学习笔记”的Web应用程序，让用户能够记录感兴趣的主题，并在学习每个主题的过程中添加日志条目。“学习笔记”的主页对这个网站进行描述，并邀请用户注册或登录。用户登录后，可以创建新主题、添加新条目以及阅读既有的条目。

### 创建项目
anaconda创建虚拟环境 useDjango

在useDjango中安装:

- python --version = 3.7.2

- Django --version = 2.2.0

在当前环境下执行如下命令：
```Python
django-admin startproject learing_log .
```

创建 learning_log 文件夹以及manage.py文件

- manage.py —— 接受命令并将其交给Django的相关部分去运行
- learning_log/settings.py —— 设置文件。指定Django如何与你的系统交互以及如何管理项目
- learning_log/urls.py —— 告诉Django应该创建哪些网页来响应浏览器请求
- learning_log/wsgi.py —— 帮助Django提供它创建的文件 ( wsgi —— web server gateway interface )