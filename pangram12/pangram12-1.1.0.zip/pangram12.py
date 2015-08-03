# Check if sentence is pangram or not
def pangram (string):
    i = 0
    P = 0
    string_lower = string.lower ()
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in alphabet:
        if i not in string_lower:
            P = 1
            #print (i)
        #else :
            #print (i,"'")
    if P == 1:
        print ('Not a pangram')
    else :
        print ('Pangram')
    print (P)
    
    
    
