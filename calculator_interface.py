'''
todo:
1.写基本图形界面 ！
2.写基本计算内核 ！
3.写输入错误处理 ！
4.进制转化 !
5.高级函数 !
6.图形界面美化 !
'''

'''
计算基本思路：
1.通过正则表达式将计算式转化为包含【数字/字母】 【括号】 【高级函数】 【运算符】的列表
2.递归
    2.1写基本运算，即运算中没有括号的运算，包括高级函数、乘除、加减
    2.2写去除括号，对最内层括号调用基本运算，将括号去除；再到外层递归去括号直到所有括号去除
    2.3最后将无括号的结果进行最后一次基本运算
3.得到长度为1或2的列表，1则正数，2为负数，将结果以字符串形式输出
'''
import tkinter as tk
import re
from math import *


# 先把字符串转化成列表
def eq_format(eq):
    '''
    :param eq:未处理的字符串计算式
    :return: 将数字、运算符、函数拆解开的列表形式的计算式
    '''
    format_list = re.findall('[\w\.]+|\(|\+|\-|\*|\/|\)|sin|cos|sqrt|exp',
                             eq)  # 正则表达式模式为'找到数字、字母、小数点的整体 或者 四则运算符 或者 高级函数'
    return format_list


# 对于存在+-，++等运算符联立的情况进行处理
def change(eq, count):
    '''
    :param eq: 存在运算符连立的列表计算式
    :param count: 连立运算符的下标
    :return: 去除连立运算符的列表计算式
    '''
    if eq[count] == '-':
        if eq[count - 1] == '-':
            eq[count - 1] = '+'
            del eq[count]
        elif eq[count - 1] == '+':
            eq[count - 1] = '-'
            del eq[count]
    return eq


# 去括号
def simplify(format_list):
    '''
    :param format_list: 未去除括号的列表
    :return: 去除一层括号的列表——递归去各层
    '''
    bracket = 0  # 用于存放左括号在格式化列表中的索引
    count = 0  # 存放括号的下标
    for i in format_list:
        if i == '(':
            bracket = count
        elif i == ')':
            temp = format_list[bracket + 1: count]
            new_temp = calculate(temp)
            format_list = format_list[:bracket] + new_temp + format_list[count + 1:]
            format_list = change(format_list, bracket)  # 解决去括号后会出现的--  +- 问题
            return simplify(format_list)  # 递归去括号
        count = count + 1
    return format_list  # 当递归到最后一层的时候，不再有括号，因此返回列表


def remove_high_function(eq):
    '''
    :param eq: 存在高级函数的列表计算式
    :return: 去除高级函数的列表计算式
    '''
    count = 0  # 高级函数的位置下标
    for i in eq:
        if i == 'sin':
            if eq[count + 1] != '-':
                eq[count] = sin(float(eq[count + 1]))  # 计算【函数】，【函数输入】，在高级函数的位置将结果替换
                del (eq[count + 1])  # 删除函数输入
            elif eq[count + 1] == '-':  # 如果结构是【函数】，【-】，【函数输入】，则先删除中间
                eq[count + 2] = sin(float(eq[count + 2]))
                eq[count] = '-'
                del (eq[count + 1])
            eq = change(eq, count - 1)  # 去除连立运算符
            return remove_high_function(eq)
        elif i == 'cos':
            if eq[count + 1] != '-':
                eq[count] = cos(float(eq[count + 1]))
                del (eq[count + 1])
            elif eq[count + 1] == '-':
                eq[count + 2] = cos(float(eq[count + 2]))
                del (eq[count])
                del (eq[count])
            eq = change(eq, count - 1)
            return remove_high_function(eq)
        elif i == 'sqrt':
            if eq[count + 1] != '-':
                eq[count] = sqrt(float(eq[count + 1]))
                del (eq[count + 1])
            else:
                pass  # 放在主函数里报错
        elif i == 'exp':
            if eq[count + 1] != '-':
                eq[count] = exp(float(eq[count + 1]))
                del (eq[count + 1])
            elif eq[count + 1] == '-':
                eq[count + 2] = exp(float(-eq[count + 2]))
                del (eq[count])
                del (eq[count])
            eq = change(eq, count - 1)
            return remove_high_function(eq)
        count = count + 1
    return eq


