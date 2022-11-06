import discum
import json
import schedule
import os


def handler(bot, file):
    data = json.load(file)
    bot.triggerSlashCommand(appID, channelID, guildID, data)
    print("Job completed successfully")


def work(bot):
    global WORKING
    if WORKING:
        data = json.load(open('commands/claim.json'))
    else:
        data = json.load(open('commands/work.json'))
    bot.triggerSlashCommand(appID, channelID, guildID, data)
    WORKING = not WORKING
    print("Job completed successfully")


if __name__ == '__main__':
    # Setup
    print("Started....")
    guildID = os.getenv('guildID')
    channelID = os.getenv('channelID')
    appID = os.getenv('appID')
    TOKEN = os.getenv('TOKEN')
    WORKING = False

    # Create Self Bot
    bot = discum.Client(token=TOKEN, log=False)

    # Claims Daily
    schedule.every().day.at("21:28").do(
        handler, bot=bot, file=open('commands/daily.json'))

    # Work and claim hourly
    schedule.every(1).hour.do(work, bot=bot)

    while True:

        schedule.run_pending()
