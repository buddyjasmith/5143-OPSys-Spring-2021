#!/usr/local/bin/python3 
'''
#*****************************************************************************
:Name:          Buddy Smith Leila Kalantari
:Date:          March 24, 2021
:Assignment:    A04
:Description:   This script acts as a client to send randomly generated to a 
:               stock server to provide consumers/producersdatetime 
:Global:        ArgParse

'''
import json
import threading
import socket, os.path, datetime, sys
import requests
import uuid
import pickle
import random
from random import uniform
import time
import logging
import sys

from datetime import datetime
import argparse

class SendData():
    '''
    #*************************************************************************
    :Class:         SendData
    :Members:       id_type: string:  'producer' or 'consumer'
    :               stock_info: dict: contains generated stock data
    :               message: string: acts as a communication channel between
    :                                server and client
    :               time_recieved: time: seconds
    :               queuedTime: time put into queue by coordinator
    :Description:   Acts as an object to be sent between client and coordinator
    :Todo:          None
    ''' 
    def __init__(self, id_type, stock_info, message):
        self.id_type = id_type
        self.stock_info = stock_info
        self.message = message
        self.time_recieved = None
        self.queuedTime = None
    def __repr__(self):
        '''
        #*********************************************************************
        :Function:      __repr__
        :params:        none
        :variables:     none
        :Description:   returns a string representation of the SendData object
        :Return:        string  
        '''
        return str(f'Id: {self.id_type} \n {self.stock_info} ')
       
        
def generatSymbol():
    '''
    #*************************************************************************
    :Func:          generateSymbol
    :params:        none
    :description:   generates a stock symbol of length 3
    :return:        string
    #*************************************************************************
    '''
    charSet = 'abcdefghijklmnopqrstuvwxyz'
    length = random.randint(3,3)
    return ''.join(map(lambda unused : random.choice(charSet).upper(), range(length)))
def generate_random_uuids(lengthof):
    '''
    #*************************************************************************
    :Func:          generate_random_uuids
    :params:        lengthof: int
    :description:   generates a list of unique uuid of length
    :return:        list object
    #*************************************************************************
    '''
    temp_list = list()
    for x in range(0, lengthof):
        temp_list.append(uuid.uuid4())
    return temp_list
