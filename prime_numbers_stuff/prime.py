import os
import sys
import time
import matplotlib.pyplot as plt

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def simple_read(file_name):
    '''simple_read data from specified file_name'''
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            # file_content = file.read().splitlines()
            file_content = file.read()
    except:
        file_content = []
    return file_content

def simple_write(file, str_content, mode):
    '''simple_write data to .txt file, with specified strContent'''
    with open(file, mode, encoding="utf-8") as f:
        f.write(str_content + "\n")
        f.close()
    return True
    
def concat_files(files):
    out = "\n".join([simple_read(file).strip() for file in files])
    simple_write("total.txt", out, "w")
    return True

def gen_prime(start, stop):
    ''' generate prime numbers in specified range '''
    if start < 2:
        start = 2
    for x in range(start, stop+1):
        counter = 0
        for divider in range(2, x+1):
            if x % divider == 0:
                counter += 1
                if counter > 1:
                    break
        if counter == 1:
            yield x

def gen_prime_to_file(file):
    ''' it checks the last number and continue '''
    script_path()
    print("< prime numbers generate in progress >")
    while True:
        # check the last item
        lastItem = read_prime_from_file(file)
        if lastItem:
            lastItem = lastItem[-1] + 1
        else:
            lastItem = 2
        start = lastItem
        stop = lastItem + 100000
        if start < 2:
            start = 2
        for x in range(start, stop+1):
            counter = 0
            for divider in range(2, x+1):
                if x % divider == 0:
                    counter += 1
                    if counter > 1:
                        break
            if counter == 1:
                simple_write(file, str(x), mode='a')
    return True
    
def check_prime(list_data):
    ''' check if items in list are prime '''
    for x in list_data:
        counter = 0
        for divider in range(2, x+1):
            if x % divider == 0:
                counter += 1
                if counter > 1:
                    break
        if counter == 1:
            yield x

def digits_sum(number):
    return sum([int(item) for item in list(str(number))])
    
def gen_diff(data, var):
    out = []
    left = data[::2]
    right = data[1::2]
    for key, _ in enumerate(left[:-1]):         # -1 is to prevent different lenght of columns
        if var == 1:
            left_sum = sum(left[:key])
            left_sum_up = sum(left[:key+1])
            right_sum = sum(right[:key])
            # print("{}. {} {} {} {}".format(key, left_sum, right_sum, (left_sum - right_sum), (left_sum + left_sum_up - 2*right_sum)))
            # print(left[key], right[key])
            # print("{}. {}".format(key, (left_sum + left_sum_up - 2*right_sum)))
            out.append(left_sum + left_sum_up - 2*right_sum)
        elif var == 2:
            out.append(left[key] - right[key])
            print(left[key], right[key])
        elif var == 3:
            out.append(digits_sum(left[key]) + digits_sum(right[key]))
        elif var == 4:
            out.append(left[key] - right[key])
        else:
            out.append(left[key] - right[key])
    # print()
    return out
    
def print_column(data):
    for item in data:
        print(item, end='\n')
    print()
    return True

def draw_chart(data, subtitle="example name"):
    plt.plot(data, linewidth=0.5)
    plt.ylabel("diff between pairs")
    plt.xlabel("number/2")
    plt.grid()
    plt.suptitle(subtitle)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')       #full window
    # plt.savefig(subtitle.split('.')[0] + ".png")
    if 1:
        plt.show()
        plt.close()
    return True
    
def read_prime_from_file(file):
    '''simple_read data from specified file_name'''
    try:
        with open(file, "r", encoding="utf-8") as file:
            file_content = file.read().splitlines()
    except:
        file_content = []
    return [int(item) for item in file_content if item.strip()]
    
def main():
    data_file = "total.txt"
    # files = [item for item in os.listdir() if item.endswith(".txt") and item != data_file]
    # concat_files(files)

    data = read_prime_from_file(data_file)     # read from file
    # data = data[:20000]
    diff = gen_diff(data, 3)                   # create different types of data
    draw_chart(diff, subtitle="prime number pairs diff from <{}>".format(data_file))
    return True
    
    
if __name__ == "__main__":
    path = script_path()
    main()
    # gen_prime_to_file("total.txt")            # it will continue to append new numbers
    
    
    
    