# 做乘除
def remove_multiplication_division(eq):
    '''
    :param eq: 去除高级函数后的列表计算时
    :return: 去除高级函数和乘除运算的列表计算时
    '''
    count = 0
    for i in eq:
        if i == '*':
            if eq[count + 1] != '-':
                eq[count - 1] = float(eq[count - 1]) * float(eq[count + 1])
                del (eq[count])
                del (eq[count])
            elif eq[count + 1] == '-':
                eq[count] = float(eq[count - 1]) * float(eq[count + 2])
                eq[count - 1] = '-'
                del (eq[count + 1])
                del (eq[count + 1])
            eq = change(eq, count - 1)
            return remove_multiplication_division(eq)
        elif i == '/':
            if eq[count + 1] != '-':
                eq[count - 1] = float(eq[count - 1]) / float(eq[count + 1])
                del (eq[count])
                del (eq[count])
            elif eq[count + 1] == '-':
                eq[count] = float(eq[count - 1]) / float(eq[count + 2])
                eq[count - 1] = '-'
                del (eq[count + 1])
                del (eq[count + 1])  # 上次删除后，下标改变，原count+2变为count+1
            eq = change(eq, count - 1)
            return remove_multiplication_division(eq)
        count = count + 1
    return eq


# 做加减
def remove_plus_minus(eq):
    '''
    :param eq: 去除高级函数、乘除运算的列表运算式
    :return: 最后结果（列表）
    '''
    count = 0
    if eq[0] != '-':
        sum = float(eq[0])
    else:
        sum = 0.0
    for i in eq:
        if i == '-':
            sum = sum - float(eq[count + 1])
        elif i == '+':
            sum = sum + float(eq[count + 1])
        count = count + 1
    if sum >= 0:
        eq = [str(sum)]
    else:
        eq = ['-', str(-sum)]
    return eq


# 基本计算
def calculate(s_eq):
    if 'sin' or 'cos' or 'sqrt' or 'exp' in s_eq:
        s_eq = remove_high_function(s_eq)
    if '*' or '/' in s_eq:
        s_eq = remove_multiplication_division(s_eq)
    if '+' or '-' in s_eq:
        s_eq = remove_plus_minus(s_eq)
    return s_eq


# 计算内核主程序
def caculator(eq):
    format_list = eq_format(eq)
    s_eq = simplify(format_list)
    ans = calculate(s_eq)
    if len(ans) == 2:
        ans = -float(ans[1])
    else:
        ans = float(ans[0])
    return ans


# 多进制计算主程序——只能进行2 8 16的整数加减计算
# 将各进制的数先转化为10进制，计算加减结果后得到10进制结果，再将10进制结果转化为各进制
def multiple_calculator(eq):
    flag = sys.get()
    if flag == 2:
        eq = eq_format(eq)
        count = 0
        if eq[0] != '-':
            sum = int(eq[0], 8)
        else:
            sum = 0
        for i in eq:
            if i == '-':
                sum = sum - int(eq[count + 1], 8)
            elif i == '+':
                sum = sum + int(eq[count + 1], 8)
            count = count + 1
        if sum >= 0:
            eq = [str(oct(sum))]
        else:
            eq = ['-' + str(oct(-sum))]
        return eq[0]
    elif flag == 3:
        eq = eq_format(eq)
        count = 0
        if eq[0] != '-':
            sum = int(eq[0], 16)
        else:
            sum = 0
        for i in eq:
            if i == '-':
                sum = sum - int(eq[count + 1], 16)
            elif i == '+':
                sum = sum + int(eq[count + 1], 16)
            count = count + 1
        if sum >= 0:
            eq = [str(hex(sum))]
        else:
            eq = ['-' + str(hex(-sum))]
        return eq[0]
    elif flag == 4:
        eq = eq_format(eq)
        count = 0
        if eq[0] != '-':
            sum = int(eq[0], 2)
        else:
            sum = 0
        for i in eq:
            if i == '-':
                sum = sum - int(eq[count + 1], 2)
            elif i == '+':
                sum = sum + int(eq[count + 1], 2)
            count = count + 1
        if sum >= 0:
            eq = [str(bin(sum))]
        else:
            eq = ['-' + str(bin(-sum))]
        return eq[0]


# 按钮输入
def button_entry(entry):
    equation_temp = equation.get()
    result_temp = result.get()
    if result_temp != '':  # 如果之前计算过结果，则清空屏幕进行新的计算
        equation_temp = '0'
        result_temp = ''
        result.set(result_temp)
    if equation_temp == '0':  # 如果初始方程显示的是0，则输入的新数字直接替换0
        equation_temp = ''
    equation_temp += entry
    equation.set(equation_temp)


# 清空屏幕
def all_clear():
    equation.set('0')
    result.set('')


# 显示结果
def show_outcome():
    try:
        if sys.get() == 1:
            equation_temp = equation.get()
            equation_temp = equation_temp.replace('X', '*')  # 将输入的计算式中的运算符替换为可计算的
            equation_temp = equation_temp.replace('÷', '/')
            ans = caculator(equation_temp)
            ans = '%.2f' % ans
            if str(ans).endswith('.00'):  # 如果结果为整数，则去掉小数部分
                result.set(str(ans[0:-3]))
            else:
                result.set(str(ans))
        else:  # 对于多进制计算则调用多进制计算器
            equation_temp = equation.get()
            ans = multiple_calculator(equation_temp)
            result.set(str(ans))
    except:
        result.set('Error!Check your input!')  # 如果计算输入错误，则在屏幕上显示错误，请检查输入


