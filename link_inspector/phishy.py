import numpy as np
import pandas as pd
import pickle
import urllib.parse
import tldextract
import json
import requests
import re
import sys
from urllib.parse import urlencode
from urllib.parse import urlparse
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from bs4 import BeautifulSoup


def err_out(msg, status="failure"):
    program_output["status"] = status
    program_output["msg"] = msg
    print(json.dumps(program_output))
    sys.exit(1)


program_output = {
    "status": "success",
    "msg": "none"
}

if len(sys.argv) != 2:
    err_out("Incorrect number of arguments (expected 1). Usage: python3 phishy.py someurl.tld")

prediction_url = sys.argv[1]
train = False
##########################################################################
#               TRAINING PORTION
##########################################################################
if train:
    dataset = pd.read_csv('dataset_phishing.csv', encoding='utf-8-sig')
    dataset['phishing'] = np.where(dataset['status'] != 'phishing', 0, 1)
    dataset.head()

    # create new dataframe without the status column
    df = dataset.drop(columns=['status', 'url'])
    corr_matrix = df.corr()
    y = df['phishing']
    X = df.drop(['phishing'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=1)

    # Train a random forest model
    RFmodel3 = RandomForestClassifier()
    RFmodel3.fit(X_train, y_train)
    status_corr = corr_matrix['phishing']


    def feature_selector_correlation(data, threshold):
        selected_features = []
        feature_score = []
        i = 0
        for score in data:
            if abs(score) > threshold:
                selected_features.append(data.index[i])
                feature_score.append(['{:3f}'.format(score)])
            i += 1
        result = list(zip(selected_features, feature_score))
        return result, selected_features, feature_score


    features_selected, selection, score = feature_selector_correlation(status_corr, 0.2)
    score = np.array(score).astype(float)

    featuresel = pd.DataFrame(selection, columns=['Features'])
    selected_features = [i for (i, j) in features_selected]
    new_df = df[selected_features]

    selected_features = [i for (i, j) in features_selected if i != 'phishing']
    selected_features.remove('domain_age')
    X_selected = new_df[selected_features]
    y = df['phishing']

    X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.10, random_state=1)
    # TRAIN LOGISTIC REGRESSION
    LRmodel = LogisticRegression(C=2, max_iter=10000, n_jobs=-1)
    LRmodel.fit(X_train, y_train)

    # TRAIN RANDOM FOREST
    RFmodel2 = RandomForestClassifier()
    RFmodel2.fit(X_train, y_train)

    # TRAIN NAIVE BAYES
    GNBmodel = GaussianNB()
    GNBmodel.fit(X_train, y_train)

    file = open('Phishing-RF.pickle', 'wb')
    pickle.dump(RFmodel2, file)
    file.close()

    file = open('Phishing-LR.pickle', 'wb')
    pickle.dump(LRmodel, file)
    file.close()

    file = open('Phishing-GNB.pickle', 'wb')
    pickle.dump(GNBmodel, file)
    file.close()

##########################################################################
#               PREDICTION PORTION
##########################################################################
file = open('./Phishing-RF.pickle', 'rb')
RFmodel = pickle.load(file)
file.close()
file = open('./Phishing-LR.pickle', 'rb')
LRmodel = pickle.load(file)
file.close()
file = open('./Phishing-GNB.pickle', 'rb')
GNBmodel = pickle.load(file)
file.close()

##########################################################################
#               URL hostname length URL and hostname
##########################################################################

def url_length(url):
    return len(url)


##########################################################################
#               Having IP address in hostname
##########################################################################

def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '[0-9a-fA-F]{7}', url)  # Ipv6
    if match:
        return 1
    else:
        return 0


##########################################################################
#              Count number of dots in hostname
##########################################################################

def count_dots(hostname):
    return hostname.count('.')


##########################################################################
#               Count question mark (?) symbol at base url
##########################################################################

def count_qm(base_url):
    return base_url.count('?')


##########################################################################
#               Count equal (=) symbol at base url
##########################################################################

def count_equal(base_url):
    return base_url.count('=')


##########################################################################
#               Count slash (/) symbol at full url
##########################################################################

def count_slash(full_url):
    return full_url.count('/')


##########################################################################
#               count www in url words (Sahingoz2019)
##########################################################################

def check_www(words_raw):
    count = 0
    for word in words_raw:
        if not word.find('www') == -1:
            count += 1
    return count


##########################################################################
#               Ratio of digits in hostname
##########################################################################

def ratio_digits(hostname):
    return len(re.sub("[^0-9]", "", hostname)) / len(hostname)


