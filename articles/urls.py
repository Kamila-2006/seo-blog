from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('author', views.create_author, name='create-author'),
    path('article', views.create_article, name='create-article'),
    path('articles/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.blog_detail, name='blog-detail'),
    path('articles/success-comment/<slug:slug>/', views.success_comment, name='success-comment'),
    path('category/<str:category>/', views.post_by_category, name='category'),
]