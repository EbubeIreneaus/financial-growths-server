import string
import random
def OTP(len):
    digits = '123456789'
    id = "".join(random.choice(digits) for _ in range(len))
    return id