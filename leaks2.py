import csv
from itertools import groupby
from functools import reduce


selected_source = 'Panama'

sources = {
    'Panama': 'panama_papers',
    'Bahamas': 'bahamas_leaks',
    'Offshore': 'offshore_leaks',
    'Paradise': 'paradise_papers'
}

def select_source(name):
    global selected_source
    if (name in sources):
        selected_source = name
        print('Source selected:', selected_source)
    else:
        print('No such source! Valid values:', ', '.join(list(sources)))

def load_file(name):
    filename = f'{selected_source}/{sources[selected_source]}.{name}.csv'
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)

def show_column_names(name):
    filename = f'{selected_source}/{sources[selected_source]}.{name}.csv'
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        return next(csv_reader)

if __name__ == '__main__':

    # print(load_file('nodes.officer')[:10])

    print('Loading officer countries...')
    officers = {row['node_id']: row['countries'] for row in load_file('nodes.officer') if row['countries']}

    print('Loading entity countries...')
    entities = {row['node_id']: row['countries'] for row in load_file('nodes.entity') if row['countries']}

    print('Combining data by edges...')
    edges = [
        # (officer's country, entity's country)
        (officers[row['START_ID']], entities[row['END_ID']])
        for row in load_file('edges')
        # filter edges to skip empty values and non-existing officers and entities
        if (row['TYPE'] == 'officer_of') and (row['START_ID'] in officers) and (row['END_ID'] in entities)
    ]

    print('Calculating stats...')
    func_key = lambda x: x[0]
    
    def calc_stats(group, officer_country):
        items = [x[1] for x in group]
        return {
            'num_total_entities': len(items),
            'percent_domestic_entities': round(100 * len([c for c in items if c == officer_country]) / len(items), 3),
            'country_variety': len(set(items)),
        }

    result = {
        officer_country: calc_stats(group, officer_country)
        for officer_country, group in groupby(sorted(edges, key=func_key), func_key)
    }

    # print(result['Albania'])

    print('>' * 40)

    print('Top 50 countries where officers prefer foreign entities:')
    i = 1
    for country, stats in sorted(result.items(), key=lambda item: item[1]['percent_domestic_entities'])[:50]:
        print(f'{i:-3} : {country:30} : {100 - stats["percent_domestic_entities"]:-7}%')
        i = i + 1

    print('-' * 40)

    print('Top 50 countries where officers prefer domestic entities:')
    i = 1
    for country, stats in sorted(result.items(), key=lambda item: item[1]['percent_domestic_entities'], reverse=True)[:50]:
        print(f'{i:-3} : {country:30} : {stats["percent_domestic_entities"]:-7}%')
        i = i + 1

    print('-' * 40)

    print('Top 20 countries where officers have entities in the widest variety of countries:')
    i = 1
    for country, stats in sorted(result.items(), key=lambda item: item[1]['country_variety'], reverse=True)[:20]:
        print(f'{i:-3} : {country:30} : {stats["country_variety"]:-4}')
        i = i + 1

    print('>>> EOF')
