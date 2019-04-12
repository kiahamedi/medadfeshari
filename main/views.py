# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .models import MyIdea, IdeaSeries, IdeaCategory
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe
import json


def homepage(request):
	return render(request=request,
				template_name="main/categories.html",
				context={"categories":IdeaCategory.objects.all(),
						"Ideas":MyIdea.objects.order_by('idea_published').reverse()})


def editPost(request):
	current_user = request.user
	if request.method == "POST":
		if str(current_user.id) == str(request.POST.get("created_by")):
			print(request.POST)
			slug_edit = request.POST.get("slug")
			slug_title = request.POST.get("title")
			slug_content = request.POST.get("conttent")
			print("url"+str(slug_edit)+"title:"+str(slug_title)+"content"+str(slug_content))
			return render(request,"main/editPost.html",
			context={"slugedit":slug_edit,
					"slugtitle":slug_title,
					"slugcontent":slug_content})
		else:
			messages.info(request, ("کار شما قشنگ نیست دوست عزیز"))
			return redirect("main:homepage")

	else:
		messages.info(request, ("کار شما قشنگ نیست دوست عزیز"))
		return redirect("main:homepage")


def editPostDone(request):
	current_user = request.user
	if request.method == "POST":

		id_post = request.POST.get("slugedit")
		title_post = request.POST.get("slugtitle")
		content_post = request.POST.get("area2")
		myPost = MyIdea.objects.get(idea_slug = id_post)
		myPost.idea_title = title_post
		myPost.idea_conttent = content_post
		myPost.save()
		messages.info(request, ("پست مورد نظر شما ویرایش گردید"))
		return redirect("main:homepage")

	else:
		messages.info(request, ("انگار مشکلی پیش اومد"))





def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,_("New Account Created: ") + username)
			basic_user = Group.objects.get(name='basicUser')
			user.groups.add(basic_user)
			#user.is_staff = True
			login(request, user)
			messages.info(request, _("You are now logged in as ") + username)


			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request,form.error_messages[msg])
				print(form.error_messages[msg])

	form = NewUserForm
	return render(request,
				"main/register.html",
				context={"form":form})


def logout_request(request):
	logout(request)
	messages.info(request,_("Logged out successfully"))
	return redirect("main:homepage")



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				messages.info(request, _("You are now logged in as ") + username)
				return redirect("main:homepage")

			else:
				messages.error(request, _("Invalid ysername or password or recaptcha"))

		else:
			messages.error(request, _("Invalid ysername or password or recaptcha"))

	form = AuthenticationForm()
	return render(request,
					"main/login.html",
					{"form":form})




def single_slug(request,single_slug):
	categories = [c.category_slug for c in IdeaCategory.objects.all()]
	#print(categories)
	if single_slug in categories:
		matching_series = IdeaSeries.objects.filter(idea_category__category_slug=single_slug)
		#print(matching_series)
		series_urls = {}
		print(len(matching_series.all()))
		for m in matching_series.all():
			part_one = MyIdea.objects.filter(idea_series__idea_series=m).earliest("idea_published")
			#part_one = MyIdea.objects.filter(idea_series__idea_series=m).earliest("idea_published")
			#print(part_one)
			#series_urls[m] = part_one.idea_slug
			series_urls[m] = part_one.idea_slug

			#print(part_one.idea_slug)
			#print(part_one)
			#series_urls[m] = m.idea_series.replace(" ","-")


		return render(request,
						"main/category.html",
						{"part_ones":series_urls})


	ideas = [t.idea_slug for t in MyIdea.objects.all()]
	print(ideas)
	if single_slug in ideas:
		#print(single_slug)
		this_idea = MyIdea.objects.get(idea_slug = single_slug)
		ideas_from_series = MyIdea.objects.filter(idea_series__idea_series=this_idea.idea_series).order_by("idea_published")

		this_idea_idx = list(ideas_from_series).index(this_idea)

		return render(request,
							"main/idea.html",
							{"idea":this_idea,
							 "sidebar": ideas_from_series,
							 "this_idea_idx":this_idea_idx})

	return HttpResponse(str(single_slug) + " dose not correspomd to anything.")


def index(request):
    return render(request, 'node-chat-app/public/index.html', {})
