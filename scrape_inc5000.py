'''
	scraping the Inc. 5000 list at http://www.inc.com/inc5000/list/2013/
	To get all 5,000 points, 100 at a time:
	append 100 * i to the end of the URL for i in (0,50)
'''
import urllib2
import html5lib
import csv
from bs4 import BeautifulSoup



'''
    get_site is a wrapper for BeautifulSoup and urllib2
'''
def get_site(url, parser=None):
    site = BeautifulSoup(urllib2.urlopen(url).read(), parser)
    return site



'''
    split_letter_number splits a string into letters and numbers
'''
def split_letter_number(string):
    letters = ''
    numbers = ''
    for char in string:
        if char in '-+.0123456789':
            numbers = numbers + char
        else:
            letters = letters + char
    return (float(numbers), letters)



'''
    convert_dollarstring takes dollar values in the 
    thousands to billions and converts them to numbers.
    also handles percents for convenience
'''
def convert_dollarstring(dollarstring):
    clean_dollarstring = dollarstring.replace('$','').\
                                      replace(',','').\
                                      lower()
    split_dollarstring = split_letter_number(clean_dollarstring)
    
    num        = split_dollarstring[0]
    letters    = split_dollarstring[1].replace(' ','')

    value_dict = {
    'thousand' : 1000, 
    'thousands': 1000, 
    'k'        : 1000,
    'millions' : 1000000, 
    'million'  : 1000000, 
    'mm'       : 1000000,
    'billions' : 1000000000, 
    'billion'  : 1000000000,
    'b'        : 1000000000,
    '%'        : .01,
    'percent'  : .01,
    'perc'     : .01,
    'cents'    : .01,
    'pennies'  : .01
    }

    if len(letters) > 0:
        num = num * value_dict.get(letters, 1)
    return num



if __name__ == '__main__':
    
    base_url = 'http://www.inc.com/inc5000/list/2013/'
    data_table = []



    for i in xrange(0,50):
        '''
            get each page
        '''
        print base_url + str(100 * i)
        site_data  = get_site(base_url + str(100 * i), 'html5lib')
        full_table = site_data.find('div', {'id':'inc5000_table'})



        '''
            loop through the table
        '''
        for tr in full_table.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                row.append(td.text.encode('ascii', 'ignore'))
            if len(row) > 0:
                data_table.append(row)



    '''
        all the data is gathered, now clean it
    '''
    for r in data_table:
        r[2] = convert_dollarstring(r[2])
        r[3] = convert_dollarstring(r[3])
        r[4] = r[4][1:]
    
    '''
        now print it
    '''
    output = open('inc5000data.csv', 'wb')
    writer = csv.writer(output, delimiter=",", quotechar='"')
    for r in data_table:
        writer.writerow(r)
    output.close()
