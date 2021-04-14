from Process import Process
def collect():
    '''
    :func:          collect
    :params:        none
    :description:   helper method to collect process data from text file
    :return         list of processes
    :dependencies   local file of process.txt containing processes
    '''
    processes = list()
    
    with open('processes.data', 'r') as file:
            for line in file:
                line = line.strip('\n')
                line = [ int(x) for x in line.split(" ") ]
                #! Arrival Time
                at = line[0]
                #! Process ID
                pid = line[1]
                #! Priority Number
                priority = line[2]
                #! Number of cpu bursts
                N = line[3]
                #! Start at element 3, every other element from 3
                cpu_bursts = line[4::2]
                #! Start at element 4, every other element from 4
                io_bursts = line[5::2]
                #! create process and append to processes
                p = Process( at,pid,priority, N ,cpu_bursts, io_bursts)
                processes.append(p)
                   
    
    return processes
