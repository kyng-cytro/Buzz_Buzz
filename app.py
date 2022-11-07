import discum
import json
import schedule
import os


def handler(bot):
    data = json.load(open('commands/daily.json'))
    bot.triggerSlashCommand(appID, channelID, guildID, data)
    print("Job completed successfully")


def work(bot):
    data = json.load(open('commands/work.json'))
    bot.triggerSlashCommand(appID, channelID, guildID, data)
    print("Job completed successfully")


if __name__ == '__main__':
    # Setup
    print("Started....")
    guildID = os.getenv('guildID')
    channelID = os.getenv('channelID')
    appID = os.getenv('appID')
    TOKEN = os.getenv('TOKEN')

    # Create Self Bot
    bot = discum.Client(token=TOKEN, log=False)

    # Claims Daily
    schedule.every().day.at("21:28").do(
        handler, bot=bot)

    # Work and claim hourly
    schedule.every(1).hour.do(work, bot=bot)

    while True:

        schedule.run_pending()
