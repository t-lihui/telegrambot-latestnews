import telebot

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

from constants import *
bot = telebot.TeleBot(API_KEY)

my_url = 'https://www.straitstimes.com/container/custom-landing-page/breaking-news'

# message to send back user
latest_news = ''
#global variables
top5titles = []
top5time = []

def retrieve_data(my_url):
    #opening up connection, grabbing the content in page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    #parse the html, makes it neater
    page_soup = soup(page_html, "html.parser")

    #collects the all of the latest news story header
    story_title = page_soup.find_all("h3", {"class":"story-title"})
    top5titles = story_title[0:5]

    #collects the time of all the latest news story header
    story_time = page_soup.find_all("div", {"class":"node-postdate"})
    top5time = story_time[0:5]

    return top5titles, top5time

def compiling_message(top5titles, top5time, boolean):
    latest_news = ''
    # runs a loop for the latest 5 news articles released in website
    for index, information in enumerate(top5titles):
        title = information.a.contents[0]
        partial_link = information.a["href"]
        full_link = 'https://www.straitstimes.com{}'.format(partial_link)
        # add time released
        timereleased = top5time[index]

        if boolean == 1 and index == 0:
            latest_news += "Latest article released: {} \n ".format(timereleased["data-lapsevalue"])
            # #add to the message
            latest_news += "\n" + title
            latest_news += "\n" + full_link + "\n"
            break 

        else:
            latest_news += "\n{}. {}".format(index+1, timereleased["data-lapsevalue"])

        # #add to the message
        latest_news += "\n" + title
        latest_news += "\n" + full_link + "\n"

    return latest_news

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Welcome to TheStraitsTimes_LatestNews bot.\
    \n\nUse the command /latest_news to view the 5 most recent articles released by The Straits Times.\
    \n\nIf you want only the latest news article, use /latest_article.")

@bot.message_handler(commands=['latest_news'])
def start(message):
    bot.send_message(message.chat.id, "Hold on.....currently consolidating articles!")
    top5titles, top5time = retrieve_data(my_url)
    latest_news = compiling_message(top5titles, top5time, 0)
    bot.send_message(message.chat.id, 'Thank you for waiting, here is a list of of articles as requested.')
    bot.send_message(message.chat.id, latest_news)

@bot.message_handler(commands=['latest_article'])
def start(message):
    bot.send_message(message.chat.id, "Hold on.....it might take awhile")
    top5titles, top5time = retrieve_data(my_url)
    latest_news = compiling_message(top5titles, top5time, 1)
    bot.send_message(message.chat.id, 'Thank you for waiting!')
    bot.send_message(message.chat.id, latest_news)

bot.polling()
