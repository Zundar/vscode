def find_keys_with_substring(data_dict, substring):
    results = []
    
    def recursive_search(d, parent_key=''):
        for key, value in d.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if substring in key:
                results.append((full_key, value))
            if isinstance(value, dict):
                recursive_search(value, full_key)
    
    recursive_search(data_dict)
    return results

# Пример словаря с вложенными полями
data_dict = {
    'ucpid_example1': 'value1',
    'some_other_key': {
        'nested_ucpid_key': 'value2',
        'deeply': {
            'deep_ucpid_key': 'value3'
        }
    },
    'not_related_key': 'value4'
}

substring = 'ucpid'
matching_items = find_keys_with_substring(data_dict, substring)

# Выводим ключи и значения
for key, value in matching_items:
    print(f'Key: {key}, Value: {value}')