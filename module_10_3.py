import threading
from random import randint
from time import sleep


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()
        self.balance_condition = threading.Condition(self.lock)

    def deposit(self):
        for _ in range(100):
            amount = randint(50, 500)
            with self.lock:
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")
                if self.balance >= 500:
                    self.balance_condition.notify_all()
            sleep(0.001)

    def take(self):
        for _ in range(100):
            amount = randint(50, 500)
            print(f"Запрос на {amount}")

            with self.balance_condition:  # Работаем с условием
                while amount > self.balance:
                    print(f"Запрос отклонён, недостаточно средств. Ожидание пополнения...")
                    self.balance_condition.wait()
                self.balance -= amount
                print(f"Снятие: {amount}. Баланс: {self.balance}")
            sleep(0.001)

bk = Bank()

th1 = threading.Thread(target=bk.deposit)
th2 = threading.Thread(target=bk.take)

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
