from django.contrib import admin
from .models import Insurance, Policy

admin.site.register([Insurance, Policy])

