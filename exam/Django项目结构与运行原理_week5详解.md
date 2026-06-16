# Django 项目结构与运行原理 —— 以 week5 课堂代码为例

> 基于 `code/week5/COMP8347proj/` 的真实文件逐一讲解。读完应能回答两类问题：
> ① 每个文件/文件夹是干什么的、谁在什么时候用它；② 一次 HTTP 请求如何穿过整个项目。

---

## 0. 先建立大局观：项目（Project）vs 应用（App）

- **项目 Project** = 整个网站的"容器"：全局配置、根路由、数据库、部署入口。由 `django-admin startproject config .` 生成。
- **App** = 一个可插拔的功能模块（本项目有 `hello` 和 `classroom`）。由 `python manage.py startapp xxx` 生成。
- 关系：**一个项目装多个 app**；app 必须写进 `settings.py` 的 `INSTALLED_APPS` 才"存在"。
- 设计哲学：app 理论上可以拷到别的项目继续用（可复用），项目只是把它们组装起来。

`hello` 和 `classroom` 正好是两个极端的对照样本：
- `hello`：最小 app——只有 views + 一个模板，**没有模型 → 没有迁移文件 → 数据库里没有它的表**。
- `classroom`：完整 MVT app——models / forms / views / urls / admin / migrations / templates / static 全套。

---

## 1. 完整目录树（注释版）

```
COMP8347proj/                      ← 项目根目录（BASE_DIR 指向这里）
│
├── manage.py                      ← 一切命令的入口（runserver/migrate/shell/…）
├── db.sqlite3                     ← SQLite 数据库文件（migrate 后才出现）
│
├── config/                        ← 项目配置包（startproject 生成）
│   ├── __init__.py                ← 空文件：声明"这是个 Python 包"
│   ├── settings.py                ← 全局配置中枢（最重要的文件）
│   ├── urls.py                    ← 根路由表（ROOT_URLCONF 指向它）
│   ├── wsgi.py                    ← 生产部署入口（同步，gunicorn/uWSGI 用）
│   └── asgi.py                    ← 生产部署入口（异步，websocket 等用）
│
├── templates/                     ← 项目级模板目录（settings TEMPLATES['DIRS'] 指定）
│   └── registration/              ← django.contrib.auth 约定的模板位置
│       ├── login.html             ← /accounts/login/ 用
│       ├── logged_out.html        ← 登出后页面
│       ├── password_change_form.html
│       └── password_change_done.html
│
├── hello/                         ← App①：最小示例
│   ├── views.py                   ← hello_world()、greet()
│   ├── templates/hello/greet.html
│   ├── models.py / admin.py / tests.py  ← 全是空壳
│   ├── apps.py                    ← HelloConfig
│   └── migrations/__init__.py     ← 没有模型 → 没有迁移
│
└── classroom/                     ← App②：核心业务
    ├── __init__.py
    ├── apps.py                    ← ClassroomConfig（app 元信息）
    ├── models.py                  ← M：Student 模型 → classroom_student 表
    ├── forms.py                   ← StudentForm（ModelForm，输入验证）
    ├── views.py                   ← V：所有视图函数 + 装饰器
    ├── urls.py                    ← app 级路由（被 config/urls.py include）
    ├── admin.py                   ← 把 Student 注册进后台
    ├── tests.py                   ← 测试占位（课程未用）
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py        ← "建 Student 表"的迁移脚本
    ├── templates/classroom/       ← T：模板（注意双层目录！）
    │   ├── base.html              ← 骨架：{% block title/content %}
    │   ├── student_list.html      ← extends base.html
    │   ├── add_student.html       ← 表单页（{% csrf_token %} + form.as_p）
    │   ├── dashboard.html / profile.html / visit_counter.html
    └── static/classroom/css/site.css  ← 静态文件（同样双层目录）
```

---

## 2. 项目骨架文件逐个讲

