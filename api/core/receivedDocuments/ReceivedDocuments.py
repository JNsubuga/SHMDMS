from api.core.helper import helper
from api.models import *

from api.core.users.Users import Users
from api.core.locale.Locale import Locale

###################
# master mdule class
class ReceivedDocuments:
    def __init__(self):
        self.users = Users()

    def getAllReceivedDocuments(self, request, lang):
        results = []
        receivedDocuments = ReceivedDocument.objects.filter(is_disabled=False).order_by("dateReceived")
        for receivedDocument in receivedDocuments:
            receivedDocument_item = {
                "id": receivedDocument.pk,
                "memo": receivedDocument.memo,
                "officeFrom": receivedDocument.officeFrom,
                "dateReceived": receivedDocument.dateReceived,
                "contactName": receivedDocument.contactName,
                "contactNumber": receivedDocument.contactNumber,
                "submitted_by": self.users.getAuthUserById(request, lang, receivedDocument.submitted_by.pk),
                # is_disabled = models.BooleanField(default=False)
                # created = models.DateTimeField(auto_now_add=True)
            }
            results.append(receivedDocument_item)
        return results
    def ReceivedDocumentExists(self, receiveddocumentid):
        return ReceivedDocument.objects.filter(pk=receiveddocumentid).exists()
    
    def getReceivedDocumentById(self, request, lang, receiveddocumentid):
        receivedDocument = ReceivedDocument.objects.filter(pk=receiveddocumentid).get()
        return {
            "id": receivedDocument.pk,
            "memo": receivedDocument.memo,
            "officeFrom": receivedDocument.officeFrom,
            "dateReceived": receivedDocument.dateReceived,
            "contactName": receivedDocument.contactName,
            "contactNumber": receivedDocument.contactNumber,
            "submitted_by": self.users.getAuthUserById(request, lang, receivedDocument.submitted_by.pk),
            # is_disabled = models.BooleanField(default=False)
            # created = models.DateTimeField(auto_now_add=True)
        }
    
    def registerReceivedDocument(self, userid, data):
        receivedDocument = ReceivedDocument.objects.create(
            memo = data["memo"],
            officeFrom = data["officeFrom"],
            dateReceived = data["dateReceived"],
            contactName = data["contactName"],
            contactNumber = data["contactNumber"],
            submitted_by = User(pk=userid),
            is_disabled = data["is_disabled"]
        )
        receivedDocument.save()
        return True

    def updateReceivedDocument(self, receiveddocumentid, data):
        toUpdate = ReceivedDocument.objects.filter(pk=int(receiveddocumentid))
        dbRecToUpdate = toUpdate.get()
        updateRecord_dic = {
            "memo": data["memo"] if data["memo"] else dbRecToUpdate.memo,
            "officeFrom": data["officeFrom"] if data["officeFrom"] else dbRecToUpdate.officeFrom,
            "dateReceived": data["dateReceived"] if data["dateReceived"] else dbRecToUpdate.dateReceived,
            "contactNumber": data["contactNumber"] if data["contactNumber"] else dbRecToUpdate.contactNumber,
            "contactName": data["contactName"] if data["contactName"] else dbRecToUpdate.contactName,
            "is_disabled": data["is_disabled"] if data["is_disabled"] else dbRecToUpdate.is_disabled
        }
        # Update edited record
        toUpdate.update(**updateRecord_dic)
        return True