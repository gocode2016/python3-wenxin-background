from uuid import uuid4


def genNO():
    return str(uuid4()).replace('-', '')
