from .models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# 편집페이지 커스터마이징
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문', {'fields': ['question_text']}),
        ('생성일', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    readonly_fields = ['pub_date']
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text', 'choice__choice_text']


admin.site.register(Question, QuestionAdmin)
