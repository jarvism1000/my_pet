import datetime
import hashlib
import json
#import flask
import random


def data_to_hash(data):
    json_data = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False) # дані в формат json
    binary_data = json_data.encode() # json to binary
    return hashlib.sha512(binary_data).hexdigest() # хеш складної структури




def add_new_block(account_from, account_to, amount): # функція додавання в блокчейн
    prev_block = blockchain[-1] # останній блок в блокчейні
    prev_hash = data_to_hash(prev_block) #  хешування попереднього блока
    time = str(datetime.datetime.now())
    number_block = prev_block["number_block"] + 1 # нумерування блоків
    block = {
        "from": account_from,
        "to": account_to,
        "amount": amount,
        "prev_hash": prev_hash,
        "time": time,
        "number_block": number_block
    }# створили блок
    proof = mine_proof_of_work(block) # майнінг блока
    block["proof"] = proof
    blockchain.append(block) # додаємо блок в блокчейн


def validate_blockchain():
    prev_block = None

    for block in blockchain: # для кожного блока в блокчейні
        if prev_block:
            # звірити хеші з 2
            actual_prev_hash = data_to_hash(prev_block) # рахуємо хеш попереднього блока
            recorded_prev_hash = block["prev_hash"] # хеш записаний в блокчейні
            #if isValidProof(prev_block, actual_prev_hash):
                #print(f"Blockchain is invalid, proof of work is wrong!")
            if actual_prev_hash != recorded_prev_hash: # якщо хеші не співпадають
              print(f"Blockchain is invalid, expected {recorded_prev_hash}, actual = {actual_prev_hash}")
            else:
              print(f"Valid hash {actual_prev_hash}")

        prev_block = block


def is_valid_hash(hash):
    return hash[0:4] == "0000"


#proof це доказ роботи, це число потрібно підібрати щоб хеш починався з 0
def is_valid_proof(block, proof): # чи підходить це число в якості доказу роботи
    block_copy = block.copy() # створюємо копію блока
    block_copy["proof"] = proof
    hash = data_to_hash(block_copy) # рахуємо новий хеш
    is_validhash = is_valid_hash(hash)
    return is_validhash # чи починається цей хеш з двох 0


def mine_proof_of_work(block): # намайнити таке число додавши його до блоку, щоб хеш починався з двох 0
    proof = 0
    while not is_valid_proof(block, proof):
        proof += 1
    return proof


def calculate_balances():
    balances = {} # зберігання балансів
    for block in blockchain:
        if block["from"] in balances:
            balance_from = balances[block["from"]]
        else:
            balance_from = 0

        if block["to"] in balances:
            balance_from = balances[block["to"]]
        else:
            balance_to = 0
        balance_from -= block["amount"]
        balance_to += block["amount"]

        balances[block["from"]] = balance_from
        balances[block["to"]] = balance_to
    print(balances)


def new_transaction():
    account_from = str(input("enter from "))
    account_to = str(input("enter to "))
    amount = str(float(input("enter amount ")))
    print(f" Check transaction! You send from account >> {account_from} << to >> {account_to} amount >> {amount}")
    check = print(input(f"If you sure enter Y/y "))

    if check == "Y" or "y":
        print("transaction send to blockchain ")
        add_new_block(account_from, account_to, amount)
    else:
        new_transaction()



#def wallet():


def main():
    pass


genesis_block = {
        "from": "", # хто відправив
        "to": "", # кому відправив
        "amount": "", # скільки відправив
        "number_block": 0
    }
genesis_block["proof"] = mine_proof_of_work(genesis_block)


blockchain = [
    genesis_block,
] # блокчейн це список транзакцій


add_new_block("adam", "james", 1000)
add_new_block("tim", "jan", 7860)
add_new_block("tim", "georg", 10060)
add_new_block("adam", "grace", 100)
add_new_block("jan", "grace", 60)
mine_proof_of_work(blockchain[4])


print(blockchain)
#print(validate_blockchain())
#print(mine_proof_of_work(blockchain[4]))
#print(calculate_balances())
print(new_transaction())
print(blockchain)
#print(new_transaction())


if __name__ == '__main__':
    pass


