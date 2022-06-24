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

# 2. 用户账户的创建和设置

## 2.1 让用户输入数据

在建立用于创建用户账户的身份验证系统之前，先添加几个页面，让用户能够输入数据，包括添加新主题，添加新条目以及编辑既有条目。

用户不需要与管理网站交互，所以使用Django的表单创建工具来创建让用户能够输入数据的页面。

### 2.1.1 添加新主题

创建基于表单的页面的方法同样是：定义URL，编写视图函数以及编写模板。此外，与之前不同，需要导入包含表单的模块forms.py。

##### 2.1.1.1 用于添加主题的表单

用户输入信息时，我们需要进行验证，确认提供的信息是正确的数据类型，而不是恶意的信息，如中断服务器的代码。然后，对这些有效信息进行处理，并将其保存到数据库的合适地方。这些工作很多都是由Django自动完成的。

在Diango中，创建表单的最简单方式是使用ModelForm，它根据已经定义好的模型中的信息自动创建表单。

在learning_logs文件夹中创建forms.py，编写第一个表单如下：
```python
from django import forms

from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
```

首先导入模块forms和模型Topic。

定义TopicForm类继承forms.ModelForm。最简单的ModelForm 版本只包含一个内嵌的Meta类，让Django根据哪个模型创建表单以及在表单中包含哪些字段。

根据模型Topic 创建表单，其中只包含字段text。

设置labels的第一个键值对让Django不要为字段text生成标签。

##### 2.1.1.2 URL模式new_topic

在learning_logs/urls.py中创建页面new_topic的URL模式如下：
```Python
urlpatterns = [
    # -------- snip -------- #

    # page for adding a new topic
    path('new_topic/', views.new_topic, name='new_topic')
]
```

当用户要添加到新主题时，切换到 http://127.0.0.1:8000/new_topic/ 。

这个URL模式将请求交给视图函数new_topic()。

##### 2.1.1.3 视图函数new_topic()

函数new_topic() 需要处理两种情形。一是刚进入new_topic页面（在这种情况下应显示空表单）；二是对提交的表单数据进行处理，并将用户重定向到页面topics。

在learning_logs/views.py中导入函数redirect，用户提交主题后将使用这个函数重定向到页面topics。函数redirect将视图名作为参数，并将用户重定向到这个视图。还导入了刚创建的表单TopicForm。

learning_logs/views.py定义新函数new_topic()如下：
```Python
from .forms import TopicForm

def new_topic(request):
    '''add a new topic'''
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
```

GET请求和POST请求：

创建Web应用程序时，将用到的两种主要请求类型是GET请求和POST请求。对于只是从服务器读取数据的页面，使用GET请求；在用户需要通过表单提交信息时，通常使用POST请求。处理所有表单时，都将指定使用POST方法。

函数new_topic()将请求对象作为参数。用户初次请求该页面时，其浏览器将发送GET请求；用户填写并提交表单时，其浏览器将发送POST请求。根据请求的类型，可确定用户请求的是空表单（GET请求）还是要求对填写好的表单进行处理（POST请求）。

new_topic()的第一个if测试确定请求方法是GET还是POST。如果请求方法不是POST，请求就可能是GET，因此需要返回一个空表单。（即便请求是其他类型的，返回空表单也不会有任何问题。）

下一行创建一个TopicForm实例，将其赋给变量form，再通过上下文字典将这个表单发送给模板。由于实例化TopicForm时没有指定任何实参，Django将创建一个空表单，供用户填写。

如果请求方法为POST，将执行else 代码块，对提交的表单数据进行处理。使用用户输入的数据（存储在request.POST中）创建一个TopicForm实例，这样对象form 将包含用户提交的信息。

要将提交的信息保存到数据库，必须先通过检查确定它们是有效的。方法is_valid() 核实用户填写了所有必不可少的字段（表单字段默认都是必不可少的），且输入的数据与要求的字段类型一致。这种自动验证避免了我们去做大量的工作。如果所有字段都有效，就可调用save()，将表单中的数据写入数据库。

