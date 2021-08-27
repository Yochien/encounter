def isInt(string):
    if string.isnumeric():
        return True
    else:
        try:
            int(string)
        except:
            return False
        else:
            return True

"""
#More possibly useful function
print(type(1))
print(type("a"))

if type(1) is int:
    print("int")
if type("1") is int:
    print ("int2")

print(isinstance("A", str))
print(isinstance("1", str))
print(isinstance(1, str))
"""