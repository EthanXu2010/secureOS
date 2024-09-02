import rumps
import subprocess
import requests
import json
import random
import time
import socket
import pyperclip
import os
import sys

if os.geteuid() != 0:
    print("This script requires sudo privileges.")
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)

# Helper functions
def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

def change_mac_address(interface):
    new_mac = f"02:00:00:{random.randint(0, 99):02x}:{random.randint(0, 99):02x}:{random.randint(0, 99):02x}"
    run_command(f"sudo ifconfig {interface} down")
    run_command(f"sudo ifconfig {interface} ether {new_mac}")
    run_command(f"sudo ifconfig {interface} up")

def change_ip(interface_name, new_ip=None):
    service_name = interface_name
    if new_ip:
        try:
            run_command(f"sudo networksetup -setmanual '{service_name}' {new_ip} 255.255.255.0 192.168.1.1")
        except Exception as e:
            print(f"Error changing IP: {e}")
    else:
        try:
            run_command(f"sudo networksetup -setdhcp '{service_name}'")
        except Exception as e:
            print(f"Error setting DHCP: {e}")

def toggle_ip(interface_name, action):
    service_name = interface_name
    try:
        if action == "down":
            run_command(f"sudo networksetup -setnetworkserviceenabled '{service_name}' off")
        else:
            run_command(f"sudo networksetup -setnetworkserviceenabled '{service_name}' on")
    except Exception as e:
        print(f"Error toggling IP: {e}")

def reset_network(interface):
    change_mac_address(interface)
    change_ip(interface)
    rumps.alert(f"Network reset on {interface}: MAC address and IP address changed.")

