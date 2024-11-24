
from authentication.models import User
from.models import Account

# Create your views here.

def accountDetails(request, userId):

    try:
        pass
        # account = Account.objects.get(profile__id = userId)
        # serialized_account = accountSerialize(account)
        # return JsonResponse(serialized_account.data, safe=False)
    except Account.DoesNotExist:
        return {'status':'failed', 'code':'account_not_found'}
    except Exception as e:
        return {'status': 'failed', 'code': str(e)}
