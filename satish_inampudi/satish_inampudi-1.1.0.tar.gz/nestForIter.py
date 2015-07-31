def nestForIter(movies):
    for each in movies:
        if isinstance(each,list):
            nestForIter(each)
        else:
            print(each)


        
