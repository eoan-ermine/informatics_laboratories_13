from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def archive(request):
	return render(request, "archive.html", {"posts": Article.objects.all()})


def get_article(request, article_id):
	try:
		post = Article.objects.get(id=article_id)
		return render(request, "article.html", {"post": post})
	except Article.DoesNotExist:
		raise Http404


def create_post(request):
	if not request.user.is_anonymous:
		if request.method == "POST":
			form = {
				"text": request.POST["text"], "title": request.POST["title"]
			}
			if form["text"] and form["title"]:
				if Article.objects.filter(title=form["title"]).exists():
					form["errors"] = "Статья с таким заголовком уже существует"
					return render(request, "create_post.html", {"form": form})
				article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
				return redirect("get_article", article_id=article.id)
			else:
				form["errors"] = "Не все поля заполнены"
				return render(request, "create_post.html", {"form": form})
		else:
			return render(request, "create_post.html")
	else:
		raise Http404


def register(request):
	if request.user.is_anonymous:
		if request.method == "POST":
			form = {
				"username": request.POST["username"], "email": request.POST["email"],
				"password": request.POST["password"]
			}
			if form["username"] and form["email"] and form["password"]:
				if User.objects.filter(username=form["username"]).exists():
					form["errors"] = "Пользователь с таким именем пользователя уже существует"
					return render(request, "registration.html", {"form": form})
				login(request, User.objects.create_user(form["username"], form["email"], form["password"]))
				return redirect("archive")
			else:
				form["errors"] = "Не все поля заполнены"
				return render(request, "registration.html", {"form": form})
		else:
			return render(request, "registration.html")
	return redirect("archive")
