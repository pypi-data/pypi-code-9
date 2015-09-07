from django.shortcuts import render
import autotag
import random
import os

# Create your views here.






if __name__ == '__main__':
    main_data = autotag.get_json_data('res/db4')
    random.shuffle(main_data)
    tagged = [d for d in main_data if d["tags"]]
    untagged = [d for d in main_data if not d["tags"]]
    N = len(tagged)
    untagged = untagged[:N]#TODO: remove
    print(N)
    train_data = tagged[:-N/10]
    test_data = tagged[-N/10:]
    path = os.getcwd()
    at = autotag.AutoTag(os.path.join(path, 'res'))
    tags = at.get_tags()
    print(tags)

    print('classifying')
    at.classify(train_data, tags=tags)
   
    print("testing")
    print(at.test(test_data))

    tagged = [d for d in main_data if '231' in d["tags"]]
    untagged = [d for d in main_data if '231' not in d["tags"]][:100]
    print(len(tagged))
    print(at.get_most_informative_features_from_data(tagged, untagged, 10))
