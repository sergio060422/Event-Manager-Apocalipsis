def getChar(s):
    for c in s.split(" "):
        if c != "":
            return True
    return False

print(getChar("a   "))