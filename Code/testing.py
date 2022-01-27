import numpy as np

rng = np.random.default_rng()
l1 = [1,2,3,4,5,6]

l2 = ["a","b","c","e","d","f"]


for i in range(100):
    new = []
    num_pairs = int(rng.normal(3.5))
    print()
    new.append(l1[:len(l1)-num_pairs])
    new.append(l2[num_pairs-1:])
    new2 = new[0]+new[1]
    #print(num_pairs)
    print(new2)
    #print("size ", len(new2))
    #print("size ", len(new[0]),len(new[1]))