### 2.1 manage.py —— 所有命令的总开关

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
execute_from_command_line(sys.argv)
```

只做两件事：**告诉 Django 配置文件在哪**（`config.settings`），然后把命令行参数交给 Django 的命令分发器。所以：

| 你敲的命令 | 实际发生 |
|---|---|
| `python manage.py runserver` | 起开发服务器（默认 127.0.0.1:8000，自动重载） |
| `python manage.py makemigrations` | 对比 models.py 与迁移历史，生成新迁移文件 |
| `python manage.py migrate` | 把未应用的迁移执行成 SQL，改数据库 |
| `python manage.py shell` | 进入加载了 Django 环境的 Python 交互器 |
| `python manage.py createsuperuser` | 往 auth_user 表插一个超级管理员 |
| `python manage.py startapp xxx` | 生成 app 脚手架 |
| `python manage.py dbshell` | 直接进数据库命令行 |

`django-admin` 与 `manage.py` 的区别：前者是全局命令（建项目时用，那时还没有 settings），后者绑定了本项目的 settings——建完项目后一律用 manage.py。

### 2.2 config/settings.py —— 全局配置中枢（重点）

按真实文件里的顺序：

- **`BASE_DIR = Path(__file__).resolve().parent.parent`**
  settings.py 的上上级目录 = 项目根。后面所有路径都基于它拼（如 `BASE_DIR / 'db.sqlite3'`、`BASE_DIR / "templates"`）。

- **`SECRET_KEY`**
  加密签名的种子：session 签名、CSRF token、密码重置链接都靠它。泄露 = 任何人能伪造你的 session。生产环境绝不能提交进代码库。

- **`DEBUG = True`**
  开发模式：报错显示完整黄页堆栈。上线必须 False（否则等于把源码结构展示给攻击者）。

- **`INSTALLED_APPS`** —— "本项目装了哪些 app"
  ```
  django.contrib.admin         ← 后台 /admin/
  django.contrib.auth          ← 用户/权限系统（auth_user 等表）
  django.contrib.contenttypes  ← 给权限系统记录"模型类型"（django_content_type 表）
  django.contrib.sessions      ← session 框架（django_session 表）
  django.contrib.messages      ← 一次性消息闪现
  django.contrib.staticfiles   ← 开发时托管静态文件
  hello, classroom             ← 我们自己的 app
  ```
  没列进来的 app：模型不会被迁移、模板找不到、admin 注册无效——官方 MCQ 样题考的就是这个。

- **`MIDDLEWARE`** —— 请求/响应的"安检通道"（顺序敏感！）
  ```
  SecurityMiddleware            ← 安全响应头
  SessionMiddleware             ← 读 sessionid cookie → 挂上 request.session
  CommonMiddleware              ← URL 规范化等杂务
  CsrfViewMiddleware            ← POST 必须带有效 CSRF token，否则 403
  AuthenticationMiddleware      ← 用 session 里的 user id → 挂上 request.user
  MessageMiddleware / XFrameOptionsMiddleware
  ```
  为什么 Session 排在 Csrf 和 Auth 前面？因为后两者**依赖 session**（token 校验、取登录用户）。每个请求"进来时从上往下穿一遍，出去时从下往上再穿一遍"（洋葱模型）。

- **`ROOT_URLCONF = 'config.urls'`** —— 告诉 Django 根路由表是哪个模块。

- **`TEMPLATES`**
  ```python
  'DIRS': [BASE_DIR / "templates"],   # 项目级模板目录（registration/ 在这里被找到）
  'APP_DIRS': True,                    # 同时自动扫描每个 app 内的 templates/
  'context_processors': [... request, auth, ...]
  ```
  `context_processors` 里的 `auth` 解释了一个"魔法"：为什么模板里不传也能直接用 `{{ user }}` 和 `{{ perms }}`（profile.html、dashboard.html 都用了）——它们是被 auth 上下文处理器自动注入每个模板的。

- **`DATABASES`**：默认 SQLite，`NAME: BASE_DIR / 'db.sqlite3'`。换 PostgreSQL/MySQL 只需改 ENGINE 和连接参数，**业务代码一行不用动**——这就是 ORM 的可移植性。

- **`AUTH_PASSWORD_VALIDATORS`**：4 个密码校验器（不能太像用户名、最短长度、不能是常见密码、不能纯数字）。`createsuperuser` 时嫌你密码弱的就是它们。

- **`STATIC_URL = 'static/'`**：`{% static 'classroom/css/site.css' %}` 渲染成 `/static/classroom/css/site.css`，开发时由 staticfiles app 自动托管。

- **`DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`**：不写主键时自动加的 `id` 用 64 位自增整数——对照 `0001_initial.py` 里的 `id = BigAutoField(...)`，正好对上。

### 2.3 config/urls.py —— 根路由表

真实文件做了三类事：

```python
path('admin/', admin.site.urls)                      # ① 挂后台
path('hello/', hello_world, name='hello')            # ② 直接绑定单个视图
path("accounts/", include("django.contrib.auth.urls"))  # ③ 整组"借"别人的路由
path("", include("classroom.urls"))                  # ③ 把 classroom 的路由挂到根
```

- `include()` 的机制：**砍掉已匹配的前缀，剩余部分交给子路由表继续匹配**。
- `include("django.contrib.auth.urls")` 一行白送 `/accounts/login/`、`/accounts/logout/`、`/accounts/password_change/` 等一整套 URL——Week 5 登录功能就是这么来的。
- `name=` 参数支撑反向解析：模板里 `{% url 'student-list' %}`、视图里 `redirect("student-list")`，URL 改了代码不用改。
- 匹配规则：**自上而下，第一个命中即停**。本项目 `students/add/` 在 config/urls.py 直接注册过、又通过 include 进来一次——生效的是先注册的那条。

### 2.4 wsgi.py / asgi.py —— 部署入口

都只暴露一个 `application` 对象。生产环境时 web 服务器（gunicorn、uWSGI、daphne）加载它来把 HTTP 请求转成 Python 调用。**WSGI = 同步标准，ASGI = 异步标准**（支持 WebSocket）。开发时 `runserver` 内置了这一层，所以你感知不到。课程层面记住一句话："WSGI-compatible web server 的 entry-point"。

### 2.5 db.sqlite3 —— 数据库本体

第一次 `migrate` 后出现。用 `sqlite3 db.sqlite3 ".tables"` 看真实表清单：

```
auth_group                  auth_user_user_permissions
auth_group_permissions      classroom_student        ← 我们唯一的业务表
auth_permission             django_admin_log
auth_user                   django_content_type
auth_user_groups            django_migrations
                            django_session
