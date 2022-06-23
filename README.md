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

URL http://127.0.0.1:8000/ 表明项目将在计算机（即127.0.0.1）的端口8000上侦听当前系统发出的请求。

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

现在，使用超级用户账户访问管理网站：访问 http://127.0.0.1:8000/admin/ ，登录超级账户。此时你能够添加和修改用户和用户组，还可管理与刚才定义的模型Topic相关的数据。

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

此时再次进入服务器 http://127.0.0.1:8000/admin/ ，将看到Learning_logs下列出了Entries。

单击Entries的Add链接，或者单击Entries再选择Add entry，将看到一个下拉列表，供你选择要为哪个主题创建条目，以及一个用于输入条目的文本框。

### 1.2.7 Django Shell

在活动状态的虚拟环境中执行时，命令```python manage.py shell```启动shell，就能够探索存储在项目数据库中的数据。

如下方代码导入了模块learning_logs.models中的模型Topic，再使用方法Topic.objects.all()获取模型Topic 的所有实例，这将返回一个称为查询集(queryset)的列表。此时可以像遍历列表一样遍历查询集。将返回的查询集存储在topics中，再打印每个主题的id属性和字符串表示。知道主题对象的ID后，就可使用方法Topic.objects.get()获取该对象并查看其属性。我们还可以查看与主题相关联的条目。前面给模型Entry定义了属性topic。这是一个ForeignKey，将条目与主题关联起来。利用这种关联，Django能够获取与特定主题相关联的所有条目。
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

当前基础URL http://127.0.0.1:8000/ 返回默认的Django网站，我们将其修改为映射到“学习笔记”的主页。

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
'''define URL patterns for learning_logs'''

from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    # home page
    path('', views.index, name='index'),
]
```

导入函数path ，使用它将URL映射到视图。导入模块views（在learning_logs文件夹下）。

变量app_name让Django能够将learning_logs/urls.py文件同项目内其他应用程序中的同名文件区分开来。在这个模块中，变量urlpatterns是一个列表，包含可在应用程序learning_logs中请求的页面。实际的URL模式是对函数path()的调用，这个函数接受三个实参。第一个是字符串，帮助Django正确地路由（route）请求。收到请求的URL后，Django力图将请求路由给一个视图。为此，它搜索所有的URL模式，找到与当前请求匹配的那个。Django忽略项目的基础URL http://17.0.0.1:8000/ ，因此空字符串与基础URL匹配。其他URL都与这个模式不匹配。如果请求的URL与任何既有的URL模式都不匹配，Django将返回一个错误页面。path() 的第二个实参指定了要调用learning_logs/view.py中的哪个函数。请求的URL与前述正则表达式匹配时，Django将调用learning_logs/view.py中的函数index()。第三个实参将这个URL模式的名称指定为index，让我们能够在代码的其他地方引用它。每当需要提供到这个主页的链接时，都将使用这个名称，而不编写URL。

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

现在，如果请求这个项目的基础URL http://127.0.0.1:8000/ ，将看到刚才创建的页面，而不是默认的Django页面。Django接受请求的URL，发现该URL与模式''匹配，因此调用函数views.index()。这将使用index.html包含的模板来渲染页面。

## 1.4 创建其他页面

将创建两个显示数据的页面，其中一个列出所有的主题，另一个显示特定主题的所有条目。对于每个页面，我们都将指定URL模式、编写一个视图函数并编写一个模板。但这样做之前，我们先创建一个父模板，项目中的其他模板都将继承它。

### 1.4.1 模板继承

创建网站时，一些通用元素几乎会在所有页面中出现。在这种情况下，可编写一个包含通用元素的父模板，并让每个页面都继承这个模板，而不必在每个页面中重复定义这些通用元素。

##### 1.4.1.1 父模板

创建learning_logs\templates\learning_logs\base.html作为父模板，其他模板可继承它。其代码如下：
```html
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a>
</p>

{% block content %}{% endblock content %}
```

第一部分创建一个包含项目名的段落，该段落也是到主页的链接。为创建链接，使用了一个模板标签 ，它是用花括号和百分号```{% %}```表示的。模板标签是一小段代码，生成要在页面中显示的信息。这里的模板标签生成一个URL，该URL与在learning_logs/urls.py中定义的名为index的URL模式匹配。在本例中，learning_logs是一个命名空间，而index是该命名空间中一个名称独特的URL模式。这个命名空间来自在文件learning_logs/urls.py中赋给app_name的值。

在简单的HTML页面中，链接是使用锚标签```<a>```定义的：
```html
<a href="link_url">link text</a>
```

通过使用模板标签来生成URL，能很容易地确保链接是最新的：只需修改urls.py中的URL模式，Django就会在页面下次被请求时自动插入修改后的URL。在本项目中，每个页面都将继承base.html，因此从现在开始，每个页面都包含到主页的链接。

接着插入了一对块标签。这个块名为content，是一个占位符，其中包含的信息由子模板指定。子模板并非必须定义父模板中的每个块，因此在父模板中，可使用任意多个块来预留空间，而子模板可根据需要定义相应数量的块。

##### 1.4.1.2 子模版

现在重写learning_logs\templates\learning_logs\index.html，使其继承learning_logs\templates\learning_logs\base.html。

修改代码如下：
```html
{% extends "learning_logs/base.html" %}

