import requests
import cloudscraper
import json
import os
from urllib.parse import parse_qs, unquote
from colorama import *
from datetime import datetime
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class Boinkers:
    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'boink.boinkers.co',
            'Origin': 'https://boink.boinkers.co',
            'Pragma': 'no-cache',
            'Referer': 'https://boink.boinkers.co/upgrade-boinker',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Safari/537.36 Edg/128.0.0.0'
        }
        self.token_file = 'tokens.json'

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Boinkers - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<SHADOW SCRIPTER>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def extract_user_data(self, query: str) -> str:
        parsed_query = parse_qs(query)
        user_data = parsed_query.get('user', [None])[0]

        if user_data:
            user_json = json.loads(unquote(user_data))
            return str(user_json.get('first_name', 'Unknown'))
        return 'Unknown'

    def load_tokens(self):
        try:
            if not os.path.exists('tokens.json'):
                return {"accounts": []}

            with open('tokens.json', 'r') as file:
                data = json.load(file)
                if "accounts" not in data:
                    return {"accounts": []}
                return data
        except json.JSONDecodeError:
            return {"accounts": []}

    def save_tokens(self, tokens):
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file, indent=4)

    def generate_tokens(self, queries: list):
        tokens_data = self.load_tokens()
        accounts = tokens_data["accounts"]

        for idx, query in enumerate(queries):
            account_name = self.extract_user_data(query)

            existing_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)

            if not existing_account:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Token Is None{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Generating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)

                token = self.users_login(query)
                if token:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )
                    accounts.insert(idx, {"first_name": account_name, "token": token})
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Blocked By Cloudflare{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)

        self.save_tokens({"accounts": accounts})

    def renew_token(self, account_name):
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])
        
        account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        
        if account and "token" in account:
            token = account["token"]
            if not self.users_me(token):
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Token Isn't Valid{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Regenerating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)
                
                accounts = [acc for acc in accounts if acc["first_name"] != account_name]
                
                query = next((query for query in self.load_queries() if self.extract_user_data(query) == account_name), None)
                if query:
                    new_token = self.users_login(query)
                    if new_token:
                        accounts.append({"first_name": account_name, "token": new_token})
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Query Is Valid{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Blocked By Cloudflare{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Query Is None. Skipping {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
        
        self.save_tokens({"accounts": accounts})

    def load_queries(self):
        with open('query.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
        
    def load_liveOpId(self, retries=3):
        url = 'https://boink.boinkers.co/public/data/config?p=android'
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.json()['liveOps'][0]['_id']
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def users_login(self, query: str, retries=3):
        url = 'https://boink.boinkers.co/public/users/loginByTelegram?tgWebAppStartParam=boink1493482017&p=android'
        data = json.dumps({"initDataString":query, "sessionParams":{}})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, data=data, timeout=10)
                response.raise_for_status()
                return response.json()['token']
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def users_me(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/users/me?p=android'
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def claim_booster(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/boinkers/addShitBooster?p=android'
        data = json.dumps({'multiplier':2, 'optionNumber':1})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, data=data, timeout=10)
                if response.status_code == 403:
                    return False
                
                response.raise_for_status()
                return True
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def claim_inbox(self, token: str, message_id: str, retries=3):
        url = 'https://boink.boinkers.co/api/inboxMessages/claimInboxMessagePrize?p=android'
        data = json.dumps({'inboxMessageId':message_id})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, data=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def collect_friends(self, token: str, friend_id: str, retries=3):
        url = f'https://boink.boinkers.co/api/friends/claimFriendMoonBoinkerReward/{friend_id}?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, json=data, timeout=10)
                if response.status_code == 403:
                    return None
                
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def push_friends(self, token: str, friend_id: str, retries=3):
        url = f'https://boink.boinkers.co/api/friends/pushFriendToPlay/{friend_id}?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, json=data, timeout=10)
                if response.status_code == 403:
                    return None
                
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def tasks(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/rewardedActions/getRewardedActionList?p=android'
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def start_tasks(self, token: str, name_id: str, retries=3):
        url = f'https://boink.boinkers.co/api/rewardedActions/rewardedActionClicked/{name_id}?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, json=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def claim_tasks(self, token: str, name_id: str, retries=3):
        url = f'https://boink.boinkers.co/api/rewardedActions/claimRewardedAction/{name_id}?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, json=data, timeout=10)
                if response.status_code == 403:
                    return None
                    
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def watch_ads(self, token: str, key: str, retries=3):
        url = 'https://boink.boinkers.co/api/rewardedActions/ad-watched?p=android'
        data = json.dumps({'adsForSpins':False, 'providerId':key})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, data=data, timeout=10)
                response.raise_for_status()
                return True
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def spin_wheel(self, token: str, game_type: str, liveOpId: str, multiplier: str, retries=3):
        url = f'https://boink.boinkers.co/api/play/spin{game_type.capitalize()}/{multiplier}?p=android'
        data = json.dumps({'liveOpId':liveOpId} if id else {})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, data=data, timeout=10)
                if response.status_code == 403:
                    return None
                    
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
    
    def open_elevator(self, token: str, liveOpId: str, retries=3):
        url = 'https://boink.boinkers.co/api/play/openElevator?p=android'
        data = json.dumps({'liveOpId':liveOpId})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, data=data, timeout=10)
                if response.status_code == 403:
                    return None
                    
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def quit_elevator(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/play/quitAndCollect?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, json=data, timeout=10)
                if response.status_code == 403:
                    return None
                
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def upgrade_boinker(self, token: str, upgrade_type: str, retries=3):
        url = f'https://boink.boinkers.co/api/boinkers/{upgrade_type}?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, json=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
    
    def raffle_data(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/raffle/getRafflesData?p=android'
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def claim_raffle(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/raffle/claimTicketForUser?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=self.headers, json=data, timeout=10)
                if response.status_code == 403:
                    return None
                
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
    
    def question(self):
        while True:
            collect_friends = input("Auto Push & Collect Friends? [y/n] -> ").strip().lower()
            if collect_friends in ["y", "n"]:
                collect_friends = collect_friends == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to push & collect or 'n' to skip.{Style.RESET_ALL}")
        
        while True:
            complete_tasks = input("Auto Complete Tasks? [y/n] -> ").strip().lower()
            if complete_tasks in ["y", "n"]:
                complete_tasks = complete_tasks == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to complete or 'n' to skip.{Style.RESET_ALL}")
        
        return collect_friends, complete_tasks

    def process_query(self, query: str, liveOpId: str, collect_friends: bool, complete_tasks: bool):
        account_name = self.extract_user_data(query)
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])
        exist_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        if not exist_account:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}Token Not Found in tokens.json{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
            )
            return
        
        if exist_account and "token" in exist_account:
            token = exist_account["token"]

            user = self.users_me(token)
            if not user:
                self.renew_token(account_name)
                tokens_data = self.load_tokens()
                new_account = next((acc for acc in tokens_data["accounts"] if acc["first_name"] == account_name), None)
                
                if new_account and "token" in new_account:
                    new_token = new_account["token"] 
                    user = self.users_me(new_token)

            if user:
                gold = user.get('currencySoft', 0)
                shit = user.get('currencyCrypto', 0)
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['userName']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {gold} 🪙 {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT} -{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {shit:.4f} 💩 {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                time.sleep(1)

                claim_booster = self.claim_booster(new_token if 'new_token' in locals() else token)
                if claim_booster:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Boost Mining{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Boost Mining{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                inbox = user['inboxMessages']
                if inbox:
                    completed = False
                    for message in inbox:
                        message_id = message['_id']
                        status = message['state']

                        if message and status != "claimed":
                            claim_inbox = self.claim_inbox(new_token if 'new_token' in locals() else token, message_id)
                            if claim_inbox:
                                reward = claim_inbox['gottenPrize']['prizeValue']
                                reward_type = claim_inbox.get('gottenPrize', {}).get('prizeName', 'Gold')
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Inbox{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {message['title']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {reward} {reward_type} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Inbox{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {message['title']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                        else:
                            completed = True

                    if completed:
                        self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Inbox{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Clear {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Inbox{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} No Available Message {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                if collect_friends:
                    friends = user['friendsInvited']
                    if friends:
                        for friend in friends:
                            friend_id = friend['_id']

                            if friend is not None:
                                collect = self.collect_friends(new_token if 'new_token' in locals() else token, friend_id)
                                if collect and collect['invitedFriendsData']:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Friend{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {friend['userName']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {collect['energyReward']} Spin Energy {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Friend{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {friend['userName']} {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}No Availabe Reward to Claim{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                time.sleep(1)

                                push = self.push_friends(new_token if 'new_token' in locals() else token, friend_id)
                                if push and push['invitedFriendsData']:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Friend{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {friend['userName']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Pushed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Friend{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {friend['userName']} {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}Not Time to Push{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                time.sleep(1)

                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Friend{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} No Available Friend {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Friend{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Push & Collect Is Skipped {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)              

                if complete_tasks:
                    claimed_tasks = user['rewardedActions']
                    tasks = self.tasks(new_token if 'new_token' in locals() else token)
                    if tasks:
                        for task in tasks:
                            name_id = task['nameId']
                            reward = task['prizes'][0]['prizeValue']
                            reward_type = task['prizes'][0]['prizeTypeName']
                            task_type = task['type']
                            delay = task['secondsToAllowClaim']

                            if task_type == 'watch-ad':
                                start = self.start_tasks(new_token if 'new_token' in locals() else token, name_id)
                                if start:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                    for remaining in range(delay, 0, -1):
                                        print(
                                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                            f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT}Seconds to Claim Reward{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}   ",
                                            end="\r",
                                            flush=True
                                        )
                                        time.sleep(1)

                                    key = task['verification']['paramKey']
                                    self.watch_ads(new_token if 'new_token' in locals() else token, key)
                                    claim = self.claim_tasks(new_token if 'new_token' in locals() else token, name_id)
                                    if claim and claim['newUserRewardedAction']['claimDateTime']:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                            f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {reward} {reward_type} {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                            f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}            "
                                        )
                                    time.sleep(1)

                            else:
                                if name_id in claimed_tasks.keys():
                                    continue

                                if task_type == 'linkWithId' or delay == 172800:
                                    continue

                                start = self.start_tasks(new_token if 'new_token' in locals() else token, name_id)
                                if start:
                                    started = start.get('clickDateTime', None)
                                    claimed = start.get('claimDateTime', None)

                                    if started and not claimed:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                            f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                        for remaining in range(delay, 0, -1):
                                            print(
                                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                                f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT}Seconds to Claim Reward{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}   ",
                                                end="\r",
                                                flush=True
                                            )
                                            time.sleep(1)

                                        claim = self.claim_tasks(new_token if 'new_token' in locals() else token, name_id)
                                        if claim and claim['newUserRewardedAction']['claimDateTime']:
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                                f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {reward} {reward_type} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                                f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}            "
                                            )
                                        time.sleep(1)

                                    elif started and claimed:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                            f"{Fore.YELLOW + Style.BRIGHT}Is Already Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )

                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )

                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Completion is Skipped {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                games_energy = user['gamesEnergy']
                if games_energy:
                    multipliers = [500, 150, 100, 50, 25, 10, 5, 3, 2, 1]

                    for game_type, details in games_energy.items():
                        if game_type in ['slotMachine', 'wheelOfFortune']:
                            energy = details['energy']

                            while energy > 0:
                                spin = None

                                for multiplier in multipliers:
                                    if energy >= multiplier:
                                        spin = self.spin_wheel(new_token if 'new_token' in locals() else token, game_type, liveOpId, str(multiplier))
                                        if spin:
                                            energy = spin['userGameEnergy']['energy']
                                            reward = spin['prize']['prizeValue']
                                            reward_type = spin.get('prize', {}).get('prizeTypeName', 'Gae')
                                            get_type = reward_type
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}[ Spin Wheel{Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT} Type {game_type} {Style.RESET_ALL}"
                                                f"{Fore.GREEN+Style.BRIGHT}Is Success{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT} {reward} {get_type} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Energy{Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT} {energy} Left {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                            )
                                            break

                                        time.sleep(1)

                                if not spin:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Spin Wheel{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} Type {game_type} {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}No Available Energy{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                    break

                            if energy == 0:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Spin Wheel{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} Type {game_type} {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}No Available Energy{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            time.sleep(1)

                    free_spin = self.spin_wheel(new_token if 'new_token' in locals() else token, 'WheelOfFortune', liveOpId, '1')
                    if free_spin:
                        energy = free_spin['userGameEnergy']['energy']
                        reward = free_spin['prize']['prizeValue']
                        reward_type = free_spin.get('prize', {}).get('prizeTypeName', 'Gae')
                        get_type = reward_type

                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Spin Wheel{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} Type wheelOfFortune {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} Free {Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT}Is Success{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {reward} {get_type} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Spin Wheel{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} Type wheelOfFortune {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} Free {Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT}Not Available{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                    time.sleep(1)

                    while True:
                        open = self.open_elevator(new_token if 'new_token' in locals() else token, liveOpId)
                        if open:
                            reward = open['prize']['prizeValue']
                            reward_type = open['prize']['prizeTypeName']

                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Elevator{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} Is Opened {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Result{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} You Win {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {reward} {reward_type} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Elevator{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} No Available Attempt {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                            time.sleep(1)

                            self.quit_elevator(new_token if 'new_token' in locals() else token)

                            break

                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Spin Wheel{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"\
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                boinkers = user['boinkers']
                if boinkers:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Boinker{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {boinkers['currentBoinkerProgression']['id']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} Level {boinkers['currentBoinkerProgression']['level']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                    time.sleep(1)

                    upgrade_type = ['megaUpgradeBoinkers', 'upgradeBoinker']
                    while True:
                        for upgrade in upgrade_type:
                            upgrade_boinker = self.upgrade_boinker(new_token if 'new_token' in locals() else token, upgrade_type=upgrade)
                            
                            if upgrade_boinker:
                                id = upgrade_boinker['userBoinkers']['currentBoinkerProgression']['id']
                                level = upgrade_boinker['userBoinkers']['currentBoinkerProgression']['level']
                                
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Boinker{Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT} Is Upgraded {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {id} {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} - Level {level} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                                
                                if upgrade == 'megaUpgradeBoinkers':
                                    break

                            else:
                                if upgrade == 'megaUpgradeBoinkers':
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Boinker{Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT} Mega Upgrade Failed {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} Balance Not Enough {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Boinker{Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT} Isn't Upgraded {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} Balance Not Enough {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )

                                break
                            
                            time.sleep(1)

                        else:
                            continue

                        break

                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Boinker{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                raffle = self.raffle_data(new_token if 'new_token' in locals() else token)
                if raffle:
                    raffle_id = raffle.get('userRaffleData', {}).get('raffleId', None)
                    milestone = raffle.get('userRaffleData', {}).get('milestoneReached', 0)
                    ticket = raffle.get('userRaffleData', {}).get('tickets', 0)
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Raffle{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} ID {raffle_id} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Milestone{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {milestone} Reached {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {ticket} Ticket {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    time.sleep(1)

                    while True:
                        claim = self.claim_raffle(new_token if 'new_token' in locals() else token)
                        if claim:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Raffle{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} Ticket {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Milestone{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {claim['milestoneReached']} Reached {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {claim['tickets']} Ticket {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Raffle{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} Ticket {Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT}Not Available to Claim{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                            break
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Raffle{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
    
    def main(self):
        self.clear_terminal()
        try:
            queries = self.load_queries()
            self.generate_tokens(queries)

            collect_friends, complete_tasks = self.question()

            while True:
                liveOpId = self.load_liveOpId()
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    if query:
                        self.process_query(query, liveOpId, collect_friends, complete_tasks)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Boinkers - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = Boinkers()
    bot.main()