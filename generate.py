#!/usr/bin/env python3

from decimal import *
import json

CATEGORY_AF_BACKERS = 'af_backers'
CATEGORY_EARLY_CORE_CONTRIBUTORS = 'early_core_contributors'
CATEGORY_RD_ECOSYSTEM_DEV = 'r&d_ecosystem_dev'
CATEGORY_PUBLIC_ALLOCATIONS_COMPLETED = 'public_allocations_completed'
CATEGORY_PUBLIC_ALLOCATIONS_FUTURE = 'public_allocations_future'

categories = [
  CATEGORY_AF_BACKERS,
  CATEGORY_EARLY_CORE_CONTRIBUTORS,
  CATEGORY_RD_ECOSYSTEM_DEV,
  CATEGORY_PUBLIC_ALLOCATIONS_COMPLETED,
  CATEGORY_PUBLIC_ALLOCATIONS_FUTURE
]

allocations = []
total_allocations = Decimal('0')
unam_per_nam = Decimal('1000000') # 1 million
total_supply = Decimal('1000000000') * unam_per_nam # 1 billion

# Load allocations for each category
for c in categories:
  with open('data/{}.json'.format(c), 'r') as f:
    data = json.load(f)
    allocations_in_category = Decimal('0')
    for allocation in data:
      allocations_in_category += Decimal(allocation['amount'])
      allocations.append(allocation)
    print('Total allocations in category {}: {} ({} %)'.format(
        c,
        allocations_in_category / unam_per_nam,
        Decimal('100') * allocations_in_category / total_supply
    ))
    total_allocations += allocations_in_category

print('Total allocations: {} ({} %)'.format(
    total_allocations / unam_per_nam,
    Decimal('100') * total_allocations / total_supply
))

# Add together multiple allocations to the same address
obj = {}
for alloc in allocations:
  addr = alloc['address']
  tokens = alloc['amount']
  if addr in obj:
    obj[addr]['amount'] += tokens
    obj[addr]['categories'] = obj[addr]['categories'].union(set([alloc['category']]))
  else:
    obj[addr] = alloc
    obj[addr]['categories'] = set([obj[addr]['category']])
allocations = [obj[addr] for addr in obj]

def format_allocation_line(allocation):
    line = '{} = "{:.6f}"'.format(allocation['address'], Decimal(allocation['amount']) / unam_per_nam)
    categories = sorted(list(allocation['categories']))
    line += ' # (categories: {})'.format(categories)
    if 'name' in allocation:
        line += ' (name: {})'.format(allocation['name'])
    return line

allocations.sort(key = lambda x: x['amount'], reverse = True)

output = \
'''[token.NAM]

{}
'''.format('\n'.join([format_allocation_line(a) for a in allocations]))

with open('balances.toml', 'w') as file_handle:
  file_handle.write(output)

print('Allocations written to balances.toml')

multisigs = json.load(open('data/multisigs.json'))
print('Configuring {} multisig accounts'.format(len(multisigs)))

def make_multisig(x):
  return '''# {}
[[established_account]]
vp = "vp_user"
threshold = {}
public_keys = {}'''.format(x[2], x[1], json.dumps(x[0]))

transactions = \
'''# Genesis multisignature accounts

{}
'''.format('\n\n'.join(make_multisig(x) for x in multisigs))

with open('transactions.toml', 'w') as file_handle:
  file_handle.write(transactions)

print('Multisigs written to transactions.toml')