# 退格，将算式的最后一个字符去掉
def back():
    equation_temp = equation.get()
    equation.set(equation_temp[:-1])


# 对结果进行进制转换，需要知道转换前后的进制
# 1十进制 2八进制 3十六进制 4二进制
def choose_sys():
    result_temp = result.get()
    try:
        if result_temp:  # 如果结果为空则不转换
            if not re.findall(r'\.\d+', result_temp):  # 如果找到小数点和后面的数则屏幕报错只能转换整数
                if sys.get() == 1:
                    if previous_sys.get() == 1:
                        pass
                    elif previous_sys.get() == 2:
                        result_temp = str(int(result_temp, 8))
                    elif previous_sys.get() == 3:
                        result_temp = str(int(result_temp, 16))
                    elif previous_sys.get() == 4:
                        result_temp = str(int(result_temp, 2))
                    previous_sys.set(1)
                elif sys.get() == 2:
                    if previous_sys.get() == 1:
                        result_temp = str(oct(int(result_temp)))
                    elif previous_sys.get() == 2:
                        pass
                    elif previous_sys.get() == 3:
                        result_temp = int(str(result_temp), 16)
                        result_temp = str(oct(int(result_temp)))
                    elif previous_sys.get() == 4:
                        result_temp = int(str(result_temp), 2)
                        result_temp = str(oct(int(result_temp)))
                    previous_sys.set(2)
                elif sys.get() == 3:
                    if previous_sys.get() == 1:
                        result_temp = str(hex(int(result_temp)))
                    elif previous_sys.get() == 2:
                        result_temp = int(str(result_temp), 8)
                        result_temp = str(hex(int(result_temp)))
                    elif previous_sys.get() == 3:
                        pass
                    elif previous_sys.get() == 4:
                        result_temp = int(str(result_temp), 2)
                        result_temp = str(hex(int(result_temp)))
                    previous_sys.set(3)
                elif sys.get() == 4:
                    if previous_sys.get() == 1:
                        result_temp = str(bin(int(result_temp)))
                    elif previous_sys.get() == 2:
                        result_temp = int(str(result_temp), 8)
                        result_temp = str(bin(int(result_temp)))
                    elif previous_sys.get() == 3:
                        result_temp = int(str(result_temp), 16)
                        result_temp = str(bin(int(result_temp)))
                    elif previous_sys.get() == 4:
                        result_temp = int(str(result_temp), 2)
                        result_temp = str(bin(int(result_temp)))
                    previous_sys.set(4)
                result.set(result_temp)
            else:
                result.set('Can not convert float!')
    except:  # 如出现因为输入问题等转化错误则屏幕报错转化错误
        result.set('Convert Fail!')
    finally:  # 为保证记录转化前进制的准确性，使用finally语句
        if sys.get() == 1:
            previous_sys.set(1)
        elif sys.get() == 2:
            previous_sys.set(2)
        elif sys.get() == 3:
            previous_sys.set(3)
        elif sys.get() == 4:
            previous_sys.set(4)


# 定义主窗口
window = tk.Tk()
window.title('Calculator')
window.resizable(0, 0)
window.geometry('400x475')
# 设定字符串变量
result = tk.StringVar()  # 记录并显示结果
equation = tk.StringVar()  # 记录并显示算式
result.set('')
equation.set('0')
# 设定显示输入方程和结果的Label
show_equation = tk.Label(window, textvariable=equation, bg='white', fg='black', font=('Arail', '15'), bd='0',
                         anchor='se')
show_result = tk.Label(window, textvariable=result, bg='white', fg='black', font=('Arail', '30'), bd='0', anchor='se')
show_equation.place(x='10', y='10', width='380', height='50')
show_result.place(x='10', y='60', width='380', height='50')
# 设定进制选择
sys = tk.IntVar()
sys.set(1)
previous_sys = tk.IntVar()
previous_sys.set(1)
button_dec = tk.Radiobutton(window, text="DEC", command=choose_sys, variable=sys, value=1).place(x='10', y='120',
                                                                                                 width='80',
                                                                                                 height='20')
button_oct = tk.Radiobutton(window, text="OCT", command=choose_sys, variable=sys, value=2).place(x='100', y='120',
                                                                                                 width='80',
                                                                                                 height='20')
button_hex = tk.Radiobutton(window, text="HEX", command=choose_sys, variable=sys, value=3).place(x='190', y='120',
                                                                                                 width='80',
                                                                                                 height='20')
