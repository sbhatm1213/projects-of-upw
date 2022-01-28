import json
import lxml
from lxml import html 

# read html file
def download_page(html_source_file):    
    content = open(html_source_file, 'r', encoding="utf8").read()
    return content

# xget function's input: xpath returning/selecting one element.
# The function will return text value of that element.
def xget(doc,xpath_loc):
    if xpath_loc:
        m = doc.xpath(xpath_loc)
        if m:
            if type(m[0]) is lxml.etree._ElementUnicodeResult:
                return m[0].strip()
            else:
                return m[0].text_content().strip()
    return ''

# xget_list function's input: xpath returning/selecting multiple elements at once.
# The function will loop each element and return text value of each into one list.
def xget_list(doc, xpath_loc):
    items = []
    if xpath_loc:
        items_raw = doc.xpath(xpath_loc)
        if items_raw:
            for item in items_raw:
                if type(item) is lxml.etree._ElementUnicodeResult:
                    items.append(item.strip())
                else:
                    items.append(item.text_content().strip())
            return items
    return items


def xget_locations_list(doc, xpath_loc):
    items = []
    if xpath_loc:
        items_raw = doc.xpath(xpath_loc)
        if items_raw:
            for item in items_raw:
                loc_item = {}
                primary = xget(item,".//span[@class='locations__primary-label']")
                loc_item['is_primary'] = True if 'primary' in primary.lower() else False
                loc_item['address_lines'] = xget_list(item,".//*[@class='locations__address-line']")
                items.append(loc_item)
    return items


# See sheet 'Company' in google sheet file::
def extract_company_page(doc, url, page_source_str):
    data = {
        'url': url,
    }
    data['canonical_url'] = xget(doc,"/html/head//link[@rel='canonical']/@href") # this one from html - it can be found as canonical
    data['company_name'] = xget(doc,"//h1[@class='top-card-layout__title']")
    data['followers_count'] = xget(doc,"//h3[@class='top-card-layout__first-subline']").split(' ')[-2]
    data['employees_count'] = xget(doc,"//a[@data-tracking-control-name='org-employees_cta_face-pile-cta']").split(' ')[-2]
    data['website'] = xget(doc,"//*[@class='basic-info-item']/*[contains(text(), 'Website')]/following-sibling::*")
    data['industry'] = xget(doc,"//*[@class='basic-info-item']/*[contains(text(), 'Industries')]/following-sibling::*")
    data['company_size'] = xget(doc,"//*[@class='basic-info-item']/*[contains(text(), 'Company size')]/following-sibling::*")
    data['headquarters'] = xget(doc,"//*[@class='basic-info-item']/*[contains(text(), 'Headquarters')]/following-sibling::*")
    data['type'] = xget(doc,"//*[@class='basic-info-item']/*[contains(text(), 'Type')]/following-sibling::*")
    data['founded'] = xget(doc,"//*[@class='basic-info-item']/*[contains(text(), 'Founded')]/following-sibling::*")
    data['specialties'] = xget(doc,"//*[@class='basic-info-item']/*[contains(text(), 'Specialties')]/following-sibling::*")
    data['description'] = xget(doc,"//div[@class='core-section-container__content']/p[@class='about-us__description']")
    #data['logo_url'] = xget(doc, "//header[@class='share-update-card__header']/a[@data-tracking-control-name='organization-update_share-update_actor-image']/img/@src")
    data['logo_url'] = json.loads(xget(doc, "/html/head/script[@type='application/ld+json']")).get('logo', {}).get('contentUrl', '')
    data['open_jobs_count'] = xget(doc,"//a[@data-tracking-control-name='organization_guest-browse_jobs']/div/div[@class='base-aside-card__metadata']")
    data['locations_address_line'] = xget_locations_list(doc, "//section[contains(@class, 'locations')]//li[@class='locations__location']")
    return data


# See sheet 'Affiliates' in google sheet file:
def extract_affiliates(doc, url):
    affiliates = []
    affiliate_elements = doc.xpath("//section[contains(@class, 'affiliated-pages')]//li")
    for el in affiliate_elements:
        affiliate = {
            'company_url': url
        }
        affiliate['affiliated_company_url'] = xget(el, ".//a[@data-tracking-control-name='affiliated-pages']/@href")
        affiliates.append(affiliate)
    return affiliates


# See sheet 'Similar Pages' in google sheet file:
def extract_similar_pages(doc, url):
    similar_companies = []
    similar_elements = doc.xpath("//section[contains(@class, 'similar-pages')]//li")
    for el in similar_elements:
        similar = {
            'company_url': url
        }
        similar['similar_company_url'] = xget(el,".//a[@data-tracking-control-name='similar-pages']/@href")
        similar_companies.append(similar)
    return similar_companies


# See sheet 'Employees' in google sheet file:
def extract_employees(doc, url):
    employees = []
    employees_elements = doc.xpath("//section[contains(@class, 'employees-at')]//li")
    for el in employees_elements:
        employee = {
            'company_url': url
        }
        employee['employee_url'] = xget(el,".//a[@data-tracking-control-name='org-employees']/@href")
        employee['position'] = xget(el,".//a[@data-tracking-control-name='org-employees']//*[@class='base-main-card__subtitle']")
        employee['full_name'] = xget(el,".//a[@data-tracking-control-name='org-employees']//*[@class='base-main-card__title']")
        employees.append(employee)
    return employees


# See sheet 'Funding' in google sheet file:
def extract_funding(doc, url):
    funding = {
        'company_url': url
    }
    funding['chrunchbase_url'] = xget(doc,"//section[contains(@class, 'funding')]//a/@href")
    funding['total_rounds'] = xget(doc,"//a[@data-tracking-control-name='funding_all-rounds']//*[@class='funding__basic-info-rounds']")
    funding['last_round_series'] = xget(doc,".//div[contains(@class,'funding__last-round')]//*[@class='funding__last-round-type']")
    funding['last_round_date'] = xget(doc,".//div[contains(@class,'funding__last-round')]//*[@class='funding__last-round-date']")
    funding['last_round_funding_amount'] = xget(doc,".//div[contains(@class,'funding__last-round')]//*[@class='funding__last-round-money-raised']")
    funding['last_round_investors'] = xget_list(doc,".//a[@data-tracking-control-name='funding_investors']")
    return funding


# code has to work and to not break on each of these 3 htmls (while testing one html at a time):

#html_source_sample = './linkedin_htmls/linkedin_Unilever.html'
#url = 'https://uk.linkedin.com/company/unilever'

#html_source_sample = './linkedin_htmls/Nuro _ LinkedIn.html'
#url = 'https://uk.linkedin.com/company/nuro-inc.'

html_source_sample = './linkedin_htmls/Busuu _ LinkedIn.html'
url = 'https://uk.linkedin.com/company/busuu'

content = download_page(html_source_sample)
doc = html.fromstring(content)
page_source_str = str(content)
#print(page_source_str)

company_data = extract_company_page(doc, url, page_source_str)
print('company_data: ', company_data)
print('=======================\n===========================\n')
affiliates = extract_affiliates(doc, url)
print('affiliates: ',affiliates)
print('=======================\n===========================\n')

similar_pages = extract_similar_pages(doc, url)
print('similar_pages: ',similar_pages)
print('=======================\n===========================\n')

jobs = extract_employees(doc, url)
print('employees: ',jobs)
print('=======================\n===========================\n')

funding = extract_funding(doc, url)
print('funding: ',funding)
