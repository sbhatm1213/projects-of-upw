import json
import lxml
from lxml import html 

# read html file
def download_page(html_source_file):    
    content = open(html_source_file, 'r', encoding='utf-8').read()
    return content

# read one xpath object
def xget(doc,xpath_loc):
    if xpath_loc:
        m = doc.xpath(xpath_loc)
        if m:
            if type(m[0]) is lxml.etree._ElementUnicodeResult:
                return m[0].strip()
            else:
                return m[0].text_content().strip()
    return ''

# read a list of xpath objects
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

# this will be useful for the array functions to refer to (I simply copied your created function for one of the previous websites)
def xget_acquisitions_list(doc, xpath_loc):
    items = []
    if xpath_loc:
        items_raw = doc.xpath(xpath_loc)
        if items_raw:
            for item in items_raw:
                acq_item = {}
#{"acquiree_name":"IntSights", "link":"https://www.crunchbase.com/organization/intsights",
#"announced_date":"Jul 19, 2021","price":"$335M","transaction_name":"IntSights acquired by Rapid7"}
                acq_item['acquiree_name'] = xget(item, ".//td[1]")
                acq_item['link'] = xget(item,".//td[1]//a/@href")
                acq_item['announced_date'] = xget(item,".//td[2]")
                acq_item['price'] = xget(item,".//td[3]")
                acq_item['transaction_name'] = xget(item,".//td[4]")
                items.append(acq_item)
    return items

def xget_investments_list(doc, xpath_loc):
    items = []
    if xpath_loc:
        items_raw = doc.xpath(xpath_loc)
        if items_raw:
            for item in items_raw:
                inv_item = {}
#{ "name":"SCADAfence", "link":"https://www.crunchbase.com/organization/scadafence","announced_date":"Mar 17, 2021",
#"money_raised":"$12M","lead_investor":"", "funding_round":"Series B - SCADAfence"},
                inv_item['name'] = xget(item, ".//td[2]")
                inv_item['link'] = xget(item,".//td[2]//a/@href")
                inv_item['announced_date'] = xget(item,".//td[1]")
                inv_item['money_raised'] = xget(item,".//td[5]")
                inv_item['lead_investor'] = xget(item,".//td[3]")
                inv_item['funding_round'] = xget(item,".//td[4]")
                items.append(inv_item)
    return items


def xget_employee_list(doc, xpath_loc):
    items = []
    if xpath_loc:
        items_raw = doc.xpath(xpath_loc)
        if items_raw:
            for item in items_raw:
                inv_item = {}
#{"name":"Jacky Ni","link":"https://www.crunchbase.com/person/jacky-ni","position":"COO"},
                inv_item['name'] = xget(item, ".//a")
                inv_item['link'] = xget(item, ".//a/@href")
                inv_item['position'] = xget(item, ".//a/following-sibling::field-formatter")
                items.append(inv_item)
    return items


def xget_contact_list(doc, xpath_loc):
    items = []
    if xpath_loc:
        items_raw = doc.xpath(xpath_loc)
        if items_raw:
            for item in items_raw:
                con_item = {}
#{"name":"Kinying Kwan","position":"Chief Executive Officer", "job_level":"Executive", "department":"Management"},
                con_item['name'] = xget(item, ".//contact-details//*[contains(@class, 'name')]")
                con_item['position'] = xget(item, ".//contact-details//*[contains(@class, 'job-title')]")
                con_item['job_level'] = xget(item, ".//contact-details//*[contains(@class, 'job-levels-department')]//field-formatter[1]")
                con_item['department'] = xget(item, ".//contact-details//*[contains(@class, 'job-levels-department')]//field-formatter[2]")
                items.append(con_item)
    return items
    
    
def xget_board_mem_list(doc, xpath_loc):
    items = []
    if xpath_loc:
        items_raw = doc.xpath(xpath_loc)
        if items_raw:
            for item in items_raw:
                board_mem_item = {}
#{"name":"Boris Chen","link":"https://www.crunchbase.com/person/boris-chen","position":"Board Member", "date":"Oct 2018"},
                board_mem_item['name'] = xget(item, ".//a")
                board_mem_item['link'] = xget(item, ".//a/@href")                
                board_mem_item['position'] = xget(item, ".//field-formatter[1]")
                board_mem_item['date'] = xget(item, ".//field-formatter[2]")
                items.append(board_mem_item)
    return items
                
                
