# *confidential*confidential*confidential*confidential*confidential*confidential*confidential* #
# # - Coded by Carson Alexander Rhodes for AlphaNeo - Confidential ~ !!!NOT TO BE SOLD OR REDISTRIBUTED!!!
# # - Intellectual Property - Confidential - NOT TO BE SOLD OR REDISTRIBUTED
# *confidential*confidential*confidential*confidential*confidential*confidential*confidential* #
import urllib.request

# variable used for google handling which is not relevant for this project:
user_database = {}

# important essential libraries:
import os, time, random

# import ebook epub:
from ebooklib import epub

# import selenium & associated methods:
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
import user_agent as UserAgent
from user_agents import parse

###################################################
# declare browser
###################################################
browser = ""

###################################################
# proxies
###################################################
''' class abandoned
class ProxyUtility:
    def __init__(self):
        self.proxy_ip = ""
    def return_proxy_ip(self):
        return self.proxy_ip

ProxyUtility = ProxyUtility()
def zip_proxy_extension():

    # Get project directory
    project_directory = os.path.abspath(os.curdir)
    extension_directory = project_directory + "/proxy/"

    # Create zipped extension
    ## Read in your extension files
    file_names = os.listdir(extension_directory)
    file_dict = {}
    for fn in file_names:
        with open(os.path.join(extension_directory, fn), 'r') as infile:
            file_dict[fn] = infile.read()

    ## Save files to zipped archive
    with zipfile.ZipFile("proxy.zip", 'w') as zippedfile:
        for fn, content in file_dict.items():
            zippedfile.writestr(fn, content)
'''


def get_ip(browser):
    browser.get("http://www.whatsmyip.org/")
    ip = browser.find_element_by_xpath("//span[@id='ip']")
    WebDriverWait(browser, 10).until(EC.visibility_of(ip))
    print("the current ip: " + ip.text)


###################################################
# mobile emulation
###################################################
mobile_emulation = {

    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},

    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}


