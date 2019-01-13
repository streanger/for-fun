from random import randint, choice, random; import json; from collections import OrderedDictclass worker():    def __init__(self):        self.counter = 0; self.clear_counter = 0; self.player_pos_x = 470; self.player_pos_y = 470; self.player_id = 0; self.c_t = 'up'        self.npc_pos_x = 0; self.npc_pos_y = 0; self.current_action = ('shoot', ''); self.current_speed = 0; self.current_positon = (0, 0)        self.metal_positions = []; self.water_positions = []; self.tinywall_positions = []; self.npc_data = {}; self.bullet_data = {}    def get_speed(self, data):        try:            if data['id'] == self.player_id: self.current_speed = data['speed']        except:            pass        return self.current_speed    def get_items_positions(self, data, item_type):        return [(item['position']['x'], item['position']['y']) for item in data['cords'] if item['type'] == item_type]    def get_c_t(self, data):        try:            if data["id"] == self.player_id and data["action"] == "change": self.c_t = data["direction"]        except:            pass        return self.c_t    def get_player_pos(self, data):        try:            if data['type'] == 'player' and data['id'] == self.player_id:                self.player_pos_x = data['position']['x']                self.player_pos_y = data['position']['y']        except:            pass        return (self.player_pos_x, self.player_pos_y)    def update_npc_data(self, data):        try:            if data['action'] == 'destroy' and data['id'] in self.npc_data.keys():                self.npc_data.pop(data['id'])                return True        except:            pass        return False    def reverse_direction(self, direction):        return {'up':'down','down':'up','right':'left','left':'right'}[direction]    def get_best_action(self, d):        try:            out = sorted(d, key=lambda k: (d[k]['cross_value'], not d[k]['obstacle'], d[k]['danger'], 1/(abs(d[k]['distance'])+1)), reverse=True)            sorted_dict = OrderedDict({item:d[item] for item in out}); self.npc_data = sorted_dict; action = list(sorted_dict.values())[0]['action']        except:            action = ''        return action    def get_npc_pos(self, data):        try:            if data['type'] == 'npc':                self.npc_pos_x = data['position']['x']; self.npc_pos_y = data['position']['y']; npc_pos = (self.npc_pos_x, self.npc_pos_y)                player_pos = (self.player_pos_x, self.player_pos_y); cross_value, you_to_enemy, distance = self.cross_line((self.npc_pos_x, self.npc_pos_y))                enemy_turn = data['direction']; danger = (enemy_turn == you_to_enemy)                if you_to_enemy in ('right', 'left'):                    metal_object = self.cib(player_pos, npc_pos, self.metal_positions, 4, vertical=False)                    tinywall_object = self.cib(player_pos, npc_pos, self.tinywall_positions, 4, vertical=False)                else:                    metal_object = self.cib(player_pos, npc_pos, self.metal_positions, 4, vertical=True)                    tinywall_object = self.cib(player_pos, npc_pos, self.tinywall_positions, 4, vertical=True)                obstacle = bool(metal_object and tinywall_object); action = ''                if cross_value and (not obstacle):                    action = 'shoot'                    if you_to_enemy != self.reverse_direction(self.c_t): action = self.reverse_direction(you_to_enemy)                self.npc_data[data['id']] = {'cross_value': cross_value, 'distance': distance, 'danger': danger, 'action': action, 'obstacle': obstacle}        except:            self.npc_pos_x = 0; self.npc_pos_y = 0        return (self.npc_pos_x, self.npc_pos_y)    def cross_line(self, npc_pos):        npc_pos_x, npc_pos_y = npc_pos; dv = 32; cross_value = False; you_to_enemy = ''; distance = 999        if abs(self.player_pos_x - npc_pos_x) < dv:            distance = self.player_pos_y - npc_pos_y            if distance > 0: you_to_enemy = 'down'            else: you_to_enemy = 'up'            cross_value = True        if abs(self.player_pos_y - npc_pos_y) < dv:            distance = self.player_pos_x - npc_pos_x            if distance > 0: you_to_enemy = 'right'            else: you_to_enemy = 'left'            cross_value = True        return cross_value, you_to_enemy, distance    def cib(self, player_pos, npc_pos, items, dv, vertical):        player_pos_x, player_pos_y = player_pos; npc_pos_x, npc_pos_y = npc_pos; objects_between = []        for ix, iy in items:            if vertical:                if iy in range(npc_pos_y, player_pos_y) or iy in range(player_pos_y, npc_pos_y):                    if abs(player_pos_x - ix) < dv: objects_between.append((ix, iy))            else:                if ix in range(npc_pos_x, player_pos_x) or ix in range(player_pos_x, npc_pos_x):                    if abs(player_pos_y - iy) < dv: objects_between.append((ix, iy))        return objects_betweenclass Game(object):    def __init__(self, loop, reader, writer):        self.loop = loop; self.reader = reader; self.writer = writer; self.player = worker(); self.data = {}; self.first_tick = False; self.start = False    async def loop_game(self):        if not self.first_tick:            await self.send(action='greet', name='useless')            self.first_tick = True        if self.start:            self.player.counter += 1; action, from_action = self.player.current_action; self.player.current_action = ('', '')            if action and self.player.counter > 5:                if action in ('left', 'right', 'up', 'down'): await self.send(action='rotate', direction=action)                elif action == 'shoot': await self.send(action='shoot')                elif action == 'start': await self.send(action='set_speed', speed=2)                elif action == 'stop': await self.send(action='set_speed', speed=0)                else: await self.send(action='shoot')            else:                if self.player.counter > 5:                    out = randint(0, 3)                    if not out: await self.send(action='set_speed', speed=2)                    else: await self.send(action='shoot')                else: await self.send(action='shoot')        self.call_soon(0.25)    def call_soon(self, time):        loop.call_later(time, self._loop)    async def receive(self, data):        status = data.get('status')        if status == 'data':            if data.get('action') == 'move': return  # too many data ;_;        elif status == 'game':            action = data.get('action')            if action == 'start': self.start = True            elif action == 'over': self.start = False        if is_silent: return    async def send(self, **data):        if data is None: return        raw_data = json.dumps(data)        writer = self.writer        writer.write(raw_data.encode())        writer.write(b'\n')        await writer.drain()    def _loop(self): return ensure_future(self.loop_game())    @staticmethod    def _get_color(data):        status = data.get('status')        if status == 'ERROR': return '\033[91m'        if status == 'OK': return '\033[35m'        if status == 'game': return '\033[34m'        if status == 'game':            action = data.get('action')            if action == 'spawn': return '\033[92m'            if action == 'destroy': return '\033[93m'        return '\033[0m'import sysfrom asyncio import get_event_loop, open_connection, ensure_futuretry:    is_silent = sys.argv[1] == 'silent'except IndexError:    is_silent = Falseasync def handle_client(loop):    reader, writer = await open_connection('127.0.0.1', 8888, loop=loop, limit=256 * 1000)    print('\033[1mCONNECTED!\033[0m')    game = Game(loop, reader, writer)    loop.call_soon(game._loop)    player_pos = (0, 0); first_tick = True    while True:        raw_data = await reader.readline()        data = json.loads(raw_data)        if first_tick:            game.player.player_id = data['id']            game.player.metal_positions = game.player.get_items_positions(data, 'metal')            game.player.water_positions = game.player.get_items_positions(data, 'water')            game.player.tinywall_positions = game.player.get_items_positions(data, 'tinywall')            first_tick = False        player_pos = game.player.get_player_pos(data); c_t = game.player.get_c_t(data); npc_pos = game.player.get_npc_pos(data)        status = game.player.update_npc_data(data); best_action = game.player.get_best_action(game.player.npc_data)        if best_action:            game.player.current_action = (best_action, 'from_best_action')            await game.receive(data)            continue        if True:            action = ''            metal_up = any([(player_pos[0]+x, player_pos[1]-32) in game.player.metal_positions for x in range(-32, 33, 8)]); metal_down = any([(player_pos[0]+x, player_pos[1]+32) in game.player.metal_positions for x in range(-32, 33, 8)])            if (metal_up and c_t == 'up') or metal_down and c_t == 'down': action = choice(['left', 'right'])            metal_left = any([(player_pos[0]-32, player_pos[1]+x) in game.player.metal_positions for x in range(-32, 33, 8)]); metal_right = any([(player_pos[0]+32, player_pos[1]+x) in game.player.metal_positions for x in range(-32, 33, 8)])            if (metal_left and c_t == 'left') or (metal_right and c_t == 'right'): action = choice(['up', 'down'])            if player_pos[0] == 0 and c_t == 'left': action = 'right'            if player_pos[0] == 480 and c_t == 'right': action = 'left'            if player_pos[1] == 0 and c_t == 'up': action = 'down'            if player_pos[1] == 480 and c_t == 'down': action = 'up'            if not game.player.current_action[0]: game.player.current_action = (action, '')        await game.receive(data)if __name__ == "__main__":    loop = get_event_loop()    handler = handle_client(loop)    loop.run_until_complete(handler)    loop.close()