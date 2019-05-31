# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .models import MyIdea, IdeaSeries, IdeaCategory , Donate , Comments
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe
import json

from django.shortcuts import redirect
from zeep import Client




MERCHANT = '*************-********-**********'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
#amount_input = 0  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'kia.arta9793@gmail.com'  # Optional
mobile = '09145480798'  # Optional
CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.

def send_request(request):
	amount_input = request.POST.get("amount")
	name_input = request.POST.get("nameinput")
	email_input = request.POST.get("emailinput")
	if amount_input == "" or name_input == "" or email_input == "":
		messages.warning(request, _("پر کردن تمامی فیلدها الزامی است"))
		return render(request, 'main/donate.html', {})

	result = client.service.PaymentRequest(MERCHANT, amount_input, description, email, mobile, CallbackURL)
	if result.Status == 100:
		userDonate = Donate()
		userDonate.name_donate = request.POST.get("nameinput")
		userDonate.email_donate = request.POST.get("emailinput")
		userDonate.amount_donate = request.POST.get("amount")
		userDonate.transaction_code_donate = "str(result.RefID)"
		userDonate.transaction_status_donate = "str(result.Status)"
		userDonate.save()
		return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
	else:
		#return HttpResponse('Error code: ' + str(result.Status))
		messages.warning(request, _("کمترین مقدار حمایت باید 100 تومان باشد"))
		return render(request, 'main/donate.html', {})

def verify(request):
	if request.GET.get('Status') == 'OK':
		userDonate = Donate.objects.latest('id')
		amount_input = userDonate.amount_donate
		#amount_input = request.POST.get("amount")
		result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount_input)
		if result.Status == 100:
			#return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
			userDonate = Donate.objects.latest('id')
			userDonate.transaction_code_donate = str(result.RefID)
			userDonate.transaction_status_donate = str(result.Status)
			userDonate.save()
			messages.success(request, _("ممنون از حمایت شما دوست گرامی\nکد تراکنش شما: " + str(result.RefID)))
			return render(request, 'main/donate.html', {})
		elif result.Status == 101:
			#return HttpResponse('Transaction submitted : ' + str(result.Status))
			userDonate = Donate.objects.latest('id')
			userDonate.transaction_code_donate = str(result.RefID)
			userDonate.transaction_status_donate = str(result.Status)
			userDonate.save()
			messages.success(request, _("تراکنش شما انجام شد: " + str(result.Status)))
			return render(request, 'main/donate.html', {})
		else:
			#return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
			userDonate = Donate.objects.latest('id')
			#userDonate.transaction_code_donate = str(result.RefID)
			userDonate.transaction_status_donate = str(result.Status)
			userDonate.save()
			messages.error(request, _("تراکنش شما ناموفق بود: " + str(result.Status)))
			return render(request, 'main/donate.html', {})
	else:
		#return HttpResponse('Transaction failed or canceled by user')
		userDonate = Donate.objects.latest('id')
		userDonate.transaction_code_donate = "str(result.RefID)"
		userDonate.transaction_status_donate = "canceled"
		userDonate.save()
		messages.error(request, _("تراکنش شما انجام نشد یا توسط خودتان لغو گردید"))
		return render(request, 'main/donate.html', {})


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
		all_comments = Comments.objects.all()
		return render(request,
							"main/idea.html",
							{"idea":this_idea,
							 "sidebar": ideas_from_series,
							 "this_idea_idx":this_idea_idx,
							 "all_comments":all_comments})

	return HttpResponse(str(single_slug) + " dose not correspomd to anything.")


def backstage(request):
	return render(request, 'main/Backstage.html', {})

def donate(request):

	query_results = Donate.objects.all()
	print(query_results)

	return render(request, 'main/donate.html', context={"alldonate":query_results})

def index(request):
    return render(request, 'node-chat-app/public/index.html', {})

def removeIdea(request):
	if request.method == "POST":
		slugidea = request.POST.get("slugpost")
		create = request.POST.get("create")

		user_idea = MyIdea.objects.get(idea_slug = slugidea)
		useridea = user_idea.created_by.id
		if int(useridea) == int(create):
			user_idea.delete()
			print("delete post")
			messages.success(request,_("پست مورد نظر شما پاک شد"))
			return redirect("main:homepage")
		else:
			messages.error(request,_("نوشته حذف نشد"))
			return redirect("main:homepage")


def addcomments(request):
	if request.method == "POST":
		post_id = request.POST.get("post_id")
		user_name = request.POST.get("user_name")
		post_title = request.POST.get("post_title")
		comment = request.POST.get("comment")
		print(post_id,user_name,post_title,comment)

		add_comments = Comments()
		add_comments.post_id = post_id
		add_comments.user_name = user_name
		add_comments.post_title = post_title
		add_comments.comment = comment
		add_comments.reply_id = "0"
		add_comments.save()
		messages.success(request,_("دیدگاه شما اضافه شد"))
		return redirect("/"+post_id)
	else:
		messages.error(request,_("مشکلی رخ داد با توسعه دهنده تماس بگیرید"))
		return redirect("main:homepage")


def replaycomments(request):
	if request.method == "POST":
		post_id = request.POST.get("post_id")
		user_name = request.POST.get("user_name")
		post_title = request.POST.get("post_title")
		reply_id = request.POST.get("reply_id")
		comment = request.POST.get("comment")
		#print(post_id,user_name,post_title,comment)
		add_comments = Comments()
		add_comments.post_id = post_id
		add_comments.user_name = user_name
		add_comments.post_title = post_title
		add_comments.comment = comment
		add_comments.reply_id = reply_id
		add_comments.save()
		messages.success(request,_("دیدگاه شما اضافه شد"))
		return redirect("/"+post_id)
	else:
		messages.error(request,_("مشکلی رخ داد با توسعه دهنده تماس بگیرید"))
		return redirect("main:homepage")



