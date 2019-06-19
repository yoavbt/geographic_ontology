# Onotology creation for Countries
Creating ontology with the following:
## relations:
- area
- population
- government
- capital
- prime minister
- president

# NLP and ontology quering with sparql
## structure of questions:
- Who is the president of country_name?
- Who is the prime minister of country_name? 
- What is the population of country_name?
- What is the area of country_name?
- What is the government of country_name?
- What is the capital of country_name?
- When was the president of country_name born?
- When was the prime minister of country_name born?
- Who is entity_name? 

# Examples
- Who is the president of Italy? **Sergio Mattarella**
- Who is the prime minister of United Kingdom? **Theresa May**
- What is the population of Democratic Republic of the Congo? **78,736,153**

# How to run
 - python geo_qa.py create ontology.nt
 - python geo_qa.py question natural_language_question_string
