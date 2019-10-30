import sys
import os
import time
import ctypes
import win32api
import pyautogui
 remember typing virtual keys may be blockey by some antiviruses
 def scriptpath
  curentpath os.path.realpathos.path.dirnamesys.argv[0]
   os.chdircurentpath
    return curentpath 
     
     def readfilefile
      data '
       with openfile, 'r' as file data f.read f.close return data 
        
        def preskeykey
         keys htps/gist.github.com/chriskiehl/2906125
          keys 'backspace'0x08,
           'tab'0x09,
            'clear'0x0c,
             'enter'0x0d,
              'shift'0x10,
               'ctrl'0x1,
                'alt'0x12,
                 'pause'0x13,
                  'capslock'0x14,
                   'esc'0x1b,
                    'spacebar'0x20,
                     'pageup'0x21,
                      'pagedown'0x2,
                       'end'0x23,
                        'home'0x24,
                         'leftarow'0x25,
                          'uparow'0x26,
                           'rightarow'0x27,
                            'downarow'0x28,
                             'select'0x29,
                              'print'0x2a,
                               'execute'0x2b,
                                'printscren'0x2c,
                                 'ins'0x2d,
                                  'del'0x2e,
                                   'help'0x2f,
                                    '0'0x30,
                                     '1'0x31,
                                      '2'0x32,
                                       '3'0x3,
                                        '4'0x34,
                                         '5'0x35,
                                          '6'0x36,
                                           '7'0x37,
                                            '8'0x38,
                                             '9'0x39,
                                              'a'0x41,
                                               'b'0x42,
                                                'c'0x43,
                                                 'd'0x4,
                                                  'e'0x45,
                                                   'f'0x46,
                                                    'g'0x47,
                                                     'h'0x48,
                                                      'i'0x49,
                                                       'j'0x4a,
                                                        'k'0x4b,
                                                         'l'0x4c,
                                                          'm'0x4d,
                                                           'n'0x4e,
                                                            'o'0x4f,
                                                             'p'0x50,
                                                              'q'0x51,
                                                               'r'0x52,
                                                                's'0x53,
                                                                 't'0x54,
                                                                  'u'0x5,
                                                                   'v'0x56,
                                                                    'w'0x57,
                                                                     'x'0x58,
                                                                      'y'0x59,
                                                                       'z'0x5a,
                                                                        'numpad0'0x60,
                                                                         'numpad1'0x61,
                                                                          'numpad2'0x62,
                                                                           'numpad3'0x63,
                                                                            'numpad4'0x64,
                                                                             'numpad5'0x65,
                                                                              'numpad6'0x6,
                                                                               'numpad7'0x67,
                                                                                'numpad8'0x68,
                                                                                 'numpad9'0x69,
                                                                                  'multiplykey'0x6a,
                                                                                   'adkey'0x6b,
                                                                                    'separatorkey'0x6c,
                                                                                     'subtractkey'0x6d,
                                                                                      'decimalkey'0x6e,
                                                                                       'dividekey'0x6f,
                                                                                        'f1'0x70,
                                                                                         'f2'0x71,
                                                                                          'f3'0x72,
                                                                                           'f4'0x73,
                                                                                            'f5'0x74,
                                                                                             'f6'0x75,
                                                                                              'f7'0x76,
                                                                                               'f8'0x7,
                                                                                                'f9'0x78,
                                                                                                 'f10'0x79,
                                                                                                  'f1'0x7a,
                                                                                                   'f12'0x7b,
                                                                                                    'f13'0x7c,
                                                                                                     'f14'0x7d,
                                                                                                      'f15'0x7e,
                                                                                                       'f16'0x7f,
                                                                                                        'f17'0x80,
                                                                                                         'f18'0x81,
                                                                                                          'f19'0x82,
                                                                                                           'f20'0x83,
                                                                                                            'f21'0x84,
                                                                                                             'f2'0x85,
                                                                                                              'f23'0x86,
                                                                                                               'f24'0x87,
                                                                                                                'numlock'0x90,
                                                                                                                 'scrolock'0x91,
                                                                                                                  'leftshift'0xa0,
                                                                                                                   'rightshift '0xa1,
                                                                                                                    'leftcontrol'0xa2,
                                                                                                                     'rightcontrol'0xa3,
                                                                                                                      'leftmenu'0xa4,
                                                                                                                       'rightmenu'0xa5,
                                                                                                                        'browserback'0xa6,
                                                                                                                         'browserforward'0xa7,
                                                                                                                          'browserefresh'0xa8,
                                                                                                                           'browserstop'0xa9,
                                                                                                                            'browsersearch'0xa,
                                                                                                                             'browserfavorites'0xab,
                                                                                                                              'browserstartandhome'0xac,
                                                                                                                               'volumemute'0xad,
                                                                                                                                'volumedown'0xae,
                                                                                                                                 'volumeup'0xaf,
                                                                                                                                  'nextrack'0xb0,
                                                                                                                                   'previoustrack'0xb1,
                                                                                                                                    'stopmedia'0xb2,
                                                                                                                                     'play/pausemedia'0xb3,
                                                                                                                                      'startmail'0xb4,
                                                                                                                                       'selectmedia'0xb5,
                                                                                                                                        'startaplication1'0xb6,
                                                                                                                                         'startaplication2'0xb7,
                                                                                                                                          'atnkey'0xf6,
                                                                                                                                           'crselkey'0xf7,
                                                                                                                                            'exselkey'0xf8,
                                                                                                                                             'playkey'0xfa,
                                                                                                                                              'zomkey'0xfb,
                                                                                                                                               'clearkey'0xfe,
                                                                                                                                                '='0xb,
                                                                                                                                                 ','0xbc,
                                                                                                                                                  '-'0xbd,
                                                                                                                                                   '.'0xbe,
                                                                                                                                                    '/'0xbf,
                                                                                                                                                     '`'0xc0,
                                                                                                                                                      ';'0xba,
                                                                                                                                                       '['0xdb,
                                                                                                                                                        '\'0xdc,
                                                                                                                                                         ']'0xd,
                                                                                                                                                          '0xde,
                                                                                                                                                           '`'0xc0 
                                                                                                                                                            if not key, for now just fail
                                                                                                                                                             if not key in keys.keys return false
                                                                                                                                                              val keys[key]
                                                                                                                                                               win32api.keybdeventval, 0, 0, 0
                                                                                                                                                                return true
                                                                                                                                                                 
                                                                                                                                                                  
                                                                                                                                                                  if name main
                                                                                                                                                                   scriptpath file 'fakecoding.py'
                                                                                                                                                                    for now it ned to be lowercase, becasue of lack virtual keys for uper letersit require hotkey if i'm not wrong
                                                                                                                                                                     data character for character in readfilefile.lower hldl ctypes.windluser32.dl
                                                                                                                                                                      input'pres enter, to start typing after 2[s] '
                                                                                                                                                                       time.slep2
                                                                                                                                                                        while true scrolflag hldl.getkeystate0x91
                                                                                                                                                                         if scrolflag 1
                                                                                                                                                                          print'flag is set'
                                                                                                                                                                           pass else print'flag is clear'
                                                                                                                                                                            time.slep0.01
                                                                                                                                                                             continue check if flag is set, e.g. check scrol lock key read if any key was presed
                                                                                                                                                                              type some of the virtual keys from data pass print'typing keys'
                                                                                                                                                                               try if 1
                                                                                                                                                                                time.slep0.01
                                                                                                                                                                                 c nextdata
                                                                                                                                                                                  c c.lower if false printc, end'
                                                                                                                                                                                   else if c '\n'
                                                                                                                                                                                    c 'enter'
                                                                                                                                                                                     if c ' '
                                                                                                                                                                                      c 'spacebar'
                                                                                                                                                                                       preskeyc
                                                                                                                                                                                        
                                                                                                                                                                                         pyautogui way; htps/pypi.org/project/pyautogui/
                                                                                                                                                                                          pyautogui.presc
                                                                                                                                                                                           printc pyautogui.typewritec
                                                                                                                                                                                            except else print'failed'
                                                                                                                                                                                             break 
                                                                                                                                                                                              
                                                                                                                                                                                              '
                                                                                                                                                                                              info
                                                                                                                                                                                               -for now only suported for lowercase -not every characters suportcan't handle e.g. 
                                                                                                                                                                                                -typing with scrol lock presed, not loking for presing butons
                                                                                                                                                                                                 -won't block keyboard when presing - typing both virtual and physical keys, cause typing on the scren. we don't want it that way, no not today.
                                                                                                                                                                                                  -for now using ctypes. think of clear code and use pyautogui as option
                                                                                                                                                                                                   -
                                                                                                                                                                                                    
                                                                                                                                                                                                    '
                                                                                                                                                                                                    