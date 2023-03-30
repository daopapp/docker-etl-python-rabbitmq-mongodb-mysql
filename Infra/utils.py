from datetime import datetime


# Tratamento de Data
def strtodate(date):
    if date:
        if '-' in date:
            return datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            return datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
    else:
        return None


def get_min_value(data_list, key):
    values = [strtodate(doc.get(key)) for doc in data_list if strtodate(doc.get(key)) is not None]
    if values:
        return min(values)
    else:
        return None


# Retornar maior Data dos objetos
def get_max_value(data_list, key):
    values = [strtodate(doc.get(key)) for doc in data_list if strtodate(doc.get(key)) is not None]
    if values:
        return max(values)
    else:
        return None
