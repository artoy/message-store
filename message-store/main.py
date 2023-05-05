import os

from slack_bolt import App

import db
import message

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
client = app.client

conn = None


@app.event("reaction_added")
def store_message(event, say):
    if event["reaction"] != "hozon":
        return

    # get reacted message
    response = client.conversations_history(channel=event["item"]["channel"], latest=event["item"]["ts"], limit=1)
    messages = response["messages"]
    if len(messages) > 0:
        m = message.Message(event["item"]["channel"], messages[0]["user"], messages[0]["text"], messages[0]["ts"])

        # insert to DB
        try:
            db.insert_message(conn, m)
            say("This message is stored successfully!")
        except Exception as e:
            say("Error: " + str(e))
    else:
        say("Error: the reacted message is not found")


if __name__ == "__main__":
    conn = db.setup()
    app.start(port=int(os.environ.get("PORT", 3000)))
    db.close(conn)
