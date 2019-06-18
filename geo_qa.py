import sys
import rdflib
import requests
import lxml.html


def create_ontology(ontology):
    g = rdflib.Graph()
    wiki_prefix = "http://en.wikipedia.org"
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)'
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath('//table[contains(@class, "wikitable")]//tbody//tr//td[2]//a/@href')
    countries = list(filter(lambda x: not '#' in x, a))[1:]
    for country in countries:
        res = requests.get(wiki_prefix + country)
        extract_president(res, g)
        extract_prime_minister(res, g)
        extract_population(res, g)
        extract_area(res, g)
        extract_government(res, g)
        extract_capital(res, g)
    g.serialize(ontology, format="nt")


def extract_president(res, g):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'President')]/../../following-sibling::td/a/text()")
    relative_link = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'President')]/../../following-sibling::td/a/@href")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0 and len(relative_link) > 0:
        country_name = rdflib.URIRef('http://example.org/' + country[0].lower().replace(' ', '_'))
        president = rdflib.URIRef('http://example.org/' + a[0].lower().replace(' ', '_'))
        presidentOf = rdflib.URIRef('http://example.org/president_of')
        g.add((country_name, presidentOf, president))
        extract_president_info(relative_link[0], country[0], president, g)
        print(a[0], country[0])


def extract_president_info(relative_link, country, president, g):
    wiki_prefix = "http://en.wikipedia.org"
    res = requests.get(wiki_prefix + relative_link)
    doc = lxml.html.fromstring(res.content)
    title = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'President')]//text()")
    birthday = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th[contains(text() ,'Born')]/following-sibling::td/text()")
    if len(title) > 0 and len(birthday) > 0:
        g.add((president, rdflib.URIRef('http://example.org/' + 'born_in'),
               rdflib.URIRef('http://example.org/' + birthday[0].lower().replace(' ', '_'))))
        g.add((president, rdflib.URIRef('http://example.org/' + 'is'),
               rdflib.URIRef('http://example.org/' + title[0].lower().replace(' ', '_'))))
        print(country, title[0], birthday[0])


def extract_prime_minister_info(relative_link, country, prime_minister, g):
    wiki_prefix =  "http://en.wikipedia.org"
    res = requests.get(wiki_prefix + relative_link)
    doc = lxml.html.fromstring(res.content)
    title = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'Prime Minister')]//text()")
    birthday = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th[contains(text() ,'Born')]/following-sibling::td/text()")
    if len(title) > 0 and len(birthday) > 0:
        g.add((prime_minister, rdflib.URIRef('http://example.org/born_in'),
               rdflib.URIRef('http://example.org/' + birthday[0].lower().replace(' ', '_'))))
        g.add((prime_minister, rdflib.URIRef('http://example.org/is'),
               rdflib.URIRef('http://example.org/' + title[0].lower().replace(' ', '_'))))
        print(country, title[0], birthday[0])


def extract_prime_minister(res, g):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'Prime Minister')]/../../following-sibling::td/a/text()")
    relative_link = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th//a[contains(text(),'Prime Minister')]/../../following-sibling::td/a/@href")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0 and len(relative_link) > 0:
        country_name = rdflib.URIRef('http://example.org/' + country[0].lower().replace(' ', '_'))
        prime_minister = rdflib.URIRef('http://example.org/' + a[0].lower().replace(' ', '_'))
        prime_minister_of = rdflib.URIRef('http://example.org/' + 'prime_minister_of')
        g.add((country_name, prime_minister_of, prime_minister))
        extract_prime_minister_info(relative_link[0], country[0], prime_minister, g)
        print(a[0], country[0])


def extract_population(res, g):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th/a[contains(text(),'Population')]/../../following-sibling::tr/td/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        country_name = rdflib.URIRef('http://example.org/' + country[0].lower().replace(' ', '_'))
        country_population = rdflib.URIRef('http://example.org/' + a[0].split(' ')[0])
        population = rdflib.URIRef('http://example.org/' + 'population')
        g.add((country_name, population, country_population))
        print(a[0].split(' ')[0], country[0])


def extract_area(res, g):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th/a[contains(text(), 'Area')]/../../following-sibling::tr/td/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        country_name = rdflib.URIRef('http://example.org/' + country[0].lower().replace(' ', '_'))
        area_country = rdflib.URIRef('http://example.org/' + a[0].split(' ')[0])
        area = rdflib.URIRef('http://example.org/' + 'area')
        g.add((country_name, area, area_country))
        print(a[0].split(' ')[0], country[0])


def extract_government(res, g):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th/a[contains(text(),'Government')]/../following-sibling::td/a/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        country_name = rdflib.URIRef('http://example.org/' + country[0].lower().replace(' ', '_'))
        government_country = rdflib.URIRef('http://example.org/' + '_'.lower().join(a).replace(' ' ,'_'))
        government = rdflib.URIRef('http://example.org/' + 'government')
        g.add((country_name, government, government_country))
        print(a)
        print('_'.lower().join(a).replace(' ' ,'_'))


