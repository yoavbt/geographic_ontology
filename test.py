import sys
import rdflib
import requests
import lxml.html

def firstQ(g):
    print("Number of prime ministers")
    q = "SELECT (COUNT(?s) AS ?triples) WHERE { ?s <http://example.org/prime_minister_of> ?o }"
    x1 = g.query(q)
    for row in x1:
        print("%s" % row)

def secondQ(g):
    print("Number of countries")
    q = "SELECT (COUNT(?s) AS ?triples) WHERE { ?s <http://example.org/capital_of> ?o }"
    x1 = g.query(q)
    for row in x1:
        print("%s" % row)


def thirdQ(g):
    print("Number of countries that are republic")
    q = "SELECT (COUNT(?s) AS ?triples) WHERE { ?s <http://example.org/government> ?o  .FILTER regex(str(?o), 'republic')}"
    x1 = g.query(q)
    for row in x1:
        print("%s" % row)

def fourthQ(g):
    print("Number of countries that are monarchy")
    q = "SELECT (COUNT(?s) AS ?triples) WHERE { ?s <http://example.org/government> ?o  .FILTER regex(str(?o), 'monarchy')}"
    x1 = g.query(q)
    for row in x1:
        print("%s" % row)

if __name__ == '__main__':
    print("Output")
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    firstQ(g1)
    secondQ(g1)
    thirdQ(g1)
    fourthQ(g1)