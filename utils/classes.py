from typing import Optional
from ninja import Schema

class NotFoundError(Schema):
    message: str
    
class LoginUserIntake(Schema):
    email: str
    password: str
# Shemas
class UserIntake(Schema):
    fullname: str
    country: str
    phone: str
    email: str
    password: str
    refId: str | None


class UserInfo(Schema):
    fullname: str
    email: str
    id: None | str
    ref_by: Optional['UserInfo'] = None

# Resolving the forward reference
UserInfo.update_forward_refs()
    


class AccountInfo(Schema):
    user: UserInfo
    balance: float
    active_investment: float
    total_withdrawal: float
    total_earnings: float
    affliate_commision: float

class CreateDepositScheme(Schema):
    id: str
    amount: int
    channel: str

class CreateWithdrawScheme(Schema):
    id: str
    amount: int
    channel: str
    wallet: str

class CreateInvestScheme(Schema):
    id: str
    amount: int
    plan: str


class OrderOut(Schema):
    orderId: str
    type: str
    status: str
    amount: int
    channel: str | None

class InvestmentOut(Schema):
    orderId: str
    plan: str
    active: bool
    amount: int
    
class ErrorSchema(Schema):
    status: bool
    code: str