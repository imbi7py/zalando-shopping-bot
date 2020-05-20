# login piotrpopisgames@gmail.com
# testertest
import smtplib
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, \
    StaleElementReferenceException

from selenium.webdriver.common.action_chains import ActionChains

def sendMail(to, file):
    """Function to inform user about founded products by e-mail."""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(open('/home/piotr/Music/music/email', 'r').read(), open('/home/piotr/Music/music/mp3.txt', 'r').read())
    from_mail = open('/home/piotr/Music/music/email', 'r').read()
    body = (open(file, "r").read())
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)


def adjust_categories(categories):
    return [cat[:len(cat) - 1] for cat in categories]


def choose_species_path(jeans, underwear, upper_part):
    if upper_part:
        return "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/div[3]/div[1]/div/span/span"
    elif jeans:
        return "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/div[3]/div[2]/div/span/span"
    elif underwear:
        return "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/div[3]/div[3]/div/span/span"
    else:
        raise ValueError


# TODO: something better than sleep, exceptions handling upgrade needed.
class ShoppingBot:
    def scroll_shim(self, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        self.driver.execute_script(scroll_by_coord)
        self.driver.execute_script(scroll_nav_out_of_way)

    def scroll_down(self):
        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            sleep(1)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height

    def distinct_structure_categories(self):
        _23fgc = False
        _2bQSu = False
        try:
            # 2bq
            element = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[1]/div/span")
            # next : /html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[2]/div/span
            print(element.text)
            _2bQSu = True
        except NoSuchElementException:
            _2bQSu = False
        try:
            # 2fgc
            element = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul[1]/li[1]/span")
            # next /html/body/div[2]/div/div/section/div[2]/div/div/div/ul[1]/li[2]/span
            print(element.text)
            _23fgc = True
        except NoSuchElementException:
            _23fgc = False
        return _2bQSu, _23fgc

    def turn_off_banner(self):
        try:
            self.driver.find_element_by_xpath(
                "//*[@id=\"uc-btn-accept-banner\"]").click()
        except NoSuchElementException:
            sys.stderr.write("Happily banner has not shown on....\n")

    def set_max_per_item(self, max_cost_per_item):

        WebDriverWait(self.driver, 5).until \
            (EC.element_to_be_clickable((By.XPATH, '//span[.="Cena"]'))).click()
        price_max=self.driver.find_element_by_xpath('//*[@id="price-max"]')
        self.driver.execute_script('document.getElementById("price-max").value = "'+str(max_cost_per_item)+'";')
        price_max.send_keys(Keys.ENTER) 


    def set_brands(self, wanted_brands):
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/section/div[2]/nav/a[3]/div/span/span')))
        except TimeoutException:
            print("Timed out waiting for page to load")
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/nav/a[3]/div/span").click()
        i = 1
        already_selected = []
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/ul/li[" + str(i) + "]/span")
                for brand in wanted_brands:
                    brand_web = sample.text.lower()
                    if brand.lower() in brand_web and brand_web not in already_selected:
                        print(brand_web)
                        already_selected.append(brand_web)
                        sample.click()
                i += 1
            except NoSuchElementException:
                break

    def set_sizes(self, wanted_sizes):
        path = choose_species_path(False, False, upper_part=True)
        self.driver.find_element_by_xpath(path).click()
        i = 1
        already_selected = []
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/ul/button[" + str(i) + "]")
                for given_size in wanted_sizes:
                    size_web = sample.text.upper()
                    if given_size == size_web and size_web not in already_selected:
                        print(size_web)
                        already_selected.append(size_web)
                        sample.click()
                i += 1
            except NoSuchElementException:
                break

    def set_categories_23fgc(self, wanted_categories):
        already_selected = []
        i = 1
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul[2]/li/ul/li[" + str(
                        i) + "]/div/span/span")
                for existence_cat in wanted_categories:
                    cat_web = sample.text.lower()
                    if existence_cat in cat_web and cat_web not in already_selected:
                        print(cat_web)
                        already_selected.append(cat_web)
                        sample.click()
                i += 1
            except NoSuchElementException:
                break

    def set_categories_2bQSu(self, wanted_categories):
        already_selected = []
        i = 1
        while i:
            try:
                xpath = "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[" + str(i)
                element = self.driver.find_element_by_xpath(xpath + "]/div/span")
                j = 1
                print(i)
                i += 1
                if 'Mężczyźn'.upper() in element.text.upper() or 'UNISE' in element.text.upper():
                    while j:
                        try:
                            print(j)
                            next_cat = xpath + "]/ul/li[" + str(j) + "]/div/span"
                            "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[3]/ul/li[2]/div/span"
                            j += 1
                            sample = self.driver.find_element_by_xpath(next_cat)
                            print(sample.text)
                            for existence_cat in wanted_categories:
                                cat_web = sample.text.lower()
                                if existence_cat in cat_web and cat_web:  # not in already_selected:
                                    already_selected.append(cat_web)
                                    sample.click()
                        except NoSuchElementException:
                            print('no more columns - categories')
                            break
            except NoSuchElementException:
                print('no more rows - categories')
                break

    def set_categories(self, wanted_categories):
        _2bQSu, _23fgc = self.distinct_structure_categories()
        if _2bQSu:
            self.set_categories_2bQSu(wanted_categories)

    def wait_for(self):
        try:
            WebDriverWait(self.driver, 1).until \
            (EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"sizeOverlayDialog")]')))
                  
            WebDriverWait(self.driver, 5).until \
            (EC.element_to_be_clickable((By.XPATH, '//span[text() = "Mimo to zamawiam oba rozmiary"]'))).click()

            WebDriverWait(self.driver, 5).until \
            (EC.element_to_be_clickable((By.XPATH, '//span[text() = "Potwierdź"]'))).click()
        except TimeoutException:

            element = WebDriverWait(self.driver, 5).until \
                (EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()
            self.wait_for()
           
    def wait_for_atcButton(self):
        try:
            # WebDriverWait(self.driver, 5).until \
            # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
            WebDriverWait(self.driver, 5).until \
            (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "transf") ]')))
            WebDriverWait(self.driver, 5).until \
            (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
            
        except TimeoutException:
            print('atcBtn')

    


        

    def __init__(self, email, password):
        options = Options()
        # options.add_argument("--disable-notifications")
        self.driver = webdriver.Firefox(options=options)

        # Open website
        self.driver.get("https://www.zalando-lounge.pl")
       
        # Wait for cookies banner and close it
        WebDriverWait(self.driver, 20).until \
            (EC.visibility_of_element_located((By.XPATH, '//*[@id=\"uc-btn-accept-banner\"]'))).click()
    
        # Open loggin panel
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()

        # email
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-email"]')))
        element.send_keys(email)

        # password
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-password"]')))
        element.send_keys(password)

        #loggin in
        element.submit()

        #Go to selected event
        campaign_id = 'campaign-ZZO11DQ'
        
        action = ActionChains(self.driver)
        first_compaing = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="'+campaign_id+'"]/div')))
        self.scroll_shim(first_compaing)
        # first_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div')
        action.move_to_element(first_compaing).perform()
        second_compaing = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="'+campaign_id+'"]/div/div[1]/div/button/span')))
        # second_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div/div[1]/div/button/span')
        action.move_to_element(second_compaing).perform()
        second_compaing.click()

        # Wait until filters load
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,'//div[starts-with(@class, "filters")]')))


        # we have to remove  last char in string
        # for example if someone input bluza or bluzy.
        # bluz is preffix that occurs in both single and multiple form.
        
        # TODO: function to decide what is in catergories [ SPODNIE, GORNE CZESCI GARDEROBY, BIELIZNA]

        selected_categories = adjust_categories(['koszule', 'koszulki'])
        selected_sizes = ['M', 'L']
        selected_brands = ['GAP', 'Fila', 'Kappa', 'Lee']

        # sometimes banner pop up
        # self.turn_off_banner()
        i = 1

        while i:
            try:
                element = "/html/body/div[2]/div/div/section/div[2]/nav/a[" + str(i) + "]"
                sample = self.driver.find_element_by_xpath(element)
                i += 1
                print(sample)
                if sample.text == 'KATEGORIE':
                    sample.click()
                    # self.set_categories(selected_categories)
                elif sample.text == 'ROZMIAR':
                    sample.click()
                    self.set_sizes(selected_sizes)
                elif sample.text == 'MARKA':
                    sample.click()
                    # self.set_brands(selected_brands)
                elif sample.text == 'CENA':
                    #sample.click()
                    self.set_max_per_item(120)
            except NoSuchElementException:
                break


        self.scroll_down()


        #Store all href for availables items
        hrefs = []

        all_items = self.driver.find_elements_by_xpath("//div[starts-with(@id, 'article-')]/a")
        for item in all_items:
            href = item.get_attribute("href")
            if (len(self.driver.find_elements_by_xpath('//a[@href="' + href[29:] + '"]/div[3]')) == 0):
                hrefs.append(href)


        selected_sizes = ['M', 'L']
        # Add all items from hrefs to cart
        for href in hrefs:
            self.driver.get(href)

            WebDriverWait(self.driver, 5).until \
            (EC.presence_of_element_located((By.XPATH, "//div[starts-with(@class, 'ArticleSizestyles')]")))

            selected = 0

            for size in selected_sizes:
                element = WebDriverWait(self.driver, 5).until \
                (EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "Size") and text()="' + size + '"]')))
                #addtoCartButton = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]')))
                parent = element.find_element_by_xpath("./..")
                is_clickable = parent.value_of_css_property("color")               
                if is_clickable == 'rgb(53, 53, 53)':
                    try:
                        ammount = self.driver.find_element_by_xpath('//*[@id="article-information"]/div[4]/div[2]/div[1]/div/span[2]')
                        print(ammount.text)
                    except NoSuchElementException:  
                        print('here')
                        element.click()
                        selected = selected + 1
                        for x in range(0,5):
                            print('X: ', x)
                            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()
                            
                            if selected==2 and x==0:
                                print("no nie dziala")
                                self.wait_for()
                                WebDriverWait(self.driver, 20).until \
                                (EC.invisibility_of_element_located((By.XPATH, '//div[contains(@class,"styles___backdrop")]')))
                            else:
                                self.wait_for_atcButton()#sleep(1.5)

                                    
                                    
           
                # if selected == 1: ZZO125F
                #     sleep(.7)
                    # WebDriverWait(self.driver, 5).until \
                    # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
                    # WebDriverWait(self.driver, 5).until \
                    # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "transf") ]')))
                    # WebDriverWait(self.driver, 5).until \
                    # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
                # if selected==2:
                #     print("no nie dziala")
                #     self.wait_for()
                    
        
    print('finished')


ShoppingBot("piotrpopisgames@gmail.com", 'testertest')
