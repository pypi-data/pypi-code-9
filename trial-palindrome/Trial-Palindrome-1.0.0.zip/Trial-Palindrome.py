def is_pal (string):
    i = 0
    a_list = []
    strng_lwr = string.lower ()                                                       # Convert every character into lower case
    for i in strng_lwr:
        a_list.append (i)                                                             # Convert string to list for better manupalating capability

    j = 0
    for j in a_list:
        if j == ' ' or j == '.' or j == "'" or j == '!' or j == '?' or j == ',':
            a_list.remove (j)

    n = 0
    for n in a_list:                                                                  # Running same 'for' loop second time as single 'for' is not getting rid
        if n == ' ' or n == '.' or n == "'" or n == '!' or n == '?' or n == ',':      # of two consecutive characters, e.g.  ', ' or '  ' or ',,', etc.                                                                    
            a_list.remove (n)                                                         # Yet to figure out why?  Shall create and call function for the same.

    k = 0                                                                             # Checkig if paindrome and creating a list to store checked values
    chk_pal = []
    for k in range (len(a_list) - 1):
        if a_list[k] == a_list[len(a_list) - k - 1]:
            chk_pal.append ('T')
        else :
            chk_pal.append ('F')
    m = 0
    F = 0
    for m in chk_pal:                                                               
        if m == 'F':
            F = 1
    if F == 1:
        print ('Not a palindrome')
    else:
        print ('Given string is a palindrome')
    
            
            
    
   