```

规律与来源：
- **`classroom_student`** = `app名_模型名小写`——models.py 里那个类的物理形态。
- **`auth_*` 六张表** = `django.contrib.auth`：用户、组、权限，以及两张多对多中间表（user↔group、user↔permission，对应讲义里 `user.groups` / `user.user_permissions` 两个 M2M 字段）。
- **`django_session`** = session 数据真正存放处（服务器端！浏览器只有 sessionid）。
- **`django_migrations`** = 迁移流水账：记录哪些迁移已应用，migrate 据此决定还要跑哪些。
- **`auth_permission`** = 每个模型自动生成的 add/change/delete/view 权限行。
- `hello` app 没有模型 → 表里**没有任何 hello_* 表**。

---

## 3. classroom app 内部逐文件讲

### 3.1 models.py —— M（数据层）

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    join_date = models.DateField(auto_now_add=True)
    def __str__(self): return self.name
```

- **类 ↔ 表，字段 ↔ 列，实例 ↔ 行**。继承 `models.Model` 后白得一切：`objects` 管理器、`save()`、`delete()`、主键 id。
- `unique=True` → 数据库层唯一约束（重复 email 在 `form.is_valid()` 阶段就会报错）。
- `auto_now_add=True` → 插入时自动填当前日期，之后不可改。
- `__str__` → admin 列表和 shell 里显示的名字。

### 3.2 migrations/ —— 数据库的版本控制

`0001_initial.py` 内容就是一条 `CreateModel(name='Student', fields=[id, name, email, join_date])`。

工作流：**改 models.py → makemigrations（生成新编号脚本）→ migrate（执行并记账到 django_migrations）**。week3 项目里加 phone_number 字段生成的 `0002_student_phone_number.py` 就是第二次迭代的活例子。迁移文件要进 git——它是"数据库结构怎么一步步变成今天这样"的历史。

### 3.3 apps.py —— app 的"身份证"

```python
class ClassroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classroom'
```

启动时 Django 据此把 app 注册进 app registry。平时几乎不碰（要写信号、启动钩子时才用）。

