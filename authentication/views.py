from django.contrib.auth import authenticate
from .models import User
from account.models import Account
from uuid import uuid4
from django.core.mail import EmailMultiAlternatives, EmailMessage
from utils.random import OTP
import datetime
from django.utils.timezone import make_aware
from django.db import transaction

# Create your views here.


def send_otp_code(id, label: str):
    otp_code = OTP(6)
    otp_valid_till = datetime.datetime.now() + datetime.timedelta(hours=24)

    try:
        user = User.objects.get(id=id)
        email = user.email
        user.OTP = otp_code
        user.OTP_VALID_TILL = otp_valid_till
        user.save()

        mail = EmailMessage()
        mail.to = [email]
        mail.from_email = "Financial Growths<service@financia-growths.com>"
        mail.subject = label
        mail.body = f"""
Dear {user.fullname}, \n
Your One-Time Password (OTP) is: {user.OTP} \n
This code is valid for the next 24 hours. \n
For your security, do not share this code with anyone. If you didn’t request this code, please contact our support team immediately.
Thank you, \n
Financial Growths \n
support@financia-growths.com
        """
        mail.send()
        print("mail success")
        return "200"
    except User.DoesNotExist:
        return "404"
    except Exception as e:
        print(str(e))
        return '500'


@transaction.atomic
def Register(**data):
    try:
        email = data["email"]
        user = User.objects.get(email=email)
        return {"status": False, "code": "Email Already Exist"}

    except User.DoesNotExist:
        refId = data['refId']
        del data['refId']
        user = User(**data)
        user.id = uuid4()
        user.set_password(data["password"])
        print(refId)
        if refId is not None:
            try:
                ref = User.objects.get(id=refId)
                user.ref_by = ref
            except: 
                pass
        user.save()
        Account.objects.create(user=user)
        send_verify_email = send_otp_code(
            id=user.id, label="Financial Growths Account Verification"
        )
        return {"status": True, "userId": user.id}

    except Exception as e:
        print(f"Error Msg {e}")
        return {"status": False, "code": str(e)}


def Login(**data):
    email = data["email"]
    try:
        user = authenticate(email=email, password=data["password"])

        if user is None:
            return {"status": "failed", "code": "No user found"}

        if not user.is_verified:
            send_verify_otp = send_otp_code(
                id=user.id, label="Account Verification"
            )
            return {"status": "unverified", "userId": user.id}

        return {"status": "success", "userId": user.id}
    except Exception as e:

        print(f"Error Msg {e}")
        return {"status": "failed", "code": "Unknown Server Error"}


def verifyOTPCode(id, otp):
    try:
        user = User.objects.get(id=id)
        otp_code = user.OTP
        otp_date = user.OTP_VALID_TILL
        today = datetime.datetime.now()
        if otp_code != otp:
            return {"status": False, "code": "Invalid OTP code"}
        if today >= otp_date:
            return {
                "status": False,
                "code": "Elapsed time please request a new code",
            }
        # if user.ref_by is not None:
        #     try:
        #         commision = 10
        #         ref = user.ref_by.id
        #         refAcct = Account.objects.get(user__id = ref)
        #         refAcct.affliate_commision += commision
        #         refAcct.balance += commision
        #         refAcct.save()
        #     except:
        #         pass
        user.OTP = None
        user.OTP_VALID_TILL = None
        user.is_verified = True
        user.save()
        return {"status": True}
    except User.DoesNotExist:
        return {"status": False, "code": "No such user found"}
    except Exception as e:
        return {"status": False, "code": str(e)}


def updateFullname(id, name):
    try:
        user = User.objects.get(id=id)
        user.fullname = name
        user.save()
        return {"status": "success", "name": user.fullname}
    except User.DoesNotExist:
        return {"status": "failed", "code": "user not found"}
    except Exception as e:
        return {"status": "failed", "code": str(e)}
