from django.contrib import admin

from .models import Skill, Title, UserStats, Language, Job, Quest, Reflection

admin.site.register(Skill)
admin.site.register(Title)
admin.site.register(UserStats)
admin.site.register(Language)
admin.site.register(Job)
admin.site.register(Quest)
admin.site.register(Reflection)

