'''
Average total weight time, total, processes processed, shortest and longest
total terminated time
'''
import sys
from CPU import CPU
from SJFS import SJFS
from collect import collect
from IO import IO
import time

from datetime import datetime
from rich.live import Live
from time import sleep
from rich.traceback import install
from RR import RR
from rich import box
from rich.align import Align
from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, track
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from State import State
from rich.columns import Columns
from ReadyQueue import ReadyQueue
from copy import deepcopy
import argparse
from rich import pretty
import logging
from Process import Process
from FCFS import FCFS
from Priority import Priority
import sys

#******************************************************************************
'''
: Author:               Buddy Smith
: Program:              A06 Scheduling
: Date:                 April 11, 2021
: Description:          This program mimics CPU scheduling algorithms given
:                       a set of processes via text file.  The scheduling 
:                       algorithm is passed by the user via command line. 
:                       Shortest Job First, First Come First Serve, Round
:                       Robin, Priority, and multiple processor scheduling
:                       are available.  The user can enter the number of 
:                       CPUS and IO devices via the command line.  DEFAULT
:                       is 1 of each unless directed otherwise.
: Dependencies:         pip3 install rich
:                       pip3 install argparse
: #Todo:                Still working on the bugs of multiple CPU and IO 
: 
'''
install()
pretty.install()
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
formatter = logging.Formatter('\nline: %(lineno)d\n\tModule:%(module)s\n\t%(asctime)s\t%(levelname)s\n\t%(message)s',"%H:%M:%S")
output_handler = logging.FileHandler('log.txt','w')
output_handler.setFormatter(formatter)
logger.addHandler(output_handler)

