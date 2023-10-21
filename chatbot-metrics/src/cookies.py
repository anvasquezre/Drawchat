import extra_streamlit_components as stx
from src.settings import settings
import jwt
def get_manager():
    return stx.CookieManager()

def validate_token(token):
    try:
        secret = settings.login.SECRET
        decoded_token = jwt.decode(token, secret, algorithms=["HS512"])
        roles = decoded_token['auth'].split(',')
        name = decoded_token['fn']
        if "ROLE_ADMIN" in roles or "ROLE_CUSTOMER_SATISFACTION" in roles:
            isAuth = True
        else:
            isAuth = False
        return isAuth , name
    except Exception as e:
        print("Not Authenticated", e)
        isAuth = False
        return isAuth , None
