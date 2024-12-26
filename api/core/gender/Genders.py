from api.core.helper import helper
from api.models import *


# master module class
class Genders:
    def __init__(self):
        self.help = helper.Helper()

    # Gender
    def getAllGenders(self, request, lang):
        results = []
        genders = Gender.objects.filter(is_disabled=False).order_by("-id")
        for gender in genders:
            gender_item = {
                "id": gender.pk,
                "gender_name": gender.gender_name,
                "initials": gender.initials,
                "code_name": gender.code_name,
                "is_disabled": gender.is_disabled,
                "created": gender.created,
            }
            results.append(gender_item)
        return results

    def GenderExists(self, request, lang, genderid):
        return Gender.objects.filter(pk=int(genderid)).exists()

    def getGenderById(self, request, lang, genderid):
        gender = Gender.objects.filter(pk=int(genderid)).get()
        return {
            "id": gender.pk,
            "gender_name": gender.gender_name,
            "initials": gender.initials,
            "code_name": gender.code_name,
            "is_disabled": gender.is_disabled,
            "created": gender.created,
        }

    def createGender(self, request, lang, data):
        data["code_name"] = data["gender_name"].lower().replace(" ", "_")
        # create Gender
        gender = Gender.objects.create(
            gender_name=data["gender_name"],
            initials=data["initials"],
            code_name=data["code_name"],
            is_disabled=data["is_disabled"],
        )
        gender.save()
        return True

    def updateGender(self, data, genderid):
        data["code_name"] = data["gender_name"].lower().replace(" ", "_")
        # select gender to update
        toUpdate = Gender.objects.filter(pk=int(genderid))
        dbRecToUpdate = toUpdate.get()
        updateRecord_dic = {
            "gender_name": (
                data["gender_name"]
                if data["gender_name"]
                else dbRecToUpdate.gender_name
            ),
            "initials": (
                data["initials"] if data["initials"] else dbRecToUpdate.initials
            ),
            "code_name": (
                data["code_name"] if data["code_name"] else dbRecToUpdate.code_name
            ),
            "is_disabled": (
                data["is_disabled"]
                if data["is_disabled"]
                else dbRecToUpdate.is_disabled
            ),
        }
        # save the record updates
        toUpdate.update(**updateRecord_dic)
        return True
