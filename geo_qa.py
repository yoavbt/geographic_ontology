import sys
import rdflib
import requests
import lxml.html


def create_ontology(ontology):
    wiki_prefix = "http://en.wikipedia.org"
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)'
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath('//table[contains(@class, "wikitable")]//tbody//tr//td[2]//a/@href')
    countries = list(filter(lambda x: not '#' in x, a))[1:]
    counter = [0]
    for country in countries:
        res = requests.get(wiki_prefix + country)
        extract_prime_minister(res , counter)
    print('number of countries with capital is: ' + str(counter[0]))


def extract_president(res, counter):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'President')]/../../following-sibling::td/a/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        counter[0] += 1
        print(a[0], country[0])


def extract_prime_minister(res, counter):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'Prime Minister')]/../../following-sibling::td/a/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        counter[0] += 1
        print(a[0], country[0])


def extract_population(res, counter):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th/a[contains(text(),'Population')]/../../following-sibling::tr/td/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        counter[0] += 1
        print(a[0], country[0])


def extract_area (res, counter):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th/a[contains(text(), 'Area')]/../../following-sibling::tr/td/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        counter[0] += 1
        print(a[0], country[0])


def extract_government(res, counter):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th/a[contains(text(),'Government')]/../following-sibling::td/a")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        counter[0] += 1
        print(a[0], country[0])


def extract_capital(res , counter):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th[contains(text(),'Capital')]/following-sibling::td//a[1]/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        counter[0] += 1
        print(a[0], country[0])


def nlp_process(arr_of_words):
    print(arr_of_words)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Bad input')
        exit(1)
    cmd = sys.argv[1]
    if cmd == 'create':
        create_ontology(sys.argv[2])
    elif cmd == 'question':
        nlp_process(sys.argv[2:])
    else:
        print('not a valid cmd')
        exit(1)

