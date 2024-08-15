# Namada genesis balances

This is the genesis allocations proposal by the Anoma Foundation for the Namada network. See [this blog post](https://namada.net/blog/namada-community-genesis-process-cryptoeconomic-mechanisms-and-the-genesis-allocations) for more information.

## Files in this repository

This repository contains two files - `balances.toml` and `transactions.toml` - which can be used as direct input for the genesis process.

## How to reconstruct these files

Original allocation data can be found in the `data` folder, associated with categories as described in the blog post.

To reconstruct the balances and transactions files, simply run (you will need Python 3):

```
./generate.py
```

To sanity check that multisignature accounts and addresses are correctly associated, run:

```
./sanity-check-multisigs.py
```