##########################################################################
#               Check if tld is used in the subdomain
##########################################################################

def tld_in_subdomain(tld, subdomain):
    if subdomain.count(tld) > 0:
        return 1
    return 0


##########################################################################
#               prefix suffix
##########################################################################

def prefix_suffix(url):
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        return 1
    else:
        return 0


##########################################################################
# shortest word length in raw word list (specifically call urlfe.shortest_word_length(words_raw_host))
##########################################################################

def shortest_word_length(words_raw):
    if len(words_raw) == 0:
        return 0
    return min(len(word) for word in words_raw)


##########################################################################
#               longest word length in raw word list
#               specifically call:
#               urlfe.longest_word_length(words_raw),
#               urlfe.longest_word_length(words_raw_host)
##########################################################################

def longest_word_length(words_raw):
    if len(words_raw) == 0:
        return 0
    return max(len(word) for word in words_raw)


##########################################################################
#               number of phish-hints in url path
##########################################################################

# LOCALHOST_PATH = "/var/www/html/"
HINTS = ['wp', 'login', 'includes', 'admin', 'content', 'site', 'images', 'js', 'alibaba', 'css', 'myaccount',
         'dropbox', 'themes', 'plugins', 'signin', 'view']


def phish_hints(url_path):
    count = 0
    for hint in HINTS:
        count += url_path.lower().count(hint)
    return count


##########################################################################
#               Number of hyperlinks present in a website (content_features)
##########################################################################
def nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
    return len(Href['internals']) + len(Href['externals']) + \
           len(Link['internals']) + len(Link['externals']) + \
           len(Media['internals']) + len(Media['externals']) + \
           len(Form['internals']) + len(Form['externals']) + \
           len(CSS['internals']) + len(CSS['externals']) + \
           len(Favicon['internals']) + len(Favicon['externals'])


# def nb_hyperlinks(dom):
#     return len(dom.find("href")) + len(dom.find("src"))

##########################################################################
#               Internal hyperlinks ratio (content features)
##########################################################################


def h_total(Href, Link, Media, Form, CSS, Favicon):
    return nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon)


def h_internal(Href, Link, Media, Form, CSS, Favicon):
    return len(Href['internals']) + len(Link['internals']) + len(Media['internals']) + \
           len(Form['internals']) + len(CSS['internals']) + len(Favicon['internals'])


def internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
    total = h_total(Href, Link, Media, Form, CSS, Favicon)
    if total == 0:
        return 0
    else:
        return h_internal(Href, Link, Media, Form, CSS, Favicon) / total


##########################################################################
#               Check for empty title (content features)
##########################################################################

def empty_title(Title):
    if Title:
        return 0
    return 1


##########################################################################
#              Domain in page title (content features)
##########################################################################

def domain_in_title(domain, title):
    if domain.lower() in title.lower():
        return 0
    return 1


##########################################################################
#               Domain age of a url (external feature)
##########################################################################
def domain_age(domain):
    url = domain.split("//")[-1].split("/")[0].split('?')[0]
    show = "https://input.payapi.io/v1/api/fraud/domain/age/" + url
    r = requests.get(show)

    if r.status_code == 200:
        data = r.text
        jsonToPython = json.loads(data)
        result = jsonToPython['result']
        if result == None:
            return -2
        else:
            return result
    else:
        return -1


##########################################################################
#               Google index (external feature)
##########################################################################


def google_index(url):
    # time.sleep(.6)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}
    query = {'q': 'site:' + url}
    google = "https://www.google.com/search?" + urlencode(query)
    data = requests.get(google, headers=headers)
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), "html.parser")
    try:
        if 'Our systems have detected unusual traffic from your computer network.' in str(soup):
            return -1
        check = soup.find(id="rso").find("div").find("div").find("a")
        if check and check['href']:
            return 0
        else:
            return 1

    except AttributeError:
        return 1


##########################################################################
#               Page Rank from OPR (external feature)
##########################################################################


def page_rank(key, domain):
    url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domain
    try:
        request = requests.get(url, headers={'API-OPR': key})
        result = request.json()
        result = result['response'][0]['page_rank_integer']
        if result:
            return result
        else:
            return 0
    except:
        return -1


# Open Page Rank API key
key = '08w0swog44g08wogcogo0k48c8g8k4gks8w8sk0w'


def get_domain(url):
    o = urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path


def getPageContent(url):
    parsed = urlparse(url)
    url = parsed.scheme + '://' + parsed.netloc
    try:
        page = requests.get(url)
    except:
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme + '://www.' + parsed.netloc
            page = requests.get(url)
    if page.status_code != 200:
        return None, None
    else:
        return url, page.content


