print ("Hello World")
try:
    a=int(input("How old are you?: "))
    if a <18:
        print("You're not an adult")
    else:
        print("You're an adult")

except ValueError:
    print("ENTER A VALID NUMBER")