{% block content %}
    <p>Learning Log helps you keep track of your learning, for any topic you are learning about.</p>
{% endblock content %}
```

子模板的第一行必须包含标签```{% extends %}```，让Django知道它继承了哪个父模板。文件base.html位于learning_logs中，因此父模板路径中包含learning_logs。这行代码导入模板base.html的所有内容，让index.html能够指定要在content块预留的空间中添加的内容。

插入了一个名为content的```{% block %}```标签，以定义content块。不是从父模板继承的内容都包含在content块中，在这里是一个描述项目“学习笔记”的段落。

使用标签```{% endblock content %}```指出了内容定义的结束位置。在标签```{% endblock %}```中，并非必须指定块名，但如果模板包含多个块，指定块名有助于确定结束的是哪个块。

*模板继承的优点：在子模板中，只需包含当前页面特有的内容。*

### 1.4.2 显示所有主题的页面

显示用户创建的所有主题，是一个需要使用数据的页面。

##### 1.4.2.1 URL模式

首先，定义显示所有主题的页面的URL。我们通常使用一个简单的URL片段来指出页面显示的信息，这里使用单词topics，因此URL http://localhost:8000/topics/ 将返回显示所有主题的页面。

在learning_logs/urls.py中修改代码如下：
```Python
'''define URL patterns for learning_logs'''

from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    # home page
    path('', views.index, name='index'),

    # page that shows all topics
    path('topics/', views.topics, name='topics'),
]
```

这里在用于主页URL的字符串参数中添加了topics/。Django检查请求的URL时，这个模式与如下URL匹配：基础URL后面跟着topics。可在末尾包含斜杠，也可省略，但单词topics后面不能有任何东西，否则就与该模式不匹配。URL与该模式匹配的请求都将交给views.py中的函数topics()处理。

##### 1.4.2.2 视图

函数topics()需要从数据库中获取数据并提交给模板，修改learning_logs/view.py如下：
```Python
from django.shortcuts import render

from .models import Topic

# Create your views here.
def index(request):
    '''show home page'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''show all topics'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
```

首先导入与所需数据相关联的模型。函数topics()包含一个形参：Django从服务器那里收到的request对象。

查询数据库——请求提供Topic对象，并根据属性date_added进行排序。返回的查询集被存储在topics中。

定义一个将发送给模板的上下文。上下文是一个字典，其中的键是将在模板中用来访问数据的名称，而值是要发送给模板的数据。这里只有一个键值对，包含一组将在页面中显示的主题。

创建使用数据的页面时，除了对象request和模板的路径外，还将变量context传递给render()

##### 1.4.2.3 模板

显示所有主题的页面的模板接受字典context，以便使用topics()提供的数据。在learning_logs/templates/learning_logs中创建topics.html，在这个模板中显示主题。其代码如下：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <p>Topics</p>

    <ul>
        {% for topic in topics %}
            <li>{{ topic }}</li>
        {% empty %}
            <li>No topics have been added yet.</li>
        {% endfor %}
    </ul>

{% endblock content %}
```

首先使用标签```{% extends %}```来继承base.html，再开始定义content块。这个页面的主体是一个项目列表，其中列出了用户输入的主题。在标准HTML中，项目列表称为无序列表，用标签```<ul></ul>```表示。包含所有主题的项目列表始于```<ul>```。

使用一个相当于for循环的模板标签，它遍历字典context中的列表topics。模板中使用的代码与Python代码存在一些重要差别：Python使用缩进来指出哪些代码行是for循环的组成部分；而在模板中，每个for循环都必须使用```{% endfor %}```标签来显式地指出其结束位置。因此在模板中，循环类似于下面这样：
```html
{% for item in list %}
    do something with each item
{% endfor %}
```

在循环中，要将每个主题转换为项目列表中的一项。要在模板中打印变量，需要将变量名用双花括号括起。这些花括号不会出现在页面中，只是用于告诉Django我们使用了一个模板变量。因此每次循环时，代码```{{ topic }}```都被替换为topic的当前值。HTML标签```<li></li>```表示一个项目列表项。在标签对```<ul></ul>```内部，位于标签```<li>```和```</li>```之间的内容都是一个项目列表项。

使用模板标签```{% empty %}```，它告诉Django在列表topics为空时该如何办。这里是打印一条消息，告诉用户还没有添加任何主题。最后两行分别结束for循环和项目列表。

下面需要修改父模板，使其包含到显示所有主题的页面的链接。修改learning_logs\templates\learning_logs\base.html代码如下：
```html
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a> - 
    <a href="{% url 'learning_logs:topics' %}">Topics</a>
</p>

{% block content %}{% endblock content %}
```

在到主页的链接后面添加一个连字符，再添加一个到显示所有主题的页面的链接——使用的也是模板标签```{% url %}```。这行让Django生成一个链接，它与learning_logs/urls.py中名为topics的URL模式匹配。

现在如果刷新浏览器中的主页，将看到链接Topics。

### 1.4.3 显示特定主题的页面

接下来，需要创建一个专注于特定主题的页面，它显示该主题的名称以及所有条目。

此外，还将修改显示所有主题的页面，让每个项目列表项都变为到相应主题页面的链接。

##### 1.4.3.1 URL模式

显示特定主题的页面的URL模式与前面的所有URL模式都稍有不同，因为它使用主题的id属性来指出请求的是哪个主题

在learning_logs/urls.py中添加与这个URL匹配的模式
```Python
urlpatterns = [
    # home page
    path('', views.index, name='index'),

    # page that shows all topics
    path('topics/', views.topics, name='topics'),

    # detail page for a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
]
```

这个URL模式中的字符串```topics/<int:topic_id>/```。这个字符串的第一部分让Django查找在基础URL后包含单词topics的URL，第二部分```/<int:topic_id>/```与包含在两个斜杠内的整数匹配，并将这个整数存储在一个名为topic_id的实参中。发现URL与这个模式匹配时，Django将调用视图函数topic()，并将存储在topic_id中的值作为实参传递给它。在这个函数中，将使用topic_id的值来获取相应的主题

##### 1.4.3.2 视图

函数topic()需要从数据库中获取指定的主题以及与之相关联的所有条目，在learning_logs\views.py中定义函数topic():
```Python
def topic(request, topic_id):
    '''show a single topic and all its entries'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
