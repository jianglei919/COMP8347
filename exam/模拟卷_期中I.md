# COMP 8347 期中 I 全真模拟卷

> 依据官方 _Mid-Term Exam I - Information_ 与 _GA and Student Instructions_ 的格式与样题风格编写。
> **总分 100 = Part I 45 分（20 MCQ，不可回退）+ Part II 55 分（15 简答，可回退）**，时长 2 小时。
> 分值为估算：MCQ-I ≈2 分/题、MCQ-II ≈2.5 分/题、SA-I ≈3 分/题、SA-II ≈5 分/题。
>
> ⚠️ 官方样题全部基于课堂代码（`classroom` app、`Student(name, email, join_date)` 模型、admin 注册、登录/权限演示）。本卷同样以课堂代码为锚点。
>
> **答题策略**：Part I 不可回退——想好再提交，别恋战（建议 ≤45 分钟）；Part II 可回退且占 55 分——先把 10 道 SA-I 快速拿下（一句话即可，不用解释），再攻 5 道 SA-II 代码题，留 15 分钟回头检查。

---

## PART I-A：MCQ Level I（概念题，10 题）

**Q1.** HTTP is described as a _stateless_ protocol. What does this mean?
A) The server encrypts every request
B) The server maintains no information about past client requests
C) The client cannot send data to the server
D) The connection never closes

**Q2.** Which HTTP status code indicates that the requested page does not exist on the server?
A) 200 B) 301 C) 404 D) 500

**Q3.** What is the primary job of DNS?
A) Encrypt traffic between client and server
B) Translate human-friendly domain names into IP addresses
C) Deliver HTML files to the browser
D) Assign session IDs to users

**Q4.** In a three-tier architecture, which Django component implements the **presentation tier**?
A) Model B) View C) Template D) ORM

**Q5.** Django's "View" corresponds to which part of the classic MVC pattern?
A) Model B) View C) Controller D) Database

**Q6.** Which command **applies** pending migrations to the database?
A) python manage.py makemigrations
B) python manage.py migrate
C) python manage.py runserver
D) python manage.py sqlmigrate

**Q7.** In a Django model field, which option means "this field may be left empty when validating a **form**"?
A) null=True B) blank=True C) default=True D) unique=True

**Q8.** A form that **changes data** in the database (e.g., adds a student) should be submitted with which HTTP method?
A) GET B) POST C) HEAD D) TRACE

**Q9.** Where does Django store the actual session **data** by default?
A) In the browser's localStorage
B) In the URL query string
C) On the server (database) — the browser only keeps a session-ID cookie
D) Inside the HTML page

**Q10.** Which algorithm does Django use **by default** to hash passwords?
A) MD5 B) Base64 C) PBKDF2 D) ROT13

---

## PART I-B：MCQ Level II（代码场景题，10 题）

**Q11.** What does the following query return?

```python
Student.objects.filter(name__icontains="a").order_by("-join_date")[:2]
```

A) All students named exactly "a"
B) The 2 most recently joined students whose name contains "a" (case-insensitive)
C) The 2 oldest students whose name starts with "a"
D) A syntax error — querysets cannot be sliced

**Q12.** Two students named "Alice" exist in the database. What happens when this runs?

```python
s = Student.objects.get(name="Alice")
```

A) Returns the first Alice
B) Returns a QuerySet with both
C) Raises Student.MultipleObjectsReturned
D) Returns None

**Q13.** Given this URL pattern:

```python
path("students/<int:student_id>/", views.detail, name="student-detail")
```

A user visits `/students/abc/`. What happens?
A) The view runs with student_id="abc"
B) The pattern does not match — Django keeps searching and returns 404 if nothing else matches
C) Django converts "abc" to 0
D) A 500 server error is always raised

**Q14.** A user typed `<script>alert("Hacked!")</script>` as their name, and the alert actually **executes** when the page loads. Which template code caused this vulnerability?
A) `{{ student.name }}`
B) `{{ student.name|escape }}`
C) `{{ student.name|safe }}`
D) `{{ student.name|lower }}`

**Q15.** What does this print?

```python
form = ContactForm()        # no data passed
print(form.is_valid())
```

A) True
B) False — an unbound form always fails is_valid()
C) Raises ValidationError
D) Depends on the fields

