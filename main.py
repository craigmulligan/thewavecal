import asyncio
from wavecal import get_data

from datetime import timedelta
from pyppeteer import launch
from ics import Calendar, Event

async def main():
    host = "https://bookings.thewave.com/twb_b2c/" 
    browser = await launch(headless=False, args=['--no-sandbox'])
    event_types = [
            {"name": "Expert Barrels", "description": "A whole session dedicated to our most popular barrel setting. Powerful waves with consistent, fun to navigate barrels", "path": "genericevent.html?event=TWB.EVN17"},
            {"name": "Expert Turns", "description": "A fast and challenging session, full of our most powerful turning waves, to test your performance turns", "path": "genericevent.html?event=TWB.EVN10" },
            {"name": "Advanced Surf Plus", "description": "A full faced wave on take off, which holds good shape and size all the way down the line. Its inside barrel section is easy to pre-empt and stays open with a fun, open face to manoeuvre.", "path": "lessonpool.html"},
            {"name": "Advance Surf", "description": "A range of open-faced waves, both right and left.", "path": "advanced.html"}
    ]

    cal = Calendar()

    for event_type in event_types:
        for start in await get_data(browser, host + event_type['path']):
            end = start + timedelta(hours=1)
            
            cal.events.add(
                Event(name=event_type["name"], begin=start, end=end, description=event_type['description'])
            )


    print(f"generated {len(cal.events)} events")
    with open('thewavecal.ics', 'w') as f:
        f.write(str(cal))

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
