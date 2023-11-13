from firebase_admin import messaging

def send_to_topic(topic):
    message = messaging.Message(
        notification= messaging.Notification(
            title="Title",
            body="Body"
        ),
        topic=topic
    )

    response = messaging.send(message)

    print("Successfully sent message", response)

send_to_topic("all_users")