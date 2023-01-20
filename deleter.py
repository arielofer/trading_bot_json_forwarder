from searcher import search_messages


def delete_messages(service, message):
    # messages_to_delete = search_messages(service, query)
    # it's possible to delete a single message with the delete API, like this:
    # service.users().messages().delete(userId='me', id=msg['id'])
    # but it's also possible to delete all the selected messages with
    # one query, batchDelete
    if messages_to_delete:
        print("[INFO]: deleting message")
        service.users().messages().trash(userId='me', id=message['id']).execute()
    else:
        print("[INFO]: no results - nothing to delete")
