from django.contrib import admin
from django import forms
from account.models import Moderator, Expert


class ModeratorCreation(admin.ModelAdmin):
    email = forms.EmailField()
    last_name = forms.CharField()
    first_name = forms.CharField()
    middle_name = forms.CharField()

    fields = ("email", "last_name", "first_name", "middle_name")

    def save_model(self, request, obj, form, change):
        if request.method == "POST" and not change:
            Moderator.objects.create_moderator(request.POST["email"],
                                               request.POST["last_name"],
                                               request.POST["first_name"],
                                               request.POST["middle_name"])


class ExpertCreation(admin.ModelAdmin):
    email = forms.EmailField()
    last_name = forms.CharField()
    first_name = forms.CharField()
    middle_name = forms.CharField()
    profession = forms.CharField()
    professional_experience = forms.IntegerField
    position = forms.CharField()
    driver_license = forms.ComboField()
    driving_experience = forms.CharField()

    fields = ("email", "last_name", "first_name", "middle_name",
              "profession", "professional_experience", "position",
              "driver_license", "driving_experience")

    def save_model(self, request, obj, form, change):
        if request.method == "POST" and not change:
            Expert.objects.create_expert(email=request.POST["email"],
                                         last_name=request.POST["last_name"],
                                         first_name=request.POST["first_name"],
                                         middle_name=request.POST["middle_name"],
                                         profession=request.POST["profession"],
                                         professional_experience=request.POST["professional_experience"],
                                         position=request.POST["position"],
                                         driver_license=request.POST["driver_license"],
                                         driving_experience=request.POST["driving_experience"])

admin.site.register(Moderator, ModeratorCreation)
admin.site.register(Expert, ExpertCreation)
