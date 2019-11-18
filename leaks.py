import csv
import operator

# filename = 'Panama/panama_papers.nodes.entity.csv'

def get_column_names(filename):
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        return next(csv_reader)

def get_first_n_rows(filename, n = 100):
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for i in range(n):
            print(i, ":", next(csv_reader))

def get_num_rows(filename):
    rows = 0
    with open(filename, encoding='utf-8') as csv_file:
        for i in csv_file:
            rows = rows + 1
        return rows - 1

def is_home_market(x):
    return x[0] in ['SWE', 'LVA', 'LTU', 'EST']


def count_values(filename, field = 'country_codes'):
    value_dict = {}
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            value = row[field]
            if not value in value_dict:
                value_dict[value] = 1
            else:
                value_dict[value] = value_dict[value] + 1

        sorted_dict = sorted(value_dict.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_dict


def count_values_home_market(filename, field = 'country_codes'):
    home_market = ['SWE', 'EST', 'LVA', 'LTU']
    value_dict = {}
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        rows = 0

        for row in csv_reader:
            rows = rows + 1
            value = row[field]
            if not value in home_market:
                continue
            if not value in value_dict:
                value_dict[value] = 1
            else:
                value_dict[value] = value_dict[value] + 1

        sorted_dict = sorted(value_dict.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'count': sorted_dict,
            'percentage': [(country, str(round((count / rows) * 100, 3)) + '%') for country, count in sorted_dict]
        }

def print_tuples(tuple_list):
    for t in tuple_list:
        print('{0:3} : {1:-6}'.format(*t))

filename = input('Enter path and filename: ')

print('Total rows:', get_num_rows(filename))

print('-' * 40)

print('Summary by all countries:')
print_tuples(count_values(filename))

print('-' * 40)

print('Summary by home market:')
print(count_values_home_market(filename))
