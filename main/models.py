# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
import time
from django.utils.translation import ugettext_lazy as _
import random
import re

from django.contrib.auth.models import User

def f():
    return int(time.time())

def u():
	return User.objects.all()


class IdeaCategory(models.Model):
	idea_category = models.CharField(max_length=200)
	category_summery = models.CharField(max_length=200)
	category_slug = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = _("Categories")

	def __str__(self):
		return self.idea_category


class IdeaSeries(models.Model):
	idea_series = models.CharField(max_length=200)
	idea_category = models.ForeignKey(IdeaCategory, default=1, verbose_name="Category" ,on_delete=models.SET_DEFAULT)
	series_summary = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = _("Series")

	def __str__(self):
		return self.idea_series



class MyIdea(models.Model):
	created_by = models.ForeignKey(User, related_name='created_by',on_delete=models.CASCADE)
	idea_title = models.CharField(max_length=200,verbose_name=_("Title"))
	idea_conttent = models.TextField(verbose_name=_("Content"))
	idea_published = models.DateTimeField(_("date published"),default=datetime.now())
	
	idea_series = models.ForeignKey(IdeaSeries, default=1 ,verbose_name=_("Series") , on_delete=models.SET_DEFAULT)
	idea_slug = models.CharField(max_length=200,default=f,verbose_name=_("url"))
	idea_publisher = models.CharField(max_length=200,default="هم مدادفشاری",verbose_name=_("نگارنده"),help_text="میتوانید نوشته خود را با یک نام خاص انتشار دهید")

	class Meta:
		verbose_name_plural = _("My idea")

	def __str__(self): 
		return self.idea_title