**Q16.** A user submits your POST form and gets **"403 Forbidden – CSRF verification failed"**. The most likely cause is:
A) The user is not logged in
B) The form template is missing `{% csrf_token %}`
C) The model was not registered in admin.py
D) The database is locked

**Q17.** Given:

```python
class Company(models.Model):
    co_name = models.CharField(max_length=50)

class Car(models.Model):
    type = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
```

How do you get **all cars made by Ford**?
A) `Car.objects.get(co_name="Ford")`
B) `Company.objects.filter(car="Ford")`
C) `ford = Company.objects.get(co_name="Ford"); ford.car_set.all()`
D) `Company.cars.all("Ford")`

**Q18.** `add_student` is decorated with `@login_required`. An anonymous (logged-out) user visits `/students/add/`. What happens?
A) 403 Forbidden
B) 500 Internal Server Error
C) Redirected to `/accounts/login/?next=/students/add/`
D) The page renders normally

**Q19.** Lecture's visit counter:

```python
def visit_counter(request):
    visits = request.session.get("visits", 0) + 1
    request.session["visits"] = visits
    return render(request, "classroom/visit_counter.html", {"visits": visits})
```

A user opens the page for the first time, then refreshes it 3 times. What does the page show on the last refresh, and how does Django recognize the same user?
A) 3; via the user's IP address
B) 4; via the `sessionid` cookie sent by the browser
C) 4; via the URL query string
D) 1; sessions reset on every request

**Q20.** You created a new model `Student`, added the app to INSTALLED_APPS, then opened `/students/` and got:
`OperationalError: no such table: classroom_student`
What did you forget?
A) Registering the model in admin.py
B) Running `makemigrations` and `migrate`
C) Adding `{% csrf_token %}`
D) Creating a superuser

---

## PART II-A：简答 Level I（一句话作答，10 题，无需解释）

**Q21.** In which file do you define your Django **models**? ****\_\_****

**Q22.** What command starts the Django development server? ****\_\_****

**Q23.** What is the name of the **default Manager** available on every Django model? ****\_\_****

**Q24.** Which template tag must appear inside every POST form to protect against cross-site request forgery? ****\_\_****

**Q25.** What is the default TCP port for **HTTPS**? ****\_\_****

**Q26.** What is the name of the cookie Django uses to identify a user's session? ****\_\_****

**Q27.** Which decorator restricts a view so that only **logged-in** users can access it? ****\_\_****

**Q28.** What command creates an **admin (superuser)** account? ****\_\_****

**Q29.** In Django's MVT pattern, which component receives the request and contains the logic that decides what data to fetch? ****\_\_****

**Q30.** A logged-in user without the required permission accesses a view protected by `@permission_required('classroom.add_student', raise_exception=True)`. Which HTTP status code do they receive? ****\_\_****

---

## PART II-B：简答 Level II（写代码，5 题）

> 模型均为课堂的 `Student`（fields: `name`, `email`, `join_date`）。

**Q31.** Write a Django ORM query to retrieve all students who joined **after January 1, 2026**, ordered with the **most recent first**.

**Q32.** Write a Django ORM query to retrieve the **first 5** students whose name contains "an" (**case-insensitive**).

**Q33.** Write a complete `ModelForm` class named `StudentForm` for the `Student` model that includes only the `name` and `email` fields.

**Q34.** Complete this view so it counts how many times the current user has visited the page, storing the count in the **session**:

```python
def visit_counter(request):
    # your code here (2 lines)
    return render(request, "classroom/visit_counter.html", {"visits": visits})
```

