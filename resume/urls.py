from django.urls import path
from .views import (
    UserInfoList, UserInfoDetail,
    WorkList, WorkDetail,
    EducationList, EducationDetail,
    SkillList, SkillDetail,
    LanguageList, LanguageDetail,
    TemplateList, TemplateDetail,
    ThemeList, ThemeDetail, GenerateTemplateView, GeneratePDFView,
)

urlpatterns = [
    path("api/userinfo/", UserInfoList.as_view(), name="userinfo-list"),
    path("api/userinfo/<int:pk>/", UserInfoDetail.as_view(), name="userinfo-detail"),

    path("api/work/", WorkList.as_view(), name="work-list"),
    path("api/work/<int:pk>/", WorkDetail.as_view(), name="work-detail"),

    path("api/education/", EducationList.as_view(), name="education-list"),
    path("api/education/<int:pk>/", EducationDetail.as_view(), name="education-detail"),

    path("api/skills/", SkillList.as_view(), name="skill-list"),
    path("api/skills/<int:pk>/", SkillDetail.as_view(), name="skill-detail"),

    path("api/languages/", LanguageList.as_view(), name="language-list"),
    path("api/languages/<int:pk>/", LanguageDetail.as_view(), name="language-detail"),

    path("api/templates/", TemplateList.as_view(), name="template-list"),
    path("api/templates/<int:pk>/", TemplateDetail.as_view(), name="template-detail"),
    path("api/template/generate/", GenerateTemplateView.as_view(), name="generate-template"),
    path("templates/pdf/", GeneratePDFView.as_view(), name="generate-pdf"),

    path("api/themes/", ThemeList.as_view(), name="theme-list"),
    path("api/themes/<int:pk>/", ThemeDetail.as_view(), name="theme-detail"),
]