# See sheet 'Summary' in google sheet file::
def extract_summary_page(doc, url):

    data = {
        'url': url,
    }

    data['name'] = xget(doc,'//profile-header//h1[@class="profile-name"]')
    data['url'] = xget(doc,'/html/head//meta[@property="og:url"]/@content')
    data['about'] = xget(doc,'//profile-section//description-card//span[@class="description"]')
    data['full_description'] = xget(doc,'//profile-section//description-card//span[contains(@class,"description") and contains(@class,"has-overflow")]')
    data['also_known_name'] = xget(doc,'//profile-section//section-card//li[contains(., "Also Known")]//field-formatter')
    data['operating_status'] = xget(doc,'//profile-section//section-card//li[contains(., "Operating") and contains(., "Status")]//field-formatter')
    data['type'] = xget(doc,'//profile-header//div[@class="profile-type"]')
    data['industries'] = xget_list(doc,'//profile-section//section-card//li[contains(., "Industries")]//field-formatter//chip')
    data['location'] = xget_list(doc,'//profile-section//section-card//li//field-formatter//*[contains(@href, "location_identifiers")]')
    data['num_employees'] = xget(doc,'//profile-section//section-card//li//field-formatter//*[contains(@href, "num_employees")]')
    data['company_type'] = xget(doc,'//profile-section//section-card//li[contains(., "Company") and contains(., "Type")]//field-formatter')
    data['website'] = xget(doc,'//page-centered-layout[contains(@class, "overview-divider")]//profile-section//section-card//li//field-formatter//a[contains(@role, "link")]')
    data['founded_date'] = xget(doc,'//profile-section//section-card//li[contains(., "Founded") and contains(., "Date")]//field-formatter')
    data['headquarters_regions'] = xget(doc,'//profile-section//section-card//li[contains(., "Headquarters") and contains(., "Regions")]//field-formatter')
    data['logo_url'] = xget(doc,'/html/head//meta[@property="og:image:secure_url"]/@content')
    data['ipo_status'] = xget_list(doc,'//page-centered-layout[contains(@class, "overview-divider")]//profile-section//section-card//li//field-formatter')[3]
    data['stock_symbol'] = xget(doc,'//profile-section//section-card//li[contains(., "Stock") and contains(., "Symbol")]//field-formatter')
    data['acquired_by'] = xget(doc,'//profile-section//section-card//li[contains(., "Acquired") and contains(., "by")]//field-formatter')
    data['acquired_by_link '] = xget(doc,'//profile-section//section-card//li[contains(., "Acquired") and contains(., "by")]//field-formatter//@href')
    data['legal_name'] = xget(doc,'//profile-section//section-card//li[contains(., "Legal") and contains(., "Name")]//field-formatter')
    data['founders'] = xget(doc,'//profile-section//section-card//li[contains(., "Founders")]//field-formatter')
    data['contact_email'] = xget(doc,'//profile-section//section-card//li[contains(., "Contact") and contains(., "Email")]//field-formatter')
    data['facebook_url'] = xget(doc,'//profile-section//section-card//li//*[contains(@title, "Facebook")]/@href')
    data['linkedin_url'] = xget(doc,'//profile-section//section-card//li//*[contains(@title, "LinkedIn")]/@href')
    data['twitter_url'] = xget(doc,'//profile-section//section-card//li//*[contains(@title, "Twitter")]/@href')

    return data