保存数据后，就可离开这个页面了。为此，使用redirect()将用户的浏览器重定向到页面topics。在页面topics中，用户将在主题列表中看到他刚输入的主题。

在这个视图函数的末尾定义了变量context ，并使用稍后将创建的模板new_topic.html来渲染页面。这些代码不在if代码块内，因此无论是用户刚进入new_topic页面还是提交的表单数据无效，这些代码都将执行。用户提交的表单数据无效时，将显示一些默认的错误消息，帮助用户提供有效的数据。

##### 2.1.1.4 模板new_topic

下面创建新模板learning_logs\templates\learning_logs\new_topic.html，用于显示刚创建的表单：
```html
{% extends "learning_logs/base.html" %}

{% block content %}
    <p>Add a new topic:</p>

    <form action="{% url 'learning_logs:new_topic' %}" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button name="submit">Add topic</button>
    </form>

{% endblock content %}
```

定义了一个HTML表单。实参action告诉服务器将提交的表单数据发送到哪里。这里将它发回给视图函数new_topic()。实参method让浏览器以POST请求的方式提交数据。

Django使用模板标签```{% csrf_token %}```来防止攻击者利用表单来获得对服务器未经授权的访问（这种攻击称为跨站请求伪造）。

只需创建模板变量```{{form.as_p }}```，就可让Django自动创建显示表单所需的全部字段。修饰符as_p让Django以段落格式渲染所有表单元素，这是一种整洁地显示表单的简单方式。

Django不会为表单创建提交按钮，因此我们手动定义。

##### 2.1.1.5 链接到页面new_topic

下面在页面topics中添加到页面new_topic的链接：
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

    <a href="{% url 'learning_logs:new_topic' %}">Add a new topic</a>

{% endblock content %}
```

这个链接放在既有主题列表的后面。

### 2.1.2 添加新条目

通过在learning_logs/forms.py再添加一个类，并进行后续的定义URL、编写视图函数和编写模板，并链接到添加新条目的页面，使得用户账户可以添加新条目。

##### 2.1.2.1 用于添加新条目的表单

需要创建一个与模型Entry相关联的表单，但这个表单的定制程度比TopicForm更高一些。

在learning_logs/forms.py再添加一个类EntryForm()
```Python
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
```

新类EntryForm继承了forms.ModelForm，它包含的Meta类指出了表单基于的模型以及要在表单中包含哪些字段。这里给字段text指定了标签'Entry:'。

定义属性widgets 。小部件（widget）是一个HTML表单元素，如单行文本框、多行文本区域或下拉列表。通过设置属性widgets，可覆盖Django选择的默认小部件。通过让Django使用forms.Textarea，我们定制了字段'text'的输入小部件，将文本区域的宽度设置为80列，而不是默认的40列。这给用户提供了足够的空间来编写有意义的条目。

##### 2.1.2.2 URL模式new_entry

在用于添加新条目的页面的URL模式中，需要包含实参topic_id，因为条目必须与特定的主题相关联。

在learning_logs/urls.py添加该URL模式如下：
```Python
urlpatterns = [
    # -------- snip -------- #

    # page for adding a new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
]
```

这个URL模式与形如 http://127.0.0.1:8000/new_entry/id/ 的URL匹配，其中的id是一个与主题ID匹配的数。代码```<int:topic_id>```捕获一个数值，并将其赋给变量topic_id。请求的URL与这个模式匹配时，Django将请求和主题ID发送给函数new_entry()。

##### 2.1.2.3 视图函数new_entry()

在learning_logs/views.py中定义并添加视图函数new_entry()：
```Python
from .forms import EntryForm

