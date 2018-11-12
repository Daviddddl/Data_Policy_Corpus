import requests
from lxml import etree

base_link = 'https://www.kegg.jp/dbget-bin/www_bget?ds:H00'
disease_id = 261


def entry(each_tr):
    return each_tr.xpath('string(./td/table/tr/td[1]/code/nobr)').strip()


def brite(each_tr):
    return each_tr.xpath('string(./td/table/tr/td[1]/code/nobr)').strip()


def gene(each_tr):
    value = each_tr.xpath('string(./td/div)').strip() + '\n'
    for each_link in each_tr.xpath('./td/div/a'):
        value += "https://www.kegg.jp" + each_link.xpath('./@href')[0] + '\n'
    return value


def pathway(each_tr):
    value = each_tr.xpath('string(./td/table/tr/td[1]/nobr/a)').strip()
    value += each_tr.xpath('string(./td/table/tr/td[2])').strip() + '\n'
    value += "https://www.kegg.jp" + each_tr.xpath('./td/table/tr/td[1]/nobr/a/@href')[0]
    return value


def network(each_tr):
    value = ''
    for each_table in each_tr.xpath('./td/table'):
        value += each_table.xpath('string(./tr/td[1]/nobr)') + each_table.xpath('string(./tr/td[2])') + '\n'
        value += "https://www.kegg.jp" + each_table.xpath('./tr/td[1]/nobr/a/@href')[0] + '\n'
    return value


def other_DBs(each_tr):
    tables = each_tr.xpath('./td/table')
    value = ''
    for each_table in tables:
        value += str(each_table.xpath('./tr/td[1]/nobr/text()')[0])
        value += str(each_table.xpath('./tr/td[2]/a/text()')[0]) + '\n'
        value += "https://www.kegg.jp" + each_table.xpath('./tr/td[2]/a/@href')[0] + '\n'
    return tables


def linkDB():
    return "https://www.genome.jp/dbget-bin/get_linkdb?disease+"


def otherCondition(each_tr):
    return each_tr.xpath('string(./td/div)').strip()


def get_each_tr(each_tr, key):
    choice = {
        'Entry': entry,
        'Brite': brite,
        'Gene': gene,
        'Pathway': pathway,
        'Network': network,
        'Other DBs': other_DBs,
        'LinkDB': linkDB
    }
    result = choice.get(key)
    if result:
        return result(each_tr)
    else:
        return otherCondition(each_tr)


page = requests.get(base_link + str(disease_id)).content.decode("utf-8")
tr_list = etree.HTML(page).xpath('//*[@name="form1"]/table/tr/td/table/tr')
res_f = open('disease_data/' + str(disease_id) + '.txt', 'w+')

for each_tr in tr_list:
    key = each_tr.xpath('string(./th/nobr)')
    value = get_each_tr(each_tr, key)
    print(value)
    res_f.write(key + ": " + str(value))

res_f.close()
