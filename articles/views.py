from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Author, Comment
from django.urls import reverse


def home(request):
    articles = Article.objects.all()
    ctx = {'articles':articles}
    return render(request, 'index.html', ctx)

def create_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        if name and bio and email:
            Author.objects.create(
                name = name,
                bio = bio,
                email = email
            )
            return redirect('home')
    return render(request, 'articles/create-author.html')

def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_id = request.POST.get('author')
        image = request.FILES.get('image')
        if title and content and author_id and image:
            author = Author.objects.get(id=author_id)
            article = Article.objects.create(
                title = title,
                content = content,
                author = author,
                image = image
            )
            return redirect('home')
    authors = Author.objects.all()
    ctx = {'authors':authors}
    return render(request, 'articles/create-article.html', ctx)

def blog_detail(request, year, month, day,slug):
    article = get_object_or_404(
        Article,
        slug = slug,
        posted_at__year = year,
        posted_at__month = month,
        posted_at__day = day
    )
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        if name and email and comment:
            Comment.objects.create(
                article = article,
                name = name,
                email = email,
                comment = comment
            )
            return redirect(reverse('articles:success-comment', kwargs={'slug': slug}))
    comments = article.comments.all()
    ctx = {'article':article, 'comments':comments}
    return render(request, 'articles/blog-detail.html', ctx)

def success_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    ctx = {'article':article}
    return render(request, 'articles/success-commented.html', ctx)