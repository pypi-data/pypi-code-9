from shellish import *

sample = {
            "Leaf 1": None,
            "Leaf 2": None,
            "Branch A": {
                "Sub Leaf 1": None,
                "Sub Branch": {
                    "Deep Leaf": None
                }
            },
            "Branch B": {
                "Sub Leaf 2": None
            }
}

dicttree({"Root": sample})


