import random
import csv
import os
plist=list()
ids = list(range(100))
for i in range(0,100):
    result = list()
    at = random.randint(0,9)
    N = random.randint(2,5)
    id = ids.pop(0)
    priority = random.randint(0,5)
    result.append(at)
    result.append(id)
    result.append(priority)
    result.append(N)
   
    print(f'Result before: \n\t{result}')
    cpu = random.sample(range(2,10), N)
    io = random.sample(range(1,10), N if N==1 else N-1)
    #result = [None] * (len(cpu)+len(io))
    
    # result[::2]=cpu
    # result[1::2]=io
    for i in range(0,len(cpu)):
        result.append(cpu[i])
        if i != N-1:
            result.append(io[i])
    print(f'REsult AFter \n\t{result}')
    plist.append(result)
    
    
plist = sorted(plist, key=lambda x: x[0])
path = os.path.join(os.getcwd(), 'processes.data')
with open(path,'w') as file:
    writer = csv.writer(file, delimiter=" ")
    for lst in plist:
        writer.writerow(lst)