def is_URL_accessible(url):
    # iurl = url
    # parsed = urlparse(url)
    # url = parsed.scheme+'://'+parsed.netloc
    page = None
    try:
        page = requests.get(url, timeout=5)
    except:
        parsed = urlparse(url)
        url = parsed.scheme + '://' + parsed.netloc
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme + '://www.' + parsed.netloc
            try:
                page = requests.get(url, timeout=5)
            except:
                page = None
                pass
        # if not parsed.netloc.startswith('www'):
        #     url = parsed.scheme+'://www.'+parsed.netloc
        #     #iurl = iurl.replace('https://', 'https://www.')
        #     try:
        #         page = requests.get(url)
        #     except:
        #         # url = 'http://'+parsed.netloc
        #         # iurl = iurl.replace('https://', 'http://')
        #         # try:
        #         #     page = requests.get(url)
        #         # except:
        #         #     if not parsed.netloc.startswith('www'):
        #         #         url = parsed.scheme+'://www.'+parsed.netloc
        #         #         iurl = iurl.replace('http://', 'http://www.')
        #         #         try:
        #         #             page = requests.get(url)
        #         #         except:
        #         #             pass
        #         pass
    if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
        return True, url, page
    else:
        return False, url, page


##########################################################################
#              Data Extraction Process
##########################################################################

def extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title,
                          Text):
    Null_format = ["", "#", "#nothing", "#doesnotexist", "#null", "#void", "#whatever",
                   "#content", "javascript::void(0)", "javascript::void(0);", "javascript::;", "javascript"]

    soup = BeautifulSoup(content, 'html.parser', from_encoding='iso-8859-1')

    # collect all external and internal hrefs from url
    for href in soup.find_all('a', href=True):
        dots = [x.start(0) for x in re.finditer('\.', href['href'])]
        if hostname in href['href'] or domain in href['href'] or len(dots) == 1 or not href['href'].startswith('http'):
            if "#" in href['href'] or "javascript" in href['href'].lower() or "mailto" in href['href'].lower():
                Anchor['unsafe'].append(href['href'])
            if not href['href'].startswith('http'):
                if not href['href'].startswith('/'):
                    Href['internals'].append(hostname + '/' + href['href'])
                elif href['href'] in Null_format:
                    Href['null'].append(href['href'])
                else:
                    Href['internals'].append(hostname + href['href'])
        else:
            Href['externals'].append(href['href'])
            Anchor['safe'].append(href['href'])

    # collect all media src tags
    for img in soup.find_all('img', src=True):
        dots = [x.start(0) for x in re.finditer('\.', img['src'])]
        if hostname in img['src'] or domain in img['src'] or len(dots) == 1 or not img['src'].startswith('http'):
            if not img['src'].startswith('http'):
                if not img['src'].startswith('/'):
                    Media['internals'].append(hostname + '/' + img['src'])
                elif img['src'] in Null_format:
                    Media['null'].append(img['src'])
                else:
                    Media['internals'].append(hostname + img['src'])
        else:
            Media['externals'].append(img['src'])

    for audio in soup.find_all('audio', src=True):
        dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
        if hostname in audio['src'] or domain in audio['src'] or len(dots) == 1 or not audio['src'].startswith('http'):
            if not audio['src'].startswith('http'):
                if not audio['src'].startswith('/'):
                    Media['internals'].append(hostname + '/' + audio['src'])
                elif audio['src'] in Null_format:
                    Media['null'].append(audio['src'])
                else:
                    Media['internals'].append(hostname + audio['src'])
        else:
            Media['externals'].append(audio['src'])

    for embed in soup.find_all('embed', src=True):
        dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
        if hostname in embed['src'] or domain in embed['src'] or len(dots) == 1 or not embed['src'].startswith('http'):
            if not embed['src'].startswith('http'):
                if not embed['src'].startswith('/'):
                    Media['internals'].append(hostname + '/' + embed['src'])
                elif embed['src'] in Null_format:
                    Media['null'].append(embed['src'])
                else:
                    Media['internals'].append(hostname + embed['src'])
        else:
            Media['externals'].append(embed['src'])

    for i_frame in soup.find_all('iframe', src=True):
        dots = [x.start(0) for x in re.finditer('\.', i_frame['src'])]
        if hostname in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1 or not i_frame['src'].startswith(
                'http'):
            if not i_frame['src'].startswith('http'):
                if not i_frame['src'].startswith('/'):
                    Media['internals'].append(hostname + '/' + i_frame['src'])
                elif i_frame['src'] in Null_format:
                    Media['null'].append(i_frame['src'])
                else:
                    Media['internals'].append(hostname + i_frame['src'])
        else:
            Media['externals'].append(i_frame['src'])

    # collect all link tags
    for link in soup.findAll('link', href=True):
        dots = [x.start(0) for x in re.finditer('\.', link['href'])]
        if hostname in link['href'] or domain in link['href'] or len(dots) == 1 or not link['href'].startswith('http'):
            if not link['href'].startswith('http'):
                if not link['href'].startswith('/'):
                    Link['internals'].append(hostname + '/' + link['href'])
                elif link['href'] in Null_format:
                    Link['null'].append(link['href'])
                else:
                    Link['internals'].append(hostname + link['href'])
        else:
            Link['externals'].append(link['href'])

    for script in soup.find_all('script', src=True):
        dots = [x.start(0) for x in re.finditer('\.', script['src'])]
        if hostname in script['src'] or domain in script['src'] or len(dots) == 1 or not script['src'].startswith(
                'http'):
            if not script['src'].startswith('http'):
                if not script['src'].startswith('/'):
                    Link['internals'].append(hostname + '/' + script['src'])
                elif script['src'] in Null_format:
                    Link['null'].append(script['src'])
                else:
                    Link['internals'].append(hostname + script['src'])
        else:
            Link['externals'].append(link['href'])

    # collect all css
    for link in soup.find_all('link', rel='stylesheet'):
        dots = [x.start(0) for x in re.finditer('\.', link['href'])]
        if hostname in link['href'] or domain in link['href'] or len(dots) == 1 or not link['href'].startswith('http'):
            if not link['href'].startswith('http'):
                if not link['href'].startswith('/'):
                    CSS['internals'].append(hostname + '/' + link['href'])
                elif link['href'] in Null_format:
                    CSS['null'].append(link['href'])
                else:
                    CSS['internals'].append(hostname + link['href'])
        else:
            CSS['externals'].append(link['href'])

    for style in soup.find_all('style', type='text/css'):
        try:
            start = str(style[0]).index('@import url(')
            end = str(style[0]).index(')')
            css = str(style[0])[start + 12:end]
            dots = [x.start(0) for x in re.finditer('\.', css)]
            if hostname in css or domain in css or len(dots) == 1 or not css.startswith('http'):
                if not css.startswith('http'):
                    if not css.startswith('/'):
                        CSS['internals'].append(hostname + '/' + css)
                    elif css in Null_format:
                        CSS['null'].append(css)
                    else:
                        CSS['internals'].append(hostname + css)
            else:
                CSS['externals'].append(css)
        except:
            continue

    # collect all form actions
    for form in soup.findAll('form', action=True):
        dots = [x.start(0) for x in re.finditer('\.', form['action'])]
        if hostname in form['action'] or domain in form['action'] or len(dots) == 1 or not form['action'].startswith(
                'http'):
            if not form['action'].startswith('http'):
                if not form['action'].startswith('/'):
                    Form['internals'].append(hostname + '/' + form['action'])
                elif form['action'] in Null_format or form['action'] == 'about:blank':
                    Form['null'].append(form['action'])
                else:
                    Form['internals'].append(hostname + form['action'])
        else:
            Form['externals'].append(form['action'])

    # collect all link tags
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
            if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link[
                'href'].startswith('http'):
                if not head.link['href'].startswith('http'):
                    if not head.link['href'].startswith('/'):
                        Favicon['internals'].append(hostname + '/' + head.link['href'])
                    elif head.link['href'] in Null_format:
                        Favicon['null'].append(head.link['href'])
                    else:
                        Favicon['internals'].append(hostname + head.link['href'])
            else:
                Favicon['externals'].append(head.link['href'])

        for head.link in soup.findAll('link', {'href': True, 'rel': True}):
            isicon = False
            if isinstance(head.link['rel'], list):
                for e_rel in head.link['rel']:
                    if (e_rel.endswith('icon')):
                        isicon = True
            else:
                if (head.link['rel'].endswith('icon')):
                    isicon = True

            if isicon:
                dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link[
                    'href'].startswith('http'):
                    if not head.link['href'].startswith('http'):
                        if not head.link['href'].startswith('/'):
                            Favicon['internals'].append(hostname + '/' + head.link['href'])
                        elif head.link['href'] in Null_format:
                            Favicon['null'].append(head.link['href'])
                        else:
                            Favicon['internals'].append(hostname + head.link['href'])
                else:
                    Favicon['externals'].append(head.link['href'])

    # collect i_frame
    for i_frame in soup.find_all('iframe', width=True, height=True, frameborder=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameborder'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, border=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['border'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, style=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['style'] == "border:none;":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)

    # get page title
    try:
        Title = soup.title.string
    except:
        pass

    # get content text
    Text = soup.get_text()

    return Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text


##########################################################################
#              Calculate features from extracted data
##########################################################################


def extract_features(url):
    def words_raw_extraction(domain, subdomain, path):
        w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
        w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())
        w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
        raw_words = w_domain + w_path + w_subdomain
        w_host = w_domain + w_subdomain
        raw_words = list(filter(None, raw_words))
        return raw_words, list(filter(None, w_host)), list(filter(None, w_path))

    Href = {'internals': [], 'externals': [], 'null': []}
    Link = {'internals': [], 'externals': [], 'null': []}
    Anchor = {'safe': [], 'unsafe': [], 'null': []}
    Media = {'internals': [], 'externals': [], 'null': []}
    Form = {'internals': [], 'externals': [], 'null': []}
    CSS = {'internals': [], 'externals': [], 'null': []}
    Favicon = {'internals': [], 'externals': [], 'null': []}
    IFrame = {'visible': [], 'invisible': [], 'null': []}
    Title = ''
    Text = ''
    state, iurl, page = is_URL_accessible(url)
    if state:
        content = page.content
        hostname, domain, path = get_domain(url)
        extracted_domain = tldextract.extract(url)
        domain = extracted_domain.domain + '.' + extracted_domain.suffix
        subdomain = extracted_domain.subdomain
        tmp = url[url.find(extracted_domain.suffix):len(url)]
        pth = tmp.partition("/")
        path = pth[1] + pth[2]
        words_raw, words_raw_host, words_raw_path = words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
        tld = extracted_domain.suffix
        parsed = urlparse(url)
        scheme = parsed.scheme

        Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text = extract_data_from_URL(hostname, content,
                                                                                                   domain, Href, Link,
                                                                                                   Anchor, Media, Form,
                                                                                                   CSS, Favicon, IFrame,
                                                                                                   Title, Text)

        row = [  # url-based features
            url_length(url),
            url_length(hostname),
            having_ip_address(url),
            count_dots(url),
            count_qm(url),
            count_equal(url),
            count_slash(url),
            check_www(words_raw),
            ratio_digits(url),
            ratio_digits(hostname),
            tld_in_subdomain(tld, subdomain),
            prefix_suffix(url),
            shortest_word_length(words_raw_host),
            longest_word_length(words_raw),
            longest_word_length(words_raw_path),
            phish_hints(url),
            # # # content-based features
            nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon),
            internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon),
            empty_title(Title),
            domain_in_title(extracted_domain.domain, Title),
            # # # thirs-party-based features
            # domain_age(domain),
            google_index(url),
            page_rank(key, domain),
        ]
        return row
    return None


