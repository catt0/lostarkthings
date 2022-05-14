"""
Copy to config.py and adjust for your needs.
"""

# Name of your server as it appears on the website, e.g. Kadan
target_server = ''
# webhook URLs for the Discord channels you want to send to
# messages are send to all channels in this list
webhook_urls = [

]
# Migration notice:
# the old config key webhook_url is still supported, messages will be send to webhook_url as well
# you should move to webhook_urls

up_message = '@everyone The server is now up (probably) :)'
down_message = 'The server is now down :('

# website that is polled
target = "https://www.playlostark.com/en-us/support/server-status"
# user agent to send
fakeagent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
# short delay between queries, used when the server is down
looptimer = 5 # seconds
# long delay between queries, used when the server is up
looptimer_long = 60
# how many times the server must be detected as "down" to switch from the "up" to the "down" state
confirmations_needed = 10