def new_entry(request, topic_id):
    '''add a new entry for a particular topic'''
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
```

导入刚刚创建的EntryForm类。

new_entry()的定义包含形参topic_id，用于存储从URL中获得的值。渲染页面和处理表单数据时，都需要知道针对的是哪个主题，因此使用topic_id来获得正确的主题。
用```if request.method != 'POST'```语句检查请求方法是POST还是GET。

如果是GET请求，就执行if代码块，创建一个空的EntryForm实例。如果请求方法为POST，就对数据进行处理：创建一个EntryForm实例，使用request对象中的POST数据来填充它。然后检查表单是否有效。如果有效，就设置条目对象的属性topic，再将条目对象保存到数据库。

调用save()时，传递实参commit=False，让Django创建一个新的条目对象，并将其赋给new_entry，但不保存到数据库中。将new_entry的属性topic设置为在这个函数开头从数据库中获取的主题，再调用save()且不指定任何实参。这将把条目保存到数据库，并将其与正确的主题相关联。

调用redirect()，它要求提供两个参数：要重定向到的视图和要给视图函数提供的参数。这里重定向到topic()，而这个视图函数需要参数topic_id。视图函数topic()渲染新增条目所属主题的页面，其中的条目列表包含新增的条目。

在视图函数new_entry()的末尾，我们创建了一个上下文字典，并使用模板new_entry.html渲染页面。这些代码将在用户刚进入页面或提交的表单数据无效时执行。

##### 2.1.2.4 模板new_entry

在learning_logs\templates\learning_logs中创建new_entry.html，并在其中创建模板new_entry:
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <p><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></p>

    <p>Add a new entry:</p>
    <form action="{% url 'learning_logs:new_entry' topic.id %}" method='post'>
        {% csrf_token %}
        {{ form.as_p }}
        <button name='submit'>Add entry</button>
    </form>
{% endblock content %}
```

在页面顶端显示主题，让用户知道自己是在哪个主题中添加条目。该主题名也是一个链接，可用于返回到该主题的主页面。

表单的实参action包含URL中的topic_id值，让视图函数能够将新条目关联到正确的主题。除此之外，这个模板与模板new_topic.html完全相同。

##### 2.1.2.5 链接到页面new_entry

接下来，需要在显示特定主题的页面中添加到页面new_entry的链接。

我们将这个链接放在条目列表前面，因为在这种页面中，执行的最常见的操作是添加新条目。

修改learning_logs\templates\learning_logs\topic.html如下：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <p>Topic: {{ topic }}</p>

    <p>Entries:</p>
    <p>
        <a href="{% url 'learning_logs:new_entry' topic.id %}">Add new entry</a>
    </p>

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

现在用户可添加新主题，还可在每个主题中添加任意数量的条目。

### 2.1.3 编辑条目

下面创建让用户账户能够编辑既有条目的页面。

##### 2.1.3.1 URL模式edit_entry

该页面的URL传递要编辑的条目的ID，所以对learning_logs/urls.py进行修改如下：
```Python
urlpatterns = [
    # -------- snip -------- #

    # page for editing an entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry')
]
```

在URL（如 http://127.0.0.1:8000/edit_entry/1/ )中传递的ID存储在形参entry_id中。

这个URL模式将与其匹配的请求发送给视图函数edit_entry()。

##### 2.1.3.2 视图函数edit_entry()

页面edit_entry收到GET请求时，edit_entry()将返回一个表单，让用户能够对条目进行编辑；收到POST请求（条目文本经过修订）时，则将修改后的文本保存到数据库。

为实现如下功能，在learning_logs/views.py中定义函数edit_entry()如下：
```Python
from .models import Entry

def edit_entry(request, entry_id):
    '''edit an existing entry'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
```

首先导入模型Entry。

entry获取用户要修改的条目对象以及与其相关联的主题。

在请求方法为GET时将执行的if代码块中，使用实参instance=entry创建一个EntryForm实例。这个实参让Django创建一个表单，并使用既有条目对象中的信息填充它。用户将看到既有的数据，并且能够编辑。

