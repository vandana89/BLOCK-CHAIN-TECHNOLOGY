import hashlib
import time


class Block:
    def __init__(self, index, timestamp, data,data2, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.data2=data2
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.data2}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain_for_user:
    def __init__(self):
        self.userchain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "user","useremail" ,"0")

    def get_latest_block(self):
        return self.userchain[-1]

    def add_block_user(self, data,data2):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.userchain),
            timestamp=time.time(),
            data=data,
            data2=data2,
            previous_hash=previous_block.hash,
        )
        self.userchain.append(new_block)


class Block_for_transaction:
    def __init__(self, index, timestamp, chaemail,chaaccnumber, chaifscode,username,usercardnumber,exipdata,cvv,amount,previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.chaemail = chaemail
        self.chaaccnumber=chaaccnumber
        self.chaifscode=chaifscode
        self.username=username
        self.usercardnumber=usercardnumber
        self.exipdata=exipdata
        self.cvv=cvv
        self.amount=amount
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.chaemail}{self.chaaccnumber}{self.chaifscode}{self.username}{self.usercardnumber}{self.exipdata}{self.cvv}{self.amount}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain_for_transaction:
    def __init__(self):
        self.transactiochain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block_for_transaction(0, time.time(), "chaemail","chaaccnumber","chaifscode"," username", "usercardnumber","exipdata","cvv","amount","0")

    def get_latest_block(self):
        return self.transactiochain[-1]

    def add_block_transaction(self, chaemail,chaaccnumber,chaifscode,username,usercardnumber,exipdata,cvv,amount):
        previous_block = self.get_latest_block()
        new_block = Block_for_transaction(
            index=len(self.transactiochain),
            timestamp=time.time(),
            chaemail = chaemail,
            chaaccnumber=chaaccnumber,
            chaifscode=chaifscode,
            username=username,
            usercardnumber=usercardnumber,
            exipdata=exipdata,
            cvv=cvv,
            amount=amount,
            previous_hash=previous_block.hash,
        )
        self.transactiochain.append(new_block)