**Q35.** In a view, you receive `username` and `password` from `request.POST`. Write the code that **verifies the credentials** and, if valid and the account is active, **logs the user into the current session** (use Django's auth functions).

---

---

# 答案与解析

## Part I-A

| 题  | 答案  | 解析                                                                                         |
| --- | ----- | -------------------------------------------------------------------------------------------- |
| Q1  | **B** | Stateless = 服务器不保留过去请求的信息，所以才需要 Cookie/Session 记住用户。                 |
| Q2  | **C** | 404 Not Found。200=成功，301=永久重定向，500=服务器内部错误。                                |
| Q3  | **B** | DNS = 互联网的"电话簿"，域名→IP。                                                            |
| Q4  | **C** | Presentation=Template，Logic=View，Data=Model/ORM。                                          |
| Q5  | **C** | MVC 的 Controller = Django 的 View；MVC 的 View = Django 的 Template。⭐必背                 |
| Q6  | **B** | `makemigrations` 只**生成**迁移文件；`migrate` 才**应用**到数据库；`sqlmigrate` 只显示 SQL。 |
| Q7  | **B** | `blank` 是表单/验证层面；`null` 是数据库层面（存 NULL）。                                    |
| Q8  | **B** | 改变系统状态的请求必须用 POST；GET 参数进 URL，只用于不改状态的请求（如搜索）。              |
| Q9  | **C** | 数据在服务器（默认数据库的 `django_session` 表），浏览器只存 `sessionid`。                   |
| Q10 | **C** | PBKDF2 + 唯一 salt + 数千轮哈希；Django 绝不存明文。                                         |

## Part I-B

| 题  | 答案  | 解析                                                                                                        |
| --- | ----- | ----------------------------------------------------------------------------------------------------------- |
| Q11 | **B** | `icontains`=忽略大小写包含；`-join_date`=降序（最新在前）；`[:2]`=SQL LIMIT 2。这是官方样题的变体，必会。   |
| Q12 | **C** | `get()` 必须恰好匹配一条：0 条→`DoesNotExist`，多条→`MultipleObjectsReturned`。                             |
| Q13 | **B** | `<int:>` 转换器只匹配数字；"abc" 不匹配该 route，Django 继续尝试后续 pattern，全部失败则 404。              |
| Q14 | **C** | `safe` 关闭自动转义→XSS。Django 默认转义 `<`、`>`、`"`，A 是安全的。                                        |
| Q15 | **B** | Unbound form（没绑定数据）的 `is_valid()` 永远返回 False，`errors` 为空字典。                               |
| Q16 | **B** | CSRF 中间件要求每个 POST 表单带 token；缺失/不匹配→403 CSRF verification failed。                           |
| Q17 | **C** | FK 反向查询默认名 = `小写模型名_set`，即 `company.car_set.all()`。讲义原题。                                |
| Q18 | **C** | `login_required`：未登录→重定向到 `settings.LOGIN_URL`，并带 `?next=原路径`，登录后跳回。不是 403！         |
| Q19 | **B** | 第 1 次=1，再刷 3 次=4。浏览器每次请求自动带 `sessionid` cookie，Django 据此找到服务器上的 session 数据。   |
| Q20 | **B** | "no such table" = 模型已定义但表没建 → 忘了跑迁移。和官方样题（忘加 INSTALLED_APPS→admin 不显示）是姊妹题。 |

## Part II-A

| 题  | 答案                               |
| --- | ---------------------------------- |
| Q21 | `models.py`（app 目录下）          |
| Q22 | `python manage.py runserver`       |
| Q23 | `objects`                          |
| Q24 | `{% csrf_token %}`                 |
| Q25 | `443`（HTTP 为 80）                |
| Q26 | `sessionid`                        |
| Q27 | `@login_required`                  |
| Q28 | `python manage.py createsuperuser` |
| Q29 | `View`（视图）                     |
| Q30 | `403`（Forbidden）                 |

## Part II-B

**Q31.**

```python
Student.objects.filter(join_date__gt="2026-01-01").order_by("-join_date")
```

（写 `__gte` 视题意"之后"含当天与否；考试中 `gt/gte` 一般都给分，注意 `-` 降序。）

**Q32.**

```python
Student.objects.filter(name__icontains="an")[:5]
```

（`icontains`=忽略大小写；切片即 SQL LIMIT，不会先取全表。）

**Q33.**

```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email"]
```

（课堂原代码。`Meta` 内 `model` + `fields` 两件套必写。）

**Q34.**

```python
def visit_counter(request):
    visits = request.session.get("visits", 0) + 1
    request.session["visits"] = visits
    return render(request, "classroom/visit_counter.html", {"visits": visits})
```

（`get("visits", 0)` 带默认值避免 KeyError；赋值回 session 才会保存。）

**Q35.**

```python
from django.contrib.auth import authenticate, login

user = authenticate(username=username, password=password)
if user is not None:
    if user.is_active:
        login(request, user)
        # redirect to success page
    else:
        ...  # account disabled
else:
    ...  # invalid login
```

（必须**先 `authenticate()` 再 `login()`**；authenticate 成功返回 User、失败返回 None。讲义原例。）

---

# 押题热点（按出题概率排序）

**MCQ-I 概念题最可能考：**

1. MVC↔MVT 映射（Controller=View, View=Template）⭐⭐⭐
2. 三层架构↔Django 组件对应 ⭐⭐⭐
3. HTTP 无状态 / Cookie vs Session 存储位置 ⭐⭐⭐
4. 状态码含义（200/301/403/404/500）⭐⭐⭐
5. makemigrations vs migrate 的区别 ⭐⭐⭐
6. GET vs POST 使用场景 ⭐⭐
7. null vs blank ⭐⭐
8. DNS 作用 / 解析顺序（浏览器缓存→OS→ISP→根→权威）⭐⭐
9. PBKDF2 密码哈希、`|safe` 与 XSS ⭐⭐
10. IPv4(32位) vs IPv6(128位)；TCP/IP 四层；HTTPS=443 ⭐

**MCQ-II 代码题最可能考（官方两道样题都是"代码排错"型）：**

1. ORM 链式查询读结果（filter+order_by+切片）⭐⭐⭐ ——官方样题原型
2. "XX 不显示/报错"排错：忘 INSTALLED_APPS、忘 migrate、忘 csrf_token、忘登录 ⭐⭐⭐
3. `get()` 的两个异常 ⭐⭐
4. login_required 重定向带 `?next=` vs permission_required 403 ⭐⭐
5. FK 反查 `xxx_set.all()`、URL `<int:>` 转换器 ⭐⭐
6. session 计数器/`request.session.get(k, default)` 代码 trace ⭐⭐
7. bound vs unbound form 的 `is_valid()` ⭐

**SA-I 填空最可能考（一句话，背就完了）：**

- 文件名：models.py / views.py / urls.py / admin.py / settings.py / forms.py
- 命令：runserver / startapp / startproject / makemigrations / migrate / createsuperuser / shell
- 名词：objects（默认 Manager）、sessionid（cookie 名）、auth_user（用户表）、`{% csrf_token %}`、`{% extends %}`/`{% block %}`、443/80、AnonymousUser、PBKDF2、`/admin/`
- 认证 vs 授权一句话区分（who you are vs what you can do）

**SA-II 写代码最可能考（官方样题就是一行 ORM）：**

1. ORM 查询：order_by / filter + lookup / 切片 / 组合 ⭐⭐⭐（最稳的押题）
2. ModelForm 完整类 ⭐⭐
3. session 计数 / set_cookie("favorite_color","blue",max_age=3600) ⭐⭐
4. authenticate→login 流程 ⭐⭐
5. path() 写 URL 模式（带 name= 或 `<int:>`）⭐
6. `__str__` 方法 / 带 FK 的简单 model 定义 ⭐

**易错警示：**

- `order_by("-join_date")` 的 `-` 别丢（官方样题专门考了）。
- `get()` vs `filter()`：要"恰好一条"才用 get。
- login_required→**重定向**，permission_required(raise_exception=True)→**403**，别混。
- 默认权限个数：老讲义（Authentication PDF）写 **3 个（add/change/delete）**，但 Week 5 课件 admin 截图含 view 共 **4 个**——若考"列出默认权限"，写 add/change/delete（+view），并知道格式 `app.add_model`。
- `set_expiry(0)` = 关浏览器即过期；`SESSION_EXPIRE_AT_BROWSER_CLOSE` 默认 **False**。
- 测试 cookie：`set_test_cookie()` 与 `test_cookie_worked()` 必须在**不同请求**里。
- Django 不自动清过期 session → 定期跑 `clearsessions`。

---

---

# 加练：基于课堂真实代码的精准押题

> 以下题目全部取材于 `code/` 目录下的实际课堂项目（week3–5 的 `classroom` app、week4 的 `guestbook` 调试挑战、week3 的 `shell_queries.py`）。
> **特别注意**：guestbook 是课堂的 Group Debugging Challenge，代码里标注了 FIX 1–9 共九处 bug——"给一段坏代码问哪里错了/什么症状"正是 MCQ Level II 的官方出题风格，这九个 bug 每个都可能变成考题。
> 答案紧跟在每题后面，自测时遮住下半部分。

## A. Guestbook 调试题（对应 FIX 1–9）

**B1.** The `EntryForm` was written as:

```python
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["message"]          # display_name missing!
```

Symptom: every saved entry shows as "Anonymous". Why?

> **答案**：`fields` 没包含 `display_name` → 该字段既不渲染也不保存，模型里 `blank=True, default=""` 让它默默存了空串。（FIX 1：把 `"display_name"` 加进 fields。）

**B2.** A user submits a message consisting only of spaces `"   "`. The form has:

```python
def clean_message(self):
    msg = self.cleaned_data.get("message", "").strip()
    if not msg:
        raise forms.ValidationError("Message cannot be empty.")
    return msg
```

What happens?

> **答案**：`strip()` 后为空 → 抛 `ValidationError` → `is_valid()` 返回 False → 表单带错误信息重新渲染（"Message cannot be empty."）。**自定义验证方法命名规则：`clean_<字段名>`，返回清洗后的值。**（FIX 2）

**B3.** `set_name_cookie` saves the cookie with key `"display_name"`, but `entry_list` reads `request.COOKIES.get("displayname", "")`. What's the symptom?

> **答案**：键名不一致 → 读永远拿到默认值 `""` → 名字预填永远不生效。Cookie 的 set 和 get 必须用**完全相同的键名**。（FIX 5/6 同理：`delete_cookie` 也必须删对键。）

**B4.** What does `resp.delete_cookie("displayname")` actually send to the browser?

> **答案**：一个让该 cookie **立即过期**的 Set-Cookie 头（值清空、过期时间设为过去），浏览器随即删除它。服务器不能"伸手"进浏览器删，只能指示浏览器删。

**B5.** If the cookie does not exist, what does `request.COOKIES.get("displayname", "")` return — and what would `request.COOKIES["displayname"]` do?

> **答案**：`get` 返回默认值 `""`；下标访问抛 **KeyError**。`request.COOKIES` 是普通字典。

**B6.** How long does this cookie live: `resp.set_cookie("displayname", name, max_age=7*24*3600)`?

> **答案**：7 天（max_age 单位是**秒**）。课堂另一例：`set_cookie("fav_color", "blue", max_age=3600)` = 1 小时。

**B7.** Is this form bound or unbound, and what does `is_valid()` return?

```python
form = EntryForm(initial={"display_name": request.COOKIES.get("displayname", "")})
```

> **答案**：**Unbound**。`initial=` 只做预填充，不算绑定数据（绑定要传**第一个位置参数** data，如 `EntryForm(request.POST)`）。Unbound 的 `is_valid()` 永远 False。

**B8.** After a successful save, the view does `return redirect("gb-list")` instead of rendering a template directly. Why?

> **答案**：**Post/Redirect/Get（PRG）模式**——防止用户刷新结果页时重复提交表单（重复插入数据）。`redirect()` 返回 `HttpResponseRedirect`。

**B9.** In `entry_list.html` the "set my name" form uses `method="get"`:

```html
<form method="get" action="{% url 'gb-set-name' %}">
  <input type="text" name="name" ... />
</form>
```

And the view reads `request.GET.get("name", "").strip()`. Where does `"name"` come from, and why is GET acceptable here?

> **答案**：来自查询串 `?name=...`（input 的 `name` 属性决定键名）。这里只是设置一个 cookie 偏好、语义上幂等且数据不敏感，GET 可接受；而**新增 guestbook 条目改变数据库状态，必须 POST**。

## B. classroom / ORM 代码题（week3/5 实码）

**B10.** Week 3 class activity: you added `phone_number = models.CharField(max_length=20, blank=True, default="")` to `Student`. Which commands make the database match, and what file appears?

> **答案**：`python manage.py makemigrations` → 生成 `classroom/migrations/0002_student_phone_number.py`；再 `python manage.py migrate` 应用。（真实项目里就有这个 0002 文件。）

**B11.** From `shell_queries.py`:

```python
deleted, info = Student.objects.filter(join_date__lt=cutoff).delete()
```

What does this do and what does it return?

> **答案**：删除所有 `join_date` 早于 cutoff 的行；返回元组 `(总删除数, 按模型分类的字典)`。注意 QuerySet 也有批量 `.update(join_date=old)`（脚本里也用了）。

**B12.** `student_list` passes `"is_empty": not qs.exists()` and `"count": qs.count()`. Why prefer `exists()`/`count()` over `len(qs)`?

> **答案**：`exists()`/`count()` 让数据库做高效判断/计数（SQL EXISTS/COUNT），不必把所有行取回 Python。讲义明确说"应使用 count 属性而不是 len()"。

**B13.** In week5 the real `views.py` accidentally defines `def dashboard(request)` **twice**. Which one does Django use?

> **答案**：**后定义的覆盖先定义的**（Python 名字重绑定，无报错无警告）。顺带一提：第一个 dashboard 里 `extra({'day': "date(join_date"})` 还少个右括号——若被问"这段代码有什么问题"，这两点都值得说。

**B14.** `Entry.objects.all().order_by("-created_at")` vs `Entry.objects.order_by("-created_at")` — difference?

> **答案**：没有区别，`all()` 只是显式起点；两者都返回按创建时间**最新在前**的 QuerySet。

**B15.** In `settings.py`:

```python
TEMPLATES = [{ ..., 'DIRS': [BASE_DIR / "templates"], 'APP_DIRS': True, ... }]
```

Why is `DIRS` needed for `templates/registration/login.html` but not for `classroom/templates/classroom/student_list.html`?

> **答案**：`APP_DIRS=True` 自动找**各 app 内**的 `templates/` 目录；而 `registration/login.html` 放在**项目根**的 templates/ 下，必须靠 `DIRS` 指路。（Week 5 配登录页时改的就是这里。）

**B16.** Template snippets from the real project — name the output of each:

```django
{{ e.display_name|default:"Anonymous" }}     {# display_name 是 "" #}
{{ e.created_at|date:"M d, Y H:i" }}
{% for e in entries %} ... {% empty %} <tr><td>No entries yet.</td></tr> {% endfor %}
```

> **答案**：① 空串为假值 → 显示 **Anonymous**；② 按格式输出如 `Jun 12, 2026 14:30`；③ `{% empty %}` 在**列表为空**时渲染。

## C. 加练写代码（SA Level II 风格）

**C1.** Write one line that sets a cookie named `displayname` (value in variable `name`) that lasts exactly 7 days, on a response object `resp`.

> **答案**：`resp.set_cookie("displayname", name, max_age=7*24*3600)`

**C2.** Write a custom validation method for `EntryForm` that rejects messages longer than 280 characters with the error "Message is too long".

> **答案**：
>
> ```python
> def clean_message(self):
>     msg = self.cleaned_data.get("message", "").strip()
>     if len(msg) > 280:
>         raise forms.ValidationError("Message is too long")
>     return msg
> ```

**C3.** Write the ORM statement used in class to list **today's** sign-ups count (Student, `join_date`):

> **答案**：`Student.objects.filter(join_date=timezone.now().date()).count()`（来自 dashboard 视图；记得 `from django.utils import timezone`。）

**C4.** Using the real project's URL names, write the template tag that links to the add-student page **only if** the user has permission:

> **答案**：
>
> ```django
> {% if perms.classroom.add_student %}
>   <a href="{% url 'add-student' %}">Add Student</a>
> {% endif %}
> ```

## 课堂代码 ↔ 考点对照表（最后过一遍）

| 代码位置                           | 必须能默写/解释的点                                                                                                                          |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `classroom/models.py`              | `EmailField(unique=True)`、`DateField(auto_now_add=True)`、`__str__`                                                                         |
| `classroom/forms.py`               | ModelForm 三件套：继承、`Meta.model`、`Meta.fields`                                                                                          |
| `classroom/views.py`               | add_student 的 POST/GET 分支全流程；`@login_required` + `@permission_required('classroom.add_student', raise_exception=True)` 叠加顺序与效果 |
| `visit_counter` / `set_fave_color` | session 计数两行 + `set_cookie` 一行                                                                                                         |
| `config/urls.py`                   | `include("django.contrib.auth.urls")` 送的免费 URL；`include("classroom.urls")`；`path(..., name=...)`                                       |
| `guestbook/*`（FIX 1–9）           | 九个 bug 的"症状→原因→修法"，尤其 csrf_token 缺失→403、cookie 键名不一致、fields 漏字段                                                      |
| `shell_queries.py`                 | create / filter(icontains) / order_by("-...") / filter(...).delete() / .update()                                                             |
| `settings.py`                      | INSTALLED_APPS 默认 6 项 + 自己的 app；TEMPLATES 的 DIRS vs APP_DIRS                                                                         |
