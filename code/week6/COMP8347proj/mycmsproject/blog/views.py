from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.shortcuts import get_object_or_404
from .models import Article

# Create your views here.
def vulnerable_article(request):
    # WARNING: insecure –  demonstrates string concatenation into SQL
    article_id = request.GET.get('id', '')
    sql = f"SELECT id, title, body FROM blog_article WHERE id = {article_id};"
    with connection.cursor() as cursor:
        cursor.execute(sql)           # vulnerable if article_id contains SQL
        rows = cursor.fetchall()
    articles = [{"id": r[0], "title": r[1], "body": r[2]} for r in rows]
    return JsonResponse({"articles": articles})

def safe_article_param(request):
    article_id = request.GET.get('id', '')
    sql = "SELECT id, title, body FROM blog_article WHERE id = %s;"
    with connection.cursor() as cursor:
        cursor.execute(sql, [article_id])  # parameterized
        rows = cursor.fetchall()
    articles = [{"id": r[0], "title": r[1], "body": r[2]} for r in rows]
    return JsonResponse({"articles": articles})

def safe_article_orm(request):
    article_id = request.GET.get('id', '')
    try:
        pk = int(article_id)
    except (ValueError, TypeError):
        return JsonResponse({"error": "invalid id"}, status=400)
    article = get_object_or_404(Article, pk=pk)
    return JsonResponse({"article": {"id": article.id, "title": article.title, "body": article.body}})