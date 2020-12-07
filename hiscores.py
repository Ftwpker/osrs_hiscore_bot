#looked up the base url for user hiscores and all the options

from requests_html import HTMLSession
import time
import praw

def main():
    username = "zezima"
    hiscore_url = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1='
    #might be used down the line
    ironman_hiscore_url = 'https://secure.runescape.com/m=hiscore_oldschool_ironman/hiscorepersonal?user1='
    ultimateironman_hiscore_url = 'https://secure.runescape.com/m=hiscore_oldschool_ultimate/hiscorepersonal?user1='
    hardcoreironman_hiscore_url = 'https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/hiscorepersonal?user1='
    session = HTMLSession()
    hiscore_html = session.get(hiscore_url+username)
    stats_dict = generate_hiscore_dict(hiscore_html)
    post_to_reddit(stats_dict,username)

def generate_hiscore_dict(hiscore_html):
    stats_data = hiscore_html.html.find('div[id="contentHiscores"]',first=True)
    # print(stats_data.html)
    tr_list=stats_data.find('tr')
    stats_dict = {}
    for tr in tr_list:
        skill_name = tr.find('td[align="left"]',first=True)
        #skill level in this list
        td_right_list = tr.find('td[align="right"]')
        if skill_name:
            # print(skill_name)
            # print(td_right_list)
            #overall stat has one less td align right elements
            if skill_name.text == "Overall":
                stats_dict[skill_name.text] = td_right_list[1].text
            else:
                stats_dict[skill_name.text] = td_right_list[2].text
    print(stats_dict)
    return stats_dict

def post_to_reddit(stats_dict,username):

    # subreddit = reddit.subreddit('gadgets')
    # for subreddit in reddit.subreddits.default(limit=10):
    for i in range(1):
        subreddit=subreddit = reddit.subreddit("test")
        print ("subreddit: ", subreddit.title)
        submissions=subreddit.new(limit=1)
        for submission in submissions:
            print ("submission: ", submission.title)
            #how to create tables in Reddit
            #https://www.reddit.com/r/YouShouldKnow/comments/y37p6/ysk_how_to_make_a_table_on_reddit/
            #formating for next line for reddit (Uses markdown)
            #https://www.reddit.com/r/redditdev/comments/1h5u3a/praw_creating_multiline_comments/
            reply_text="Username | "+ username + "\n  :--|--: \n  "
            for key,value in stats_dict.items():
                reply_text+=key+" | "+ value + "\n  "
            print(reply_text)
            try:
                submission.reply(reply_text)
            except Exception as e:
                print ("Error in submitting reply: " + str(e))
    print ("finished")

if __name__ == "__main__":
    main()
