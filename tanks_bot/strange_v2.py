from random import randint, choice, random
from colorama import init
init()
import json
import time
import sys
import os
import pprint
from collections import OrderedDict

class worker():
    def __init__(self):
        # think of some default values of atributtes
        self.counter = 0
        self.clear_counter = 0
        self.player_pos_x = 0
        self.player_pos_y = 0
        # self.player_pos = (self.player_pos_x, self.player_pos_y)
        self.player_id = 0
        self.current_turn = 'up'        # or left empty
        self.npc_pos_x = 0
        self.npc_pos_y = 0
        self.current_action = 'shoot'   # or left empty
        self.current_speed = 0
        
        self.current_positon = (0, 0)
        self.stuck_count = 0
        self.probably_stuck = False
        
        self.metal_positions = []
        self.water_positions = []
        self.tinywall_positions = []
        
        # need to get full info for each tick, and clear it after send command
        self.npc_data = {}
        self.bullet_data = {}
        
    def action(self):
        pass
        
    def update_map(self):
        ''' get map of all objects at start & update it every turn '''
        return True
        
    def get_speed(self, data):
        try:
            if data['id'] == self.player_id:
                self.current_speed = data['speed']
        except:
            pass
        return self.current_speed
    
    def count_up(self):
        self.counter += 1
        
    def analyze_position(self):
        return True
        
    def find_rays(self, data, player_pos):
        ''' find which ways does bullet goes 
        -False - means no danger
        -string out -> action to avoid bullet ray
        todo:
            when you are in fire range in front of npc shoot instead of run away
            treat npc like a bullet
            find out how long the ray really is(check metal or tinywall between)
            
            ignore if bullet is going outside
            if x=0 and turn left
            if x=480 and turn right
            if y=0 and turn up
            if y=480 and turn down
        '''
        in_front_range = 8 # 16
        try:
            # if data['type'] == 'bullet':
            if data['type'] in ('bullet', 'npc'):
                # bullet = (data['direction'], (data['position']['x'], data['position']['y']))
                bullet = (data['direction'], data['position'])
                
                # *************************************************
                # this might works
                if bullet[1]['x'] < 32 and bullet[0] == 'left':
                    return False
                if bullet[1]['x'] > 448 and bullet[0] == 'right':
                    return False
                if bullet[1]['y'] < 32 and bullet[0] == 'up':
                    return False
                if bullet[1]['y'] > 448 and bullet[0] == 'down':
                    return False
                # *************************************************
                
                # check parent
                if data['parent'] == self.player_id:
                    # simple_write('strange_things.txt', "\tTRY TO AVOID BULLET OF YOURS")
                    return False
                
                if bullet[0] in ('left', 'right'):
                    if bullet[0] == 'left':
                        if bullet[1]['y'] in range(player_pos[1]-in_front_range, player_pos[1]+in_front_range):
                            if player_pos[0] in range(0, bullet[1]['x']):
                                print("\n\tin fire range -> go away")
                                if self.current_turn == 'right':
                                    return 'shoot'      # attack is the best defence
                                else:
                                    return choice(['up', 'down'])   # for now
                            
                        if (player_pos[1] - bullet[1]['y']) in range(in_front_range, 64) and self.current_turn == 'up':
                            if player_pos[0] in range(0, bullet[1]['x']):
                                print("\n\twill go into fire rain(up from you). STOP")
                                return 'stop'
                        if -(player_pos[1] - bullet[1]['y']) in range(in_front_range, 64) and self.current_turn == 'down':
                            if player_pos[0] in range(0, bullet[1]['x']):
                                print("\n\twill go into fire rain(down from you). STOP")
                                return 'stop'
                    else:
                        if bullet[1]['y'] in range(player_pos[1]-in_front_range, player_pos[1]+in_front_range):
                            if player_pos[0] in range(bullet[1]['x'], 480):
                                print("\n\tin fire range -> go away")
                                if self.current_turn == 'left':
                                    return 'shoot'      # attack is the best defence
                                else:
                                    return choice(['up', 'down'])   # for now
                            
                        if (player_pos[1] - bullet[1]['y']) in range(in_front_range, 64) and self.current_turn == 'up':
                            if player_pos[0] in range(bullet[1]['x'], 480):
                                print("\n\twill go into fire rain(up from you). STOP")
                                return 'stop'
                        if -(player_pos[1] - bullet[1]['y']) in range(in_front_range, 64) and self.current_turn == 'down':
                            if player_pos[0] in range(bullet[1]['x'], 480):
                                print("\n\twill go into fire rain(down from you). STOP")
                                return 'stop'
                else:
                    if bullet[0] == 'up':
                        if bullet[1]['x'] in range(player_pos[0]-in_front_range, player_pos[0]+in_front_range):
                            if player_pos[1] in range(0, bullet[1]['y']):
                                print("\n\tin fire range -> go away")
                                if self.current_turn == 'down':
                                    return 'shoot'      # attack is the best defence
                                else:
                                    # ******************************************************
                                    # use it in whole function if works
                                    # metal_object = self.check_items_between(player_pos, npc_pos, self.metal_positions, 32, vertical=True)    # check_metal
                                    metal_object = self.check_items_between(player_pos, (bullet[1]['x'], bullet[1]['y']), self.metal_positions, 32, vertical=True)    # check_metal
                                    tinywall_object = self.check_items_between(player_pos, (bullet[1]['x'], bullet[1]['y']), self.tinywall_positions, 32, vertical=True)    # check_metal
                                    if metal_object or tinywall_object:
                                        # simple_write('strange_things.txt', "\tFALSE BULLET RAY, METAL OBJECTS or TINYWALL BETWEEN: {}, {}".format(metal_object, tinywall_object))
                                        return False
                                    else:
                                        # simple_write('strange_things.txt', "\tTRY TO AVOID BULLET RAY FROM: {}".format('down'))
                                        return choice(['left', 'right'])   # for now
                                    # ******************************************************
                            
                        if (player_pos[0] - bullet[1]['x']) in range(in_front_range, 64) and self.current_turn == 'left':
                            if player_pos[1] in range(0, bullet[1]['y']):
                                print("\n\twill go into fire rain(left from you). STOP")
                                return 'stop'
                        if -(player_pos[0] - bullet[1]['x']) in range(in_front_range, 64) and self.current_turn == 'right':
                            if player_pos[1] in range(0, bullet[1]['y']):
                                print("\n\twill go into fire rain(right from you). STOP")
                                return 'stop'
                    else:
                        if bullet[1]['x'] in range(player_pos[0]-in_front_range, player_pos[0]+in_front_range):
                            if player_pos[1] in range(bullet[1]['y'], 480):
                                print("\n\tin fire range -> go away")
                                if self.current_turn == 'up':
                                    return 'shoot'      # attack is the best defence
                                else:
                                    # ******************************************************
                                    # use it in whole function if works
                                    # metal_object = self.check_items_between(player_pos, npc_pos, self.metal_positions, 32, vertical=True)    # check_metal
                                    metal_object = self.check_items_between(player_pos, (bullet[1]['x'], bullet[1]['y']), self.metal_positions, 32, vertical=True)    # check_metal
                                    if metal_object:
                                        # simple_write('strange_things.txt', "\tFALSE BULLET RAY, METAL OBJECTS BETWEEN: {}".format(metal_object))
                                        return False
                                    else:
                                        # simple_write('strange_things.txt', "\tTRY TO AVOID BULLET RAY FROM: {}".format('up'))
                                        return choice(['left', 'right'])   # for now
                                    # ******************************************************
                            
                        if (player_pos[0] - bullet[1]['x']) in range(in_front_range, 64) and self.current_turn == 'left':
                            if player_pos[1] in range(bullet[1]['y'], 480):
                                print("\n\twill go into fire rain(left from you). STOP")
                                return 'stop'
                        if -(player_pos[0] - bullet[1]['x']) in range(in_front_range, 64) and self.current_turn == 'right':
                            if player_pos[1] in range(bullet[1]['y'], 480):
                                print("\n\twill go into fire rain(right from you). STOP")
                                return 'stop'
        except:
            # print("\n\tfailed to find ray of bullet")
            # print(data)
            pass
        return False
        
    def get_items_positions(self, data, item_type):
        ''' use it at start '''
        out = [(item['position']['x'], item['position']['y']) for item in data['cords'] if item['type'] == item_type]
        return out
        
    def get_current_turn(self, data):
        try:
            if data["id"] == self.player_id and data["action"] == "change":
                self.current_turn = data["direction"]
        except:
            pass
        return self.current_turn
        
    def get_player_id(self, data):
        ids = []
        try:
            ids = [item['id'] for item in data['cords'] if item['type'] == 'player']
        except:
            pass
        return ids
        
    def get_player_pos(self, data):
        try:
            if data['type'] == 'player' and data['id'] == self.player_id:
            # if 'player' in str(data):
                self.player_pos_x = data['position']['x']
                self.player_pos_y = data['position']['y']
        except:
            pass
        # simple_write('player_position.txt', (self.player_pos_x, self.player_pos_y))
        return (self.player_pos_x, self.player_pos_y)
        
    def update_npc_data(self, data):
        try:
            if data['action'] == 'destroy' and data['id'] in self.npc_data.keys():
                self.npc_data.pop(data['id'])       # remove destroyed npc from dict
                return True
        except:
            pass
        return False
        
    def reverse_direction(self, direction):
        ''' get current direction and return reverse value '''
        out = {'up': 'down',
               'down': 'up',
               'right': 'left',
               'left': 'right'}
        return out[direction]
        
    def get_best_action(self, d):
        try:
            ''' try different order of sorting '''
            # out = sorted(d, key=lambda k: (d[k]['cross_value'], d[k]['danger'], 1/(abs(d[k]['distance'])+1)), reverse=True)
            out = sorted(d, key=lambda k: (d[k]['cross_value'], d[k]['danger'], 1/(abs(d[k]['distance'])+1)), reverse=True)
            sorted_dict = OrderedDict({item:d[item] for item in out})
            # pprint.pprint(sorted_dict)
            action = list(sorted_dict.values())[0]['action']
        except:
            action = ''
        return action
        
    def get_npc_pos(self, data):
        try:
        # if 1:
            if data['type'] == 'npc':
                self.npc_pos_x = data['position']['x']
                self.npc_pos_y = data['position']['y']
                npc_pos = (self.npc_pos_x, self.npc_pos_y)
                player_pos = (self.player_pos_x, self.player_pos_y)
                #check cross_line
                cross_value, you_to_enemy, distance = self.cross_line((self.npc_pos_x, self.npc_pos_y))
                enemy_turn = data['direction']
                #check check front_or_not
                #check distance
                #shoot to the nearest, but decide before sending command
                #check if enemy is front to you
                #check if you are turn to enemy
                    #if True: shoot
                    #else: turn & then shoot
                    
                
                danger = (enemy_turn == you_to_enemy)
                if you_to_enemy in ('right', 'left'):
                    metal_object = self.check_items_between(player_pos, npc_pos, self.metal_positions, 32, vertical=False)          # check_metal
                    tinywall_object = self.check_items_between(player_pos, npc_pos, self.tinywall_positions, 8, vertical=False)     # check_tinywall
                else:
                    metal_object = self.check_items_between(player_pos, npc_pos, self.metal_positions, 32, vertical=True)           # check_metal
                    tinywall_object = self.check_items_between(player_pos, npc_pos, self.tinywall_positions, 8, vertical=True)      # check_tinywall
                obstacle = bool(metal_object and tinywall_object)
                # obstacle = False
                action = ''
                if cross_value and (not obstacle):
                    action = 'shoot'
                    # if enemy_turn == self.reverse_direction(self.current_turn):  
                        # action = self.reverse_direction(enemy_turn)
                    if you_to_enemy != self.reverse_direction(self.current_turn):  
                        action = self.reverse_direction(you_to_enemy)
                        
                        
                # get actions to shoot enemy if in cross
                # self.npc_data[data['id']] = {'position': (self.npc_pos_x, self.npc_pos_y), 'cross_value': cross_value, 'you_to_enemy': you_to_enemy, 'distance': distance, 'your_turn': self.current_turn, 'enemy_turn': enemy_turn, 'danger': danger}    # add to container; cross_line, append also distance, and front or not -> True/False
                self.npc_data[data['id']] = {'position': player_pos, 'npc_pos': npc_pos, 'you_to_enemy': you_to_enemy, 'cross_value': cross_value, 'distance': distance, 'enemy_turn': enemy_turn, 'danger': danger, 'action': action, 'obstacle': obstacle}
                
                
                # self.npc_data = self.get_best_action(self.npc_data)
                # out = self.npc_data.values[0]['actions']
                # then just decide before sending command
        # except KeyError as err:
        except:
        # else:
            self.npc_pos_x = 0
            self.npc_pos_y = 0
            # print('\n'*5, err, '\n'*5)
        # simple_write('npc_position.txt', (self.npc_pos_x, self.npc_pos_y))
        
        return (self.npc_pos_x, self.npc_pos_y)
        
    def distance(self, object_pos):
        value = 128
        return value
        
    def check_front(self, object):
        return True
        return False
    
    def cross_line(self, npc_pos):
        ''' modified check_way function 
        info:
            -player position need to be 
        '''
        npc_pos_x, npc_pos_y = npc_pos
        diff_value = 32 # 33
        cross_value = False
        you_to_enemy = ''
        distance = 999
        if abs(self.player_pos_x - npc_pos_x) < diff_value:
            distance = self.player_pos_y - npc_pos_y
            if distance > 0:        # because -values are True
                # you are 'down' to opponent
                you_to_enemy = 'down'
            else:
                you_to_enemy = 'up'
            cross_value = True
        if abs(self.player_pos_y - npc_pos_y) < diff_value:
            distance = self.player_pos_x - npc_pos_x
            if distance > 0:
                # you are 'down' to opponent
                you_to_enemy = 'right'
            else:
                you_to_enemy = 'left'
            cross_value = True
        return cross_value, you_to_enemy, distance
        
    def shoot_action(self):
        # check if you're towards the opponent. if not turn
        # stop
        # fire the bullet
        return True

    def check_items_between(self, player_pos, npc_pos, items, diff_value, vertical):
        ''' this function should check if object like metal is between line player-npc '''
        # diff_value = 32 # 16 ??
        player_pos_x, player_pos_y = player_pos
        npc_pos_x, npc_pos_y = npc_pos
        objects_between = []
        for item_x, item_y in items:
            if vertical:
                if item_y in range(npc_pos_y, player_pos_y) or item_y in range(player_pos_y, npc_pos_y):
                    if abs(player_pos_x - item_x) < diff_value:
                        # return True
                        # return (item_x, item_y)
                        objects_between.append((item_x, item_y))
            else:
                if item_x in range(npc_pos_x, player_pos_x) or item_x in range(player_pos_x, npc_pos_x):
                    if abs(player_pos_y - item_y) < diff_value:
                        # return True
                        # return (item_x, item_y)
                        objects_between.append((item_x, item_y))
        return objects_between
        # return False
        
    def check_way(self, player_pos, npc_pos, current_turn):
        ''' check if npc is in the player cross '''
        player_pos_x, player_pos_y = player_pos
        npc_pos_x, npc_pos_y = npc_pos
        diff_value = 64 # 33
        if abs(player_pos_x - npc_pos_x) < diff_value:
            # up/down
            metal_object = self.check_items_between(player_pos, npc_pos, self.metal_positions, 32, vertical=True)    # check_metal
            tinywall_object = self.check_items_between(player_pos, npc_pos, self.tinywall_positions, 8, vertical=True)    # check_tinywall
            if metal_object:
                print("\n\t METAL OBJECT BETWEEN\n")
                return False
            if len(tinywall_object) > 15:
                print("\n\t TOO MUCH TINYWALL OBJECT BETWEEN: {}\n".format(len(tinywall_object)))
                return False
                
            if player_pos_y < npc_pos_y:
                # turn down
                # get player position
                # shoot or turn
                if current_turn == 'down':
                    return 'shoot'
                else:
                    return 'down'
            else:
                # turn up
                # get player position
                # shoot or turn
                if current_turn == 'up':
                    return 'shoot'
                else:
                    return 'up'
            
        if abs(player_pos_y - npc_pos_y) < diff_value:
            # left/right
            # simple_write("strange_things.txt", "player vs npc [y]: {} {}".format(player_pos_y, npc_pos_y))
            out = self.check_items_between(player_pos, npc_pos, self.metal_positions, 32, vertical=False)    # check_metal
            tinywall_object = self.check_items_between(player_pos, npc_pos, self.tinywall_positions, 8, vertical=False)    # check_tinywall
            if out:
                print("\n\t METAL OBJECT BETWEEN\n")
                return False
            if len(tinywall_object) > 15:
                print("\n\t TOO MUCH TINYWALL OBJECT BETWEEN: {}\n".format(len(tinywall_object)))
                return False
                
            if player_pos_x > npc_pos_x:
                # turn left
                # get player position
                # shoot or turn
                if current_turn == 'left':
                    return 'shoot'
                else:
                    return 'left'
            else:
                # turn right
                # get player position
                # shoot or turn
                if current_turn == 'right':
                    return 'shoot'
                else:
                    return 'right'
        return False
        
    def command(self):
        commands = ['shoot', 'set_speed', 'rotate']
        directions = ['left', 'right', 'up', 'down']
        speed = randint(0, 2)
        return True
       

       
