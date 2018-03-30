#coding:utf-8
import os
import rstr
import random
import argparse
import string

def gen_urls():
    reg_str = 'ABC'
    reg_str = r'[A-Z]\d[A-Z] \d[A-Z]\d'
    reg_str = '!"#$%&\'()*+,-./@:;<=>[\\]^_`{|}~'
    #reg_str = "((https?://|ftp://|www\.|[^\s:=]+@www\.).*?[a-z_\/0-9\-\#=&])(?=(\.|,|;|\?|\!)?(\"|'|«|»|\[|\s|\r|\n|$))"
    #reg_str = "https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,}"
    #reg_str = "http?[12345]"
    #reg_str = "(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?"
    #reg_str = "(\b(https?)://)?www\.[-A-Za-z0-9+?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"
    reg_str = "^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$"
    reg_str = 'http://{0}.{1}/{2}/?{3}'.format(rstr.domainsafe(),
                                rstr.letters(3),
                                rstr.urlsafe(),
                                rstr.urlsafe())
    #reg_str = "((https?://)?)www\.(([a-z_0-9\-\#=&]{4,10})\.){1,3}(com|cn|org|edu|com\.cn|net|xin|cc|tech|top|info|gov)"                     
    #reg_str = "((https?://)?)(www\.)?(([a-z_0-9\-]{4,10})\.){1,3}(com|cn|org|edu|com\.cn|net|xin|cc|tech|top|info|gov)"                     
    #reg_str = "((https?://)?)(www\.)?(([a-z_0-9\-]{4,10})\.){1,2}(com|cn|org|edu|com\.cn|net|xin|cc|tech|top|info|gov)"                     
    
    #reg_str = "((https?://)?)(www\.)?(([a-z_0-9\-]{3,6})\.){1,2}(com|cn|org|edu|com\.cn|net|xin|cc|tech|top|info|gov)"

    #reg_str_1 = "((https?://)?)(www\.)?(([a-z_0-9\-]{4,8})\.){1}(com|cn|org|edu|com\.cn|net|xin|cc|tech|top|info|gov)"
    #reg_str_2 = "((https?://)?)(www\.)?(([a-z_0-9\-]{3,4})\.){2}(com|cn|org|edu|com\.cn|net|xin|cc|tech|top|info|gov)"
    

    s = rstr.rstr(reg_str, 6, 20)
    s = rstr.xeger(reg_str)
    #print s
    return s 

def gen_equation_atom():
    if g_use_frac:
        if random.choice([0, 1]) == 0:
            return gen_frac()

    return str(random.choice(range(1, 99)))

def gen_frac():
    item_str = '\\frac{0}{1}'
    number1 = random.choice(range(1, 99))
    number2 = random.choice(range(1, 99))

    s = item_str.format('{' + str(number1) + '}', '{' + str(number2) + '}')

    addInteger = random.choice(range(1, 5))
    if addInteger == 1:
        number1 = random.choice(range(1, 99))
        s = str(number1) + s

    return s

def gen_equation_left():
    operator_list = ['+', '-', '×', '÷']
    count_of_operator = random.choice(range(1, 4))
    s = gen_equation_atom()

    bracket_num = 10000
    if random.choice(range(0, 5)) == 0:
        bracket_num = random.choice(range(0, 3)) - 1
    for i in range(count_of_operator):
        if bracket_num == i:
            s = '(' + s + random.choice(operator_list) + gen_equation_atom() + ')'
        else:
            s = s + random.choice(operator_list) + gen_equation_atom()
    return s

def gen_equation_left_with_star_atom():
    operator_list = ['+', '-', '×', '÷']
    count_of_operator = random.choice(range(1, 4))
    s = gen_equation_atom()

    bracket_num = 10000
    if random.choice(range(0, 5)) == 0:
        bracket_num = random.choice(range(0, 3)) - 1

    star_operator_idx = random.choice(range(0, count_of_operator))

    for i in range(count_of_operator):
        if bracket_num == i:
            if star_operator_idx == i:
                s = s + random.choice(operator_list) + '?'
            else:
                s = '(' + s + random.choice(operator_list) + gen_equation_atom() + ')'
        else:
            if star_operator_idx == i:
                s = s + random.choice(operator_list) + '?'
            else:
                s = s + random.choice(operator_list) + gen_equation_atom()
    return s

def gen_star_equator():
    operator_list = ['+', '-', '×', '÷']
    count_of_operator = random.choice(range(1, 4))
    s = gen_equation_atom()

    bracket_num = 10000
    if random.choice(range(0, 5)) == 0:
        bracket_num = random.choice(range(0, 3)) - 1

    unknow_num = random.choice(range(0, count_of_operator))

    for i in range(count_of_operator):
        if bracket_num == i:
            if unknow_num == i:
                s = '(' + s + '?' + gen_equation_atom() + ')'
            else:
                s = '(' + s + random.choice(operator_list) + gen_equation_atom() + ')'
        else:
            if unknow_num == i:
                s = s + '?' + gen_equation_atom()
            else:
                s = s + random.choice(operator_list) + gen_equation_atom()
    return s

def gen_equator():
    return random.choice(['=', '>', '≈', '<', '≤', '≥', '≠'])

def gen_latex():
    equation_str = '{0}{1}{2}'

    left = gen_equation_left()
    right = gen_equation_atom() # a simple result

    if g_use_unkown == 1:
        left = gen_star_equator()
    if g_use_unkown == 2:
        right = '?'

    s = equation_str.format(left, gen_equator(), right)
    if g_use_unkown == 3:
        s = equation_str.format(left, '?', right)

    return s

def gen_daiyu_chufa2():
    num = random.choice(range(1, 10))
    return str(num) + '=?......?'

def gen_daiyu_chusu():
    left = str(random.choice(range(1, 99))) + '......' + str(random.choice(range(1, 10)))
    return left


def main():

    # gen_daiyu_chusu()     # example: 19......5
    # gen_daiyu_chufa2()    # example: 7=?......?
    # gen_equator() # example: ≤
    # gen_star_equator()    # example: 14×10?72×94
    # gen_equation_left_with_star_atom() # example: 98-28÷?×50
    # gen_equation_left()   # example: 54×9÷14
    # gen_frac()            # example: 28\frac{59}{41}
    # gen_equation_atom()   # example: 28
    # gen_urls()            # example: http://qVtptNQV/WbMY_f2t
    total_count = g_total_count

    dst_file = os.path.abspath(g_out_file)
    print "dst file: ", dst_file

    dst_list = []
    for i in range(total_count):
        s = gen_latex()
        dst_list.append(s)

    open(dst_file, 'w').write('\n'.join(dst_list))


if __name__ == '__main__': 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_file",
        help=("input label file.")
    )

    parser.add_argument(
        "total",
        type = int,
        help=("the total num. ")
    )

    # parser.add_argument(
    #     "frac",
    #     type = int,
    #     help=("is use frac or not")
    # )

    parser.add_argument(
        "unknown",
        type = int,
        help=("is use unknown or not")
    )

    args = parser.parse_args()

    g_total_count = args.total
    g_out_file = args.output_file
    g_use_frac = False
    g_use_unkown = args.unknown


    main()