class Computer:
    def __init__(self, cpu,io,scheduler=None, max_size=sys.maxsize):
        #******************************************************************************
        '''
        :Method         Constructor
        :@params:       cpu: int representing number of CPUS for system
        :               io: int representing number of IO Devices in System
        :               scheduler: string: choose the scheduling algorithm 
        :               max_size: int: Can only be changed with Round Robin, else Error
        :Data Members:  io: list() contains io devices
        :               rq: ReadyQueue Object
        :               console: Rich object representing console object
        :               layout: Rich object for dividing the console into sections
        :               cpu: list() object containing CPU objects
        :               scheduler: Abstract class containing scheduler object
        :               pre_processes: A glimpse into the future.
        :               state_dict: dictionary containing color codes for states
        :               run_process_cnt: number of processes processed
        :Member Func:   make_layout(): Defines page layout
        :               get_terminated_info(): returns string value of term. process
        :               manage_terminated_windows(): draw terminated window
        :               create_proces_info: convert ready que proc. to string for disp
        :               manage_footer_window: draw proc. in ready q
        :               create_io_info: convert io proc to string
        :               manage_io_box: draw io proc in io box    
        :               create_wait_info: returns a string for proc. in io wait q
        :               create_wait_window: redraw wait window info


        '''
        self.io = list()
        self.rq = ReadyQueue()
        self.console = Console()
        self.layout = Layout()
        self.cpu = list()
        
        for i in range(0,cpu):
            self.cpu.append(CPU(max_size))
        for i in range(0,io):
            self.io.append(IO())
        
        self.pre_processes= collect()
        self.total_processes = len(self.pre_processes)
        self.state_dict ={
            'ready': 'rgb(0,128,0)', # Regular Green
            'running': 'rgb(95,255,215)', # Aquamarine
            'waiting': 'rgb(255,255,95)', #Yellowish
            'terminated': 'red',
        }
        self.scheduler = scheduler     
        self.make_layout()
        self.layout["header"].update(Header())
        self.system_time = -1
        self.run_sum = list()
        self.startup()
    
    def make_layout(self) :
        #*********************************************************************
        """
        :method:            make_layout
        :param:             none
        :returns:           none
        :description:       Defines the layout for rich :
        :#todo:             split cpu window into section per cpu
        """
        
        self.layout = Layout(name="root")
        #! Sets up main layout
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=10),
        )
        #! Subdivide main into 2 rows
        self.layout["main"].split_row(
            Layout(name="side", ratio=1),
            Layout(name="body", ratio=2, minimum_size=60),
        )
        #!Subdivide body into 2 column s
        self.layout["body"].split_column(
            Layout(name='cpubox',ratio=2),
            Layout(name='terminated', ratio=2),
        )
        #! Subdivide side into 2 columns
        self.layout["side"].split_column(
            Layout(name='iobox', ratio=3),
            
            Layout(name="iowait", ratio=2)
        )
    def get_terminated_info(self,p):
        #*********************************************************************
        '''
        :method:            get_terminated_info
        :params:            p: process to obtain info from
        :description:       this method returns pertinent info about process
        :                   residing in the terminated queue
        :return             f string
        :#todo              none
        '''
        id = p.id if p else None
        finished = p.proc_done if p else None
        finished1 = p.io_done if p else None
        process = f'P{id}'
        completion = f'P Time: {p.proc_done}' 
        io_complete = f'IO Time: {finished1}'
        
        return f'{process}\n{completion}\n{io_complete}'

    def manage_terminated_box(self):
        '''
        :method:            manage_terminated_box
        :params:            none
        :description:       method modifies the terminated window with
        :                   info regarding processes in the terminated
        :                   queue.  A renderable list is created with info
        :                   for each process and updates that window with 
        :                   new info
        :#todo:             none
        '''
        
        renderable = list()
        
        renderable = [
        Panel(
            self.get_terminated_info(p), 
            style="magenta",
            expand=True, 
            title=f'[yellow]P{p.id}') for p in self.rq.finished
        ] 
        self.layout['terminated'].update(
            Panel(
                Columns(renderable),
                padding=(2,2),
                title=f'[b][green]Finished Processes[/b]',
                box=box.ROUNDED,
                border_style='blue'
            ) 
        )
        time.sleep(args.sleep)
 
    def create_io_info(self,io,num):
        '''
        :method:            create_io_info
        :params:            io: element in io processing
        :                   num: which io number
        :description:       returns a string which contains pertinent info
        :                   about process in io
        :return             f string
        :#todo              Add functionality for multiple io devices
        '''
        current = io.quantum if io.quantum else None
        color = self.state_dict[io.state.name.lower()]
        
        id = f'Servicing: {self.rq.current_process.id}'
        cp = f'CBE: {io.quantum}' if io.quantum else f'CBE: None'
        return f'[b][green]{id}[/b]\n[color]{cp}'
    def manage_io_box(self):
        '''
        :method:            manage_io_box
        :params:            none
        :description:       draws an io column in the 'iobox' layout containing
        :                   information regarding process obtaining io requests
        :#todo              add functionallity for multiple io devices
        '''
        renderable = list()
        num = 1
        for io in self.io:
            renderable.append(
                Panel(
                    self.create_io_info(io,num),
                    style='white',
                    expand=True,
                    title=f'[b]IO {num}[/b]' 
                )
            )
            num+=1
        self.layout['iobox'].update(
            Panel(
                Columns(renderable),
                padding=(2,2),
                title=f'[b][green]IO Instance(s)[/b]',
                box=box.ROUNDED,
                border_style='blue'
            ) 
        )
        time.sleep(args.sleep)
    def get_process_info(self, process):
        '''
        :method:            get_process_info
        :params:            process: Process object in readyqueue
        :description:       returns string of info for process in readyq
        :#todo:             none
        :return:            f string
        '''
        process_id = f'Process: {process.id}'
        at = f'Arrived: {process.arrival_time}'
        cb = f'CB: {process.curr_burst}'
        pr = f'Priority: {process.priority}'
        total_cpu_time = f'({process.N}:{sum(process.cpu_bursts)})'
        return f'[b][blue]{process_id}[/b]\n[yellow]{at}\n[yellow]{pr}\n\[yellow]{cb}\n[white]{total_cpu_time}'        

    def manage_footer(self):
        '''
        :method:            manage_footer
        :param:             none
        :description:       redraws information regarding processes in the readyq. 
        :returns:           none
        :#todo:             none
        '''
        renderable = [
        Panel(
            self.get_process_info(p), 
            style="magenta",
            expand=True, 
            title=f'[yellow]P{p.id}') for p in self.rq.ready_queue
        ]   
    
        self.layout["footer"].update(
            Panel(
                Columns(renderable),
                padding=(1,2),
                title="Process Pool",
                box=box.ROUNDED,
                border_style='blue'
                )
            ) 
        
    def create_wait_info(self,process):
        '''
        :method:            create_wait_info
        :params:            process: Process Object
        :description:       creates f string with info about process in
        :                   wait q.
        :returns:           f string
        :#todo:             none
        '''
        estimate = process.io_bursts[0] if process.io_bursts else None
        process = process.id 
        
        return f'P{process} Waiting on IO\nIOE: {estimate}'
    def manage_wait_window(self):
        '''
        :method:            manange_wait_window
        :params:            none
        :description:       draws info about processes in wait q
        :return:            none
        :#todo:             none
        '''
        renderable = list()
        for i in self.rq.io_wait_list:
            renderable.append(
                Panel(
                    self.create_wait_info(i),
                    style='magenta',
                    expand=True,
                    title=f'[yellow]P{i.id}'
                    )
                )
            
        # renderable = [
        # Panel(
        #     self.create_wait_info(), 
        #     style="magenta",
        #     expand=True, 
        #     title=f'[yellow]P{p.id}') for p in self.rq.io_wait_list
        # ] 
        self.layout["iowait"].update(
            Panel(
                Columns(renderable),
                padding=(1,2),
                title="IO Wait Box",
                box=box.ROUNDED,
                border_style='magenta'
            )
        )
        
    def create_cpu_info(self,cpu):
        '''
        :method:            create_cpu_info
        :params:            none
        :description:       returns info about process residing in 
        :                   cpu current proces
        :return             fstring
        :#todo:             add functionality for multiple cpu
        '''
        id = cpu.process.id if cpu.process else None
        cp = cpu.quantum if cpu.quantum else None
        
        id = f'Servicing: {id}'
        cp = f'CBE: {cp}' 
        color = self.state_dict[cpu.state.name.lower()]
        return f'[b][green]{id}[/b]\n[color]{cp}'
        
    def manage_cpu_window(self):
        '''
        :method:            manage_cpu_window
        :params:            none
        :description:       draws information regarding current
        :                   process of the cpu
        :return             none
        :#todo:             multiple cpu functionality
        '''
        renderable = list()
        num = 1
        for cpu in self.cpu:
            renderable.append(
                Panel(
                    self.create_cpu_info(cpu),
                    style='white',
                    expand=True,
                    title=f'[b]CPU {num}[/b]'
                )
            )
            num+=1
        
        self.layout['cpubox'].update(
            Panel(
                Columns(renderable),
                padding=(2,2),
                title=f'[b][green]CPU Instance(s)[/b]',
                box=box.ROUNDED,
                border_style='blue'
            ) 
        )
        
    def create_io_info(self,io):
        '''
        :method:            create_io_info
        :params:            none
        :description:       returns f string pertinent to info
        :                   about process of IO
        :return             f string
        :#todo:             multiple io objects
        '''
        id = io.process.id if io.process else None
        quantum = io.quantum if io.quantum else None
        color = self.state_dict[io.state.name.lower()]
        
        id = f'Servicing: {id}'
        cp = f'CBE: {quantum}' 
        return f'[b][green]{id}[/b]\n[color]{cp}'
    def manage_io_box(self):
        '''
        :method:            manage_io_box
        :params:            none
        :description:       draws panels containing processes residing in io
        :return:            none
        :#todo:             multiple io objects
        '''
        renderable = list()
        num = 1
        for io in self.io:
            renderable.append(
                Panel(
                    self.create_io_info(io),
                    style='white',
                    expand=True,
                    title=f'[b]IO {num}[/b]'
                )
            )
            num+=1
        self.layout['iobox'].update(
            Panel(
                Columns(renderable),
                padding=(2,2),
                title=f'[b][green]IO Instance(s)[/b]',
                box=box.ROUNDED,
                border_style='blue'
            ) 
        )
    def kill_loop(self):
        rq_check = False
        if self.rq.empty():
            if len(self.rq.io_wait_list) == 0:
                rq_check = True
        cpu_check = False
        for cpu in self.cpu:
            if cpu.process == None:
                cpu_check = False
            else:
                cpu_check = True
                break
        for io in self.io:
            if io.process == None:
                io_check=False
            else:
                io_check = True
                break
        return (io_check and cpu_check and rq_check)



    def set_scheduler(self, scheduler):
        '''
        :method:        set_scheduler
        :params:        scheduler object
        :description:   sets abstract base scheduler to scheduler instance
        :return:        na
        :todo:          none
        '''
        self.scheduler = scheduler
    
    def check_arrivals(self):
        '''
        :method:        check_arrivals
        :params:        none
        :description:   checks new arrivals by comparing current time to 
        :               the current time and adds them to the ready queue once 
        :               arrived.  If added to ready queue they are removed from 
        :               pre_processes.
        :return:        none
        :#todo:         none
        '''
        departure_list = []
        

        temp = self.pre_processes
        del_list = list()
        start_time = 0
        
        if self.pre_processes == 0:
            return None
        for i in range(0,len(self.pre_processes)):
            # if arrivaltime <= (time.time()-self.boot_time) we need to add it to 
            
            if self.pre_processes[i].arrival_time <= self.system_time:
                logger.info(f'Recieved Process {self.pre_processes[i].id} at Time: {self.system_time} {self.pre_processes[i].__repr__()}')
                #self.rq.put(self.pre_processes[i], logger)
                
                self.scheduler.set_schedule(self.rq, self.pre_processes[i], logger, self.system_time) 

                
                        
            else:
                #Time is in the "Future", ignore
                break
        self.pre_processes = [x for x in self.pre_processes if x not in self.rq.ready_queue]
        time.sleep(args.sleep)
        
        
       
    def startup(self):
        '''
        :method:        startup
        :params:        none
        :description:   This is the main driver function for the computer class.
        :               The function starts by creating updating the rich objects
        :               layout with correct labels and parameters:  With each iteration
        :               of the while loop, system time is incremented by 1.  New arrivals
        :               are checked with each iteration of the system time and added to 
        :               the ready queue. The states of the process determine the next location
        :               of each process:  Ready:  process goes to ready q.  Waiting: moves
        :               to the io wait q:  Terminated moves to the terminated q.  The while
        :               loop loops until no processes remain in the readyq, waitq, or preprocessq
        :returns:       none
        :todo:          add multiple cpu and io functionality
        '''
        self.console.clear()
        
        
        
        with Live(self.layout, refresh_per_second=10, screen=True) as live:
            while self.total_processes != 0:
                
                #**************************************************************
                #! Set system time and draw all window components
                self.system_time +=1
                self.check_arrivals()
                self.manage_footer()
                self.manage_cpu_window()
                self.manage_io_box()
                self.manage_wait_window()
                self.manage_terminated_box()

                #**************************************************************
                #! IF Process in IO, perform io
                for io in self.io:
                    if io.process != None:
                        ioresult = io.process_io(logger)
                        self.manage_io_box()
                        if isinstance(ioresult, Process):
                            if ioresult.io_bursts == None:
                                ioresult.io_done = self.system_time
                            #! if result.io_bursts is null, set time
                            #self.rq.put(ioresult, logger)
                            self.scheduler.set_schedule(self.rq, ioresult, logger, self.system_time)
                            self.manage_footer()
                            self.manage_io_box()

                #**************************************************************
                #! IF item exists in the wait list, set IO process
                for io in self.io:
                    if len(self.rq.io_wait_list) > 0 and io.process == None:
                        io.set_process(self.rq.io_wait_list.pop(0),logger)

                for process in self.rq.ready_queue:
                    process.cpu_wait += 1
                for process in self.rq.io_wait_list:
                    process.io_wait += 1
                #**************************************************************
                #! IF CPU has process, perform computation
                for cpu in self.cpu:
                    if cpu.process != None:
                        
                        result = cpu.perform_computation(logger)
                        self.manage_cpu_window()
                        
                        if result:
                            logger.info(f'Process returned P{result.id} Status{result.status}')
                            if (result.status== State.TERMINATED):
                                #! add item to finished if none
                                self.run_sum.append({'ProcessId': result.id,
                                                    'TotalTime': (self.system_time - result.start_time)})
                                result.proc_done = self.system_time
                                self.total_processes -=1
                                self.rq.finished.append(result)
                                self.manage_terminated_box()
                            elif  (result.status == State.WAITING):
                                #! move process to waiting queue for io
                                logger.info(f'P{result.id} being added to wait list')
                                # add process to iowait for IO processing
                                self.rq.io_wait_list.append(result)
                                self.manage_wait_window()
                            
                            elif  (result.status == State.READY):
                                #! move process to ReadyQue for CPU processing
                                #iobursts is empty, cpu is not, put result for one last run
                                # or process returned incomplete from round robin, put back on rq
                                #self.rq.ready_queue.put(result, logger)
                                self.scheduler.set_schedule(self.rq, result, logger, self.system_time)
                                self.manage_footer()
                                self.manage_cpu_window()


                #**************************************************************
                #! If CPU's process is None, set it to first value of readyQueue
                for cpu in self.cpu:
                    if (cpu.process == None) and (self.rq.empty()==False):
                        p = self.rq.pop()
                        if p != None:
                            if p.start_time == -1:
                                p.start_time = self.system_time
                            #if p is none, no process on the ready queue, wait for iowait to return process
                            cpu.set_process(p, logger)
                            
                
        

        if self.total_processes == 0:
            self.console.clear()
            self.console.print('All Processing Complete')
            self.console.print(f'Total Processes Processed {len(self.rq.finished)}')
            output_handler = logging.FileHandler('results.dat','w')
            output_handler.setFormatter(formatter)
            logger.addHandler(output_handler)
            for i in self.rq.finished:
                logger.info(i)
            output_handler = logging.FileHandler('RUN_TIMES.dat','w')
            output_handler.setFormatter(formatter)
            logger.addHandler(output_handler)
            logger.info('Run Times for each process')
            my_list = sorted(self.run_sum, key=lambda k: k['TotalTime'])
            sum_of_p = 0
            for iter in self.run_sum:
                sum_of_p += iter['TotalTime']
            lengthof = len(my_list)
            logger.info(f'Average Time: {sum_of_p / len(self.rq.finished)}')
            logger.info(f'SHORTEST PROCESS: {my_list[0]}')
            logger.info(f'LONGEST PROCESS: {my_list[-1]}')
            for process in my_list:
                logger.info(process)

     

