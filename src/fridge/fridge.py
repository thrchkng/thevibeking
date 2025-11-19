import datetime
from decimal import Decimal

def add(items, title, amount, expiration_date=None):
    if expiration_date is not None:
        if isinstance(expiration_date, str):
            year, month, day = map(int, expiration_date.split('-'))
            expiration_date = datetime.date(year, month, day)
    
    new_batch = {
        'amount': amount if isinstance(amount, Decimal) else Decimal(str(amount)),
        'expiration_date': expiration_date
    }
    
    if title in items:
        items[title].append(new_batch)
    else:
        items[title] = [new_batch]

def add_by_note(items, note):
    parts = note.split()
    
    expiration_date = None
    if len(parts) >= 3 and '-' in parts[-1]:
        try:
            date_str = parts.pop()
            year, month, day = map(int, date_str.split('-'))
            expiration_date = datetime.date(year, month, day)
        except (ValueError, IndexError):
            parts.append(date_str)
    
    amount_str = parts.pop()
    try:
        amount = Decimal(amount_str)
    except:
        parts.append(amount_str)
        amount = Decimal('1')
    
    title = ' '.join(parts)
    
    add(items, title, amount, expiration_date)

def find(items, needle):
    needle_lower = needle.lower()
    
    found_products = []
    for product_name in items.keys():
        if needle_lower in product_name.lower():
            found_products.append(product_name)
    
    return found_products

def amount(items, needle):
    needle_lower = needle.lower()
    
    total_amount = Decimal('0')
    
    for product_name, batches in items.items():
        if needle_lower in product_name.lower():
            for batch in batches:
                total_amount += batch['amount']
    
    return total_amount
