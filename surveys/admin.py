from django.contrib import admin

from .models import Survey, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date', 'author'], 'classes': ['collapse']}),
    # ]
    inlines = [ChoiceInline]

admin.site.register(Survey, SurveyAdmin)
