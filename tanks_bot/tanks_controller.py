import os
import time
import subprocess


def call_script(command, shell=False):
    if shell:
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(command)
    return True
    
    
if __name__ == "__main__":
    runPath = 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai'
    os.chdir(runPath)
    
    
    #****** run server ******
    command = ['py', '-3.7', '-m', 'battle_city.server']
    # command = ['py', '-3.7', '-m', 'battle_city.server', '--show-collision-border']
    # command = ['py', '-3.7', '-m', 'battle_city.server', '--hidden-window']
    call_script(command)
    
    
    
    #****** run player1 ******
    # command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\radom.py']
    # command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\enemy.py']
    # command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\strange_npc.py']
    # command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\strange_best_actions.py']
    command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\useless_bot.py']
    call_script(command)
    print("player1 is running")
    # time.sleep(.1)
    
    #****** run player2 ******
    # command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\strange.py']
    # command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\strange_attack_and_avoid.py']
    # command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\strange_npc.py']
    command = ['py', '-3.7', 'C:\\Users\\quiter\\Desktop\\tank_bot\\battle-city-ai\\battle_city\\examples\\python\\useless_bot.py']
    call_script(command)    
    print("player2 is running")
    
    
    
    
    
    
