from slackclient import SlackClient

slack_token = 'xoxp-393387664416-394034945139-520496789715-1ed9777320aa3a0d3b56cb67a1e7edf5'
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="Ruben Forkink",
  text=":ralph:"
)