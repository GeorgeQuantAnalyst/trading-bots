import datetime
import http.client
import json
import logging
import sys
from datetime import datetime, timedelta


class EquityLevelTraderBotCapitalAuthHelper:

    def __init__(self, config: dict):
        self.capital_api_config = config["capitalApi"]

    def get_authorization_token(self):
        logging.debug("Get authorization token")
        now = datetime.now()

        if hasattr(self, "_cached_token") and hasattr(self, "_token_expiry") and now.time() < self._token_expiry:
            logging.debug("Authorization token return from cache...")
            return self._cached_token
        else:
            logging.debug("Get new authorization token, because token expire or not exist in cache.")
            token_expire_minutes = self.capital_api_config["TokenExpireMinutes"]
            self._cached_token = self._get_new_authorization_token()
            self._token_expiry = (datetime.now() + timedelta(minutes=token_expire_minutes)).time()

        return self._cached_token

    def _get_new_authorization_token(self):
        try:
            conn = http.client.HTTPSConnection(self.capital_api_config["url"])
            payload = json.dumps({
                "identifier": self.capital_api_config["username"],
                "password": self.capital_api_config["password"]
            })
            headers = {
                'X-CAP-API-KEY': self.capital_api_config["apiKey"],
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/api/v1/session", payload, headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))

            logging.debug(f"Response get_new_authorization_token: {data}")
            if res.status != 200:
                raise Exception(f"HTTP Error {res.status}: {res.reason}")

            authorization_token = {
                "X-SECURITY-TOKEN": res.getheader("X-SECURITY-TOKEN"),
                "CST": res.getheader("CST")
            }
            account_id = self._parse_account_id(data, self.capital_api_config["subAccountName"])
            self._switch_to_sub_account(account_id, authorization_token)

            return authorization_token
        except Exception as e:
            logging.error(f"Failed call POST method /api/v1/session on capital.com REST api: {str(e)}")
            sys.exit(-1)

    def _switch_to_sub_account(self, account_id: int, authorization_token: dict):
        try:
            logging.debug(f"Switch to account: {account_id}")
            conn = http.client.HTTPSConnection(self.capital_api_config["url"])
            payload = json.dumps({
                "accountId": account_id
            })
            headers = {
                'X-SECURITY-TOKEN': authorization_token["X-SECURITY-TOKEN"],
                'CST': authorization_token["CST"],
                'Content-Type': 'application/json'
            }
            conn.request("PUT", "/api/v1/session", payload, headers)
            res = conn.getresponse()
            data = res.read()
            logging.debug(f"Response switch_to_sub_account: {data.decode('utf-8')}")

            if res.status != 200:
                raise Exception(f"HTTP Error {res.status}: {res.reason}")

        except Exception as e:
            logging.error(f"Failed call PUT method /api/v1/session on capital.com REST api: {str(e)}")
            sys.exit(-1)

    @staticmethod
    def _parse_account_id(create_session_response, account_name):
        result = [x["accountId"] for x in create_session_response["accounts"] if x["accountName"] == account_name]
        return result[0] if len(result) > 0 else None
