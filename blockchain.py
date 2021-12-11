import datetime
import hashlib
import json
import os
import sys


def data_to_hash(data):
    """хешування даних"""
    json_data = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)  # дані в формат json
    binary_data = json_data.encode()  # json to binary
    return hashlib.sha512(binary_data).hexdigest()  # хеш складної структури


def add_new_block(account_from, account_to, amount):  # функція додавання в блокчейн
    """додавання нового блоку в блокчейн"""
    prev_block = blockchain[-1]  # останній блок в блокчейні
    prev_hash = data_to_hash(prev_block)  # хешування попереднього блока
    time = str(datetime.datetime.now())
    number_block = prev_block["number_block"] + 1  # нумерування блоків
    block = {
        "from": account_from,
        "to": account_to,
        "amount": amount,
        "prev_hash": prev_hash,
        "time": time,
        "number_block": number_block
    }  # створили блок
    proof = mine_proof_of_work(block)  # майнінг блока
    block["proof"] = proof
    blockchain.append(block)  # додаємо блок в блокчейн
    blockchain_dir = os.curdir + "/blockchain"
    with open(blockchain_dir + "test.json", "w") as file:  # збереження блокчейна у файл json
        json.dump(blockchain, file, sort_keys=True, indent=4, ensure_ascii=False)


def validate_blockchain():
    """перевірка блокчейна на правильність, звірювання хешів блоків"""
    prev_block = None
    for block in blockchain:  # для кожного блока в блокчейні
        if prev_block:
            actual_prev_hash = data_to_hash(prev_block)  # рахуємо хеш попереднього блока
            recorded_prev_hash = block["prev_hash"]  # хеш записаний в блокчейні
            if actual_prev_hash != recorded_prev_hash:  # якщо хеші не співпадають
                print(f"Blockchain is invalid, expected {recorded_prev_hash}, actual = {actual_prev_hash}")
            else:
                print(f"Valid hash {actual_prev_hash}")

        prev_block = block


def is_valid_hash(hash):
    """повернення хеша з певним початком"""
    return hash[0:2] == "00"


def is_valid_proof(block, proof):  # чи підходить це число в якості доказу роботи
    """перевірка чи правильний доказ роботи"""
    block_copy = block.copy()  # створюємо копію блока
    block_copy["proof"] = proof
    hash = data_to_hash(block_copy)  # рахуємо новий хеш
    is_validhash = is_valid_hash(hash)
    return is_validhash  # чи починається цей хеш з двох 0


def mine_proof_of_work(block):  # намайнити таке число додавши його до блоку, щоб хеш починався з двох 0
    """ускладнення хешування"""
    proof = 0
    while not is_valid_proof(block, proof):
        proof += 1
    return proof


def calculate_balances():
    """підрахунок балансів"""
    balances = {}  # зберігання балансів
    for block in blockchain:
        if block["from"] in balances:
            balance_from = balances[block["from"]]
        else:
            balance_from = float(0)
        if block["to"] in balances:
            balance_from = balances[block["to"]]
        else:
            balance_to = float(0)
        a = balance_from - block["amount"]
        b = balance_to + block["amount"]

        balances[block["from"]] = a
        balances[block["to"]] = b
    return balances


def new_transaction(hash_words):
    """нова транзакція у блокчейн"""
    account_from = str(hash_words)
    account_to = str(input("enter recipient address >>"))
    amount = float(input("enter amount >>"))
    print(f" Check transaction! You send from account >> {account_from} << to >> {account_to} amount >> {amount}")
    check = input(f"If you sure enter Y/y ")
    if check in ("Y", "y"):
        print("transaction send to blockchain ")
        add_new_block(account_from, account_to, amount)
    else:
        new_transaction(hash_words)


def wallet():
    """гаманець валюти"""
    first_question = (input("If you want create wallet enter C/c.>>If you want open enter O/o >>"))
    if first_question in ("C", "c"):
        seed_words = input("Input 4 words and remember or write on sheet of paper >>")
        seed_numeric = input("Input 4 numbers and remember or write on sheet of paper >>")
        hash_words = data_to_hash(seed_words)
        hash_numeric = data_to_hash(seed_numeric)
        hash_private = hash_numeric + hash_words
        private_key = data_to_hash(hash_private)
        print(f"Is you public address {hash_words}")
        print(f"Is you private key SAVE and do not show anyone {private_key}")
        second_question = input("If you save private key and words with numeric enter C/c >>")
        if second_question in ("C", "c"):
            print("You are create wallet and can send new transaction")
            new_transaction(hash_words)
        else:
            pass
    else:
        pass
    if first_question in ("O", "o"):
        seed_words = input("Input 4 words ")
        seed_numeric = input("Input 4 numbers")
        hash_words = data_to_hash(seed_words)
        hash_numeric = data_to_hash(seed_numeric)
        hash_private = hash_numeric + hash_words
        private_key = data_to_hash(hash_private)
        print(f"Is you public address {hash_words}")
        print(f"Is you private key SAVE and do not show anyone {private_key}")
        second_question = input("If you save private key and words with numeric enter C/c")
        if second_question in ("C", "c"):
            print("You are open wallet and can send new transaction ")
            new_transaction(hash_words)
        else:
            wallet()


genesis_block = {
        "from": "",  # хто відправив
        "to": "",  # кому відправив
        "amount": float(),  # скільки відправив
        "number_block": int(0)  # номер блока
    }
genesis_block["proof"] = mine_proof_of_work(genesis_block)


blockchain = [
    genesis_block
]  # блокчейн це список транзакцій


def main():
    wallet()


if __name__ == '__main__':
    main()