def toggle_ad_blocker(state):
    ad_domains = [
    "pagead2.googlesyndication.com",
    "adservice.google.com",
    "stats.g.doubleclick.net",
    "ad.doubleclick.net",
    "static.doubleclick.net",
    "m.doubleclick.net",
    "media.net",
    "static.media.net",
    "mediavisor.doubleclick.net",
    "adservetx.media.net",
    "google-analytics.com",
    "o2.mouseflow.com",
    "w1.luckyorange.com",
    "analytics.google.com",
    "click.googleanalytics.com",
    "api.luckyorange.com",
    "ssl.google-analytics.com",
    "cdn.luckyorange.com",
    "cdn.mouseflow.com",
    "browser.sentry-cdn.com",
    "cdn-test.mouseflow.com",
    "ads.linkedin.com",
    "analytics.pointdrive.linkedin.com",
    "extmaps-api.yandex.net",
    "appmetrica.yandex.ru",
    "trk.pinterest.com",
    "metrika.yandex.ru",
    "an.facebook.com",
    "ads.yahoo.com",
    "geo.yahoo.com",
    "udc.yahoo.com",
    "udcm.yahoo.com",
    "analytics.query.yahoo.com",
    "partnerads.ysm.yahoo.com",
    "log.fc.yahoo.com",
    "notify.bugsnag.com",
    "sessions.bugsnag.com",
    "adfstat.yandex.ru",
    "api.bugsnag.com",
    "offerwall.yandex.net",
    "adfox.yandex.ru",
    "app.bugsnag.com",
    "webview.unityads.unity3d.com",
    "pixel.facebook.com",
    "api.ad.xiaomi.com",
    "data.mistat.india.xiaomi.com",
    "data.mistat.rus.xiaomi.com",
    "metrics.data.hicloud.com",
    "ads.youtube.com",
    "iadsdk.apple.com",
        "pagead2.googlesyndication.com",
    "adservice.google.com",
    "stats.g.doubleclick.net",
    "ad.doubleclick.net",
    "static.doubleclick.net",
    "m.doubleclick.net",
    "media.net",
    "static.media.net",
    "mediavisor.doubleclick.net",
    "adservetx.media.net",
    "google-analytics.com",
    "o2.mouseflow.com",
    "w1.luckyorange.com",
    "analytics.google.com",
    "click.googleanalytics.com",
    "api.luckyorange.com",
    "ssl.google-analytics.com",
    "cdn.luckyorange.com",
    "cdn.mouseflow.com",
    "browser.sentry-cdn.com",
    "cdn-test.mouseflow.com",
    "ads.linkedin.com",
    "analytics.pointdrive.linkedin.com",
    "extmaps-api.yandex.net",
    "appmetrica.yandex.ru",
    "trk.pinterest.com",
    "metrika.yandex.ru",
    "an.facebook.com",
    "ads.yahoo.com",
    "geo.yahoo.com",
    "udc.yahoo.com",
    "udcm.yahoo.com",
    "analytics.query.yahoo.com",
    "partnerads.ysm.yahoo.com",
    "log.fc.yahoo.com",
    "notify.bugsnag.com",
    "sessions.bugsnag.com",
    "adfstat.yandex.ru",
    "api.bugsnag.com",
    "offerwall.yandex.net",
    "adfox.yandex.ru",
    "app.bugsnag.com",
    "webview.unityads.unity3d.com",
    "pixel.facebook.com",
    "api.ad.xiaomi.com",    
    "analytics.s3.amazonaws.com",
    "cs.luckyorange.net",
    "upload.luckyorange.net",
    "pagead2.googleadservices.com",
    "afs.googlesyndication.com",
    "adc3-launch.adcolony.com",
    "realtime.luckyorange.com",
    "wd.adcolony.com",
    "adserver.unityads.unity3d.com",
    "config.unityads.unity3d.com",
    "auction.unityads.unity3d.com",
    "log.pinterest.com",
    "ads.pinterest.com",
    "analytics.pinterest.com",
    "ads-api.twitter.com",
    "books-analytics-events.apple.com",
    "samsung-com.112.2o7.net",
    "api-adservices.apple.com",
    "weather-analytics-events.apple.com",
    "notes-analytics-events.apple.com",
    "freshmarketer.com",
    "settings.luckyorange.net",
    "smetrics.samsung.com",
    "luckyorange.com",
    "analytics.tiktok.com",
    "ads30.adcolony.com",
    "events3alt.adcolony.com",
    "mouseflow.com",
    "script.hotjar.com",
    "analyticsengine.s3.amazonaws.com",
    "advice-ads.s3.amazonaws.com",
    "static.ads-twitter.com",
    "insights.hotjar.com",
    "analytics.yahoo.com",
    "adtago.s3.amazonaws.com",
    "ads-api.tiktok.com",
    "ads.tiktok.com",
    "business-api.tiktok.com",
    "log.byteoversea.com",
    "analytics-sg.tiktok.com",
    "events.redditmedia.com",
    "stats.wp.com",
    "app.getsentry.com",
    "ads-sg.tiktok.com",
    "fwtracks.freshmarketer.com",
    "tools.mouseflow.com",
    "identify.hotjar.com",
    "adm.hotjar.com",
    "claritybt.freshmarketer.com",
    "iot-eu-logser.realme.com",
    "iot-logser.realme.com",
    "gemini.yahoo.com",
    "grs.hicloud.com",
    "surveys.hotjar.com",
    "logbak.hicloud.com",
    "metrics2.data.hicloud.com",
    "adx.ads.oppomobile.com",
    "adtech.yahooinc.com",
    "bdapi-ads.realmemobile.com",
    "data.ads.oppomobile.com",
    "ck.ads.oppomobile.com",
    "tracking.rus.miui.com",
    "analytics-api.samsunghealthcn.com",
    "logservice.hicloud.com",
    "sdkconfig.ad.intl.xiaomi.com",
    "sdkconfig.ad.xiaomi.com",
    "data.mistat.xiaomi.com",
    "bdapi-in-ads.realmemobile.com",
    "logservice1.hicloud.com",
    "adsfs.oppomobile.com",
    "samsungads.com",
    "careers.hotjar.com",
    "click.oneplus.cn",
    "data.mistat.india.xiaomi.com",
    "data.mistat.rus.xiaomi.com",
    "metrics.data.hicloud.com",
    "ads.youtube.com",
    "iadsdk.apple.com",
    "metrics.icloud.com",
    "metrics.mzstatic.com",
    "events.hotjar.io",
    "gtm.mouseflow.com",
    "open.oneplus.net",
    "api.mouseflow.com",
    "nmetrics.samsung.com",
    "metrics.icloud.com",
    "metrics.mzstatic.com",
    "events.hotjar.io",
    "gtm.mouseflow.com",
    "open.oneplus.net",
    "api.mouseflow.com",
    "nmetrics.samsung.com",
    "analytics.s3.amazonaws.com",
    "cs.luckyorange.net",
    "upload.luckyorange.net",
    "pagead2.googleadservices.com",
    "afs.googlesyndication.com",
    "adc3-launch.adcolony.com",
    "realtime.luckyorange.com",
    "wd.adcolony.com",
    "adserver.unityads.unity3d.com",
    "config.unityads.unity3d.com",
    "auction.unityads.unity3d.com",
    "log.pinterest.com",
    "ads.pinterest.com",
    "analytics.pinterest.com",
    "ads-api.twitter.com",
    "books-analytics-events.apple.com",
    "samsung-com.112.2o7.net",
    "api-adservices.apple.com",
    "weather-analytics-events.apple.com",
    "notes-analytics-events.apple.com",
    "freshmarketer.com",
    "settings.luckyorange.net",
    "smetrics.samsung.com",
    "luckyorange.com",
    "analytics.tiktok.com",
    "ads30.adcolony.com",
    "events3alt.adcolony.com",
    "mouseflow.com",
    "script.hotjar.com",
    "analyticsengine.s3.amazonaws.com",
    "advice-ads.s3.amazonaws.com",
    "static.ads-twitter.com",
    "insights.hotjar.com",
    "analytics.yahoo.com",
    "adtago.s3.amazonaws.com",
    "ads-api.tiktok.com",
    "ads.tiktok.com",
    "business-api.tiktok.com",
    "log.byteoversea.com",
    "analytics-sg.tiktok.com",
    "stats.wp.com",
    "app.getsentry.com",
    "ads-sg.tiktok.com",
    "fwtracks.freshmarketer.com",
    "tools.mouseflow.com",
    "identify.hotjar.com",
    "adm.hotjar.com",
    "claritybt.freshmarketer.com",
    "iot-eu-logser.realme.com",
    "iot-logser.realme.com",
    "gemini.yahoo.com",
    "grs.hicloud.com",
    "surveys.hotjar.com",
    "logbak.hicloud.com",
    "metrics2.data.hicloud.com",
    "adx.ads.oppomobile.com",
    "adtech.yahooinc.com",
    "bdapi-ads.realmemobile.com",
    "data.ads.oppomobile.com",
    "ck.ads.oppomobile.com",
    "tracking.rus.miui.com",
    "analytics-api.samsunghealthcn.com",
    "logservice.hicloud.com",
    "sdkconfig.ad.intl.xiaomi.com",
    "sdkconfig.ad.xiaomi.com",
    "data.mistat.xiaomi.com",
    "bdapi-in-ads.realmemobile.com",
    "logservice1.hicloud.com",
    "adsfs.oppomobile.com",
    "samsungads.com",
    "careers.hotjar.com",
    "click.oneplus.cn",
    ]

    if state == "enable":
        with open("/etc/hosts", "r+") as hosts_file:
            lines = hosts_file.readlines()
            hosts_file.seek(0)
            for line in lines:
                if not any(domain in line for domain in ad_domains):
                    hosts_file.write(line)
            # Now add the ad domains
            for domain in ad_domains:
                hosts_file.write(f"127.0.0.1 {domain}\n")
            hosts_file.truncate()
        rumps.alert("Ad Blocker Enabled")

    else:
        with open("/etc/hosts", "r") as hosts_file:
            lines = hosts_file.readlines()

        with open("/etc/hosts", "w") as hosts_file:
            for line in lines:
                if not any(domain in line for domain in ad_domains):
                    hosts_file.write(line)
        rumps.alert("Ad Blocker Disabled")

