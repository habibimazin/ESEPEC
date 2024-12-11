class InMemoryDB:
    def __init__(self):
        self.main_storage = {}
        self.transaction_active = False
        self.temp_storage = {}

    def get(self, key):
        if self.transaction_active and key in self.temp_storage:
            return self.temp_storage[key]
        return self.main_storage.get(key, None)

    def put(self, key, value):
        if not self.transaction_active:
            raise Exception("No active transaction to execute put operation")
        self.temp_storage[key] = value

    def begin_transaction(self):
        if self.transaction_active:
            raise Exception("A transaction is already in progress")
        self.transaction_active = True
        self.temp_storage = {}

    def commit(self):
        if not self.transaction_active:
            raise Exception("No active transaction to commit")
        for key, value in self.temp_storage.items():
            self.main_storage[key] = value
        self.transaction_active = False
        self.temp_storage = {}

    def rollback(self):
        if not self.transaction_active:
            raise Exception("No active transaction to rollback")
        self.transaction_active = False
        self.temp_storage = {}

def main():
    db = InMemoryDB()

    print("Get 'A':", db.get("A"))  # None

    try:
        print("Put 'A' without transaction")
        db.put("A", 5)  # Error
    except Exception as e:
        print(f"Error: {e}")

    print("Begin transaction")
    db.begin_transaction()

    print("Put 'A' = 5")
    db.put("A", 5)

    print("Get 'A' in transaction:", db.get("A"))  # None

    print("Update 'A' = 6")
    db.put("A", 6)

    print("Commit transaction")
    db.commit()

    print("Get 'A' after commit:", db.get("A"))  # 6

    try:
        print("Commit without transaction")
        db.commit()  # Error
    except Exception as e:
        print(f"Error: {e}")

    try:
        print("Rollback without transaction")
        db.rollback()  # Error
    except Exception as e:
        print(f"Error: {e}")

    print("Get 'B':", db.get("B"))  # None

    print("Begin transaction")
    db.begin_transaction()

    print("Put 'B' = 10")
    db.put("B", 10)

    print("Rollback transaction")
    db.rollback()

    print("Get 'B' after rollback:", db.get("B"))  # None

if __name__ == "__main__":
    main()