def Main():
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
   
    formatter = logging.Formatter('\nline:{%(lineno)d}\n\t%(asctime)s\n\t%(threadName)s\n\t%(levelname)s\n\t%(message)s',"%H:%M:%S ")
    output_file_handler = logging.FileHandler('client.log', mode='w')
    output_file_handler.setFormatter(formatter)
    
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    # if --log-to-file is passed, add handler, else leave it out
    
    logger.addHandler(output_file_handler)
    parser = argparse.ArgumentParser(description='Client Module')
    parser.add_argument('-p','--producer-cycles', type=int, nargs='+',help='Cycle order of Client Producers')
    parser.add_argument('-c', '--consumer-cycles', type=int, nargs='+', help='Cycle order of Client Consumers')
    parser.add_argument('-s', '--shuffle', type=bool, help='Randomize consumer producers: Not to be used with "-r --randomize"')
    parser.add_argument('-t','--sleep-time', type=float, help='Designate sleep time between packets sent')
    parser.add_argument('--starve-consumers', action='store_true' ,help='Deny consumers producers, use for debugging Server')
    parser.add_argument('--starve-producers', action='store_true', help='Deny producers consumers, use for debugging Server')
    parser.add_argument('--producer-uuids', type=str, nargs='+', help='Define uuids for producers in list of values')
    parser.add_argument('--consumer-uuids', type=str, nargs='+', help='Define uuids for consumers in list of values')
    parser.add_argument('--sleep-time-deny', type=float, help='Set custom sleep time between denies, default = .1')
    parser.add_argument('--uuid-count-producers', type=int, help='Enter the number of unique identifiers to create for producers to user')
    parser.add_argument('--uuid-count-consumers', type=int, help='Enter the number of unique identifiers to create for consumers')
    parser.add_argument('--log-to-file', action='store_true', help='')
    args= parser.parse_args()
    if args:
        #* determine logging requirements immediately, verbose logs to screen, 
     
        log_to_file = args.log_to_file
        #* set sleep time to parsed value, or random between .2 and 1.2 if not passed
        sleep_time = args.sleep_time if args.sleep_time else random.uniform(.2,1.2)
        #* set time to sleep if denied
        sleep_time_deny = args.sleep_time_deny if args.sleep_time_deny else random.uniform(.1, .5)
        logger.info(f'Quantum Time Set: {str(sleep_time)}')
        #* create list of producer cycles, randomize if not passed
        producer_cycles = args.producer_cycles if args.producer_cycles else random.sample(range(1,6), 5)
        logger.info(f'Producer Cycles : {producer_cycles}')
        #* create list of consumer cycles matching passed values, else randomize list of size 5
        consumer_cycles = args.consumer_cycles if args.consumer_cycles else random.sample(range(1,6),5)
        logger.info(f'Consumer Cycles: {consumer_cycles}')

        #* Just for S&G, shuffle the lists..  idk
        if args.shuffle:   
            logger.info(f'Shuffle passed by User')
            producer_cycles = random.shuffle(producer_cycles)
            consumer_cycles = random.shuffle(consumer_cycles)
        
        if args.starve_consumers:
            #! WARNING: Only consumers will be ran. Useful for debugging server
            logger.critical('STARVING CONSUMERS')
            producer_cycles = list()
        if args.starve_producers:
            #! WARNING: Only producers will be ran.  Useful for debugging server
            logger.critical('STARVING PRODUCERS')
            consumer_cycles = list()

        if len(producer_cycles) != len(consumer_cycles):
            #! WARNING: Warn user of potential deny conditions
            print('Lists unbalanced.  Do you wish to proceed? ')
            inpt = input( 'Type (Y/y)es or (N/n)o: ')
            if inpt.lower().startswith('n'):
                logger.critical('User closing program...')
                sys.exit('Exiting via user command!')
        #* Determine if user passed custom count for uuids for consumers/producers
        uuid_count_producers = args.uuid_count_producers if args.uuid_count_producers else random.randint(2,5)
        uuid_count_consumers = args.uuid_count_consumers if args.uuid_count_consumers else random.randint(2,5)
       
        #* Determine if user pass custom uuids
        producer_uuids = args.producer_uuids if args.producer_uuids else generate_random_uuids(uuid_count_producers)
        consumer_uuids = args.consumer_uuids if args.consumer_uuids else generate_random_uuids(uuid_count_consumers)
        logger.info(f'Producers IDS: {producer_uuids}')
        logger.info(f'Consumer IDS: {consumer_uuids}\n')

        

    logger.warning('Client Process beginiing')
    logger.info('This is a test')
    host = '165.227.212.52'
    port = 22100
    data = None
    logger.info('Individual number of cycle to be performed: ')
    logger.info(f'Consumer cycles:  {sum(consumer_cycles)}')
    logger.info(f'Producer cycles:  {sum(producer_cycles)}')
    
    

    # with open('file.json') as file:
    #     data = json.load(file)
    pc_decider = random.getrandbits(1)
    pc_decider = bool(pc_decider)
    while True:
        #s = socket.socket()
        #s.connect((host, port))
        # Determine which cycle starts first, if True, producers, else consumers
        pc_decider = not pc_decider
        #* start producer cycle which first int of producer cycle list
        if producer_cycles and pc_decider:
            first_producer_cycle = producer_cycles[0]
            producer_cycles.pop(0)
            logger.info(f'New Producer cycle sum:  {sum(producer_cycles)}')
            logger.info(f'Beginning producer cycle of {first_producer_cycle}')
            for i in range(0,first_producer_cycle):
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((host, port))
                #@params def __init__(self, id_type, stock_info, message)
                sd = SendData('Producer',{
                    'Name': generatSymbol(),
                    'Price': round(random.uniform(1.00, 1000.0),2),
                    'CreationTime':time.time(),
                    'ProducerId': random.choice(producer_uuids),
                    'ConsumerId': None,
                    'ConsumedTime': None,
                    }, 
                    'Message:')
                logger.info(f'Producer object created:\n\t{repr(sd)}')
                s.sendall(pickle.dumps(sd))
                time.sleep(sleep_time)
                try:
                    data = s.recv(1024)
                    s.shutdown(socket.SHUT_WR)
                except ConnectionResetError as e:
                    logger.warning(f'Server Reset connection for ')

                try:
                    data = pickle.loads(data)
                    logger.info(f'Recieved {data.message}')
                except EOFError :
                    logger.critical(f'Server failed to respond')
                except TypeError:
                    logger.critical(f'Server failed to respond.')
                
            
           # t = threading.Thread(target=send_producers, args=(sd, s))
        elif consumer_cycles and not pc_decider:
            logger.info(f'Consumer cycle sum:  {sum(consumer_cycles)}')
            logger.info(f'Consumer cycles: {consumer_cycles}')
            first_consumer_cycle = consumer_cycles[0]
            consumer_cycles.pop(0)
            logger.info(f'Beginning Consumer cycle of {first_consumer_cycle}')
            for i in range(0,first_consumer_cycle):
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((host, port))
                #@params def __init__(self, id_type, stock_info, message)
                sd = SendData('Consumer',{
                    'Name': None,
                    'Price': None,
                    'CreationTime':None,
                    'ProducerId': None,
                    'ConsumerId': random.choice(consumer_uuids),
                    'ConsumedTime': None,
                    }, 
                    'Message:')
                logger.info(f'Consumer {sd.stock_info.get("ConsumerId")} created:')
                logger.info(f'Consumer: {sd.stock_info.get("ConsumerId") } SENT')
                sendmessage = pickle.dumps(sd)
                
                
                s.sendall(sendmessage)
                time.sleep(sleep_time)
                data = s.recv(1024)
                s.shutdown(socket.SHUT_WR)
                try:
                    data = pickle.loads(data)
                    #logger.debug(f'Complete Data message:  {repr(data)}')

                except EOFError:
                    
                    logger.critical('Server failed to send return message')
                    
            
                

    #     time.sleep(3)
    #     data = s.recv(1024)
    #     s.shutdown(socket.SHUT_WR)
    #     data = pickle.loads(data)
    #     print(data.message)
    # # send_data = json.dumps(data).encode('utf-8')
    # # sd = SendData(0,uuid.uuid4(),data)
    
    # # send_data = pickle.dumps(sd)
    # # s.sendall(send_data)
    # # s.shutdown(socket.SHUT_WR)
    # # data = s.recv(1024)
    # # data = pickle.loads(data)
    # # print(data)

if __name__ == '__main__':
    Main()

    