def simple_write(file, data):
    '''simple_write data to .txt file, with specified data'''
    with open(file, "a") as f:
        f.write(str(data) + "\n")
        f.close()
    return True
    
def read_json_to_dict(file):
    with open(file) as f:
        data = json.load(f)
    return data
    
def script_path():
    '''change current path to script one'''
    current = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current)
    return current
    
    
class Game(object):

    def __init__(self, loop, reader, writer):
        self.loop = loop
        self.reader = reader
        self.writer = writer
        self.player = worker()
        self.data = {}
        self.first_tick = False
        self.start = False

    async def loop_game(self):
        """
        sometimes execute any random action
        for example this tank make random choices (is a dummy tank!)
        """
        if not self.first_tick:
            await self.send(action='greet', name='STRANGER')
            self.first_tick = True

        if self.start:
            # await self.send(action='shoot')
            #****************** top ******************
            # '''
            self.player.count_up()
            
            
            
            # read action from object
            action = self.player.current_action
            # if (not action) and (self.player.stuck_count > 30) and self.player.probably_stuck:
                # make round left, down, right, up
                # self.player.stuck_count = 0
                # self.player.probably_stuck = False
                # actions = ['left', 'down', 'right', 'up']
                # action = actions[(actions.index(self.player.current_turn)+1)%4]
                # simple_write("strange_things.txt", "\tBOT UNSTACKED, current action: {}".format(action))
                
            # simple_write("strange_things.txt", "action: {}".format(action))
            
            simple_write("containers_data.txt", "npc_data: {}".format(self.player.npc_data))
            
            
            # self.player.npc_data = {}
            # print("\n\n\t\t\t\t\taction: '{}'\n\n".format(action))
            if action and self.player.counter > 15:
                # input("here" + self.player.counter)
                if action == 'left':
                    await self.send(action='rotate', direction='left')            
                elif action == 'right':
                    await self.send(action='rotate', direction='right')            
                elif action == 'up':
                    await self.send(action='rotate', direction='up')            
                elif action == 'down':
                    await self.send(action='rotate', direction='down')            
                elif action == 'shoot':
                    await self.send(action='shoot')            
                elif action == 'start':
                    await self.send(action='set_speed', speed=1)            
                elif action == 'stop':
                    await self.send(action='set_speed', speed=0)
                else:
                    await self.send(action='shoot')
                    
                # clear action after send
                self.player.current_action = ''
            else:
                if self.player.counter > 15:
                    self.player.stuck_count += 1
                    # print("counter: {}".format(self.player.counter))
                    out = randint(0, 1)
                    # speed = self.player.current_speed
                    # if not out:
                    if not out:
                        await self.send(action='set_speed', speed=2)    # 1
                    else:
                        pass
                        # await self.send(action='shoot')     # better to shoot than nothing (in most cases)
                    # await self.send(action='shoot')
                    
                    # direction = choice(['left', 'right', 'up', 'down'])
                    # await self.send(action='rotate', direction=direction)
                else:
                    # await self.send(action='set_speed', speed=0)
                    await self.send(action='shoot')
                    
            
            # clear some data here
            # self.player.clear_counter += 1
            # if self.player.clear_counter > 3:
                # self.player.clear_counter = 0
                # self.player.npc_data = {}
                
                
            # '''
            #****************** bottom ******************
            
        self.call_soon(0.25)

    def call_soon(self, time):
        loop.call_later(time, self._loop)

    async def receive(self, data):
        status = data.get('status')
        if status == 'data':
            if data.get('action') == 'move':
                return  # too many data ;_;
        elif status == 'game':
            action = data.get('action')
            if action == 'start':
                self.start = True
            elif action == 'over':
                self.start = False

        if is_silent:
            return

        # print(self._get_color(data), data, '\033[0m')

    async def send(self, **data):
        if data is None:
            return
        raw_data = json.dumps(data)
        writer = self.writer
        writer.write(raw_data.encode())
        writer.write(b'\n')
        await writer.drain()

    def _loop(self):
        return ensure_future(self.loop_game())

    @staticmethod
    def _get_color(data):
        status = data.get('status')
        if status == 'ERROR':
            return '\033[91m'  # red color
        if status == 'OK':
            return '\033[35m'  # purple color
        if status == 'game':
            return '\033[34m'  # blue color
        if status == 'game':
            action = data.get('action')
            if action == 'spawn':
                return '\033[92m'  # green color
            if action == 'destroy':
                return '\033[93m'  # orange color
        return '\033[0m'  # default color


