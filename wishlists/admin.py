from django.contrib import admin
from wishlists.models import List, Item, Pledge

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title','deadline','expired', 'created_at', 'modified_at')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('list','image','title','description','price',
                    'created_at', 'modified_at')

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('item', 'pledge_value','pledge_id',
                    'created_at', 'modified_at')
