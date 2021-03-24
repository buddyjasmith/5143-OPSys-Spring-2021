#!/usr/bin/python3
'''
#*****************************************************************************
:Descriptor:    Coordinator/Server
:authors:       Buddy Smith, Leila Kalantari
:date:          March 24, 2018
:Description:   This program acts as a producer consumer coordinator via 
:               sockets. The program maintains a queue containing producer
:               generated stock information, and delegates the consumption
:               of these stocks to consumers. A denied_producer/
:               denied_consumer priority dictionary is maintained to keep 
:               track of denied: After a given amount of n time, these lists
:               will be recursively reduced.
#******************************************************************************
'''
import socket
import os
import sys
import json
from constant import FILE
import queue
import pickle
import time
import sys
import threading
import copy
from random import uniform
from threading import Thread, Condition
from datetime import datetime
import logging
from dataclasses import dataclass, field
from typing import Any
from pqdict import pqdict
import argparse
import copy
import coloredlogs
import colorama
from bug import printbug
#* Begin argument parsing

parser = argparse.ArgumentParser(description='Server Module')
parser.add_argument('--max-q-size',type=int, default=5,help='Define the max size of the stock queue. Default=5')
parser.add_argument('--deny-time', type=float, default=10.0, help='Define max time item spends in denied queue. Default=10')
parser.add_argument('--stall-time', type=float, default=10,help='Define time to wait for denied Producers/Consumers. Default=10')
parser.add_argument('--sleep-time', type=float,default=uniform(.2,.8) ,help='Define sleep time between threads.  Default random(.2, .8)')
args = parser.parse_args()


q = queue.PriorityQueue(maxsize=args.max_q_size)
sucessful_clients = pqdict()
denied_producers = pqdict()
denied_consumer = pqdict()
stock_queue = queue.Queue()

#* Assign Logging Handlers
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

formatter = logging.Formatter('\nline:{%(lineno)d}\n\t%(asctime)s\n\t%(threadName)s\n\t%(levelname)s\n\t%(message)s',"%H:%M:%S ")

output_file_handler = logging.FileHandler('server.log', 'w')

output_file_handler.setFormatter(formatter)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
logger.addHandler(output_file_handler)

coloredlogs.install(level='NOTSET', logger=logger)
@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any=field(compare=False)
class StockQueueFull(Exception):
    pass
class StockQueueEmpty(Exception):
    pass

