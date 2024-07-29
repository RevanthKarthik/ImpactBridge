from django.contrib import admin
from taggit.admin import TagAdmin
from taggit.admin import TaggedItemInline
from .models import ProfilePersonal , kyc , Userdefine,NGOdetail,Causes

class kycAdmin(admin.ModelAdmin):
    readonly_fields = ('vendor_id',)  # Make vendor_id read-only
    

admin.site.register(NGOdetail)

admin.site.register(ProfilePersonal)
admin.site.register(Userdefine)
admin.site.register(Causes)
admin.site.register(kyc,kycAdmin)

