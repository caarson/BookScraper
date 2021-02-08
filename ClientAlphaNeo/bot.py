# import the bot
import main
import time

# declare needed classes
browser1 = main.start_api(firefox=True, chrome=False, proxy=False, user_agent=True, recache=False)
WebHandler1 = main.WebHandler(browser_passthrough=browser1)

# use WebHandler class to navigate around.
WebHandler1.load_site()
WebHandler1.login(username="AlphaNeo", password="mo1mo2mo3")
#WebHandler1.check_balance(cost_per_chapter=4)

book_information = WebHandler1.get_book_information(use_input_url=False, url="https://activetranslations.xyz/vip/")  # sample url: https://activetranslations.xyz/vip/
scrapped_data = WebHandler1.scrape_book(url="https://activetranslations.xyz/vip/", number_of_chapters=10, book_information=book_information)  # sample url: https://activetranslations.xyz/vip/
WebHandler1.create_book(use_inputs=False, book_data=book_information, scrape_data=scrapped_data, language_for_book="en")