class ClientThread():
    '''
    #*************************************************************************
    :Class:         :ClientThread
    :Members:       global q
    :               global denied_producers
    :               global denied_consumers
    :               client_ip
    :               client_port
    :Methods:       run(self,  client, sent_object)
    :               set_stock(self, sent_object)
    :               producer(self, client,  sent_object)
    :               get_stock(self)
    :               consumer(self, client, sent_object)
    :               
    '''
    def __init__(self,ip,port,client, sent_object):
        '''
        :method:        init method for ThreadClient
        :descirption    initializes  passed values pertaining to client
        :               and stores variables as data class members.
        :               The init method calls the run function which then 
        :               decides which client functions to perform
        :returns:       none
        '''
        global q
        global denied_producers
        global denied_consumer
        self.client_ip = ip
        self.client_port = port
        #self.daemon = True
        logger.info(f'Creating thread for {self.client_ip}:{self.client_port}')
        self.run(client, sent_object)
        
    def run(self,  client, sent_object):
        '''
        :method:        run
        :params:        client: client object to send and recieve data
        :               sent_object: data sent via socket to coordinator
        :Description    This method determines if a client is a producer 
        :               or consumer.  It is then delegated to the correct
        :               corresponding member functions and further
        :               actions are taken outside of this method.
        '''
        time.sleep(uniform(.2, 2))
        # Object is of Consumer Type
        if sent_object.id_type == 'Consumer':
            logger.info(f'Beginning thread for Consumer: {sent_object.stock_info.get("ConsumerId")}')
            self.consumer(client, sent_object)
            
        # Object is of Producer Type
        elif sent_object.id_type =='Producer':
            logger.info(f'Beginning thread for Producer: {sent_object.stock_info.get("ProducerId")}')
            self.producer( client,  sent_object)
            logger.info(f'Producer {sent_object.stock_info.get("ProducerId")} produced: {sent_object.message}')
        
    def set_stock(self, sent_object):
        '''
        :method:        set_stock
        :params:        sent_object
        :description:   method puts the sent_object produced by producers on the
        :               q for consumer consumption. If successful, the return message
        :               is sent back to the producer with a message describing 
        :               success/denied.  If the producer was on the denied list, it is
        :               removed.  If the attempt to add stock was unsuccessful, the 
        :               producer is then put on the denied list.  A message is sent
        :               back to the producer informing it of this.
        '''
        now = time.time()
        sent_object.queuedTime = now
        pi = PrioritizedItem(now, sent_object)
        producer_id = sent_object.stock_info.get('ProducerId')
        try:
            q.put(pi, block=False, timeout=1)
            logger.info(f'QSIZE= {q.qsize()}')
            sent_object.message = str(f'Success adding stock. {sent_object.stock_info.get("ProducerId")} ')
            if  producer_id in denied_producers:
                del denied_producers[producer_id]
                denied_producers.heapify()
                logger.info(f'{producer_id} was removed from denied producers queue.')
        except queue.Full:
            now = time.time()
            denied_producers[producer_id]=now
            sent_object.message = 'Denied: Queue is full.  You have been added to denied producers.'
            logger.info(sent_object.message)
            logger.info(f'DeniedProducer size = {len(denied_producers)}')
           
                
        
        

    def producer(self, client,  sent_object):
        '''
        :method:        producer
        :params:        client: client object to send data back
        :               sent_object: object created by producer to 
        :               be queued.
        :Description:   The method attempts to put sent_object on 
        :               the queue.  After attempt, the producer is
        :               sent a message describing success or failure.

        '''
        now = time.time()
        # if q.qsize() <= args.max_q_size:
        self.set_stock(sent_object)    
        client.sendall( pickle.dumps(sent_object))
        client.close()
        

    def get_stock(self):
        '''
        :method:        get_stock
        :params:        none
        :description:   retrieves stock from q
        :returnL:       nada
        '''
        pi = q.get()
        return pi.item

    def consumer(self, client, sent_object):
        '''
        :method:        consumer
        :params:        client: client object
        :               sent_object: object sent by consumer, 
        :               data from get method will be copied into this
        :               object to be returned
        :returns:       none
        '''
        qsize = q.qsize()
        consumer_id = sent_object.stock_info.get('ConsumerId')
        if (q and (qsize != 0) and (qsize <= args.max_q_size)):
            logger.info(f'Condition Met: Begin Operations for consumer {sent_object.stock_info.get("ConsumerId")}')
            item = q.get()
            
            item.item.stock_info['ConsumerId'] = sent_object.stock_info.get("ConsumerId")
            sent_object = copy.deepcopy(item.item)
            
            sent_object.message = str(f'Successfuly recieved Stock prodcued by {sent_object.stock_info.get("ProducerId")}')
            
            sent_object.stock_info['ConsumerId'] = consumer_id
            sent_object.stock_info['ConsumedTime']= time.time()
            client.sendall( pickle.dumps(sent_object))
            logger.info(f'Consumer {sent_object.stock_info.get("ConsumerId")}:Message {sent_object.message}')
            if consumer_id in denied_consumer:
                denied_consumer.pop(consumer_id)
                denied_consumer.heapify()
                logger.info(f'{consumer_id} removed from denied consumers')
                logger.info(f'New denied consumer size is {len(denied_consumer)}')
            logger.info(f'Stock sent to {sent_object.stock_info.get("ConsumerId")}')
            client.close()
        else:
            reason = 'Queue is full' if qsize >=5 else 'Queue is empty'
            message = 'Denied: ' + reason
            logger.warning(f'Reason: {message}')
            
            
            sent_object.message = message
            
            client.send( pickle.dumps(sent_object))
            client.close()
            now = time.time()
            if not consumer_id in denied_consumer:
                denied_consumer[consumer_id]= time.time()
                logger.warning(f'New length of Denied Consumer Queue: {len(denied_consumer)}')
            
    

class SendData():
    #*************************************************************************
    '''
    :Class:         SendData
    :Members:       id_type: producer or consumer
    :               stock_info: dictionary: all information relating to stock
    :               time_recieved: time recieved by coordinator
    :               queuedTime: time put into que
    '''
    def __init__(self, id_type, stock_info, message):
        
        self.id_type = id_type
        self.stock_info = stock_info
        self.message = message
        self.time_recieved = time.time()
        self.queuedTime = None
    def __repr__(self):
        return str(f'Id: {self.id_type} \n {self.stock_info} ')

