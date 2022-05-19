from urllib.parse import urlparse
import re
import urllib
import pandas as pd
import numpy as np
def url_Lexical_Features(df,url_column):

    host_name = [] #1
    url_length = [] #2
    url_scheme = [] #3
    path_length = [] #4
    ip_present = [] #5
    number_of_digits = [] #6
    number_of_parameters = [] #7
    number_of_fragments = [] #8
    is_url_encoded = [] #9
    number_encoded_char = [] #10
    number_of_subdirectories = [] #11
    host_length = [] #12
    number_of_periods = [] #13
    has_client = [] #14
    has_admin = [] #15
    has_server = [] #16
    has_login = [] #17
    number_of_dashes = [] #18
    have_at_sign = [] #19
    is_tiny_url = [] #20
    get_tld = [] #21
    number_of_subdomains_and_extensions = [] #22
    number_of_spaces = [] #23
    number_of_zeros = [] #24
    is_url_single_character_directory = [] #25
    number_of_uppercase = [] #26
    number_of_lowercase = [] #27
    ratio_upper_to_lower = [] #28
    number_of_double_slashes = [] #29
    
    for i in df[url_column]:       
        
#         Url Parse detail
        url_parse = urlparse(i)
        
        host_name.append(url_parse.hostname) # hostname
        url_length.append(len(i)) #length
        url_scheme.append(url_parse.scheme) # scheme
        path_length.append(len(url_parse.path)) # path length
        
        
#         if ip address present
        ip_present.append(len(re.findall(r'\d+\.\d+\.\d+\.\d|0x\d+\.0x\d+\.0x\d+\.0x\d|\w+:\w+:\w+:\w+:\w+:\w+:\w+:\w+',str(url_parse.hostname))))
        number_of_digits.append(len(re.findall(r'\d',i))) # number of digits
        
#         number of parameters in query string
        if url_parse.query:
            number_of_parameters.append(len(url_parse.query.split('&')))
        else:
            number_of_parameters.append(0)
            
#         number of fragments
        if url_parse.fragment:
            number_of_fragments.append(len(url_parse.fragment.split('#')))
        else:
            number_of_fragments.append(0) 
        
        is_url_encoded.append('%' in i) # if the url has encoded charecters or not
        number_encoded_char.append(len(re.findall(r'%',i))) # number of encoded charecters
        number_of_subdirectories.append(len(url_parse.path.split('/'))-1) #number of subdirectories
        host_length.append(len(re.findall(r'(www\.)?([^\.]+)\.(.+)',str(url_parse.hostname))[0][1])) # length of host name
        number_of_periods.append(len(re.findall(r'.',i))) # number of (.) in url string
        has_client.append('client' in i.lower()) # if the url string contains word client
        has_admin.append('admin' in i.lower()) # if the url string contains word admin
        has_server.append('server' in i.lower()) # if the url string contains word server
        has_login.append('login' in i.lower()) # if the url string contains word login
        number_of_dashes.append(len(re.findall(r'-',url_parse.netloc))) # number of dashes in domain name
        have_at_sign.append('@' in i) # have @ symbol in Url string
        
#         if the url is shortened or not
#              listing shortening services
        shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                  r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                  r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                  r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                  r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                  r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                  r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                  r"tr\.im|link\.zip\.net"
        
        matches = len(re.findall(shortening_services,i))
        if matches:
            is_tiny_url.append(1)
        else:
            is_tiny_url.append(0)
            
        
        
        get_tld.append(url_parse.netloc.split('.')[-1].split(':')[0]) # to get top level domain
        number_of_subdomains_and_extensions.append(len(url_parse.netloc.split(':')[0].split('.'))-1) # total number of subdomains and extensions
        number_of_spaces.append(len(re.findall(r'%20',i))) # number of encoded spaces in url string
        number_of_zeros.append(len(re.findall(r'0',i))) # number of zeros in url string
        number_of_double_slashes.append(len(re.findall(r'\/\/',i))) # number of double slashes in url string
        
        
#         does url has a single character directory
        temp = 0
        for j in url_parse.path.split('/'):
            if len(j) == 1:
                temp = 1
                break
        is_url_single_character_directory.append(temp)
        
#         Uppercase and Lowercase letters in url string and their ratio
        u = len([j for j in i if j.isupper()])
        l = len([j for j in i if j.islower()])
        
        number_of_uppercase.append(u) # number of uppercase letters in url string
        number_of_lowercase.append(l) # number of lowercase letters in url string
        ratio_upper_to_lower.append(u/(l+1))            
            
    df2 = df[[url_column]]
        
    df2['host_name'] = host_name #1
    df2['url_length'] = url_length #2
    df2['url_scheme'] = url_scheme #3
    df2['path_length'] = path_length #4
    df2['ip_present'] = ip_present #5
    df2['number_of_digits'] = number_of_digits #6
    df2['number_of_parameters'] = number_of_parameters #7
    df2['number_of_fragments'] = number_of_fragments #8
    df2['is_url_encoded'] = is_url_encoded #9
    df2['number_encoded_char'] = number_encoded_char #10
    df2['number_of_subdirectories'] = number_of_subdirectories #11
    df2['host_length'] = host_length #12
    df2['number_of_periods'] = number_of_periods #13
    df2['has_client'] = has_client #14
    df2['has_admin'] = has_admin #15
    df2['has_server'] = has_server #16
    df2['has_login'] = has_login #17
    df2['number_of_dashes'] = number_of_dashes #18
    df2['have_at_sign'] = have_at_sign #19
    df2['is_tiny_url'] = is_tiny_url #20
    df2['get_tld'] = get_tld #21
    df2['number_of_subdomains_and_extensions'] = number_of_subdomains_and_extensions #22
    df2['number_of_spaces'] = number_of_spaces #23
    df2['number_of_zeros'] = number_of_zeros #24
    df2['is_url_single_character_directory'] = is_url_single_character_directory #25
    df2['number_of_uppercase'] = number_of_uppercase #26
    df2['number_of_lowercase'] = number_of_lowercase #27
    df2['ratio_upper_to_lower'] = ratio_upper_to_lower #28
    df2['number_of_double_slashes'] = number_of_double_slashes #29

    return df2