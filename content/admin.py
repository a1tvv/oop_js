from django.contrib import admin
from .models import Track,FeaturedVideo

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
from .models import RiyadhAsSalihin

@admin.register(RiyadhAsSalihin)
class RiyadhAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'created_at')
    
    list_display_links = ('title',) 
    list_editable = ('order',) 
    search_fields = ('title',)

@admin.register(FeaturedVideo)
class FeaturedVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'detected_at')
    readonly_fields = ('detected_at',)
    search_fields = ('title',)