### 3.4 forms.py —— 输入验证层

```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email"]
```

ModelForm 从模型**自动推导**表单字段（EmailField → EmailInput + 格式校验 + unique 查重）。它是"不信任用户输入"原则的体现：所有外部输入先过 `is_valid()`，干净数据从 `cleaned_data` 拿，`form.save()` 直接落库。

### 3.5 views.py —— V（逻辑层，项目的发动机）

每个函数 = 一个端点，统一签名：**收 HttpRequest，还 HttpResponse**。本文件五个视图正好展示五种典型形态：

| 视图 | 形态 | 关键 API |
|---|---|---|
| `student_list` | 查库 → 渲染列表 | `Student.objects.all()`、`qs.count()`、`qs.exists()`、`render()` |
| `add_student` | 表单双分支 + PRG | `request.method`、`StudentForm(request.POST)`、`form.save()`、`redirect()` |
| `profile` | 登录保护 | `@login_required`、`request.user` |
| `visit_counter` | session 状态 | `request.session.get("visits", 0)` |
| `set_fave_color` | 手写 cookie | `resp.set_cookie("fav_color", "blue", max_age=3600)` |

`add_student` 头上叠了两个装饰器，执行顺序自上而下：

```python
@login_required                    # 没登录？302 → /accounts/login/?next=...
@permission_required('classroom.add_student', raise_exception=True)  # 没权限？403
def add_student(request): ...
```

⚠️ 该文件还有个课堂遗留问题：`dashboard` 定义了两次，Python 静默用**后一个**（名字重绑定）；第一个里 `extra({'day': "date(join_date"})` 还少个右括号。这本身就是一道现成的"找 bug"考题。

### 3.6 urls.py（app 级）

```python
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("students/", views.student_list, name="student-list"),
    path("students/add/", views.add_student, name="add-student"),
]
```

被 `config/urls.py` 的 `include("classroom.urls")` 挂载。**app 管自己的路由、项目只管挂载**——这就是 app 可插拔的关键。

### 3.7 admin.py —— 两行换一个后台

```python
admin.site.register(Student)
```

配合 `createsuperuser`，立刻获得 `/admin/` 里 Student 的增删改查界面。生效三前提：app 在 INSTALLED_APPS、模型已 migrate、用户 `is_staff=True`。

### 3.8 templates/ —— T（呈现层）与"双层目录"之谜

为什么是 `classroom/templates/classroom/base.html` 而不是 `classroom/templates/base.html`？

因为 `APP_DIRS=True` 时，Django 把**所有 app 的 templates/ 目录合并成一个大查找池**。如果两个 app 都有 `base.html`（不带前缀），先注册的 app 永远赢，另一个 app 的模板被悄悄覆盖。多套一层与 app 同名的目录 = **命名空间**，于是引用时写 `render(request, "classroom/student_list.html")`。static 同理：`classroom/static/classroom/css/site.css`。

模板查找顺序：先查 `DIRS`（项目级 `templates/`），再按 INSTALLED_APPS 顺序查各 app（APP_DIRS）。所以 `registration/login.html` 放项目级目录就能覆盖 auth 自带的登录模板。

继承链（真实文件）：

```
base.html        {% load static %} + <link {% static 'classroom/css/site.css' %}>
   ▲                定义 {% block title %} 和 {% block content %}
   │ extends
student_list.html / add_student.html / dashboard.html / ...
                    只写自己那块内容，骨架免费继承
```

add_student.html 里三件必考套件：`{% extends %}`（必须是文件第一个标签）、`{% csrf_token %}`（POST 表单保命符）、`{{ form.as_p }}`（表单自动渲染）。

---

## 4. 运行原理：两条时间线

### 4.1 启动时（python manage.py runserver）

1. manage.py 设置 `DJANGO_SETTINGS_MODULE` → 加载 settings.py
2. 按 INSTALLED_APPS 填充 **app registry**（导入每个 app 的 apps.py、models.py）
3. admin 自动发现：导入每个 app 的 admin.py（`register` 在此刻执行）
4. 加载 ROOT_URLCONF，编译 urlpatterns
5. 监听 127.0.0.1:8000，并监视文件变动自动重载

