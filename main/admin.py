# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import MyIdea , IdeaSeries , IdeaCategory,Donate
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.
class MyIdeaAdmin(admin.ModelAdmin):

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




admin.site.register(IdeaSeries)
admin.site.register(IdeaCategory)

admin.site.register(MyIdea,MyIdeaAdmin)

admin.site.register(Donate)