from authentication.models import User
from .models import Order, Investment
import string
import random
import datetime
from django.utils import timezone
from account.models import Account
from django.db import transaction
from decimal import Decimal
from django.core.mail import EmailMessage


# Create your views here.
def generateOrderId(length=7):
    id = "".join(random.choice(string.digits) for _ in range(length))
    try:
        order = Order.objects.get(orderId=id)
        return generateOrderId()
    except Order.DoesNotExist:
        return id
    except Exception as e:
        return Exception(message=e)


def generateInvestmentId(length=7):
    id = "".join(random.choice(string.digits) for _ in range(length))
    try:
        order = Investment.objects.get(orderId=id)
        return generateInvestmentId()
    except Investment.DoesNotExist:
        return id
    except Exception as e:
        return Exception(message=e)


@transaction.atomic
def update_all_investment(userId):

    plans = {
        "starter": {"duration": 24, "min": 50, "roi": 0.2},
        "basic": {"duration": 48, "min": 500, "roi": 0.3},
        "silver": {"duration": 72, "min": 4000, "roi": 0.6},
        "gold": {"duration": 98, "min": 10000, "roi": 0.8},
        "estate": {"duration": 120, "min": 20000, "roi": 1},
    }
    now = timezone.now()

    try:
        account = Account.objects.get(user__id=userId)
        investment = Investment.objects.filter(user__id=userId, active=True)

        def update(inv):
            today = datetime.datetime.now()
            plan = inv.plan
            profit = inv.amount * Decimal(plans[plan]["roi"])
            nextProfitDate = inv.next_profit + datetime.timedelta(
                hours=plans[plan]["duration"]
            )
            inv.next_profit = nextProfitDate
            account.balance += profit
            account.total_earnings += profit
            if inv.next_profit <= today:
                return update(inv)
            inv.save()
            account.save()
            return True

        # loop through all investments and get which date is due
        for inv in investment:
            today = datetime.datetime.now()
            if inv.next_profit is not None and inv.next_profit <= today:
                update(inv=inv)

        return True
    except Exception as e:
        print(f"error updating transaction: {e}")


def createDepositFun(**data):
    orderId = generateOrderId()
    try:
        user = User.objects.get(id=data["id"])
        del data["id"]
        order = Order.objects.create(orderId=orderId, user=user, type="deposit", **data)
        return order.orderId
    except User.DoesNotExist:
        return "user does not exist"
    except Exception as e:
        return str(e)


@transaction.atomic
def createInvestFun(**data):
    try:
        orderId = generateInvestmentId()
        userId = data["id"]
        del data["id"]
        plans = {
            "starter": {"duration": 24, "min": 50, "roi": 0.2},
            "basic": {"duration": 48, "min": 500, "roi": 0.3},
            "silver": {"duration": 72, "min": 4000, "roi": 0.6},
            "gold": {"duration": 98, "min": 10000, "roi": 0.8},
            "estate": {"duration": 120, "min": 20000, "roi": 1},
        }
        amount = int(data["amount"])
        plan = data["plan"]

        if amount < plans[plan].get("min"):
            return {"status": False, "code": "please enter a valid amount"}

        user = User.objects.get(id=userId)
        order = Investment.objects.create(
            orderId=orderId, user=user, amount=amount, plan=plan
        )
            
        try:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"""
Dear {user.fullname},

Thank you for initiating an investment with us.

Transaction Details:
- Order ID: {order.orderId}
- Amount: ${order.amount:,.2f}
- Return on Investment (ROI): ${plans[order.plan].get('roi', 0) * order.amount:,.2f}
- Duration: Every {plans[order.plan].get('duration')} hours
- Date: {current_date}

Kindly make payment to the wallet address below (USDT TRC-20) and reply to this email with a screenshot of your payment:

Wallet Address: TNjKts9eymPyQbWXexrP2ZcHJ32pRYXF1U

Best regards,
Financial Growths
support@financial-growths.com
                """

            mail = EmailMessage()
            mail.subject = "Transaction Details - Financial Growths"
            mail.from_email = "Financial Growths<service@financial-growths.com>"
            mail.to = [user.email]
            mail.reply_to = ["support@financial-growths.com"]
            mail.body = message
            mail.send(fail_silently=False)
            print(f'transaction mail sent to {user.email}')
        except Exception as e:
            print('error_sending_investment_email', str(e))

        return {"status": True, "orderId": order.orderId}
    except User.DoesNotExist:
        return {"status": False, "code": "user does not exist"}
    except Exception as e:
        return {"status": False, "code": str(e)}


@transaction.atomic
def createWithdrawFun(**data):
    orderId = generateOrderId()
    userId = data["id"]
    del data["id"]
    try:
        user = User.objects.get(id=userId)
        account = Account.objects.get(user__id=userId)
        if account.balance < data["amount"]:
            return {"status": "failed", "code": "insufficient wallet balance"}
        account.pending_withdraw += data["amount"]
        account.save()
        order = Order.objects.create(
            orderId=orderId, user=user, type="withdraw", **data
        )
        return order.orderId
    except User.DoesNotExist:
        return {"status": "failed", "code": "user does not exist"}
    except Exception as e:
        return str(e)