```

这是除request对象外还包含另一个形参的视图函数。这个函数接受表达式```/<int:topic_id>/```捕获的值，并将其存储到topic_id中。

使用get()来获取指定的主题，就像前面在Django shell中所做的那样。

获取与该主题相关联的条目，并根据date_added进行排序。date_added前面的减号指定按降序排列，即先显示最近的条目。

将主题和条目都存储在字典context中，再将这个字典发送给模板topic.html

*注意：get和entry_set处的代码称为查询，因为它们向数据库查询了特定的信息。比起先编写视图和模板、再在浏览器中检查结果，在shell中执行代码可更快获得反馈。*

##### 1.4.3.3 模板

这个模板需要显示主题的名称和条目的内容。如果当前主题不包含任何条目，也需向用户指出：

创建learning_logs\templates\learning_logs\topic.html，写入特定主题的模板：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <p>Topic: {{ topic }}</p>

    <p>Entries:</p>

    <ul>
    {% for entry in entries %}
        <li>
            <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
            <p>{{ entry.text|linebreaks }}</p>
        </li>
    {% empty %}
        <li>There are no entries for this topic yet.</li>
    {% endfor %}
    </ul>

{% endblock content %}
```

首先继承base.html。

接下来，显示当前的主题，它存储在模板变量```{{ topic }}```中。变量topic包含在字典context中，所以可以使用。

定义一个显示每个条目的项目列表，并像前面显示所有主题一样遍历条目。每个项目列表项都将列出两项信息：条目的时间戳和完整的文本。

为列出时间戳，我们显示属性date_added的值。在Django模板中，竖线表示模板过滤器，即对模板变量的值进行修改的函数。过滤器```date: 'M d,Y H:i'```以类似于这样的格式显示时间戳：```January 1, 2018 23:00```。

接下来的一行显示text 的完整值，而不仅仅是前50字符。过滤器linebreaks将包含换行符的长条目转换为浏览器能够理解的格式，以免显示为不间断的文本块。

使用模板标签```{% empty %}```打印一条消息，告诉用户当前主题还没有条目。

##### 1.4.3.4 将显示所有主题的页面中的主题设置为链接

在浏览器中查看显示特定主题的页面前，需要修改模板learning_logs\templates\learning_logs\topics.html，让每个主题都链接到相应的页面，其代码修改如下：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <p>Topics</p>

    <ul>
        {% for topic in topics %}
            <li>
                <a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
            </li>
        {% empty %}
            <li>No topics have been added yet.</li>
        {% endfor %}
    </ul>

{% endblock content %}
```

使用模板标签url根据learning_logs中名为topic的URL模式生成了合适的链接。这个URL模式要求提供实参topic_id，因此在模板标签url中添加了属性'topic.id'。现在，主题列表中的每个主题都是链接了，链接到显示相应主题的页面，如 http://127.0.0.1:8000/topics/1/ 。

如果现在刷新显示所有主题的页面，再单击其中的一个主题，就可看到相应的特定主题

*注意：topics.html中添加的是属性topic.id而非实参topic_id。topic.id和topic_id之间存在细微而重要的差别。表达式topic.id检查主题并获取其ID值，而在代码中，变量topic_id是指向该ID的引用。*