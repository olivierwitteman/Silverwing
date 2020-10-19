from slackclient import SlackClient

slack_token = '/////'
sc = SlackClient(slack_token)

for _ in range(1):
  sc.api_call(
    "chat.postMessage",
    channel="silverdinner",
    text="Can I join too?"
  )

