from django.contrib import admin
from wishlists.models import List, Item, Pledge, Profile


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','deadline','expired',
                    'created_at', 'modified_at')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'list','image','title','description','price',
                    'created_at', 'modified_at')

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'pledge_value',
                    'created_at', 'modified_at')

