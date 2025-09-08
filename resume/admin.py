from django.contrib import admin
from .models import UserInfo, Work, Education, Skill, Language, Template, Theme


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "phone", "location", "linkedin")
    search_fields = ("fullname", "email", "phone", "location")
    list_filter = ("location",)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("company_name", "position", "start_date", "end_date")
    search_fields = ("company_name", "position")
    list_filter = ("company_name", "start_date")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution_name", "degree", "field", "start_date", "end_date")
    search_fields = ("institution_name", "degree", "field")
    list_filter = ("degree", "field")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "level")
    search_fields = ("name", "level")
    list_filter = ("level",)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "selected")
    search_fields = ("name",)
    list_filter = ("selected",)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "selected")
    search_fields = ("name",)
    list_filter = ("selected",)
