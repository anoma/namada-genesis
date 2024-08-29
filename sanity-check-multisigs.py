#!/usr/bin/env python3

import json, subprocess

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
# Load allocations for each category
for c in categories:
  with open('data/{}.json'.format(c), 'r') as f:
    data = json.load(f)
    for allocation in data:
      allocations.append(allocation)

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

multisigs = json.load(open('data/multisigs.json'))

def make_multisig(x):
  return '''# {}
[[established_account]]
vp = "vp_user"
threshold = {}
public_keys = {}'''.format(x[2], x[1], json.dumps(x[0]))

for m in multisigs:
  data = make_multisig(m)
  print('Searching for allocation for multisig: {}'.format(m[2]))
  open('/tmp/transactions.toml', 'w').write(data)
  addr = subprocess.getoutput('namadac utils derive-genesis-addresses --path /tmp/transactions.toml | grep Address | cut -c 28-')
  alloc = obj[addr]
  print('Found allocation: {} for {}'.format(alloc['amount'], alloc['address']))
