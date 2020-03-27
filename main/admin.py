# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import MyIdea , IdeaSeries , IdeaCategory, Donate, Comments
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.

# Costum Idea Panel
class MyIdeaAdmin(admin.ModelAdmin):
	list_display = ("idea_title","idea_series","idea_slug","idea_publisher","idea_published")
	list_filter = ("idea_series","idea_publisher")
	search_fields = ("idea_title","idea_slug","idea_publisher")
	fieldsets = [
		("Title/date",{"fields":["idea_title","idea_published"]}),
		("URL",{"fields":["idea_slug","idea_publisher"]}),
		("Series",{"fields":["idea_series"]}),
		("Content",{"fields":["idea_conttent"]})
	]
	readonly_fields=('idea_slug', )
	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}
	}
	def save_model(self, request, obj, form, change):
		instance = form.save(commit=False)
		if not hasattr(instance,'created_by'):
			instance.created_by = request.user
		instance.edited_by = request.user
		instance.save()
		form.save_m2m()
		return instance

	def save_formset(self, request, form, formset, change):

		def set_user(instance):
			if not instance.created_by:
				instance.created_by = request.user
			instance.edited_by = request.user
			instance.save()

		if formset.model == Article:
			instances = formset.save(commit=False)
			map(set_user, instances)
			formset.save_m2m()
			return instances
		else:
			return formset.save()
admin.site.register(MyIdea,MyIdeaAdmin)

# Costum Idea Series Panel
class CustomIdeaSeriesPanel(admin.ModelAdmin):
	list_display = ("idea_series","idea_category","series_summary")
	list_filter = ("idea_series","idea_category")
admin.site.register(IdeaSeries,CustomIdeaSeriesPanel)

# Costum Idea Cat Panel
class CustomIdeaCategoryPanel(admin.ModelAdmin):
	list_display = ("idea_category","category_summery","category_slug")
	list_filter = ("idea_category","category_summery")
admin.site.register(IdeaCategory,CustomIdeaCategoryPanel)

# Costum Donate Panel
class CustomDonatePanel(admin.ModelAdmin):
	list_display = ("name_donate","email_donate","amount_donate","transaction_code_donate","transaction_status_donate")
	search_fields = ("name_donate","email_donate","amount_donate")
admin.site.register(Donate,CustomDonatePanel)

# Costum Comments Panel
class CustomCommentsPanel(admin.ModelAdmin):
	list_display = ("user_name","post_title","post_id","reply_id","comment")
	search_fields = ("user_name","post_title","post_id","reply_id")
admin.site.register(Comments,CustomCommentsPanel)
