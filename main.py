import decimal
import logging
import argparse

MULTIPLICITY = 50
PERCENT_REMOVAL = decimal.Decimal(15) / decimal.Decimal(1000)
MIN_REMOVAL = decimal.Decimal(30)
MAX_REMOVAL = decimal.Decimal(600)
PERCENT_DEPOSIT = decimal.Decimal(3) / decimal.Decimal(100)
COUNTER4PERCENTAGES = 3
RICHNESS_PERCENT = decimal.Decimal(10) / decimal.Decimal(100)
RICHNESS_SUM = decimal.Decimal(10_000_000)

bank_account = decimal.Decimal(0)
count = 0
operations = []


logging.basicConfig(filename='bank.log', level=logging.INFO,
                    encoding='UTF-8', format='%(levelname)s %(asctime)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def check_multiplicity(amount):
    if amount % MULTIPLICITY == 0:
        return True
    else:
        return False


def deposit(amount):
    if check_multiplicity(amount):
        global bank_account
        bank_account += amount
        operations.append(f"Пополнение карты на {amount} у.е. Итого {bank_account} у.е.")
        logging.info(f"Пополнение карты на {amount} у.е. Итого {bank_account} у.е.")
    else:
        print(f"Сумма должна быть кратной {MULTIPLICITY} у.е.")


def withdraw(amount):
    commission = amount * PERCENT_REMOVAL
    if commission < MIN_REMOVAL:
        commission = MIN_REMOVAL
    if commission > MAX_REMOVAL:
        commission = MAX_REMOVAL

    if check_multiplicity(amount):
        global bank_account

        if bank_account >= amount + commission:
            bank_account -= amount + commission
            operations.append(
                f"Снятие с карты {amount} у.е. Процент за снятие {int(commission)} у.е.. Баланс: {int(bank_account)} у.е.")
            logging.info(
                f"Снятие с карты {amount} у.е. Процент за снятие {int(commission)} у.е.. Баланс: {int(bank_account)} у.е.")
        else:
            operations.append(
                f"Недостаточно средств. Сумма с комиссией {int(amount + commission)} у.е. На карте {int(bank_account)} у.е.")
            logging.error(f"Недостаточно средств на счете.")
    else:
        print(f"Сумма должна быть кратной {MULTIPLICITY} у.е.")
        operations.append(
            f"Сумма должна быть кратной {MULTIPLICITY} у.е.")
        logging.error(f"Сумма должна быть кратной {MULTIPLICITY} у.е.")


def exit():
    global bank_account
    global operations
    if bank_account > RICHNESS_SUM:
        tax = bank_account * RICHNESS_PERCENT
        bank_account -= tax
        operations.append(f"Вычтен налог на богатство 0.1% в сумме {tax} у.е. Итого {bank_account} у.е.")

    operations.append(f"Возьмите карту на которой {bank_account} у.е.")
    for el in operations:
        print(el)



def run():

    while True:
        print(f"На Вашем счету {bank_account} у.е.")
        print("Введите от 1 до 3")
        print("1 - Пополнить счет")
        print("2 - Снять со счета")
        print("3 - Выйти")
        choice = input()
        match choice:
            case "1":
                deposit(int(input("Введите сумму на которую вы хотите пополнить счет: ")))
            case "2":
                withdraw(int(input("Введите сумму снятия: ")))
            case "3":
                print('История операций:')
                exit()
                break
            case _:
                print("Введено не верное значение")
                logging.error("Введено не верное значение")



def pars():
    parser = argparse.ArgumentParser(description="Bank Account Operations")
    parser.add_argument(
        "--operation",
        "-o",
        choices=["deposit", "withdraw", "exit"],
        help="Operation to perform: 'deposit', 'withdraw', or 'exit'",
        required=True,
    )
    parser.add_argument(
        "--amount",
        "-a",
        type=int,
        help="Amount for 'deposit' or 'withdraw' operation",
    )

    args = parser.parse_args()

    if args.operation == "deposit":
        deposit(args.amount)
    elif args.operation == "withdraw":
        withdraw(args.amount)
    elif args.operation == "exit":
        exit()


if __name__ == '__main__':
    # p = pars()
    # python .\main.py -o deposit - a 100
    # python .\main.py -o withdraw - a 100
    # python .\main.py -o exit

    run()