处理POST请求时，传递实参instance=entry和data=request.POST，让Django根据既有条目对象创建一个表单实例，并根据request.POST中的相关数据对其进行修改。然后，检查表单是否有效。如果有效，就调用save()且不指定任何实参，因为条目已关联到特定的主题。然后，重定向到显示条目所属主题的页面，用户将在其中看到其编辑的条目的新版本。

如果要显示表单让用户编辑条目或者用户提交的表单无效，就创建上下文字典并使用模板edit_entry.html渲染页面。

##### 2.1.3.3 创建模板edit_entry

在learning_logs\templates\learning_logs创建edit_entry.html文件并在其中创建edit_entry模板。
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <p><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></p>

    <p>Edit entry:</p>

    <form action="{% url 'learning_logs:edit_entry' entry.id %}" method='post'>
        {% csrf_token %}
        {{ form.as_p }}
        <button name="submit">Save changes</button>
    </form>

{% endblock content %}
```

实参action将表单发送给函数edit_entry()处理。在标签```{% url %}```中，将条目ID作为一个实参，让视图函数edit_entry()能够修改正确的条目对象。

将提交按钮的标签设置成Save changes，旨在提醒用户：单击该按钮将保存所做的编辑，而不是创建一个新条目。

##### 2.1.3.4 链接到页面edit_entry

在显示特定主题的页面中给每个条目添加到页面edit_entry的链接。

为此，修改learning_logs\templates\learning_logs\topic.html如下：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <p>Topic: {{ topic }}</p>

    <p>Entries:</p>
    <p>
        <a href="{% url 'learning_logs:new_entry' topic.id %}">Add new entry</a>
    </p>

    <ul>
    {% for entry in entries %}
        <li>
            <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
            <p>{{ entry.text|linebreaks }}</p>
            <p>
                <a href="{% url 'learning_logs:edit_entry' entry.id %}">Edit entry</a>
            </p>
        </li>
    {% empty %}
        <li>There are no entries for this topic yet.</li>
    {% endfor %}
    </ul>

{% endblock content %}
```

将编辑链接放在了每个条目的日期和文本后面。在循环中，使用模板标签```{% url %}```根据URL模式edit_entry和当前条目的ID属性(entry.id)来确定URL。链接文本为Edit entry，它出现在页面中每个条目的后面。

至此，“学习笔记”已具备了需要的大部分功能。用户可添加主题和条目，还可根据需要查看任何条目。

## 2.2 创建用户账户

建立用户注册和身份验证系统，让用户能够注册账户，进而登录和注销。

为此，新建一个应用程序，其中包含与处理用户账户相关的所有功能。这个应用程序将尽可能使用Django自带的用户身份验证系统来完成工作。

还将对模型Topic稍做修改，让每个主题都归属于特定用户。

### 2.2.1 应用程序users

命令行中使用startapp命令创建名为users的应用程序：
```shell
python manage.py startapp users
```

接着需要在learning_log/settings.py中，将这个新的应用程序添加到INSTALLED_APPS中，使得Django将应用程序users包含到项目中：
```Python
INSTALLED_APPS = [
    # my applications
    'learning_logs',
    'users',

    # default django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

接下来，修改learning_log/urls.py，使其包含将为应用程序定义的URL，即与任何users打头的URL都匹配：
```Python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('learning_logs.urls')),
]
```

### 2.2.2 实现登录页面

使用Django提供的默认视图login ，因此这个应用程序的URL模式稍有不同。

在learning_log/users文件夹下，新建urls.py：
```Python
'''define URL patterns for users'''

from django.urls import path, include


