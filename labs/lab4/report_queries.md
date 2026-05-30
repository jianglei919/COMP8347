# COMP 8347 — Lab #4 Report (Query Section)

> Project: Django 6.0.5, app `myapp`. Run queries with:
> `python manage.py shell < queries.py`

---

## Part 2.6 — Basic queries

```python
import django
from myapp.models import Publisher, Book, Member, Order
```

**a. List all the books in the db**
```python
Book.objects.all()
```
Result: Machine Learning For Dummies, Data Science For Dummies, Artificial Intelligence, Computer Networking, The Night Circus, The Underground Railroad, Becoming, A Walk in the Woods

**b. List all the members in the db**
```python
Member.objects.all()
```
Result: Elena Kwon, Marcus Reed, Priya Shah, James Bennett, Aisha Ncube, Leo Kwon

**c. List all the orders in the db**
```python
Order.objects.all()
```
Result: 7 orders (#1 elena Borrow, #2 marcus Borrow, #3 aisha Borrow, #4 james Borrow, #5 leo Purchase, #6 elena Purchase, #7 aisha Purchase)

**d. List all the publishers in the db**
```python
Publisher.objects.all()
```
Result: Wiley, Pearson, Penguin Random House

---

## Part 3 — Query practice

**a. Members whose last name is 'Kwon'**
```python
Member.objects.filter(last_name='Kwon')
```
Result: Elena Kwon, Leo Kwon

**b. Publishers with headquarters in 'USA'**
```python
Publisher.objects.filter(country='USA')
```
Result: Wiley, Penguin Random House

**c. Members that live in 'Ottawa'**
```python
Member.objects.filter(city='Ottawa')
```
Result: Marcus Reed, James Bennett, Leo Kwon

**d. Members that live on an 'Avenue' and live in ON province**
```python
Member.objects.filter(address__icontains='Avenue', province='ON')
```
Result: James Bennett
*(Elena is on an Avenue too but lives in BC, so correctly excluded.)*

**e. Members that have borrowed the book 'The Night Circus'**
```python
Member.objects.filter(borrowed_books__title='The Night Circus')
```
Result: Elena Kwon, Marcus Reed, James Bennett

**f. Books that cost more than $40.00**
```python
Book.objects.filter(price__gt=40.00)
```
Result: Artificial Intelligence ($197.32), Computer Networking ($143.99), The Night Circus ($41.00), Becoming ($45.00)

**g. Members that do NOT live in province ON**
```python
Member.objects.exclude(province='ON')
```
Result: Elena Kwon (BC), Priya Shah (SK), Aisha Ncube (MB)

**h. Orders placed by a client whose first_name is 'Elena'**
```python
Order.objects.filter(member__first_name='Elena')
```
Result: Order #1 (Borrow), Order #6 (Purchase)

**i. Members whose status are 'Regular Member'**
```python
Member.objects.filter(status=1)
```
Result: Marcus Reed, Priya Shah

**j. Books with 300–500 pages (inclusive) in category 'Science&Tech'**
```python
Book.objects.filter(num_pages__range=(300, 500), category='S')
```
Result: Machine Learning For Dummies (464p), Data Science For Dummies (432p)

**k. First name of Members who have borrowed exactly 2 books**
```python
from django.db.models import Count
Member.objects.annotate(n=Count('borrowed_books')).filter(n=2).values_list('first_name', flat=True)
```
Result: Elena, James, Marcus

**l. Books that Member with username 'Marcus' is currently borrowing**
```python
Book.objects.filter(member__username='marcus')
```
Result: Artificial Intelligence, The Night Circus

**m. Members who live in ON and have auto_renew enabled**
```python
Member.objects.filter(province='ON', auto_renew=True)
```
Result: Marcus Reed, James Bennett

**n. Books that 'Leo' has purchased**  *(order_type 0 = Purchase)*
```python
Book.objects.filter(order__member__username='leo', order__order_type=0)
```
Result: The Night Circus, A Walk in the Woods

**o. City where the headquarters of the publisher of the book purchased by 'Elena' is located**
```python
Publisher.objects.filter(
    books__order__member__first_name='Elena',
    books__order__order_type=0,
).values_list('city', flat=True).distinct()
```
Result: London
*(Elena purchased 'Artificial Intelligence' → published by Pearson → headquartered in London.)*