def remove_cp_from_denied(so):
    '''
    :function:      remove_cp_from_denied
    :params:        so: SendObject
    :description:   This is a redundant function and needs to be 
    :               removed.  I found a much easier way.  
    :Todo:          Refactor and remove from code base
    '''
    global denied_consumer
    global denied_producers
    item_type = so.id_type
    found = False
    if item_type == 'Producer' and denied_producers:
        logger.info(f'Length of denied producers before deletion = {len(denied_producers)}')
        item_id = so.stock_info.get('ProducerId')
        denied_producers = {key:val for key, val in denied_producers.items() if key != item_id}
        logger.info(f'Length of denied producers after deletion = {len(denied_producers)}')
        Found = True
        denied_producers = pqdict(denied_producers)
        denied_producers.heapify()
    elif denied_consumer:
        logger.info(f'Length of denied consumers before deletion = {len(denied_consumer)}')
        item_id = so.stock_info.get('ConsumerId')
        found = True
        denied_consumer = {key:val for key, val in denied_consumer.items() if key != item_id}
        logger.info(f'Length of denied consumers after deletion = {len(denied_consumer)}')

        denied_consumer = pqdict(denied_consumer)
        denied_consumer.heapify()
    return found
def get_longest(pdict):
    '''
    :func:          get_longest
    :params         pqdict: priority queue dictionary
    :description:   returns the time of the longest item
    :               in the priority dictionary
    :return         float: time
    '''
    thyme = None
    if pdict:
        temp = pdict.topitem()
        print(f'Key value is {temp[0]}. Value is {temp[1]}')
        thyme = time.time() - temp[1]
    return thyme


def death_to_producers(type, server_socket):
    '''
    :func:          death_to_producers
    :params:        type: consumer or producer
    :               server_socket:  socket used to send and recieve
    :description:   This is a recursive function that serves and removes
    :               all members of the denied_producer pqdict.  It begins
    :               by first serving all instances of stock on the queue.
    :               it then begins producing items for the queue.  
    :               if denied_producers is still not empty, it does this
    :               until complete or timedout
    '''
    if len(denied_producers) == 0:
        logger.info('Successfully removed all denied producers')
        return
    time_out = time.time() +30
    length= len(denied_producers) 
    q_size = q.qsize()
        # Raw and dirty, we are only letting in Consumers consume the
        # queue until empty to pave the way for producers 
    while q_size > 0:
        if time.time() > time_out:
            logger.info('Going over in time')
            break
        client, client_addr = server_socket.accept()
        client_ip, client_port = client_addr
        data = client.recv(1024)
        data = pickle.loads(data)
        if data:
            logger.info('Client recieved in producer denial handling.')
            client_type = data.id_type
            client_id = data.stock_info.get('ProducerId') 
            if client_type == 'Producer':
                # only need consumers to remove queue right now
                #*TODO allow producers on the denied queue maybe. idk
                logger.info('Rejected Producer.  Waiting for consuemrs.')
                data.message = 'Error: 503.  Try again'
                client.sendall(pickle.dumps(data))
                client.close()
            else:
                #if producers, fill to max, wait for denied consumers
                logger.info('Consumer allocated.')
                client_id = 'Thread-'+client_id
                ct = threading.Thread(target=ClientThread, name=client_id,  args=(client_ip, client_port,client, data)) # Make thread B as a daemon thread
                ct.daemon = True
                ct.start()
    producer_list = [denied_producers.keys()]
    time_out = time.time() - 30
    while len(denied_producers) >0:
        #* 
        if (time.time() > time_out) or q.full():
            break
        client, client_addr = server_socket.accept()
        client_ip, client_port = client_addr
        data = client.recv(1024)
        data = pickle.loads(data)
        if data.id_type == 'Producers':
            if client_id not in producer_list:
                # client not in deniedprodcuers
                data.message = 'Error: 503. Try Again!'
                client.sendall(pickle.dumps(data))
                client.close()
            else:
                # client producer is in denied_producers
                client_id = 'Thread-'+client_id
                ct = threading.Thread(target=ClientThread, name=client_id,  args=(client_ip, client_port,client, sent_object)) # Make thread B as a daemon thread
                ct.daemon = True
                ct.start()
           
        else:
            # handle consumer clients
            client_id = data.stock_info.get('ConsumerId')
            if client_id not in consumer_list:
                data.message = 'Error: 503. Try Again!'
                client.sendall(pickle.dumps(data))
                client.close()
            
    if len(denied_consumer) > 0:
        death_to_denials(type, server_socket)

