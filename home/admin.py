from django.contrib import admin
from .models import Policy, ContactMessage, CodeSession, CodeMessage, StudySession, StudyMessage
# Register your models here.
admin.site.register(ContactMessage)

admin.site.register(CodeSession)
admin.site.register(CodeMessage)
admin.site.register(StudySession)
admin.site.register(StudyMessage)

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'policy_type', 'updated_at')
    search_fields = ('title', 'policy_type')
    list_filter = ('policy_type', 'updated_at')