from django.contrib import admin
from .models import Template, Theme, UserInfo, Work, Education, Skill, Language


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'selected')
    list_filter = ('selected',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'selected')
    list_filter = ('selected',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'phone', 'location')
    search_fields = ('fullname', 'email', 'phone', 'location')
    ordering = ('fullname',)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'company_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('position', 'company_name')
    ordering = ('-start_date',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'degree', 'institution_name', 'field', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('degree', 'institution_name', 'field')
    ordering = ('-start_date',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level')
    search_fields = ('name', 'level')
    ordering = ('name',)
