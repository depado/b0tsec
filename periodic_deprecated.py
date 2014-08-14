# -*- coding: utf-8 -*-

@periodic_task(60)
def tasked():
    """
    A periodic task that retrieves the json of the intrepid bbs website.
    """
    data = urllib.request.urlopen('https://tools.intrepid-linux.info/bbs/json').read().decode("utf-8")
    thread_dict = json.loads(data)
    try:
        saved_dict = pickle.load(open("thread_dict.p", "rb"))
        if thread_dict['thread_number'] != saved_dict['thread_number']:
            diff = thread_dict['thread_number']-saved_dict['thread_number']
            if diff > 1:
                message = "{} New Threads on the BBS".format(diff)
            else:
                message = "One New Thread on the BBS : {}".format(thread_dict['threads'][str(thread_dict['thread_number'])]['url'])
            serv.privmsg(chan, message)
            pickle.dump(thread_dict, open("thread_dict.p", "wb"))

        if thread_dict['comment_number'] != saved_dict['comment_number']:
            for new_id in thread_dict['threads'].keys():
                for saved_id in saved_dict['threads'].keys():
                    if new_id == saved_id:
                        unique_id = new_id
                        diff = thread_dict['threads'][unique_id]['comments'] - saved_dict['threads'][unique_id]['comments']
                        if diff == 1:
                            m_bit = "One New Comment"
                        elif diff > 1:
                            m_bit = "{} New Comments".format(diff)
                        else:
                            continue
                        serv.privmsg(chan, "{} on Thread {}".format(m_bit, thread_dict['threads'][unique_id]['url']))
            pickle.dump(thread_dict, open("thread_dict.p", "wb"))
    except FileNotFoundError:
        pickle.dump(thread_dict, open("thread_dict.p", "wb"))
tasked()