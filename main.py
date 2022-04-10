from re import T
from follow_bot import spotify
import threading, os, time



lock = threading.Lock()
counter = 0



class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def safe_print(arg):
    lock.acquire()
    print(arg)
    lock.release()


def thread_follow(account):
    global counter
    obj = spotify(account)
    result = obj.follow()
    if result:
        counter += 1
        safe_print("Followed {}".format(counter))
    else:
        print(result)
        safe_print("Error")
        

def follow_user(account: str, threads: int):
    while True:
        if threading.active_count() <= threads:
            try:
                threading.Thread(target = thread_follow, args=(account, )).start()
            except Exception as e:
                print(e)
                safe_print("Error")

def thread_create():
    try:
        global counter
        obj = spotify()
        result = obj.register_account()
        auth_token = obj.get_token(result)
        if auth_token != None:
            
            with open("accounts.txt", "a") as f:
                f.write(f"\n{auth_token}")
            counter += 1
            safe_print("Created {}".format(counter))
            
    except:
        pass
        

def create_account(threads: int):
    while True:
        if threading.active_count() <= threads:
            try:
                threading.Thread(target = thread_create).start()
            except:
                safe_print("Error")

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    print("1. Follow Accounts")
    print("2. Create accounts")
    userinpt = int(input(""))
    clear()
    if userinpt == 1:
        threads = input("Threads: ")
        account = input("Account: ")
        follow_user(account, int(threads))
    elif userinpt == 2:
        threads = input("\nThreads: ")
        create_account(int(threads))
    else:
        print("Invalid input"); time.sleep(1); clear(); main()
if __name__ == "__main__":
    main()

    