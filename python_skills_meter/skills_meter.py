import sys
import os
import random
import json


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def read_json(file):
    '''read json file, to dict'''
    with open(file) as f:
        data = json.load(f)
    return data
    
    
def write_json(file, data):
    '''write dict to json file'''
    with open(file, 'w') as fp:
        json.dump(data, fp, sort_keys=True, indent=4, ensure_ascii=False)
    return True
    
    
def parse_questions(data):
    '''from dict to list'''
    out = []
    for key, value in data.items():
        # remove white characters
        key = key.strip()
        value = [item.strip() for item in value]
        
        out.append([key, value])
    return out
    
    
def randomize_questions(data):
    '''randomize questions and options positions'''
    out = data.copy()
    
    # shuffle options position
    for key, value in out:
        random.shuffle(value)
        
    # shuffle questions position
    random.shuffle(out)
    
    return out
    
    
def wrap_questions(data):
    '''add prefix and other, to questions and options'''
    out = []
    options_prefix = 'abcdefghij'
    positive_char = '(+)'
    positive_char_len = len(positive_char)
    
    for key, value in data:
        # add question mark
        if not key.endswith('?'):
            key += '?'
            
        # capitalize first letter
        key = key[0].upper() + key[1:]
        
        # wrap options (a, b, c...)
        wrapped_value = []
        positive = ''
        for index, option in enumerate(value[:5]):     # limit options to number of 5
            if option.endswith(positive_char):
                positive = options_prefix[index]
                option = option[:-positive_char_len]
            wrapped_option = '{}) {}'.format(options_prefix[index], option)
            wrapped_value.append(wrapped_option)
            
        if positive:
            out.append((key, wrapped_value, positive))
    return out
    
    
def str_wrap(data):
    '''return questions wrapped to string format'''
    out = []
    tab = ' '*4
    for key, value, positive in data:
        question = '\n{}'.format(tab).join([key] + value)
        out.append((question, positive))
    return out
    
    
def skills_meter_cmd(data):
    '''command line skill meter'''
    data = str_wrap(data)               # list -> str
    
    total_questions = len(data)
    number_length = len(str(total_questions))
    points = 0
    for key, (question, positive) in enumerate(data):
        print('{}/{}. {}'.format(str(key+1).zfill(number_length), total_questions, question))
        choice = input('option: ').lower().strip()
        if choice == positive:
            points += 1
        print()
        
    points_percentage = (points/total_questions)*100
    user_level = levels(points_percentage)
    print('total points: {}/{}'.format(str(points).zfill(number_length), total_questions))
    print('total percentage: {} [%]'.format(round(points_percentage, 2)))
    print('you are: {}'.format(user_level))
    
    return points_percentage
    
    
def skills_meter_gui(data):
    '''gui skill meter'''
    result = 0
    return result
    
    
def example_write():
    '''example of write to json'''
    questions = {
        'what is the answer?': ('23', '444', '42', '442'),
        'what is the question': ('some', 'option', 'last', 'line'),
        'the value of pi': ('1', '2', '3', '3.14'),
        }
        
    file = 'questions.json'
    write_json(file, questions)
    return False
    
    
def levels(percentage):
    '''map percentage value to user level'''
    
    percentage = min(percentage, 100)
    percentage = max(percentage, 0)
    
    levels_dict = {
        'Computer Illiterate': (0, (100/7)*1),
        'a User': (0, (100/7)*2),
        'an Operator': (0, (100/7)*3),
        'a Nerd': (0, (100/7)*4),
        'a Hacker': (0, (100/7)*5),
        'a Guru': (0, (100/7)*6),
        'a Wizard': (0, (100/7)*7),
    }
    for key, value in levels_dict.items():
        if value[0] <= percentage <= value[1]:
            return key
    return "a Looser"
    
    
if __name__ == "__main__":
    script_path()
    
    file = 'questions.json'
    data = read_json(file)              # json -> dict
    data = parse_questions(data)        # dict -> list
    data = randomize_questions(data)    # list -> list
    data = wrap_questions(data)         # list -> list (3 elements)
    
    
    result = skills_meter_cmd(data)
    # result = skills_meter_gui(data)     # todo
    
    
'''
info, todo:
    -add bar with questions progress (cmd, gui)
    -mix questions and options position (+)
    -make possible to set any number of options (a, b, c, d...) (+)
    -how to mark positive option in .json or .txt?  (+)
    -add read/write to .txt file (human format)
    -
    
'''