###################################################
# browser
###################################################
def start_api(firefox, chrome, proxy, user_agent, recache):  # start call for the api

    # startup script
    print("@ ItsLit Records LLC -- This API is built for ItsLit Records LLC")
    print("Redistribution of this API startup is not allowed unless explicit permission from ItsLit Records LLC.")
    print("yvngbull crhodee - All Rights Reserved")
    print("Supports: Chrome, more coming soon...\n\n")

    #############
    # user options
    #############

    # load configuration
    config_file = open("config.txt", "r")
    contents = config_file.read()
    contents = contents.split('"')

    mobile_emulation = contents[1]
    proxy_ip = contents[3]
    fire_fox = contents[5]
    driver_path = contents[7]
    random_user_agent = contents[9]

    ###############
    ###############
    def get_random_user_agent():
        print("\nfetching a random user agent...")

        def fetch_user_agents():
            print("now fetching a cache / list of user agents...")
            try:
                time.sleep(1)
                useragent = UserAgent.generate_user_agent(os=None, navigator=None, platform=None, device_type=None)
                print("printing user cache: " + str(useragent))

                return useragent  # return the user_agent

            except Exception as exception:
                print("unable to load user cache!\n" + str(exception))

        # parse user agent information
        def user_agent_parser(useragent):
            #### print "user_agent" type:
            print("\nparsing the user_agent info...")

            print("user_agent being passed to parser: " + str(useragent))
            # parse user agent information.
            try:
                print("parsing user agent...")
                parsed_user_agent = parse(useragent)
            except Exception as exception:
                print("failed to parse user_agent!" + str(exception))
                exit()

            user_agent_version = parsed_user_agent.browser.version_string

            return user_agent_version, parsed_user_agent, useragent

        ##########
        # find the correct user agent with right version.
        # check the fetched user agents

        count_of_user_agents_tested = 0
        user_agent_found = False
        # count_of_tries = 0

        print("checking user agents...")
        while not user_agent_found:  # while false
            count_of_user_agents_tested = count_of_user_agents_tested + 1

            # fetch the user_agents
            print("fetching the user_agents...")
            try:
                user_agent = fetch_user_agents()  # retrieves UA list
                print("\nuseragents retrieved: \n" + str(user_agent) + "\nprinting type: " + str(type(user_agent)))

            except Exception as exception:
                print("there was an issue fetching the user_agents!\n" + str(exception))
                exit()

            print(user_agent)

            useragent_info = user_agent_parser(
                useragent=user_agent)  # returns user_agent_version, parsed_user_agent, user_agent

            print("user agent info: \n" + str(useragent_info) + "\n")
            print("version: " + useragent_info[0])

            # count_of_tries = count_of_tries + 1

            # if count_of_tries == 20:
            #    exit()

            # check if user_agent is equal to a version defined below.
            if int(useragent_info[1].browser.version_string.split(".")[0]) > 60:
                user_agent_found = True

        try:  # if unable to find user_agent
            print("\nuseragent: " + str(useragent_info[0]) + "\nNew Version: " + str(useragent_info[2]))

            return useragent_info
        except Exception as exception:
            print("unable to fetch user agent, try again.\n" + str(exception))

    ##############################

    random_useragent = get_random_user_agent()  # recache is a bool
    print("\n" + "random useragent identified!:\n" + str(random_useragent) + str(type(random_useragent)) + "\n")

    print("now seperating the variables inside of random_useragent")
    fetched_user_agent = random_useragent[2]

    # declare needed imported classes
    chrome_options = Options()

    if mobile_emulation != "False":
        print("launching with mobile emulation enabled...")
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    if proxy_ip == "":
        print("no proxy_ip! \ncheck config.")
        exit()

    ####
    # launch browser:
    ####

    ####
    # if proxy is disabled, launch browser without proxy:
    if proxy == False:

        # launch firefox:
        if firefox == True:
            try:
                print("no proxy enabled -- relaunching with capabilities disabled.")
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", fetched_user_agent)

                browser = webdriver.Firefox(firefox_profile=profile, executable_path=driver_path + "/geckodriver")

                return (browser)  # return browser for global use

            except Exception as exception:
                print("unable to launch browser!")
                print(" ")
                print("error:")
                print(exception)

        # launch chrome:
        if chrome == True:
            try:
                print("no proxy enabled -- relaunching with capabilities disabled.")
                chrome_options.add_argument(f'user-agent={user_agent}')
                browser = webdriver.Chrome(chrome_options=chrome_options,
                                           executable_path=driver_path + '/chromedriver')  # replace or switch browser, should be compatible with every browser

                return (browser)  # return browser for global use
            except ValueError:
                browser = webdriver.Chrome(
                    executable_path=driver_path + '/chromedriver')  # replace or switch browser, should be compatible with every browser

                return (browser)  # return browser for global use

            except Exception as exception:
                print("unable to launch browser!")
                print(" ")
                print("error:")
                print(exception)

    ####
    # if proxy is enabled, launch browser with proxy:
    if proxy == True:

        # launch firefox with proxy
        if firefox == True:
            print("proxy enabled -- launching with proxy")
            try:
                proxy_ip = proxy_ip
                print("connecting to: " + proxy_ip)
                firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
                firefox_capabilities['marionette'] = True

                firefox_capabilities['proxy'] = {
                    "proxyType": "MANUAL",
                    "httpProxy": proxy_ip,
                    "ftpProxy": proxy_ip,
                    "sslProxy": proxy_ip
                }

                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", fetched_user_agent)

                browser = webdriver.Firefox(firefox_profile=profile, capabilities=firefox_capabilities,
                                            executable_path=driver_path + "/geckodriver")

                get_ip(browser)

                return browser
            except Exception as exception:
                print("unable to bind proxy...")
                print(exception)

        # launch chrome with proxy (unfinished statement)
        if chrome == True:
            print("no proxy launch enabled for chrome yet. \ncheck at a later time.")
            exit()