app_name = 'users'
urlpatterns = [
    # include default auth urls
    path('', include('django.contrib.auth.urls')),
]
```

导入函数path和include，以便包含Django定义的一些默认的身份验证URL。这些默认的URL包含具名的URL模式，'login' 和'logout'。

我们将变量app_name设置成'users'，让Django能够将这些URL与其他应用程序的URL区分开来。即便是Django提供的默认URL，将其包含在应用程序users的文件中后，也可通过命名空间users进行访问。

登录页面的URL模式与URL http://127.0.0.1:8000/users/login/匹配 。这个URL中的单词users让Django在users/urls.py中查找，而单词login让它将请求发送给Django的默认视图login。

##### 2.2.2.1 模板login.html

用户请求登录页面时，Django将使用一个默认的视图函数，但我们依然需要为这个页面提供模板。默认的身份验证视图在文件夹registration中查找模板，因此我们需要创建这个文件夹。为此，在目录users中新建一个名templates的目录，再在这个目录中新建一个名为registration的目录。下面是模板login.html，应将其存储到目录users\templates\registration中：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    {% if form.errors %}
        <p>Your username and password didn't match. Please try again.</p>
    {% endif %}
    
    <form method="post" action="{% url 'users:login' %}">
        {% csrf_token %}
        {{ form.as_p }}
    
        <button name="submit">Log in</button>
        <input type="hidden" name="next" value="{% url 'learning_logs:index' %}" />
    </form>
    
{% endblock content %}
```

这个模板继承了base.html，旨在确保登录页面的外观与网站的其他页面相同。

*注意：一个应用程序中的模板可继承另一个应用程序中的模板。*

如果设置表单的errors属性，就显示一条错误消息，指出输入的用户名密码对与数据库中存储的任何用户名密码对都不匹配。

我们要让登录视图对表单进行处理，因此将实参action设置为登录页面的URL。登录视图将一个表单发送给模板。在模板中，我们显示这个表单并添加一个提交按钮。

包含了一个隐藏的表单元素'next'，其中的实参value告诉Django在用户成功登录后将其重定向到什么地方。在本项目中，用户将返回主页。

##### 2.2.2.2 链接到登录界面

下面在learning_logs\templates\learning_logs\base.html中添加到登录页面的链接，让所有页面都包含它。

用户已登录时，我们不想显示这个链接，因此将它嵌套在一个```{% if %}```标签中：
```html
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a> - 
    <a href="{% url 'learning_logs:topics' %}">Topics</a> - 
    {% if user.is_authenticated %}
        Hello, {{ user.username }}.
    {% else %}
        <a href="{% url 'users:login' %}">Log in</a>
    {% end if %}
</p>

{% block content %}{% endblock content %}
```

在Django身份验证系统中，每个模板都可使用变量user。这个变量有一个is_authenticated属性：如果用户已登录，该属性将为True，否则为False。这让你能够向已通过身份验证的用户显示一条消息，而向未通过身份验证的用户显示另一条消息。

这里向已登录的用户显示问候语。对于已通过身份验证的用户，还设置了属性username。这里使用该属性来个性化问候语，让用户知道自己已登录。

对于尚未通过身份验证的用户，显示到登录页面的链接。

##### 2.2.2.3 使用登录页面

前面建立了一个用户账户，下面来登录一下，看看登录页面是否管用。

访问 http://127.0.0.1:8000/admin ，登出管理员超级账户

登出后，访问 http://127.0.0.1:8000/users/login ，即可看到登录页面

### 2.2.3 登出

现在需要提供一个让用户登出的途径。为此，我们将在learning_logs\templates\learning_logs\base.html中添加一个登出链接。用户单击这个链接时，将进入一个确认其已登出的页面。

##### 2.2.3.1 在base.html中添加登出链接

下面在learning_logs\templates\learning_logs\base.html中添加注销链接，让每个页面都包含它。将注销链接放在```{% if user.is_authenticated %}```部分中，这样只有已登录的用户才能看到它，默认的具名登出URL模式为'logout'：
```html
    {% if user.is_authenticated %}
        Hello, {{ user.username }}.
        <a href="{% url 'users:logout' %}">Log out</a>
    {% else %}
```

