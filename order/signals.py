from decimal import Decimal
import logging
from django.forms import model_to_dict
from account.models import Account
from django.db import transaction
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.core.mail import EmailMessage

from authentication.models import User


def handle_order_signal(old_data, new_data):
    old_status, new_status = (old_data["status"], new_data["status"])
    userId = new_data["user"]
    orderId = new_data["orderId"]
    amount = new_data["amount"]
    type = new_data["type"]
    try:
        account = Account.objects.get(user__id=userId)

        if old_status == new_status:
            print("status did not change")
            return True

        if new_status == "approved":
            # if type is deposit
            if type == "deposit":
                return True
                account.balance += amount
                account.last_deposit = amount
                account.save()

            # if type is withdraw
            if type == "withdraw":
                account.balance -= amount
                account.pending_withdraw -= amount
                account.total_withdrawal += amount
                account.save()

                try:
                    message = f"""
Dear {account.user.fullname},

Your withdrawal with ID {orderId} has been approved.

${amount:,.2f} have been credited to your wallet, {new_data['channel']}:- {new_data['wallet']}

Thank you for trusting us with your investment.

Best regards,  
Financial Growths
support@financia-growths.com
                            """

                    mail = EmailMessage()
                    mail.subject = "Withdrawal Approved - Financial Growths"
                    mail.from_email = "Financial Growths<service@financia-growths.com>"
                    mail.to = [account.user.email]
                    mail.reply_to = ["support@financia-growths.com"]
                    mail.body = message
                    mail.send(fail_silently=False)
                    print(f"Withdrawal approved mail sent to {account.user.email}")
                except Exception as e:
                    print("error_sending_withdrawal_approved_email", str(e))

        if new_status == "declined":
            # remove from pending withdraw if type if withdraw
            if type == "withdraw":
                account.pending_withdraw -= amount
                account.save()

    except Exception as e:
        print(f"error signaling order presave: {str(e)}")


@transaction.atomic
def handle_investment_signal(old_data, instance):
    new_data = model_to_dict(instance)
    old_status = old_data["active"]
    new_status = new_data["active"]

    userId = new_data["user"]
    amount = new_data["amount"]
    investId = new_data["id"]

    if old_status == new_status:
        print("status did not change")
        return True

    plans = {
        "starter": {"duration": 24, "min": 50},
        "basic": {"duration": 48, "min": 500},
        "silver": {"duration": 72, "min": 4000},
        "gold": {"duration": 98, "min": 10000},
        "estate": {"duration": 120, "min": 20000},
    }

    try:
        account = Account.objects.get(user__id=userId)

        if new_status:
            if instance.next_profit is not None:
                return False

            nextProfit = datetime.now() + timedelta(
                hours=plans[instance.plan]["duration"]
            )
            # instance.active = True
            instance.next_profit = nextProfit
            account.active_investment += amount
            instance.save()
            account.save()

            # check refferal, is first investment and reward refferal
            if instance.user.ref_by and not instance.user.has_made_investment:
                try:
                    user = User.objects.get(id=userId)
                    ref_id = user.ref_by.id
                    refAccount = Account.objects.get(user__id=ref_id)
                    refAccount.affliate_commision += Decimal(
                        0.1 * float(instance.amount)
                    )
                    refAccount.balance += Decimal(
                        0.1 * float(instance.amount)
                    )
                    user.has_made_investment = True
                    refAccount.save()
                    user.save()
                    
                except Exception as e:
                    print("Error updating refferal bonus", str(e))

            try:

                message = f"""
Dear { account.user.fullname },

Your investment with ID {instance.orderId} has been activated.

Thank you for trusting us with your investment.

Best regards,  
Financial Growths
support@financia-growths.com
                        """

                mail = EmailMessage()
                mail.subject = "Investment Approved - Financial Growths"
                mail.from_email = "Financial Growths<service@financia-growths.com>"
                mail.to = [account.user.email]
                mail.reply_to = ["support@financia-growths.com"]
                mail.body = message
                mail.send(fail_silently=False)
                print(f"investment approved mail sent to {account.user.email}")
            except Exception as e:
                print("error_sending_investment_approved_email", str(e))

        else:
            account.active_investment -= amount
            account.save()

    except Exception as e:
        print(f"error signaling order presave: {str(e)}")
