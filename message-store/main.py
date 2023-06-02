import os

from slack_bolt import App

import db
import message

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
client = app.client


# store a message
@app.event("reaction_added")
def store_message(event, say):
    if event["reaction"] != os.environ.get("REACTION"):
        return

    # get reacted message
    response = client.conversations_history(channel=event["item"]["channel"], inclusive=True,
                                            latest=event["item"]["ts"],
                                            oldest=event["item"]["ts"], limit=1)
    messages = response["messages"]
    if len(messages) > 0:
        m = message.Message(event["item"]["channel"], messages[0]["user"], messages[0]["text"], messages[0]["ts"])

        # insert to DB
        try:
            db.insert_message(pool, m)
            say(f"The message '{messages[0]['text']}' is stored successfully!")
        except Exception as e:
            say("Error: " + str(e))
    else:
        say("Error: the reacted message is not found")


# response all messages
@app.event("app_mention")
def get_all_messages(event, say):
    print(event["text"])
    if event["text"] != os.environ.get("MENTION"):
        return

    # get all messages
    messages = db.get_all_messages(pool)

    # response all messages
    if len(messages) > 0:
        for m in messages:
            say(f"Channel: {m.channel_id}, User: {m.user}, Text: {m.text}, Timestamp: {m.timestamp}")
    else:
        say("Error: no message is found")


if __name__ == "__main__":
    pool = db.setup()
    try:
        app.start(port=int(os.environ.get("PORT", 3000)))
    finally:
        db.close()