##### 2.2.3.2 登出确认页面

成功登出后，用户希望获悉这一点。因此默认的注销视图使用模板logged_out.html渲染注销确认页面。

在users\templates\registration目录中创建logged_out.html：
```html
{% extends "learning_logs/base.html" %}

{% block content %}
    <p>You have been logged out. Thank you for visiting!</p>
{% endblock content %}
```

### 2.2.4 注册页面

下面创建一个页面供新用户注册。我们将使用Django提供的表单UserCreationForm，但编写自己的视图函数和模板。

##### 2.2.4.1 注册页面的URL模式

在users\urls.py中添加注册页面的URL模式：
```Python
from . import views

app_name = 'users'
urlpatterns = [
    # include default auth urls
    path('', include('django.contrib.auth.urls')),
    # registration page
    path('register/', views.register, name='register'),
]
```

注册页面的URL模式与URL http://127.0.0.1:8000/users/register/ 匹配，并将请求发送给视图函数register() 。

##### 2.2.4.2 视图函数register()

在注册页面首次被请求时，视图函数register()需要显示一个空的注册表单，并在用户提交填写好的注册表单时对其进行处理。如果注册成功，这个函数还需让用户自动登录。

在users/views.py中输入代码如下：
```Python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """register a new user"""
    if request.method != 'POST':
        # display blank registration form
        form = UserCreationForm()
    else:
        # process completed form
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # log the user in and then redirect to home page
            login(request, new_user)
            return redirect('learning_logs:index')

    # display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)
```

首先导入函数render()和redirect()，然后导入函数login()，以便在用户正确填写了注册信息时让其自动登录。

还导入默认表单UserCreationForm。在函数register()中，检查要响应的是否是POST请求。如果不是，就创建一个UserCreationForm 实例，且不给它提供任何初始数据。

如果响应的是POST请求，就根据提交的数据创建一个UserCreationForm实例，并检查这些数据是否有效。就本例而言，有效是指用户名未包含非法字符，输入的两个密码相同，以及用户没有试图做恶意的事情。

如果提交的数据有效，就调用表单的方法save()，将用户名和密码的散列值保存到数据库中。方法save()返回新创建的用户对象，我们将它赋给了new_user。保存用户的信息后，调用函数login()并传入对象request和new_user，为用户创建有效的会话，从而让其自动登录。最后，将用户重定向到主页，而主页的页眉中显示了一条个性化的问候语，让用户知道注册成
功了。

在这个函数的末尾，我们渲染了注册页面：它要么显示一个空表单，要么显示提交的无效表单。

##### 2.2.4.3 注册模板

下面创建注册页面的模板users\templates\registration\register.html：
```html
{% extends "learning_logs/base.html" %}

{% block content %}

    <form method="post" action="{% url 'users:register' %}">
        {% csrf_token %}
        {{ form.as_p }}

        <button name="submit">Register</button>
        <input type="hidden" name="next" value="{% url 'learning_logs:index' %}" />
    </form>

{% endblock content %}
```

方法as_p让Django在表单中正确地显示所有的字段，包括错误消息——如果用户没有正确地填写表单。

##### 2.2.4.4 链接到注册页面

在用户没有登录时，需要显示到注册页面的链接。

在learning_logs\templates\learning_logs\base.html中修改代码如下：
```html
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a> -
    <a href="{% url 'learning_logs:topics' %}">Topics</a> - 
    {% if user.is_authenticated %}
        Hello, {{ user.username }}.
        <a href="{% url 'users:logout' %}">Log out</a>
    {% else %}
        <a href="{% url 'users:register' %}">Register</a> -
        <a href="{% url 'users:login' %}">Log in</a>
    {% endif %}
</p>
  
{% block content %}{% endblock content %}
```

现在，已登录的用户看到的是个性化的问候语和注销链接，而未登录的用户看到的是注册链接和登录链接。