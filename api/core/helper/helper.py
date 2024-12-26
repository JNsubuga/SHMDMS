import random
import math
import hashlib
import json
import socket
from django.core.validators import validate_email
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.authtoken.models import Token


class Helper:
    def getRandom(self):
        return math.ceil(random.random() * 1000000)
    
    def getAuthToken(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header:
            if len(auth_header.split()) == 2:
                token = auth_header.split()[1]
                if Token.objects.filter(key=token).exists():
                    return {
                        "token": token,
                        "message": "Incomplete data request!!!",
                        "status": True,
                    }
                else:
                    return {
                        "token": None,
                        "message": "Invalid Authentication credentials",
                        "status": False,
                    }
            else:
                return {
                    "token": None,
                    "message": "Invalid Authentication credentials",
                    "status": False,
                }
        else:
            return {
                "token": None,
                "message": "Authentication credentials were not provided.",
                "status": False,
            }

    def passwordEncrypt(self, password):
        return hashlib.sha256(str(password).encode("utf-8")).hexdigest()

    def generateCodeName(self, word):
        return word.lower().replace(" ", "_")

    def calculateTimePast(self, starttime, endtime):
        start_time = datetime.strptime(starttime, "%H:%M:%S")
        end_time = datetime.strptime(endtime, "%H:%M:%S")
        delta = end_time - start_time
        sec = delta.total_seconds()
        min = sec / 60
        # get difference in hours
        hours = sec / (60 * 60)
        return {"seconds": sec, "minutes": min, "hours": hours}

    def convertToDate(self, dateString):
        splited_date = dateString.strip().split("-")
        year = int(splited_date[0])
        month = int(splited_date[1])
        days = int(splited_date[2])
        return datetime.date(year, month, days)

    def is_number(self, s):
        try:
            float(s)  # for int, long and float
        except ValueError:
            try:
                complex(s)  # for complex
            except ValueError:
                return False
        return True

    def isEqual(self, f1, f2):
        f1 = float(f1)
        f2 = float(f2)
        ans1 = f1 - f2
        ans2 = f2 - f1
        return ans1 == ans2

    def compareDates(self, startdate, enddate):
        # 2022-04-28
        now = self.getCurrentDate()
        delta = enddate[0] - now
        hours_left = delta.days if delta.days else 0
        minutes = hours_left * 60
        # months = self.months_between(now, enddate[0]) if self.months_between(now, enddate[0]) else 0
        return {
            "is_expired": now > enddate[0],
            "is_equal": (startdate == enddate),
            "is_greater_than": startdate > enddate,
            "is_less_than": startdate < enddate,
            "minutes_left": minutes,
            "days_left": hours_left,
            "months_left": 0,
            "years_left": 0,
        }

    def months_between(self, date1, date2):
        if date1 > date2:
            date1, date2 = date2, date1
        m1 = date1.year * 12 + date1.month
        m2 = date2.year * 12 + date2.month
        months = m2 - m1
        if date1.day > date2.day:
            months -= 1
        elif date1.day == date2.day:
            seconds1 = date1.hour * 3600 + date1.minute + date1.second
            seconds2 = date2.hour * 3600 + date2.minute + date2.second
            if seconds1 > seconds2:
                months -= 1
        return months

    def getNextYear(self):
        today = self.getCurrentDate()
        return datetime.date(today.year + 1, today.month, today.day)

    def isEmailValid(self, email):
        valid_email = False
        try:
            validate_email(email)
            valid_email = True
        except:
            valid_email = False
        return valid_email

    def parseJson(self, request):
        return json.loads(request.decode("utf-8"))

    def getCurrentDate(self):
        return datetime.date.today()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(("10.255.255.255", 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    def getCurrentDateString(self):
        return str(datetime.date.today())

    def getDateTime(self):
        return timezone.datetime.now()

    def calculateTimePast(self, starttime, endtime):
        start_time = datetime.strptime(starttime, "%H:%M:%S")
        end_time = datetime.strptime(endtime, "%H:%M:%S")
        delta = end_time - start_time
        sec = delta.total_seconds()
        min = sec / 60
        # get difference in hours
        hours = sec / (60 * 60)
        return {"seconds": sec, "minutes": min, "hours": hours}

    def empty(self, text):
        return not str(text)

    def vistor_ip_address(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