class WebHandler:
    def __init__(self, browser_passthrough):
        self.browser = browser_passthrough

    def load_site(self):
        print("Loading site data...")
        url = "https://activetranslations.xyz/"

        self.browser.get(url)

        # now find the logo and wait until it has finished loading into the webpage:
        loaded_elem = WebDriverWait(self.browser, 10).until(lambda x: x.find_element_by_xpath(
            "//header/div[@id='header-grid']/nav[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/div[1]/p[1]"))

    def login(self, username, password):
        print("Logging in...")
        self.browser.find_element_by_xpath(
            xpath="//header/div[@id='header-grid']/nav[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ul[1]/li[3]/a[1]").click()

        # wait until the login button on the page is visible.
        loaded_elem = WebDriverWait(self.browser, 10).until(lambda x: x.find_element_by_xpath(
            "//header/div[@id='header-grid']/nav[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/div[1]/p[1]"))

        # send username and password:
        username_input_box = self.browser.find_element_by_xpath(xpath="//input[@id='username']").send_keys(username)
        time.sleep(random.randint(a=1, b=4))  # short wait
        password_input_box = self.browser.find_element_by_xpath(xpath="//input[@id='password']").send_keys(password)

        # wait:
        time.sleep(random.randint(a=2, b=5))

        # click login:
        login_button = self.browser.find_element_by_xpath(
            xpath="//body/div[1]/main[1]/main[1]/div[1]/article[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/form[1]/div[1]/div[1]/p[3]/input[3]").click()

    def check_balance(self, cost_per_chapter):
        print("Checking balance...")
        url = "https://activetranslations.xyz/account/"

        self.browser.get(url)

        balance = self.browser.find_element_by_xpath(xpath="//div[@class='myCRED-balance mycred_default']")
        print("\ncurrent balance: \n$" + str(balance.text) + "\n")

        total_chapters = int(balance.text) / cost_per_chapter
        print("You may purchase a total of: " + str(total_chapters) + " chapters.")

    def prompt(self):
        print("Do you wish to proceed? \n(Y/N)")
        user_input = input()
        if user_input.upper() == "N":
            exit()
        else:
            pass

    def get_book_information(self, use_input_url, url):
        print("Getting book information...")
        # Get URL for the book:
        if use_input_url == True:
            print("What's the URL of the book?: \n")
            url_for_book = input()  # sample url : https://activetranslations.xyz/vip/a-vip-as-soon-as-you-log-in-28/

            # Check for validity:
            if "activetranslations.xyz" in url_for_book:
                print("url is valid, proceeding...\n")
            else:
                print("enter a URL from 'activetranslations.xyz'")
                exit()
        else:
            url_for_book = url

        # if a string exists in URL proceed with opening that link
        if isinstance(url, str):
            ############
            # open new tab get url:
            self.browser.get(url_for_book)

            # wait:
            time.sleep(random.randint(a=2, b=5))

        ############
        # Get book name & chapter

        header_of_tab = self.browser.title

        book_information = header_of_tab.split("\u2013")  # split name by character "-"
        cut_pos = len(book_information[0])

        book_name = book_information[0][:cut_pos - 1]  # book name is [0], chapter number and name should be [1]

        ############
        # Get author and novel cover:

        # new tab
        body = self.browser.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 't')

        # open novelupdates
        self.browser.get("https://www.novelupdates.com/")

        # wait until search is visible - click it.
        load = WebDriverWait(self.browser, 10).until(
            lambda x: self.browser.find_element_by_xpath("//body/div[2]/div[1]/div[2]/div[1]/span[1]/span[4]"))
        self.browser.find_element_by_xpath("//body/div[2]/div[1]/div[2]/div[1]/span[1]/span[4]").click()

        # click the search button, enter the name of the novel exactly as passed and enter query:
        self.browser.find_element_by_xpath("//input[@placeholder='Search...']").send_keys(book_name, Keys.RETURN)

        # wait until results are visible.
        load = WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_xpath(
            "//body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]"))

        ####### 
        # find book:
        base_xpath = "//body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div["  # increments by 2 (move one down by adding 2)

        # variables being declared:
        number = 0
        count_over = False
        book_found = False
        ######

        # load the results before proceeding
        load = WebDriverWait(self.browser, 10).until(
            lambda x: self.browser.find_element_by_xpath("//body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]"))
        time.sleep(2)
        ##########

        while book_found == False:
            # non-static variables for the loop:
            number = number + 2
            current_row = base_xpath + str(number) + "]"
            #########

            # search for results/rows, if there are no more, terminate the while loop and continue code.
            if count_over == False:
                try:
                    self.browser.find_element_by_xpath(current_row)

                except Exception as error:
                    print(
                        "The maximum number of books has been reached or the program was unable to fetch anymore. \n" + str(
                            error))
                    count_over = True

            # search each individual row for the title
            try:
                title_from_result = self.browser.find_element_by_xpath(current_row + "/div[2]/div[1]/a[1]")

            except Exception as error:
                print("Could not retrieve the book's title! \nMaybe there are no results?\n" + str(error))
                exit()

            # compare book name and title from result and see if there's a match:
            try:
                if title_from_result.text.lower() == book_name.lower():
                    book_found = True

            except:
                pass

        # open book from results page
        try:
            title_from_result.click()

        except Exception as error:
            print("Unable to open book!" + str(error))

        # load the results before proceeding
        load = WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_xpath(
            "//body/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/img[1]"))

        ############
        # get novel cover and save the img source file:
        try:
            novel_cover = self.browser.find_element_by_xpath(
                "//body/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/img[1]")
            novel_cover_img_url = novel_cover.get_attribute("src")

        except Exception as error:
            print("There was an error! \n" + str(error))

        ############
        # fetch authors
        try:
            authors = self.browser.find_element_by_xpath("//div[@id='showauthors']").text
        except Exception as error:
            print("There was an error getting the authors! \n" + str(error))

        ##########
        # return the gathered information:
        return book_name, novel_cover_img_url, authors

    def scrape_book(self, url, number_of_chapters, book_information):
        print("Scraping book data...")

        # variables + lists:
        number = 0
        max_chapter = False
        books_chapters_text = []  # contains the book's chapter's content, all of the chapters are returned.

        # while loop to get all the chapters:
        while max_chapter == False:
            ##########
            # fetch URL
            self.browser.get(url)

            # Wait for the page to load before continuing:
            time.sleep(random.randint(1, 10))

            # re-assign xpath to a new number and continue until each chapter has been completely read or the max chapter has been reached.
            number = number + 1
            xpath = "//div[1]/div[1]/div[1]/div[1]/div[" + str(number) + "]/div[1]/a[1]"

            # Find chapter box
            chapter = self.browser.find_element_by_xpath(xpath)

            # open the link associated with the box:
            cut_pos = len(book_information[0])
            chapter_information = chapter.text.split("Chapter")[0][:cut_pos]

            # open the link associated with the box:
            if book_information[0].lower() == chapter.text.split("Chapter")[0][
                                              :cut_pos].lower():  # statement compares strings to ensure that it is not clicking active translation's logo
                # get the link for the chapter:
                chapter_link = chapter.get_attribute("href")

                # get the chapter's page:
                self.browser.get(chapter_link)

                # Wait for the page to load before continuing:
                time.sleep(random.randint(1, 10))

                # cycle through them and click and download the content on the chapter's page:
                text_on_page = self.browser.find_element_by_xpath("//div[@class='row']")  # get the text

                # now convert this to a text object:
                text_for_chapter = text_on_page.text
                books_chapters_text.append(text_for_chapter)

            # terminate loop and collection if the number_of_chapters variable is reached:
            if number_of_chapters == number:
                max_chapter = True

        return books_chapters_text

    def create_book(self, use_inputs, book_data, scrape_data, language_for_book):
        print("Creating book...")

        # create book object
        book = epub.EpubBook()

        if use_inputs == True:
            # Get name for book from user
            print("What's the name of the book?: \n")
            name_for_book = input()

            # Get ID for book from user
            print("What's the ID of the book?: \n")
            id_for_book = input()

            # Get language for book from user
            print("What's the language of the book?: \n")
            language_for_book = input()

            # Get author for book from user
            print("What's the author of the book?: \n")
            author_for_book = input()
        else:  # set locale and
            book_cover = book_data[1]
            book_name = book_data[0]
            book_author = book_data[2]

        # set project directory:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        #####
        # convert the url to an image file and save it in ClientAlphaNeo/bookcovers:
        full_file_name_for_cover = os.path.join(ROOT_DIR, "bookcovers", book_name + ".png")

        # send http request and get the image and save it:
        urllib.request.urlretrieve(book_cover, full_file_name_for_cover)

        book = epub.EpubBook()

        book.set_title(str(book_name))
        book.set_identifier("NA12345")
        book.set_language(str(language_for_book))
        book.add_author(str(book_author))

        # This ASSUMES cover is PNG. Extension must be correct because content type will be guessed
        # according to the extension.

        # This will put file at EPUB/cover.png location. If you used 'images/cover.png' it would be
        # placed in EPUB/images/cover.png location. The 2nd thing is what you want. You want
        # to put all images in images/ .css files in style/ and etc.

        # This first argument is location inside of EPUB file, not where it is on the disk.
        book.set_cover(book_name + '.png', open(full_file_name_for_cover, 'rb').read())

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

        # add CSS file
        book.add_item(nav_css)

        # I ASSUME here that scrape_data is something like ['content of chapter 1', 'content of chapter 2']
        chapters_local = scrape_data

        # Initialize variables for the loop:
        number = 0

        # cycle through chapters:
        spine = ['nav']
        toc = []

        for content in chapters_local:
            number = number + 1

            # create chapter objects:
            chapter = epub.EpubHtml(
                title=book_name,
                file_name='chapter' + str(number) + '.xhtml',
                lang='en')

            chapter.set_content('<html><body><p>' + content + '</p></body></html>')

            book.add_item(chapter)

            # Everything you put in spine and toc must exists inside of the book. EPUB will bot be valid if
            # they don't exist.
            spine.append(chapter)
            toc.append(chapter)

        # Define book spine:
        book.spine = spine

        # This is very simple version of the TOC. It puts all of your chapters inside of one Section.
        book.toc = ((epub.Section('My book'), toc),) # It is important to define a section of the book, it is required for epub

        # write file:
        full_file_name_for_novel = os.path.join(ROOT_DIR + "\\books")

        ''' outdated code 
        # write and close the file:
        xml_file.write(os.path.join(ROOT_DIR + "\\temp"))
        xml_file.close()
        '''

        # write file:
        epub.write_epub(os.path.join(ROOT_DIR, "books", book_name + '.epub'), book) # create book directory for saving books:
        print("Output at: \n" + full_file_name_for_novel + "\\" + book_name + '.epub')
