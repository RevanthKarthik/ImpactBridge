from django.contrib import admin
from .models import Donation, Media, Blog

class MediaInline(admin.TabularInline):
    model = Media
    extra = 1  # Number of extra forms to display (you can adjust this)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    list_display = ('title', 'category', 'date_posted', 'end_date', 'goal_amount')
    list_filter = ('category', 'date_posted', 'end_date')
    search_fields = ('title', 'description', 'story')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('donation', 'media_type', 'file')
    list_filter = ('media_type', 'donation')
    search_fields = ('donation__title',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'donation', 'date_posted')
    list_filter = ('date_posted', 'donation')
    search_fields = ('title', 'content', 'donation__title')