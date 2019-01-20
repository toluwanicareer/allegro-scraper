import csv
unicode=str
def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'latin-1'):unicode(value, 'latin-1') for key, value in row.iteritems()}