def predict1(res):
    # Returns a 3-digit binary. 1->Malicious, 0->Normal
    # Digit 1: Random Forest
    # Digit 2: Logistic Regression
    # Digit 1: Gaussian Naive-Bayes
    prediction = ""
    prediction += str(RFmodel.predict(res)[0])
    prediction += str(LRmodel.predict(res)[0])
    prediction += str(GNBmodel.predict(res)[0])
    return prediction


def parseURL(input):
    res = extract_features(input)

    if isinstance(res, list):
        res = np.array(res)
        res = np.reshape(res, (1, -1))
        parsed = pd.DataFrame(res, columns=['length_url',
                                            'length_hostname',
                                            'ip',
                                            'nb_dots',
                                            'nb_qm',
                                            'nb_eq',
                                            'nb_slash',
                                            'nb_www',
                                            'ratio_digits_url',
                                            'ratio_digits_host',
                                            'tld_in_subdomain',
                                            'prefix_suffix',
                                            'shortest_word_host',
                                            'longest_words_raw',
                                            'longest_word_path',
                                            'phish_hints',
                                            'nb_hyperlinks',
                                            'ratio_intHyperlinks',
                                            'empty_title',
                                            'domain_in_title',
                                            'google_index',
                                            'page_rank'])
        return predict1(parsed)
    else:
        err_out("Could not resolve URL", "unreachable")
        #err_out("Link returns an HTTP Error. Here are possible reasons: \n1. Malware \n2. Page is no longer available \n3. Website owners forbid access due to copyright")


# RESULT: Random Forest | Logistic Regression | Gaussian Naive-Bayes
program_output["msg"] = parseURL(prediction_url)
print(json.dumps(program_output))
