from django.contrib import admin

from backend.models import URL, History, Product, Store

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id','description',)  
    search_fields = ('description',)  
    
admin.site.register(Store, StoreAdmin)

class URLAdmin(admin.ModelAdmin):
    list_display = ('store','created_at','url')  
    search_fields = ('store',)  
    
admin.site.register(URL, URLAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','store','description',)  
    search_fields = ('store',)  
    
    def has_add_permission(self, request):
        return False 

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False 

    
admin.site.register(Product, ProductAdmin)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('at','default_price','offer_price','offer','category')  
    search_fields = ('category',)  
    list_filter = ('at','offer') 
    
    
    def has_add_permission(self, request):
        return False 

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False 
admin.site.register(History, HistoryAdmin)