import sys

from asyncio import get_event_loop, open_connection, ensure_future

try:
    is_silent = sys.argv[1] == 'silent'
except IndexError:
    is_silent = False


async def handle_client(loop):
    reader, writer = await open_connection('127.0.0.1', 8888, loop=loop, limit=256 * 1000)
    print('\033[1mCONNECTED!\033[0m')

    game = Game(loop, reader, writer)
    loop.call_soon(game._loop)

    player_pos = (0, 0)     # at start
    first_tick = True
    while True:
        raw_data = await reader.readline()
        data = json.loads(raw_data)
        
        if first_tick:
            # get id of your player
            ids = game.player.get_player_id(data)
            game.player.player_id = ids[1]      # not sure if correct 0 v 1
            game.player.metal_positions = game.player.get_items_positions(data, 'metal')
            game.player.water_positions = game.player.get_items_positions(data, 'water')
            game.player.tinywall_positions = game.player.get_items_positions(data, 'tinywall')
            first_tick = False
          

        #****************** top ******************
            
        # get info about npc's and danger
        # get info about bullets
        # get info about stuck
        # get info about prepare attack
        # calc best solution
        # game.player.current_action = game.player.calc_best_solution()
        
        game.data = data
        # if game.player.get_player_pos(data) == player_pos:
            # game.player.probably_stuck = True                   # check if bot really stuck
            
        player_pos = game.player.get_player_pos(data)
        # if player_pos == game.player.current_positon:
            # game.player.stuck_count += 1
        game.player.current_positon = player_pos
        npc_pos = game.player.get_npc_pos(data)
        # simple_write('strange_things.txt', "\tNPC_POS: {}".format(npc_pos))
        # npc_pos = (0, 0)
        status = game.player.update_npc_data(data)
        if status:
            simple_write('strange_things.txt', "\tENEMY DESTROYED: {}".format(data['id']))
        best_action = game.player.get_best_action(game.player.npc_data)
        game.player.current_action = best_action
        
        
        
        currentTurn = game.player.get_current_turn(data)
        # action = game.player.check_way(player_pos, npc_pos, currentTurn)
        # simple_write("strange_things.txt", "{}, {}".format(game.player.counter, action))    # this should help with strange actions at start
        # if action:
            # game.player.current_action = action         # this cause he is turn after few strikes
            

            
        bullet_avoid = game.player.find_rays(data, player_pos)
        if bullet_avoid:
            print("\n\n\n\t\t\t\t\t\tBULLET RAY AVOIDED: {}\n\n\n".format(bullet_avoid))
            simple_write('strange_things.txt', "\tBULLET RAY AVOIDED: {}".format(bullet_avoid))
            # simple_write('bullet_ray.txt', (data, player_pos))
            game.player.current_action = bullet_avoid   # test for now
        # game.player.get_speed(data)
        
        
       
        # check if you are in 32, 64 and others position, when front to the enemy
        
        
        # simple_write('best_actions_vs_actions.txt', "\tBEST VS ACTION VS BULLET_AVOID: '{}' | '{}' | '{}'".format(best_action, action, bullet_avoid))
        simple_write('best_actions_vs_actions.txt', "\tBEST VS BULLET_AVOID: '{}' | '{}'".format(best_action, bullet_avoid))
        #****************** bottom ******************
            
            
            
            
            
        # info: position of things is top,left corner
            
        # else:
            # pass
            # if game.player.stuck_count > 200:
                # or just reverse direction
                # game.player.stuck_count = 0
                # game.player.current_action = choice(['left', 'right', 'up', 'down'])
            # come closer to enemy
            # do something else. For now shoot
            # game.player.current_action = 'shoot'
            # game.player.current_action = choice(['', 'shoot'])
        
        
        # print("player: {}".format(player_pos))
        # print("npc: {}".format(npc_pos))
        # print("\nplayer vs npc: {}".format(action))
        # print("\ncurrentTurn: {}".format(currentTurn))
        # print(game.player.metal_positions)
        

        out = 'response\\data_' + str(time.time()).split('.')[0] + str(random()).split('.')[1] + '.json'
        # if 'player' in str(data):
        # if 'bullet' in str(data):
        if 'destroy' in str(data) and data['id'] in game.player.npc_data.keys():
            with open(out, 'w') as fp:
                json.dump(data, fp, sort_keys=True, indent=4)     # save to json
                
                
        '''
        if 'type' in data.keys():
            if data['type'] == 'npc':
                with open(out, 'w') as fp:
                    json.dump(data, fp, sort_keys=True, indent=4)     # save to json
        '''    
        await game.receive(data)


