import facebook
import requests
import re

atoken = "YOUR_AUTHENTICATION_TOKEN"
page_id = "YOUR_PAGE_ID"

# Connecting to Facebook's Graph API
graph = facebook.GraphAPI(access_token=atoken, version="2.12")

# simple regex expression to search for emails in conversations
regex = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# dictionary containing data of last 25 conversations and paging info
conv = graph.get_object('me/conversations')

# number of elements in paging element
# paging can have 3 elements:
# cursors
# next
# prev
# if it doesn't have prev - it is the first page
# if it doesn't have next - it is the last page of messages
paging_len_prev = conv['paging'].__len__()
paging_len_now = 3

# page number
it = 1

f = open("YOUR_FILE_NAME.txt", "w")
while True:
    print("Going through page number: ", it)
    for el in conv['data']:
        # for every conversation, get all messages from this person
        allmessagesfromconv = graph.get_object(el['id'], fields='messages')
        # get the number of messages
        msg_count = graph.get_object(el['id'], fields='message_count')
        # you can use msg_count to iterate over all messages
        # for my purpouse i iterated over only the first page of messages(?)

        # from senders field, you can get the full name and the default facebook email of the person
        participants = graph.get_object(el['id'], fields='senders')
        try:
            for msg in allmessagesfromconv['messages']['data']:
                # single message sent
                singlemess = graph.get_object(msg['id'], fields='message')['message']
                # searching for the regular expression
                result = re.search(regex, singlemess)
                if result:
                    # printing and writing found email to file
                    print(result[0])
                    f.write(result[0])
                    f.write(', ')
                    # and the name of the sender
                    if participants['senders']['data'][0]['name'] == 'Janusz Walentukiewicz - ubezpieczenia':
                        # you can also print the name of the sender
                        # print(participants['senders']['data'][1]['name'])
                        f.write(participants['senders']['data'][1]['name'] + '\n')
                    else:
                        # print(participants['senders']['data'][0]['name'])
                        f.write(participants['senders']['data'][0]['name'] + '\n')
        except:
            # some people blocked me and it broke my script
            # so simple try, except fixed the problem
            print("This person probably blocked you")
            pass

    # if the previous page had fewer elements
    # it means that there are another pages
    if (paging_len_prev <= paging_len_now):
        paging_len_prev = conv['paging'].__len__()
        conv = requests.get(conv['paging']['next']).json()
        paging_len_now = conv['paging'].__len__()
        it += 1
    else:
        print("Finished going through all messages")
        loop_is_working = 0
        break
f.close()