def death_to_consumers(type, server_socket):
    '''
    :func       death_to_consumers
    :params     server_socket:
    :desc:      This is a recursive function that serves and removes
    :           all members of the denied_consumer pqdict.  It begins
    :           by filling the que with producer stock until full.
    :           it then begins consuming items from the queue.  
    :           if denied_consumers is still not empty, it does this
    :           until complete or timedout
    '''
    if len(denied_consumer) == 0:
        logger.info('Successfully removed all denied consumers')
        return
    time_out = time.time() +30
    length= len(denied_producers) if type == 'Producers' else len(denied_producers)
    q_size = q.qsize()
   
        # Raw and dirty, we are only letting in Producers and 
    while q_size <= args.max_q_size:
        if time.time() > time_out:
            logger.info('Going over in time')
            break
        client, client_addr = server_socket.accept()
        client_ip, client_port = client_addr
        data = client.recv(1024)
        data = pickle.loads(data)
        if data:
            logger.info('Client recieved in consumer denial handling.')
            client_type = data.id_type
            client_id = data.stock_info.get('ConsumerId') if client_type == 'Consumer' else data.stock_info.get('ProducerId')
            if client_type == 'Consumer':
                logger.info('Rejected consumer.  Waiting for producers.')
                data.message = 'Error: 503.  Try again'
                client.sendall(pickle.dumps(data))
                client.close()
            else:
                #if producers, fill to max, wait for denied consumers
                logger.info('Producer allocated.')
                client_id = 'Thread-'+client_id
                ct = threading.Thread(target=ClientThread, name=client_id,  args=(client_ip, client_port,client, data)) # Make thread B as a daemon thread
                ct.daemon = True
                ct.start()
    consumer_list = [denied_consumer.keys()]
    time_out = time.time() - 30
    while len(denied_consumer) >0:
        if time.time() > time_out:
            break
        client, client_addr = server_socket.accept()
        client_ip, client_port = client_addr
        data = client.recv(1024)
        data = pickle.loads(data)
        if data.id_type == 'Producers':
            data.message = 'Error: 503. Try Again!'
            client.sendall(pickle.dumps(data))
            client.close()
        else:
            # deal with producers below
            client_id = data.stock_info.get('ConsumerId')
            if client_id not in consumer_list:
                # fuvk tyhem
                data.message = 'Error: 503. Try Again!'
                client.sendall(pickle.dumps(data))
                client.close()
            else:
                # One client down
                consumer_list.remove(client_id)
                client_id = 'Thread-'+client_id
                ct = threading.Thread(target=ClientThread, name=client_id,  args=(client_ip, client_port,client, sent_object)) # Make thread B as a daemon thread
                ct.daemon = True
                ct.start()
    if len(denied_consumer) > 0:
        death_to_denials(type, server_socket)

    

def Main():
    '''
    :func:          main
    :params:        none
    :description    In main we begin listening on out local port and then
    :               begin delegating client requests to the ClientThread
    :               class as daemon threads.The deny hold times are checked
    :               and then delgated to the appropriate kill functions.
    '''

    now = datetime.now()
    info = {'stop': False}
    host = '165.227.212.52'
    port = 22100
    
    global stock_queue
    
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ThreadCount = 0
    try:
        server_socket.bind((host,port))
    except socket.error as e:
        logger.critical(f'Unable to bind to ip/port. {str(e)}  ')
    logger.info(f'Beginning Server @ {host}:{port}')
    server_socket.listen(5)
    producer_count = 0
    consumer_count = 0
    while True:
        long_p = get_longest(denied_consumer)
        long_c = get_longest(denied_producers)
        # if long_c:
        #     death_to_denials('Consumer', server_socket)
        if (long_c) and ((long_c > 20.0)):
            #* if longest time of denied producers or denied consumers greater
            #* than 20 seconds....  Go into super deny mode
            death_to_consumers('Consumer', server_socket)
        if (long_p) and ((long_p > 20.0)):
            death_to_producers('Producer',)
       
        # Start listening for clients
        client, client_addr = server_socket.accept()
        client_ip, client_port = client_addr
        logger.info(f'Connection accepted from {client_ip}:{client_port}') 
        data = client.recv(1024)
        
        # unpack data recieved from client
        sent_object = pickle.loads(data)
        client_type = sent_object.id_type
       
        # start daemon thread for client
        client_id = sent_object.stock_info.get('ConsumerId') if client_type == 'Consumer' else sent_object.stock_info.get('ProducerId')
        client_id = 'Thread-'+client_id
        ct = threading.Thread(target=ClientThread, name=client_id,  args=(client_ip, client_port,client, sent_object)) # Make thread B as a daemon thread
        ct.daemon = True
        ct.start()

if __name__ == '__main__':

    Main()