button_bin = tk.Radiobutton(window, text="BIN", command=choose_sys, variable=sys, value=4).place(x='280', y='120',
                                                                                                 width='80',
                                                                                                 height='20')
# 设定各种按钮
# x=10,90,170,250，330 y=150,205,260,315,370,425
# 第一行按钮
button_sin = tk.Button(window, text='sin', command=lambda: button_entry('sin'))
button_sin.place(x='10', y='150', width='60', height='40')
button_cos = tk.Button(window, text='cos', command=lambda: button_entry('cos'))
button_cos.place(x='90', y='150', width='60', height='40')
button_sqrt = tk.Button(window, text='sqrt', command=lambda: button_entry('sqrt'))
button_sqrt.place(x='170', y='150', width='60', height='40')
button_exp = tk.Button(window, text='exp', command=lambda: button_entry('exp'))
button_exp.place(x='250', y='150', width='60', height='40')
# 第二行按钮
button_ac = tk.Button(window, text='AC', command=all_clear)
button_ac.place(x='10', y='205', width='60', height='40')
button_back = tk.Button(window, text='Back', command=back)
button_back.place(x='90', y='205', width='60', height='40')
button_dot = tk.Button(window, text='.', command=lambda: button_entry('.'))
button_dot.place(x='170', y='205', width='60', height='40')
button_division = tk.Button(window, text='÷', command=lambda: button_entry('÷'))
button_division.place(x='250', y='205', width='60', height='40')
# 第三行按钮
button_7 = tk.Button(window, text='7', command=lambda: button_entry('7'))
button_7.place(x='10', y='260', width='60', height='40')
button_8 = tk.Button(window, text='8', command=lambda: button_entry('8'))
button_8.place(x='90', y='260', width='60', height='40')
button_9 = tk.Button(window, text='9', command=lambda: button_entry('9'))
button_9.place(x='170', y='260', width='60', height='40')
button_multi = tk.Button(window, text='X', command=lambda: button_entry('X'))
button_multi.place(x='250', y='260', width='60', height='40')
# 第四行按钮
button_4 = tk.Button(window, text='4', command=lambda: button_entry('4'))
button_4.place(x='10', y='315', width='60', height='40')
button_5 = tk.Button(window, text='5', command=lambda: button_entry('5'))
button_5.place(x='90', y='315', width='60', height='40')
button_6 = tk.Button(window, text='6', command=lambda: button_entry('6'))
button_6.place(x='170', y='315', width='60', height='40')
button_sub = tk.Button(window, text='-', command=lambda: button_entry('-'))
button_sub.place(x='250', y='315', width='60', height='40')
# 第五行按钮
button_1 = tk.Button(window, text='1', command=lambda: button_entry('1'))
button_1.place(x='10', y='370', width='60', height='40')
button_2 = tk.Button(window, text='2', command=lambda: button_entry('2'))
button_2.place(x='90', y='370', width='60', height='40')
button_3 = tk.Button(window, text='3', command=lambda: button_entry('3'))
button_3.place(x='170', y='370', width='60', height='40')
button_plus = tk.Button(window, text='+', command=lambda: button_entry('+'))
button_plus.place(x='250', y='370', width='60', height='40')
# 第六行按钮
button_0 = tk.Button(window, text='0', command=lambda: button_entry('0'))
button_0.place(x='10', y='425', width='60', height='40')
button_lbracket = tk.Button(window, text='(', command=lambda: button_entry('('))
button_lbracket.place(x='90', y='425', width='60', height='40')
button_rbracket = tk.Button(window, text=')', command=lambda: button_entry(')'))
button_rbracket.place(x='170', y='425', width='60', height='40')
button_equal = tk.Button(window, text='=', command=show_outcome)
button_equal.place(x='250', y='425', width='60', height='40')
# 第五列按钮
button_a = tk.Button(window, text='a', command=lambda: button_entry('a'))
button_a.place(x='330', y='150', width='60', height='40')
button_b = tk.Button(window, text='b', command=lambda: button_entry('b'))
button_b.place(x='330', y='205', width='60', height='40')
button_c = tk.Button(window, text='c', command=lambda: button_entry('c'))
button_c.place(x='330', y='260', width='60', height='40')
button_d = tk.Button(window, text='d', command=lambda: button_entry('d'))
button_d.place(x='330', y='315', width='60', height='40')
button_e = tk.Button(window, text='e', command=lambda: button_entry('e'))
button_e.place(x='330', y='370', width='60', height='40')
button_f = tk.Button(window, text='f', command=lambda: button_entry('f'))
button_f.place(x='330', y='425', width='60', height='40')

window.mainloop()
