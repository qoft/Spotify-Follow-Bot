import requests, random, string

class spotify:

    def __init__(self, profile= None):
        self.session = requests.Session()
        self.profile = profile
    
    def register_account(self):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.spotify.com/"
        }
        email = ("").join(random.choices(string.ascii_letters + string.digits, k = 8)) + "@gmail.com"
        data = f"birth_day=1&birth_month=01&birth_year=1970&collect_personal_info=undefined&creation_flow=&creation_point=https://www.spotify.com/uk/&displayname=qoftgenlol&email={email}&gender=neutral&iagree=1&key=a1e486e2729f46d6bb368d6b2bcda326&password=D8c7mc82chb4sdX2Q&password_repeat=D8c7mc82chb4sdX2Q&platform=www&referrer=&send-email=1&thirdpartyemail=0&fb=0"
        try:
            create = self.session.post(
                "https://spclient.wg.spotify.com/signup/public/v1/account",
                headers = headers,
                data = data
            )
            return create.json()['login_token']
        except:
            return None
        
    def get_csrf_token(self):
        try:
            r = self.session.get("https://www.spotify.com/uk/signup/?forward_url=https://accounts.spotify.com/en/status&sp_t_counter=1")
            return r.text.split('csrfToken":"')[1].split('"')[0]
        except:
            return None
        
    def get_token(self, login_token):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRF-Token": self.get_csrf_token(),
            "Host": "www.spotify.com"
        }
        self.session.post("https://www.spotify.com/api/signup/authenticate", headers = headers, data = "splot=" + login_token)
        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "app-platform": "WebPlayer",
            "Host": "open.spotify.com",
            "Referer": "https://open.spotify.com/"
        }
        try:
            r = self.session.get(
                "https://open.spotify.com/get_access_token?reason=transport&productType=web_player",
                headers = headers
            )
            return r.json()["accessToken"]
        except:
            return None

    def follow(self, sex = None):
        try:
            if "/user/" in self.profile:
                self.profile = self.profile.split("/user/")[1]
            if "?" in self.profile:
                self.profile = self.profile.split("?")[0]
            login_token = self.register_account()
            if login_token == None:
                return None
            auth_token = self.get_token(login_token)
            if auth_token == None:
                return None
            if sex:
                auth_token = sex
            headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "accept-language": "en",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "app-platform": "WebPlayer",
                "Referer": "https://open.spotify.com/",
                "spotify-app-version": "1.1.52.204.ge43bc405",
                "authorization": "Bearer {}".format(auth_token.replace("\n", "")),
            }
            try:
                d = self.session.put(
                    "https://api.spotify.com/v1/me/following?type=user&ids=" + self.profile,
                    headers = headers
                )
                return True
            except Exception as e:
                print(e)
                return False
        except Exception as e:
            print(e)
    def follow_playlist(self, id:str):
        login_token = self.register_account()
        if login_token == None:
            return None
        auth_token = self.get_token(login_token)
        if auth_token == None:
            return None
        headers = {
            "accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "app-platform": "WebPlayer",
            "Referer": "https://open.spotify.com/",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Content-Length": "758",
            "authorization": "Bearer {}".format(auth_token),
        }
        try:
            d = self.session.post(
                "https://spclient.wg.spotify.com/gabo-receiver-service/v3/events",
                headers = headers, 
                data = {
                    "suppress_persist":False,
                    "events":[
                        {
                            "sequence_id":"WLSxv+OyaJ3m6CNeqPP3CQ==",
                            "sequence_number":11,
                            "event_name":"KmInteraction",
                            "fragments":{
                                "context_sdk":{
                                "version_name":"2.2.0",
                                "type":"javascript"
                                },
                                "context_time":{
                                "timestamp":1649607621032
                                },
                                "context_client_id":{
                                "value":"2KXtlY0nTC6O5xfmpLCXHQ=="
                                },
                                "context_application":{
                                "version":"web-player_2022-04-09_1649503793238_e326937"
                                },
                                "context_user_agent":{
                                "value":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
                                },
                                "context_correlation_id":{
                                "value":"55037208-7927-45b0-afae-8605da6e1229"
                                },
                                "message":{
                                "page":"playlist",
                                "view_uri":f"/playlist/{id}",
                                "action_intent":"save",
                                "action_type":"click",
                                "target_uri":f"spotify:playlist:{id}",
                                "item_id":""
                                }
                            }
                        }
                    ]
                    }
            )
            print(d.status_code)
            return True
        except:
            return False
