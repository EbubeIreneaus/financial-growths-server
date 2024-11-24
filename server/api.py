from typing import List
import json
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from ninja.security import APIKeyHeader
from account.models import Account
from authentication.views import Register, Login, updateFullname, verifyOTPCode, send_otp_code
from order.models import Investment, Order
from order.views import createDepositFun, createInvestFun, createWithdrawFun, update_all_investment
from utils.classes import (
    CreateInvestScheme,
    InvestmentOut,
    LoginUserIntake,
    UserIntake,
    OrderOut,
    UserInfo,
    NotFoundError,
    AccountInfo,
    CreateDepositScheme,
    CreateWithdrawScheme,
    ErrorSchema
)
from authentication.models import User
from django.utils import timezone


class AuthRequest(APIKeyHeader):
    param_name = "X-API-Key"
    
    def authenticate(self, request, userId):
        try:
            user = User.objects.get(id=userId)
            return user.id
        except User.DoesNotExist:
            raise Exception({'status':False, 'code': 'user not found'})
        except Exception as e:
            raise Exception({'status': False, 'code': str(e)})
        

api = NinjaAPI()




@api.post("/auth/signup")
def newUser(request, payload: UserIntake):
    user = Register(**payload.dict())
    return user


@api.post("/auth/signin")
def authUser(request, payload: LoginUserIntake):
    user = Login(**payload.dict())
    return user

@api.get("/auth/getAcct")
def get_account_link_with_email(request, email: str):
    """Get Account userid want to authorize access to account without password"""
    try:
        user = User.objects.get(email=email)
        return {'status': 'success', 'userId': user.id}
    except User.DoesNotExist:
        return {'status': 'failed', 'code': "user with this email not found"}
    except Exception as e:
        return {'status': 'failed', 'code': str(e)}


@api.get("/requestOTP")
def sendOTP(request, id: str, label: str):
    """REQUEST OTP CODE"""
    requestOTP = send_otp_code(id=id, label=label)
    return {"status": "reached", "code": requestOTP}


@api.get("/verifyOTP")
def verifyOTP(request, id: str, otp: int):
    """verify User OTP code"""
    res = verifyOTPCode(id=id, otp=otp)
    return res


@api.get("/userInfo", response={200: UserInfo})
def userInfo(request, id: str):
    user = get_object_or_404(User, id=id)
    return user


@api.get("/accountInfo", auth=AuthRequest(), response={200: AccountInfo, 500: ErrorSchema})
def accountInfo(request):
    """Get Account Details"""
    try:
        userId = request.auth
        account = Account.objects.get(user__id=userId)
        print(account)
        return 200, account
    except Exception as e:
        return 500, {'status': False, 'code': str(e)}


@api.post("/order/deposit")
def createDeposit(request, payload: CreateDepositScheme):
    req = createDepositFun(**payload.dict())
    return req


@api.post("/order/withdraw")
def createWithdraw(request, payload: CreateWithdrawScheme):
    req = createWithdrawFun(**payload.dict())
    return req

@api.post("/order/invest")
def createInvest(request, payload: CreateInvestScheme):
    req = createInvestFun(**payload.dict())
    return req

@api.get("/order", response=List[OrderOut])
def get_orders(request, id: str):
    req = Order.objects.filter(user__id=id)
    return req


@api.get("/update/fullname")
def editName(request, id: str, name: str):
    req = updateFullname(id, name)
    return req

@api.get("/update/password")
def editPassword(request, id: str, psw: str):
    try:
        user = User.objects.get(id=id)
        user.set_password(psw)
        user.save()
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'failed', 'code': str(e)}

@api.get("/order/active", response=List[InvestmentOut])
def getActiveInvestment(request, id: str):
    """Get all active investment"""
    try:
        update_all_investment(userId=id)
        req = Investment.objects.filter(user__id=id, active=True)
        return req
    except Exception as e:
        return str(e)
