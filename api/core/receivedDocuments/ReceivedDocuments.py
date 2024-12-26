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
                "submitted_by": self.users.getAuthUserById(request, lang, receivedDocument.submitted_by),
                # is_disabled = models.BooleanField(default=False)
                # created = models.DateTimeField(auto_now_add=True)
            }
            results.append(receivedDocument_item)
        return results
    def ReceivedDocumentExists(self, receivedDocumentid):
        return ReceivedDocument.objects.filter(pk=receivedDocumentid).exists()
    
    def getReceivedDocumentById(self, request, lang, receivedDocumentid):
        receivedDocument = ReceivedDocument.objects.filter(pk=receivedDocumentid)
        return {
            "id": receivedDocument.pk,
            "memo": receivedDocument.memo,
            "officeFrom": receivedDocument.officeFrom,
            "dateReceived": receivedDocument.dateReceived,
            "contactName": receivedDocument.contactName,
            "contactNumber": receivedDocument.contactNumber,
            "submitted_by": self.users.getAuthUserById(request, lang, receivedDocument.submitted_by),
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
            submitted_by = userid,
            is_disabled = data["is_disabled"]
        )
        receivedDocument.save()
        return True