### 4.2 一次请求的完整旅程（以"已登录的 Teacher 提交新学生"为例）

```
浏览器 POST /students/add/   表单数据 + Cookie(sessionid, csrftoken)
  │
  ▼ ① WSGI 层把原始 HTTP 解析成 HttpRequest 对象
  ▼ ② 中间件入栈（自上而下）
       SessionMiddleware:  读 sessionid → 查 django_session 表 → request.session 就绪
       CsrfViewMiddleware: POST？校验表单里的 csrf token，失败 → 403 到此为止
       AuthMiddleware:     session 里取 user id → 查 auth_user → request.user 就绪
  ▼ ③ URL 解析：ROOT_URLCONF 自上而下匹配 "students/add/" → add_student
  ▼ ④ 装饰器关卡：
       @login_required      → request.user 已认证？否则 302 带 ?next=
       @permission_required → has_perm('classroom.add_student')？否则 403
  ▼ ⑤ 视图主体：
       form = StudentForm(request.POST)      ← 绑定（bound）
       form.is_valid()                        ← 触发全部字段校验 + email 查重
       form.save()                            ← ORM 生成 INSERT INTO classroom_student...
       request.session['added_count'] += 1    ← 标记 session 已修改
       return redirect("student-list")        ← 反向解析 name → 302 Location:/students/
  ▼ ⑥ 中间件出栈（自下而上）：SessionMiddleware 把修改写回 django_session 表
  ▼ ⑦ 302 响应到浏览器
  │
浏览器自动发起 GET /students/（PRG 模式，防刷新重复提交）
  → student_list → Student.objects.all() → SELECT * FROM classroom_student
  → render("classroom/student_list.html") → extends base.html → 200 HTML
  → 浏览器解析 HTML，再发一个 GET /static/classroom/css/site.css → 页面完整呈现
```

注意整个旅程**精确对应 MVT**：urls 选路 → View 决策 → Model 取数 → Template 化妆 → 响应回家。而 session/csrf/auth 这些"全局关切"都在中间件层统一处理，视图保持干净。

### 4.3 数据从代码到表的旅程

```
models.py 改动
  → makemigrations   对比"模型现状 vs 迁移历史"，生成 000N_xxx.py
  → migrate          翻译成 SQL 执行；django_migrations 记一笔
  → ORM 查询时       Student.objects.filter(...) 翻译成 SELECT ... WHERE
```

---

## 5. 哪些名字是"死规定"，哪些只是约定？

| 名字 | 性质 |
|---|---|
| `manage.py`、`settings.py` 里的配置项名 | 死的 |
| `migrations/` 目录名、`templates/`、`static/`（APP_DIRS 机制） | 死的 |
| `models.py`、`admin.py`、`apps.py` | 约定 + 框架按名导入（admin 自动发现找的就是 admin.py）|
| `views.py`、`forms.py` | 纯约定——只要 import 路径对，叫啥都行（但别) |
| `urls.py`（app 级） | 名字由 `include("classroom.urls")` 字符串决定 |
| `config/` 这个包名 | 建项目时定的，可以叫 mysite/ 等 |
| `templates/registration/login.html` | auth 系统的**约定路径**，放对位置即自动生效 |
| `base.html`、`{% block content %}` 的名字 | 自己定义，保持一致即可 |

---

## 6. 快速自检（合上文档能答出来吗？）

1. `manage.py runserver` 之后到第一个页面渲染，settings.py 的哪些配置项被用到了？（至少说 5 个）
2. 为什么模板要放 `classroom/templates/classroom/` 双层目录？
3. `request.session` 和 `request.user` 分别是哪个中间件挂上去的？顺序能换吗？
4. `db.sqlite3` 里 `django_session`、`auth_permission`、`django_migrations` 各存什么？
5. `include("django.contrib.auth.urls")` 白送了哪些 URL？登录模板必须放哪？
6. 从 `form.save()` 到磁盘上的数据，中间经历了什么？
7. hello app 为什么没有迁移文件、数据库里也没有 hello 表？
8. 一个 POST 请求在哪三个关卡可能被拦下，分别返回什么？（CSRF→403、login_required→302、permission_required→403）
