from datetime import datetime, timezone

async def get_data(browser, url):
    """
        <div class="d-none daybox" data-available="0" data-day="06/13/2022"
            data-generaladmission="false" data-totalavailable="24">

    """
    FORMAT = '%m/%d/%Y %H:%M %p'

    print("getting page")
    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle2')

    events = [] 
    for i in range(3):
        if i > 0:
            datepicker = await page.querySelector(".datepicker")
            elem = await datepicker.querySelector(".next")
            await elem.click()

        cal = await page.querySelector("#calendar-dp") 
        days = await cal.querySelectorAll(".daybox")
        for day in days:
            date = await page.evaluate('(element) => element.getAttribute("data-day")', day)
            times = await day.querySelectorAll(".calendar-time")

            for time in times:
                time_input = await time.querySelector("input[type='submit']")
                t = await page.evaluate('(element) => element.getAttribute("value")', time_input)
                dt = datetime.strptime(f"{date} {t}", FORMAT)
                dt = dt.replace(tzinfo=timezone.utc)
                events.append(
                    dt,
                )

    return events
