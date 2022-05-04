"""
Copy to config.py and adjust for your needs.
"""

# Name of your server as it appears on the website, e.g. Kadan
target_server = ''
# webhook URL for the Discord channel you want to send to
webhook_url = ''

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