def is_connected():
    try:
        # Connect to the public Google DNS server to check internet connectivity
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# Generate a disposable email address using Guerrilla Mail
def generate_disposable_email():
    url = "https://api.guerrillamail.com/ajax.php"
    params = {
        "f": "get_email_address",
        "ip": "127.0.0.1",
        "agent": "Mozilla_foo_bar",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        email_data = response.json()
        email_address = email_data.get('email_addr', None)
        return email_address
    except requests.exceptions.RequestException as e:
        print(f"Failed to generate a disposable email: {e}")
        return None

# Check the inbox for any new emails using Guerrilla Mail
def check_inbox(email_address):
    url = "https://api.guerrillamail.com/ajax.php"
    params = {
        "f": "check_email",
        "email_user": email_address.split('@')[0],
        "agent": "Mozilla_foo_bar",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        # Check if the response content is empty
        if not response.content:
            print("Empty response received from the server.")
            return []

        inbox_data = response.json()  # Attempt to parse the response as JSON
        return inbox_data.get("list", [])
    except requests.exceptions.RequestException as e:
        print(f"Failed to check inbox: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")
        return []

# Main application class
class SecureOSApp(rumps.App):
    def __init__(self):
        super(SecureOSApp, self).__init__("SecureOS", icon=None, template=True)
        self.interface = "Wi-Fi"  # Change to your correct network interface name
        self.ad_blocker_enabled = False
        self.disposable_emails = []  # Store generated disposable emails
        self.menu = ["Toggle IP", "Change IP", "Change MAC Address", "Toggle Ad Blocker", "Generate Disposable Email", "Reset Network"]

    @rumps.clicked("Toggle IP")
    def toggle_ip(self, _):
        current_state = subprocess.check_output(f"networksetup -getnetworkserviceenabled '{self.interface}'", shell=True).decode().strip()
        if "Enabled" in current_state:
            toggle_ip(self.interface, "down")
            rumps.alert("IP Hidden")
        else:
            toggle_ip(self.interface, "up")
            rumps.alert("IP Visible")

    @rumps.clicked("Change IP")
    def change_ip(self, _):
        new_ip = f"192.168.1.{random.randint(2, 254)}"
        change_ip(self.interface, new_ip=new_ip)
        rumps.alert(f"IP changed to {new_ip} on {self.interface}")

    @rumps.clicked("Change MAC Address")
    def change_mac(self, _):
        run_command(f"sudo ifconfig {self.interface} down")
        run_command(f"sudo ifconfig {self.interface} up")
        time.sleep(1)
        change_mac_address(self.interface)
        rumps.alert(f"MAC address changed on {self.interface}")

    @rumps.clicked("Toggle Ad Blocker")
    def toggle_ad_blocker(self, _):
        if not self.ad_blocker_enabled:
            toggle_ad_blocker("enable")
            self.ad_blocker_enabled = True
        else:
            toggle_ad_blocker("disable")
            self.ad_blocker_enabled = False

    @rumps.clicked("Generate Disposable Email")
    def generate_email(self, _):
        email = generate_disposable_email()
        if email:
            self.disposable_emails.append(email)
            pyperclip.copy(email)  # Copy the email to the clipboard
            rumps.alert(f"Disposable Email: {email}\n(Email copied to clipboard!)")

            # Add the generated email to the menu for easy access
            email_item = rumps.MenuItem(email, callback=self.show_inbox)
            self.menu["Generate Disposable Email"].add(email_item)

    @rumps.clicked("Reset Network")
    def reset_network_settings(self, _):
        reset_network(self.interface)

    def show_inbox(self, sender):
        email = sender.title
        inbox = check_inbox(email)
        if inbox:
            inbox_contents = "\n\n".join([f"From: {msg['mail_from']}\nSubject: {msg['mail_subject']}\nDate: {msg['mail_date']}\n\n{msg['mail_excerpt']}" for msg in inbox])
            rumps.alert(f"Inbox for {email}", inbox_contents)
        else:
            rumps.alert(f"Inbox for {email}", "No new messages.")

if __name__ == "__main__":
    SecureOSApp().run()
