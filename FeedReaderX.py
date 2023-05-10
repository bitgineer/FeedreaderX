import asyncio
import feedparser
import discord

RSS_FEED_URL  = "https://unlimitedhangout.com/feed/"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/993283883682496662/6fTXOeseo_LkKEQ-_BpNph-TrKGaM12YJNa9eD2JVH_mHpdBFa0Q2nkrTlxj_pT2W-VD"

client = discord.Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())

async def check_feed():
    last_updated = None
    while True:
        feed = feedparser.parse(RSS_FEED_URL)
        if feed.status != 200:
            print(f"Error: Unable to access feed ({feed.status})")
            await asyncio.sleep(60)  # wait for 60 seconds before trying again
            continue
        
        if not last_updated:
            # set last_updated to the most recent entry in the feed
            last_updated = feed.entries[0].published_parsed
        else:
            # check if any new entries have been added to the feed
            for entry in feed.entries:
                entry_published = entry.published_parsed
                if entry_published > last_updated:
                    # send update to Discord
                    embed = discord.Embed(title=entry.title, url=entry.link, description=entry.summary)
                    await client.send(embed=embed)
                    # update last_updated to the latest entry
                    last_updated = entry_published
        
        await asyncio.sleep(60)  # wait for 60 seconds before checking the feed again

loop = asyncio.get_event_loop()
loop.create_task(check_feed())
loop.run_forever()