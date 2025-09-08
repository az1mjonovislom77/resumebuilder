import os
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import UserInfo, Work, Education, Skill, Language, Template, Theme
from .serializers import (
    UserInfoSerializer,
    WorkSerializer,
    EducationSerializer,
    SkillSerializer,
    LanguageSerializer,
    TemplateSerializer,
    ThemeSerializer,
)


@extend_schema(tags=['User'])
class UserInfoList(APIView):
    def get(self, request):
        users = UserInfo.objects.all()
        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['User'])
class UserInfoDetail(APIView):
    def get(self, request, pk):
        try:
            user = UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = UserInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            user = UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        user.delete()
        return Response(status=204)


@extend_schema(tags=['Work'])
class WorkList(APIView):
    def get(self, request):
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Work'])
class WorkDetail(APIView):
    def get(self, request, pk):
        try:
            work = Work.objects.get(pk=pk)
        except Work.DoesNotExist:
            return Response({"error": "Work not found"}, status=404)
        serializer = WorkSerializer(work)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            work = Work.objects.get(pk=pk)
        except Work.DoesNotExist:
            return Response({"error": "Work not found"}, status=404)

        serializer = WorkSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            work = Work.objects.get(pk=pk)
        except Work.DoesNotExist:
            return Response({"error": "Work not found"}, status=404)
        work.delete()
        return Response(status=204)


@extend_schema(tags=['Education'])
class EducationList(APIView):
    def get(self, request):
        edu = Education.objects.all()
        serializer = EducationSerializer(edu, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Education'])
class EducationDetail(APIView):
    def get(self, request, pk):
        try:
            edu = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response({"error": "Education not found"}, status=404)
        serializer = EducationSerializer(edu)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            edu = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response({"error": "Education not found"}, status=404)

        serializer = EducationSerializer(edu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            edu = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response({"error": "Education not found"}, status=404)
        edu.delete()
        return Response(status=204)


@extend_schema(tags=['Skill'])
class SkillList(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Skill'])
class SkillDetail(APIView):
    def get(self, request, pk):
        try:
            skill = Skill.objects.get(pk=pk)
        except Skill.DoesNotExist:
            return Response({"error": "Skill not found"}, status=404)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            skill = Skill.objects.get(pk=pk)
        except Skill.DoesNotExist:
            return Response({"error": "Skill not found"}, status=404)

        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            skill = Skill.objects.get(pk=pk)
        except Skill.DoesNotExist:
            return Response({"error": "Skill not found"}, status=404)
        skill.delete()
        return Response(status=204)


@extend_schema(tags=['Language'])
class LanguageList(APIView):
    def get(self, request):
        langs = Language.objects.all()
        serializer = LanguageSerializer(langs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Language'])
class LanguageDetail(APIView):
    def get(self, request, pk):
        try:
            lang = Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=404)
        serializer = LanguageSerializer(lang)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            lang = Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=404)

        serializer = LanguageSerializer(lang, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            lang = Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=404)
        lang.delete()
        return Response(status=204)


@extend_schema(tags=['Template'])
class TemplateList(APIView):
    def get(self, request):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Template'])
class TemplateDetail(APIView):
    def get(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return Response({"error": "Template not found"}, status=404)
        serializer = TemplateSerializer(template)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return Response({"error": "Template not found"}, status=404)

        serializer = TemplateSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return Response({"error": "Template not found"}, status=404)
        template.delete()
        return Response(status=204)


@extend_schema(tags=['Template'])
class GenerateTemplateView(APIView):
    def post(self, request):
        template_id = request.data.get("templateId")
        data = request.data.get("data", {})

        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"error": "Template not found"}, status=404)

        with open(template.html_file.path, "r", encoding="utf-8") as f:
            html_content = f.read()

        for key, value in data.items():
            html_content = html_content.replace(f"{{{{{key}}}}}", str(value))

        generated_dir = os.path.join(settings.MEDIA_ROOT, "generated")
        os.makedirs(generated_dir, exist_ok=True)
        user_id = request.user.id if request.user.is_authenticated else "anon"
        generated_filename = f"template_{template.id}_{user_id}.html"
        generated_path = os.path.join(generated_dir, generated_filename)

        with open(generated_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        generated_url = os.path.join(settings.MEDIA_URL, "generated", generated_filename)

        return Response({"url": generated_url}, status=200)


@extend_schema(tags=['Template'])
class GeneratePDFView(APIView):
    def post(self, request):
        template_id = request.data.get("templateId")
        data = request.data.get("data", {})

        if not template_id:
            return HttpResponse("templateId is required", status=400)

        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return HttpResponse("Template not found", status=404)

        with open(template.html_file.path, "r", encoding="utf-8") as f:
            html_content = f.read()

        for key, value in data.items():
            html_content = html_content.replace(f"{{{{{key}}}}}", str(value))

        result = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=result)

        if pisa_status.err:
            return HttpResponse("Error creating PDF", status=500)

        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="resume_{template_id}.pdf"'
        return response


@extend_schema(tags=['Theme'])
class ThemeList(APIView):
    def get(self, request):
        themes = Theme.objects.all()
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ThemeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Theme'])
class ThemeDetail(APIView):
    def get(self, request, pk):
        try:
            theme = Theme.objects.get(pk=pk)
        except Theme.DoesNotExist:
            return Response({"error": "Theme not found"}, status=404)
        serializer = ThemeSerializer(theme)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            theme = Theme.objects.get(pk=pk)
        except Theme.DoesNotExist:
            return Response({"error": "Theme not found"}, status=404)

        serializer = ThemeSerializer(theme, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            theme = Theme.objects.get(pk=pk)
        except Theme.DoesNotExist:
            return Response({"error": "Theme not found"}, status=404)
        theme.delete()
        return Response(status=204)
