from django.contrib import admin
from home.models import contact,userInfo,userCarpools

# Register your models here.
admin.site.register(contact)
admin.site.register(userInfo)
admin.site.register(userCarpools)