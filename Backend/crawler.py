import tldextract, re

def markAsResult(text):
	return f'RESULT:<{text}>'

def getElementText(driver, xpath):
	return markAsResult(driver.find_element_by_xpath(xpath).text)

def crawlUrl(driver, url):
	tdl = tldextract.extract(url)
	domain = tdl.domain
	print(f'domain: {domain}')
	if domain == 'expedia':
		return crawlExpedia(driver, tdl.suffix)
	elif domain == 'whatsmyua': 
		return crawlUserAgent(driver)
	elif domain == 'ipstack':
		return crawlLocation(driver)
	elif domain == 'w3schools':
		return crawlCookies(driver)
	else: 
		return ""

# -----------------------------------------------------------------------------------------------------
# Requires website: https://www.w3schools.com/js/js_cookies.asp
# Clicks on button that shows existing cookies, then clicks button that creates cookie, then returns value from first step
# This is useful to test whether the cookie we created persists through sessions

def crawlCookies(driver):
	displayCookieButton = driver.find_element_by_xpath('//*[@id="main"]/p[21]/button[1]')
	createCookieButton = driver.find_element_by_xpath('//*[@id="main"]/p[21]/button[2]')
	displayCookieButton.click()
	# Opens a popup that shows the existing cookies saved by the page
	popup = driver.switchTo().alert()
	cookies = popup.getText()
	popup.accept()
	# Click the OK on the alert popup
	createCookieButton.click()
	return markAsResult(cookies)

# -----------------------------------------------------------------------------------------------------
# Requires website: https://ipstack.com/
# The website shows our location

def crawlLocation(driver):
	return markAsResult(getElementText(driver, '/html/body/div/section[1]/div/div/div[2]/div[2]/div/div[7]/span'))

# -----------------------------------------------------------------------------------------------------
# Requires website: https://www.whatsmyua.info 
# This website shows which user agent we are using

def crawlUserAgent(driver):
	return markAsResult(getElementText(driver, '//*[@id="rawUa"]').replace('rawUa: ',''))

# -----------------------------------------------------------------------------------------------------
# Requries website such as: 

def valuta(x):
    return {
        'com'   : '$',			############# WATCH OUT, BECAUSE .COM DATES ARE DIFFERENT, SO WE CAN'T JUST CONVERT 
        'dk'   	: 'DKK ',
        'co.uk' : '£', 
        'de' 	: '€' 			############# THIS DOESN'T WORK EITHER, SINCE .DE PRICES ARE REVERSED: 210 € instead of € 210
    }.get(x, 'DKK')    

# Returns price of top element in flightModuleList
def crawlExpedia(driver, urlSuffix):
	print(f'suffix: {urlSuffix}')
	text      = getElementText(driver, '//*[@id="flightModuleList"]')

	priceList = regexFindAllIn(text, "\d+[,.]?\d*\s*\$|\$\s*\d+[.,]?\d*", "Price")
	durationList = regexFindAllIn(text, "[\d]+:[\d]+[^A-Z]*[[\d]+:[\d]+[^\s]*", "Duration")
	ratingList = regexFindAllIn(text, "\(\d*.\d*\/\d*\)", "Rating")
	timeList = regexFindAllIn(text, "\d+[a-zA-Z]+\s\d*[a-zA-Z]*\s\W(?:\d+\s*)?[a-zA-Z]*\W", "Time")
	legList = regexFindAllIn(text, "[A-Z]{3} -(?:(?:\s*\d+[a-z]+)+\s[a-z]+\s+[A-Z]{3}(?:[a-zA-Z\s]+(?:\s*\d+[a-z]+)+\s[a-z]+\s+[A-Z]{3})+)?\s[a-zA-Z\s:]*\s*(?:- )?[A-Z]{3}", "Leg")

	resultList = [priceList[0], durationList[0], ratingList[0], timeList[0], legList[0]]
	return markAsResult(resultList)


def regexFindAllIn(textToSearch, regexString, resultName):
	regex  = re.compile(regexString)
	resultList = regex.findall(textToSearch)
	if resultList:
	    print(f'---{resultName}---')
	    print(*resultList[0])
	else: print(f'{resultName} was empty')
	return resultList