if __name__ == "__main__":
    # out = worker()
    current = os.chdir('C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai')
    # data = read_json_to_dict('coords.json')
    
    # npc_data = {'type':'npc', 'id': 1234, 'position': {'x':100, 'y':200}, 'direction': 'down'}
    # thing = out.get_npc_pos(npc_data)
    # data = read_json_to_dict('npc.json')
    # data = read_json_to_dict('bullet.json')
    
    
    loop = get_event_loop()
    handler = handle_client(loop)
    loop.run_until_complete(handler)
    loop.close()
    
    
    
'''
    x=0         max=480 (v 0-511)
    +--------->
 y=0|
    |
    |
    |
max V
=480
(v 0-511)   

one square is 32x32 size


goals:
-get id of your player
-get current position of yours
-get positions of npcs
-check if they're in your 'cross'
-make action like speed->0, turn->right, shoot



******************************************
general purposes:
-find npc's & shoot them
-avoid bullets
-explore
-kill or avoid human player
******************************************



-shoot her...


todo (up 28.12.18):
-get all informations in one tick
-it will help to compare wage of critical actions like avoiding bullets or destroing npc's
-find out why he is turn right/left after few ticks
    its because of avoiding bullets -> need to check if metal is between
    true reason:
    	TRY TO AVOID BULLET RAY FROM: down
        BULLET RAY AVOIDED: left
    or maybe my own bullets ???
    	TRY TO AVOID BULLET OF YOURS
        :)

todo:
    -conflict of interests -> avoid from one fire to other
    -at first look at the nearest enemy
    -think of reach stable position like 32, 64, 96, not 88 v 80 which is dangerous
    -if target is really close to you and there is no danger from buller ray
        make it as main target to kill him
        
    -if not in front of bullet ray -> run away
        
    -make containers with npcs and others, make command, and clear containers after all(every tick)    
     
     
    -make controller to iter over many configurations to get the most efficient
     
    -bullets avoid still causes some errors
     
REMEMBER:
10kB max script size
'''
