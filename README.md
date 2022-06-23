# 用 Django 创建“学习笔记”Web应用程序

编写一个名为“学习笔记”的Web应用程序，让用户能够记录感兴趣的主题，并在学习每个主题的过程中添加日志条目。“学习笔记”的主页对这个网站进行描述，并邀请用户注册或登录。用户登录后，可以创建新主题、添加新条目以及阅读既有的条目。

# 1. 使用Django

## 1.1 建立项目

### 1.1.1 创建项目
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

### 1.1.2 创建数据库

命令行中输入：
```Python
python manage.py migrate
```
新建一个数据库，让Django确保数据库与项目的当前状态匹配

### 1.1.3 查看项目
核实Django正确地创建了项目：

命令行输入：
```Python
python manage.py runserver
```
查看项目的状态

可以看到Django启动了一个名为 development server 的服务器，使能够查看系统中的项目，了解其工作情况。如果在浏览器中输入URL以请求页面，该Django服务器将进行响应：生成合适的页面，并将其发送给浏览器。

URL(http://127.0.0.1:8000/)表明项目将在计算机（即127.0.0.1）的端口8000上侦听当前系统发出的请求。

当要关闭这个服务器时，可切换到执行命令runserver 时所在的终端窗口，再退出。

## 1.2 创建应用程序

在保持runserver运行的前提下，打开新终端窗口，在manage.py所在目录下激活虚拟环境

命令行中输入：
```Python
python manage.py startapp learning_logs
```

让Django搭建创建应用程序所需的基础设施

此时在当前目录下创建learning_logs文件夹，该文件夹下包含：

- learning_logs/admin.py
- learning_logs/apps.py
- learning_logs/models.py —— 定义要在应用程序中管理的数据
- learning_logs/tests.py
- learning_logs/views.py
- learning_logs/migrations

### 1.2.1 定义模型

打开 learning_logs/models.py，初始文件如下：
```Python
from django.db import models

# Create your models here.
```

learning_logs/models.py导入models模块，并让我们创建模型，告诉Django如何处理应用程序中存储的数据。

建立用户将存储的主题模型如下：
```Python
from django.db import models

# Create your models here.
class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text
```

在Topic类中添加两个属性：text(type:CharField) 和 date_added(type:DateTimeField)，分别用以存储主题名和创建新主题时当前的日期和时间

Django通过调用方法__str__()来显示模型的简单表示

### 1.2.2 激活模型
让Django将前述应用程序包含到项目中激活模型后才能使用这些模型

在learning_log/settings.py文件的INSTALLED_APPS列表中添加个人创建的learning_logs应用程序，最终列表如下所示：
```Python
INSTALLED_APPS = [
    # my applications
    'learning_logs',

    # default applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

*注意：将自己创建的应用程序放在默认应用程序之前，覆盖默认应用程序的行为*

接下来需让Django修改数据库，使其能够存储与模型Topic相关的信息。

在命令行中输入：
```Python
python manage.py makemigrations learning_logs
```

命令makemigrations让Django确定该如何修改数据库，使其能够存储与前面定义的新模型相关联的数据。输出表明Django创建了一个名为learning_logs/migrations/0001_initial.py的迁移文件，这个文件将在数据库中为模型Topic创建一个表。

下面应用这种迁移，让Django替我们修改数据库，在命令行中输入：
```Python
python manage.py migrate
```

综上，此后每当需要修改“学习笔记”管理的数据时，都采取如下三个步骤：

修改learning_logs/models.py，对learning_logs调用makemigrations，以及让Django迁移项目。

### 1.2.3 Django管理网站

Django提供的管理网站（admin site）让你能够轻松处理模型。管理网站只有网站管理员可以使用。1.2.3就建立管理网站，并通过它使用模型Topic来添加一些主题。

##### 1.2.3.1 创建超级账户

在命令行中输入：
```Python
python manage.py createsuperuser
```

超级账户管理员创建如下：
```Python
Username: django_admin
Email address: 123456@gmail.com
Password: learning_log123
Password (again): learning_log123
```

##### 1.2.3.2 向管理网站注册模型

打开 learning_logs/admin.py，初始文件如下：
```Python
from django.contrib import admin

# Register your models here.
```

为向管理网站注册Topic，在 learning_logs/admin.py 中首先导入要注册的模型。admin.site.register()让Django通过管理网站管理模型
```Python
from django.contrib import admin

# Register your models here.
from .models import Topic

admin.site.register(Topic)
```

现在，使用超级用户账户访问管理网站：访问(http://127.0.0.1:8000/admin/)，登录超级账户。此时你能够添加和修改用户和用户组，还可管理与刚才定义的模型Topic相关的数据。

##### 1.2.3.3 添加主题

向管理网站注册Topic 后，来添加第一个主题。为此，单击Topics进入主题页面。单击Add，出现用于添加新主题的表单。输入内容后Save保存。

### 1.2.4 定义模型Entry

用户需要在学习笔记中能够添加条目，定义多对一关系（一个特定主题有多个条目与之关联）的模型Entry，并放入learning_logs/models.py中。

```Python
class Entry(models.Model):
    '''学到某个主题的具体知识'''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        '''返回模型的字符串表示'''
        return f"{self.text[:50]}..."
```

像Topic 一样，Entry 也继承了Django基类Model。

第一个属性topic是个ForeignKey实例。foreign key指向数据库中的另一条记录，这里是将每个条目关联到特定主题。创建每个主题时，都分配了一个键（ID）。需要在两项数据之间建立联系时，Django使用与每项信息相关联的键。我们稍后将根据这些联系获取与特定主题相关联的所有条目。

实参on_delete=models.CASCADE让Django在删除主题的同时删除所有与之相关联的条目（级联删除cascading delete）。

属性text是TextField实例。

属性date_added让我们能够按创建顺序呈现条目，并在每个条目旁边放置时间戳。

在Entry类中嵌套了Meta类。Meta存储用于管理模型的额外信息。在这里，它让我们能够设置一个特殊属性，让Django在需要时使用Entries来表示多个条目。如果没有这个类，Django将使用Entrys来表示多个条目。

方法__str__()告诉Django，呈现条目时应显示哪些信息。

### 1.2.5 迁移模型Entry

在learning_logs/models.py中添加新模型后，如 1.2.2 中所说，需要再次迁移数据库。

命令行中输入：
```Python
python manage.py makemigrations learning_logs
```

再输入：
```Python
python manage.py migrate
```

完成数据库的迁移并查看输出

此时生成一个新的迁移文件learning_logs/migrations/0002_entry.py，它告诉Django如何修改数据库，使其能够存储与模型Entry相关的信息

### 1.2.6 向管理网站注册Entry

还需要注册模型Entry。为此learning_logs/admin.py文件中添加如下代码：
```Python
admin.site.register(Entry)
```

此时再次进入服务器(http://127.0.0.1:8000/admin/)，将看到Learning_logs下列出了Entries。

单击Entries的Add链接，或者单击Entries再选择Add entry，将看到一个下拉列表，供你选择要为哪个主题创建条目，以及一个用于输入条目的文本框。

### 1.2.7 Django Shell

在活动状态的虚拟环境中执行时，命令```python manage.py shell```启动shell，就能够探索存储在项目数据库中的数据。

如下方代码导入了模块learning_logs.models中的模型Topic，再使用方法Topic.objects.all() 获取模型Topic 的所有实例，这将返回一个称为查询集(queryset)的列表。此时可以像遍历列表一样遍历查询集。将返回的查询集存储在topics中，再打印每个主题的id属性和字符串表示。知道主题对象的ID后，就可使用方法Topic.objects.get()获取该对象并查看其属性。我们还可以查看与主题相关联的条目。前面给模型Entry定义了属性topic。这是一个ForeignKey，将条目与主题关联起来。利用这种关联，Django能够获取与特定主题相关联的所有条目。
```Shell
# python manage.py shell

>>> from learning_logs.models import Topic
>>> Topic.objects.all()
<QuerySet [<Topic: Chess>, <Topic: Rock Climbing>]>
>>> topics = Topic.objects.all()
>>> for topic in topics:
...     print(topic.id, topic)
...
1 Chess
2 Rock Climbing
>>> t = Topic.objects.get(id=1)
>>> t.text
'Chess'
>>> t.date_added
datetime.datetime(2022, 6, 22, 11, 36, 53, 999755, tzinfo=<UTC>)
>>> t.entry_set.all()
<QuerySet [<Entry: The opening is the first part of the game, roughly...>, <Entry: In the opening phase of the game, it is important t...>]>
>>> 
```

要通过外键关系获取数据，可使用相关模型的小写名称、下划线和单词set。例如，假设有模型Pizza 和Topping，而Topping通过一个外键关联到Pizza。如果有一个名为my_pizza的Pizza对象，就可使用代码my_pizza.topping_set.all() 来获取这张比萨的所有配料。

编写用户可请求的页面时，我们将使用这种语法。确认代码能获取所需的数据时，shell很有帮助。如果代码在shell中的行为符合预期，那么它们在项目文件中也能正确地工作。如果代码引发了错误或获取的数据不符合预期，那么在简单的shell环境中排除故障要比在生成页面的文件中排除故障容易得多。我们不会太多地使用shell，但应继续使用它来熟悉对存储在项目中的数据进行访问的Django语法。

*注意：每次修改模型后，都需要重启shell，这样才能看到修改的效果。要退出shell会话，linux按Ctrl+D，Windows按Ctrl+Z，再按Enter。*

## 1.3 创建学习笔记主页

使用Django创建页面的过程分三个阶段：定义URL，编写视图和编写模板。URL模式描述了URL是如何设计的，让Django知道如何将浏览器请求与网站URL匹配，以确定返回哪个页面。

每个URL都被映射到特定的视图——视图函数获取并处理页面所需的数据。视图函数通常使用模板来渲染页面，而模板定义页面的总体结构。

### 1.3.1 映射URL

当前基础URL(http://127.0.0.1:8000/)返回默认的Django网站，我们将其修改为映射到“学习笔记”的主页。

打开learning_log/urls.py，其代码如下：
```Python
"""learning_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

导入了一个模块和一个函数，以便对管理网站的URL进行管理。

主体定义变量urlpatterns。在这个针对整个项目的learning_log/urls.py文件中，变量urlpatterns包含项目中应用程序的URL。

模块admin.site.urls定义了可在管理网站中请求的所有URL。

修改urlpatterns的值如下，使其包含learning_logs的URL
```Python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls')),
]
```

默认的urls.py包含在文件夹learning_log中，现在需要在文件夹learning_logs中再创建一个urls.py文件。再在learning_logs/urls.py中输入如下代码：
```Python
'''定义learning_logs的URL模式'''

from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    # main page
    path('', views.index, name='index')
]
```

导入函数path ，使用它将URL映射到视图。导入模块views（在learning_logs文件夹下）。

变量app_name让Django能够将learning_logs/urls.py文件同项目内其他应用程序中的同名文件区分开来。在这个模块中，变量urlpatterns是一个列表，包含可在应用程序learning_logs中请求的页面。实际的URL模式是对函数path()的调用，这个函数接受三个实参。第一个是字符串，帮助Django正确地路由（route）请求。收到请求的URL后，Django力图将请求路由给一个视图。为此，它搜索所有的URL模式，找到与当前请求匹配的那个。Django忽略项目的基础URL(http://17.0.0.1:8000/)，因此空字符串与基础URL匹配。其他URL都与这个模式不匹配。如果请求的URL与任何既有的URL模式都不匹配，Django将返回一个错误页面。path() 的第二个实参指定了要调用learning_logs/view.py中的哪个函数。请求的URL与前述正则表达式匹配时，Django将调用learning_logs/view.py中的函数index()。第三个实参将这个URL模式的名称指定为index，让我们能够在代码的其他地方引用它。每当需要提供到这个主页的链接时，都将使用这个名称，而不编写URL。

### 1.3.2 编写视图

视图函数接受请求中的信息，准备好生成页面所需的数据，再将这些数据发送给浏览器——这通常是使用定义页面外观的模板实现的。

learning_logs/views.py是执行命令```python manage.py startapp```时自动生成的，当前代码如下：
```Python
from django.shortcuts import render

# Create your views here.

```
当前，这个文件只导入了函数render() ，它根据视图提供的数据渲染响应。

我们在这个文件中添加为主页编写视图的代码：
```Python
from django.shortcuts import render

# Create your views here.
def index(request):
    '''main page of the learning log project'''
    return render(request, 'learning_logs/index.html')
```

URL请求与刚才定义的模式匹配时，Django将在文件learning_logs/views.py中查找函数index()，再将对象request传递给这个视图函数。这里不需要处理任何数据，因此这个函数只包含调用render()的代码。这里向函数render()提供了两个实参：对象request以及一个可用于创建页面的模板。

### 1.3.3 编写模板

1.3.2中最后已经提供了一个可用于创建页面的模板。现在来编写这个模板。

模板定义页面的外观，而每当页面被请求时，Django将填入相关的数据。模板让你
能够访问视图提供的任何数据。

在文件夹learning_logs中新建一个文件夹，并将其命名为templates。在文件夹templates中，再新建一个文件夹，并将其命名为learning_logs，则建立了Django能够明确解读的结构，即便项目很大、包含很多应用程序亦如此。

在最里面的文件夹learning_logs中，新建一个文件，并将其命名为index.html（这个文件的路径为learning_logs/templates/learning_logs/index.html），再在其中编写如下代码：
```html
<p>Learning Log</p>

<p>Learning Log helps you keep track of your learning, for any topic you are learning about.</p>
```

标签<p></p>标识段落。标签<p>指出段落的开头位置，而标签</p>指出段落的结束位置。这里定义了两个段落：第一个充当标题，第二个阐述了用户可使用“学习笔记”来做什么。

现在，如果请求这个项目的基础URL(http://127.0.0.1:8000/)，将看到刚才创建的页面，而不是默认的Django页面。Django接受请求的URL，发现该URL与模式''匹配，因此调用函数views.index()。这将使用index.html包含的模板来渲染页面。