# See sheet 'Financial' in google sheet file:
def extract_financial_page(doc, url):

    fin = {
        'url': url,
    }

    fin['funding_round'] = xget(doc,'//profile-section//section-card//label-with-info[contains(., "Funding") and contains(., "Rounds")]/following-sibling::field-formatter')
    fin['lead_investors'] = xget(doc,'//profile-section//section-card//label-with-info[contains(., "Lead") and contains(., "Investors")]/following-sibling::field-formatter')
    fin['total_funding_amount'] = xget(doc,'//profile-section//section-card//label-with-info[contains(., "Funding") and contains(., "Amount")]/following-sibling::field-formatter')
    fin['num_investors'] = xget(doc,'//profile-section//section-card//label-with-info[contains(., "Investors") and not(contains(., "Lead"))]/following-sibling::field-formatter')
    fin['num_investments'] = xget(doc,'//profile-section//section-card//label-with-info[contains(., "Investments")]/following-sibling::field-formatter')
    fin['ipo_date'] = xget(doc,'//profile-section//section-card//li[contains(., "IPO") and contains(., "Date")]//field-formatter')
    fin['ipo_link'] = xget(doc,'//profile-section//section-card//li[contains(., "Stock") and contains(., "Symbol")]//field-formatter//a/@href')
    fin['num_acquisitions'] = xget(doc,'//profile-section//section-card//label-with-info[contains(., "Number") and contains(., "Acquisitions")]/following-sibling::field-formatter')
    fin['acquisitions'] = xget_acquisitions_list(doc, '//profile-section//section-card//h2[contains(@class, "section-title") and contains(., "Acquisitions")]/ancestor::section-card//table//tbody//tr')
    fin['investments'] =  xget_investments_list(doc, '//profile-section//section-card//h2[contains(@class, "section-title") and contains(., "Investments")]/ancestor::section-card//table//tbody//tr')

    return fin


# See sheet 'People' in google sheet file:
def extract_people_page(doc, url):

    canonical_url = xget(doc,'/html/head//link[@rel="canonical"]/@href')

    peo = {
        'url': canonical_url,
    }

    peo['num_employee_profiles'] = xget(doc,'//profile-section//anchored-values//label-with-info[contains(., "Employee") and contains(., "Profiles")]/following-sibling::field-formatter')
    peo['num_contacts'] = xget(doc,'//profile-section//anchored-values//label-with-info[contains(., "Contacts")]/following-sibling::field-formatter')
    peo['num_board_members_advisors'] = xget(doc,'//profile-section//anchored-values//label-with-info[contains(., "Number of Board Member")]/following-sibling::field-formatter')
    peo['employees'] = xget_employee_list(doc, '//profile-section//section-card//h2[contains(@class, "section-title") and contains(., "Employee")]/ancestor::section-card//image-list-card//ul/li')
    peo['contacts'] = xget_contact_list(doc, '//profile-section//section-card//h2[contains(@class, "section-title") and contains(., "Contacts")]/ancestor::section-card//contacts-card//contacts-card-row')
    peo['board_members_advisors'] = xget_board_mem_list(doc, '//profile-section//section-card//h2[contains(@class, "section-title") and contains(., "Board Member")]/ancestor::section-card//image-list-card//ul/li')
    
    return peo

# See sheet 'Technology' in google sheet file::
def extract_technology_page(doc, url):

    technology = {
        'url': url,
    }

    technology['monthly_visits'] = xget(doc,'//profile-section//anchored-values//label-with-info[contains(., "Monthly") and contains(., "Visits") and not(contains(., "Growth"))]/following-sibling::field-formatter')
    technology['monthly_visits_growth'] = xget(doc,'//profile-section//anchored-values//label-with-info[contains(., "Monthly") and contains(., "Visits") and contains(., "Growth")]/following-sibling::field-formatter')

    return technology


def get_html_contents(html_file_name):
    content = download_page(html_file_name)
    doc = html.fromstring(content)
    page_source_str = str(content)
    return (content, doc, page_source_str)


url = 'https://www.crunchbase.com/organization/rapid7'
content, doc, page_source_str = get_html_contents('Rapid7 - Summary Tab.html')
summary_data = extract_summary_page(doc, url)
print(json.dumps(summary_data, indent=2))

url = 'https://www.crunchbase.com/organization/rapid7/company_financials'
content, doc, page_source_str = get_html_contents('Rapid7 - Financials Tab.html')
financial_data = extract_financial_page(doc, url)
print(json.dumps(financial_data, indent=2))

url = 'https://www.crunchbase.com/organization/rapid7/people'
content, doc, page_source_str = get_html_contents('Rapid7 - People Tab.html')
people_data = extract_people_page(doc, url)
print(json.dumps(people_data, indent=2))

url = 'https://www.crunchbase.com/organization/rapid7/technology'
content, doc, page_source_str = get_html_contents('Rapid7 - Technology Tab.html')
technology_data = extract_technology_page(doc, url)
print(json.dumps(technology_data, indent=2))

