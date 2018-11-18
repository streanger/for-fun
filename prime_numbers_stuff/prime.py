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

def simple_write(file, str_content):
    '''simple_write data to .txt file, with specified strContent'''
    with open(file, "w", encoding="utf-8") as f:
        f.write(str_content + "\n")
        f.close()
    return True
    
def concat_files(files):
    out = "\n".join([simple_read(file).strip() for file in files])
    simple_write("total.txt", out)
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
            # yield x
            print(x)
            
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
            
def gen_diff(data):
    out = []
    left = data[::2]
    right = data[1::2]
    for key, _ in enumerate(left):
        left_sum = sum(left[:key])
        left_sum_up = sum(left[:key+1])
        right_sum = sum(right[:key])
        # print("{}. {} {} {} {}".format(key, left_sum, right_sum, (left_sum - right_sum), (left_sum + left_sum_up - 2*right_sum)))
        # print(left[key], right[key])
        # print("{}. {}".format(key, (left_sum + left_sum_up - 2*right_sum)))
        out.append(left_sum + left_sum_up - 2*right_sum)
    # print()
    return out
    
def print_column(data):
    for item in data:
        print(item, end='\n')
    print()
    return True

def draw_chart(data, subtitle="example name"):
    plt.plot(data)
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
    path = script_path()
    begin = time.time()
    # some = list(gen_prime(0, 2000))           # generate from function
    data_file = "total.txt"
    files = [item for item in os.listdir() if item.endswith(".txt") and item != data_file]
    concat_files(files)
    data = read_prime_from_file(data_file)     # read from file
    diff = gen_diff(data)
    draw_chart(diff, subtitle="prime number pairs diff from <{}>".format(data_file))
    print("time elapsed: {}".format(time.time() - begin))
    # print_column(some)
    
    
if __name__ == "__main__":
    main()
    # gen_prime(300000, 600000)
    
    
    