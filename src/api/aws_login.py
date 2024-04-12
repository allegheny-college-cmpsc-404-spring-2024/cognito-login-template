import os
import boto3
import base64
import hashlib
import hmac

from dotenv import load_dotenv
from cognitojwt import jwt_sync

class AWSLogin:

  def __init__(self, username: str = "", password: str = ""):
    load_dotenv()
    self.username = username
    self.password = password
    self.secret_hash = self.__generate_secret_hash()
    self.client = client = boto3.client(
      "cognito-idp",
      os.getenv("AWS_REGION")
    )

  def __generate_secret_hash(self) -> str:
    id = os.getenv("CLIENT_ID")
    key = os.getenv("CLIENT_SECRET").encode()
    msg = bytes(self.username + id, "utf-8")
    hashed = base64.b64encode(
      hmac.new(key, msg, digestmod=hashlib.sha256).digest()
    ).decode()
    return hashed

  def __reset_user_password(self) -> str:
    pass

  def do_login(self):
    auth_status = self.client.initiate_auth(
      AuthFlow = "USER_PASSWORD_AUTH",
      ClientId = os.getenv("CLIENT_ID"),
      AuthParameters = {
        "USERNAME": self.username,
        "PASSWORD": self.password,
        "SECRET_HASH": self.secret_hash
      }
    )

    #if "ChallengeName" in auth_status and auth_status["ChallengeName"] == "NEW_PASSWORD_REQUIRED":
    #  auth_status = reset_password(self.client, self.username, auth_status["Session"])
    print(auth_status)
    data = jwt_sync.decode(
      auth_status["AuthenticationResult"]["IdToken"],
      os.getenv("AWS_REGION"),
      os.getenv("AWS_POOL_ID")
    )

    print(data)
