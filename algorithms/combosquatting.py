from urllib.parse import urlparse
import tldextract
import sys

sys.path.append(".")
from db import getAllDomains


def find_combosquatting(url):
    domain = urlparse(url).netloc
    false_trademark = domain.split('.')[1]

    print(f'DOMAIN: {domain} FALSE: {false_trademark}')
    return is_substring(false_trademark, 4, 'database')


def is_substring(false_domain_name, minimal_str_len=4, source_list='database'):
    """
    Takes a false domain name and scans a file or database to check
    for registered trademarks of which the the false domain name is a substring and
    returns a list containing any matches found whose length is less than 
    minimal_str_len.
    """

    matches = []
    # compare with trademarks on database
    if source_list == 'database':
        domain_dict = getAllDomains()
        print(domain_dict)

        for entry in domain_dict:
            domain = tldextract.extract(entry['domain']).domain
            if domain in false_domain_name \
                    and domain != false_domain_name \
                    and len(domain) >= minimal_str_len:
                matches.append(domain)
    # combare with trademarks in file
    else:
        filename = source_list
        path = \
            '/Users/obedababio/Documents/Spring 2021/CPSC 490/SafeLink/SafeLinkBackEnd/algorithms/combosquatting/' + filename
        custom_file = open(path, 'r')
        lines = custom_file.readlines()
        for string in lines:
            trademark_name = tldextract.extract(string).domain
            if trademark_name in false_domain_name \
                    and trademark_name != false_domain_name:
                matches.append(trademark_name)
    matches = set(matches)
    return list(matches)


print(find_combosquatting('http://www.somethingfacebooksomething.test/foo/bar'))
