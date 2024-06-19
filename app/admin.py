from django.contrib import admin
from django.contrib.auth.models import User

from app.models import Item, Supplier

# Register your models here.


admin.register(Item)
admin.register(Supplier)
admin.register(User)