class Header:
    """Display header with clock."""
    def __rich__(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Process Monitor[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")  
    
if __name__=='__main__':
    parser = argparse.ArgumentParser('CPU Scheduling')
    parser.add_argument('--sjfs', action='store_true', help='Run Shortest Job First Scheduling')
    parser.add_argument('--cpu', type=int, default=1,help='OPTIONAL: Designate number of CPU devices for program. DEFAULT=1.')
    parser.add_argument('--io', type=int, default=2, help="OPTIONAL: Designate number of IO devices for program. DEFAULT=2.")
    parser.add_argument('--sleep', type=float, default=.5, help="Designate the sleep time betweeen redrawings. DEFAULT=.5")
    parser.add_argument('scheduler', type=str,  help='Set scheduling algorithm')
    parser.add_argument('--max-q', type=int, default=sys.maxsize, help='Required only if using Round Robin.  Set max exectution time. DEFAULT=sys.maxsize')

    args =parser.parse_args()
    scheduler = None
    #! if sjfs is selected, user may set max_q
    if args.scheduler.lower() == 'sjfs':
        if args.max_q != sys.maxsize:
            parser.error('SJFS does not take a quantum time')
        scheduler = SJFS()
    #! if fcfs is selected, user may not set max_q
    elif args.scheduler.lower() == 'fcfs':
        if args.max_q != sys.maxsize:
            parser.error('FCFS does not take a quantum time')
        scheduler = FCFS()
    #! if round robin is selected, user must set max_q
    elif args.scheduler.lower() == 'rr':
        if args.max_q == sys.maxsize:
            parser.error('Use [--max-q] in conjunction with RR to set time Quantum')
        else:
            scheduler = RR(args.max_q)
    elif args.scheduler.lower() == 'priority':
        if args.max_q != sys.maxsize:
            parser.error('Priority does not take quantum time')
        else:
            scheduler = Priority()
            
    print(args.sjfs)
    
    c = Computer(args.cpu,args.io, scheduler, args.max_q)
    
   
  