# 分支heroku-deploy：部署“学习笔记”到服务器

由于众所周知的特殊网络原因，以及相较于heroku，国内有更好的云服务器可以使用，故main分支中只限于“学习笔记”在本地计算机中运行，有关使用heroku部署到服务器的内容记录在本分支中。

# 1. 建立Heroku账户

很简单，只需要到官网注册即可，注意需要使用魔法，可以尝试一下 https://github.com/freefq/free （以上纯属二进制码的随机组合生成的文字，与本人毫无关系，特此声明）

# 2. 创建应用程序网站

在官网创建新应用程序，这里名称选为 https://learning-log-for-free.herokuapp.com ，堆栈选择heroku-20

# 3. 安装必要的包

还需安装三个包，以便在服务器上支持Django项目提供的服务。

在虚拟环境中安装：
- django-heroku  --version = 0.3.1
- gunicorn  --version = 19.9.0
- psycopg2  --version = 2.7.7

为管理Heroku使用的数据库，psycopg2包必不可少。

djangoheroku包用于管理应用程序的各种配置，使其能够在Heroku服务器上正确地运行。这包括管理数据库，以及将静态文件存储到合适的地方，以便能够妥善地提供它们。静态文件包括样式规则和JavaScript文件。

gunicorn包让服务器能够实时地支持应用程序。

# 4. 创建文件requirements.txt

heroku需要知道项目依赖于哪些包，因此我们用```pip freeze```命令生成requirements.txt文件。这个文件包含当前项目中安装的所有包。

在命令行行中输入：
```shell
pip freeze > requirements.txt
```

生成的requirements.txt文件如下：
```txt
dj-database-url==0.5.0
Django==2.2
django-bootstrap4==0.0.7
django-heroku==0.3.1
gunicorn==19.9.0
psycopg2==2.7.7
pytz==2018.9
sqlparse==0.2.4
whitenoise==6.2.0
wincertstore==0.2
```

我们部署“学习笔记”时，Heroku将安装requirements.txt列出的所有包，从而创建一个环境，其中包含在本地使用的所有包。

# 5. 指定python版本

访问Heroku Dev Center网站的Language Support页面，再单击到Specifying a Python Runtime的链接。

了解支持的Python版本，并使用与你的Python版本最接近的版本。

这里我们使用heroku-20堆栈，官网上查询得与本地环境中使用的python3.7.2最接近的版本是3.7.13，故在项目根目录下创建runtime.txt，在其中输入：
```txt
python-3.7.13
```

# 6. 为部署到Heroku而修改settings.py

在learning_log/settings.py末尾添加heroku环境设置：
```Python
# heroku settings
import django_heroku
django_heroku.settings(locals())
```

这里导入了模块django_heroku 并调用了函数settings()。这个函数将一些设置修改为Heroku环境要求的值。

# 7. 创建启动进程的Procfile

Procfile告诉Heroku应该启动哪些进程，以便正确地提供项目需要的服务。

在项目根目录下创建Procfile文件，在其中输入：
```txt
web: guincore learning_log.wsgi --log-file - 
```

这行代码让Heroku将Gunicorn用作服务器，并使用learning_log/wsgi.py中的设置来启动应用程序。标识log-file 告诉Heroku应将哪些类型的事件写入日志。

# 8. 部署到heroku

将“学习笔记”部署到heroku服务器，heroku提供了三种方法：
- Heroku Git (Use Heroku CLI)
- GitHub (connect)
- Container Registry (Use Heroku CLI)

这里我们选择第二种，直接通过GitHub部署。

首先将文件git commit到本地分支heroku-deploy完毕，并推送到GitHub仓库的同名分支中。

*注意：这里通过git上传时，.gitignore文件需加上*"\*.sqlite3"*来忽略跟踪对本地数据库的修改，因为如果在服务器上使用的是SQLite，将项目推送到服务器时，可能会不小心用本地测试数据库覆盖在线数据库。*

在heroku中关联上GitHub账户，连接上本项目，选择heroku-deploy分支，进行构建，直至构建完成。

*注意：第一次启动程序时可能出现无论是登录还是注册网页出错的页面，这是没有迁移数据库导致的。在settings中选择run console，在控制台中输入*```python manage.py migrate```*进行数据库迁移，然后重新构建即可。*

至此完成了简易的服务器部署。

也可以用heroku CLI进行部署和推送，具体可以查看[Python Crash Course, 2nd Edition by Eric Matthes](https://github.com/ehmatthes/pcc_2e)，这里也附上有关这一节的书：
- [Python Crash Course, 2nd Edition by Eric Matthes p448-461, EN]()
- [Python Crash Course, 2nd Edition by Eric Matthes p514-529, CH]()