def extract_capital(res, g):
    doc = lxml.html.fromstring(res.content)
    a = doc.xpath(
        "//table[contains(@class, 'infobox')][1]//tbody//th[contains(text(),'Capital')]/following-sibling::td//a[1]/text()")
    country = doc.xpath('//h1[1]//text()')
    if len(a) > 0:
        country_name = rdflib.URIRef('http://example.org/' + country[0].lower().replace(' ', '_'))
        capital_country = rdflib.URIRef('http://example.org/' + a[0].lower().replace(' ', '_'))
        capital_of = rdflib.URIRef('http://example.org/' + 'capital_of')
        g.add((country_name, capital_of, capital_country))
        print(a[0], country[0])


def nlp_process(arr_of_words, g1):
    qst = arr_of_words[0]
    if qst == "What":
        handleWhat(arr_of_words, g1)
    elif qst == "Who":
        handleWho(arr_of_words, g1)
    elif qst == "When":
        handleWhen(arr_of_words, g1)
    else:
        print("Not part of the question structure...")


def handleWhen(arr_of_words, g):
    relation = arr_of_words[3]
    del arr_of_words[-1]
    if relation == "president":
        country = "<http://example.org/" + '_'.join(arr_of_words[5:]).lower() + ">"
        q = "select ?d where { " + country + " <http://example.org/president_of> ?c . ?c <http://example.org/born_in> ?d}"
        x1 = g.query(q)
        for row in x1:
            print(("%s" % row).split('/')[3].replace("_", " "))
    elif relation == "prime":
        if arr_of_words[4] != "minister":
            print("Dont try to fool me..")
            return
        country = "<http://example.org/" + '_'.join(arr_of_words[6:]).lower() + ">"
        q = "select ?d where { " + country + " <http://example.org/prime_minister_of> ?c . ?c <http://example.org/born_in> ?d}"
        x1 = g.query(q)
        for row in x1:
            print(("%s" % row).split('/')[3].replace("_", " ").title())
    else:
        print("Bad format of the 'When' structure")


def handleWho(arr_of_words, g):
    if len(arr_of_words) < 3:
        print("Bad format of the 'Who' structure")
        return
    if arr_of_words[2] == "the":
        relation = arr_of_words[3]
        if relation == "president":
            country = "<http://example.org/" + '_'.join(arr_of_words[5:]).lower() + ">"
            q = "select ?c where { " + country + " <http://example.org/president_of> ?c }"
            x1 = g.query(q)
            for row in x1:
                print(("%s" % row).split('/')[3].replace("_", " ").title())
        elif relation == "prime":
            if arr_of_words[4] != "minister":
                print("Dont try to fool me..")
                return
            country = "<http://example.org/" + '_'.join(arr_of_words[6:]).lower() + ">"
            q = "select ?c where { " + country + " <http://example.org/prime_minister_of> ?c }"
            x1 = g.query(q)
            for row in x1:
                print(("%s" % row).split('/')[3].replace("_", " ").title())
        else:
            print("Bad format of the 'Who' structure")
    else:
        entity = "<http://example.org/" + '_'.join(arr_of_words[2:]).lower() + ">"
        q = "select ?c where { " + entity + " <http://example.org/is> ?c }"
        x1 = g.query(q)
        for row in x1:
            print(("%s" % row).split('/')[3].replace("_", " ").title())


def handleWhat(arr_of_words, g):
    relation = arr_of_words[3]
    if relation == "population":
        country = "<http://example.org/" + '_'.join(arr_of_words[5:]).lower() + ">"
        q = "select ?c where { " + country + " <http://example.org/population> ?c }"
        x1 = g.query(q)
        for row in x1:
            print(("%s" % row).split('/')[3].replace("_", " "))
    elif relation == "area":
        country = "<http://example.org/" + '_'.join(arr_of_words[5:]).lower() + ">"
        q = "select ?c where { " + country + " <http://example.org/area> ?c }"
        x1 = g.query(q)
        for row in x1:
            print(("%s" % row).split('/')[3].split('\xa0')[0] + " km2")
    elif relation == "government":
        country = "<http://example.org/" + '_'.join(arr_of_words[5:]).lower() + ">"
        q = "select ?c where { " + country + " <http://example.org/government> ?c }"
        x1 = g.query(q)
        for row in x1:
            print(("%s" % row).split('/')[3].replace("_", " "))
    elif relation == "capital":
        country = "<http://example.org/" + '_'.join(arr_of_words[5:]).lower() + ">"
        q = "select ?c where { " + country + " <http://example.org/capital_of> ?c }"
        x1 = g.query(q)
        for row in x1:
            print(("%s" % row).split('/')[3].replace("_", " ").title())
    else:
        print("Bad format of the 'What' structure")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Bad input')
        exit(1)
    cmd = sys.argv[1]
    if cmd == 'create':
        create_ontology(sys.argv[2])
    elif cmd == 'question':
        g1 = rdflib.Graph()
        try:
            g1.parse("ontology.nt", format="nt")
        except:
            create_ontology("ontology.nt")
            g1.parse("ontology.nt", format="nt")
        nlp_process(sys.argv[2:], g1)
    else:
        print('not a valid cmd')
        exit(1)
