import sys
from operator import attrgetter
import re


RE = "((?P<coef>[+-]?\d+\.?\d*)?\*?[Xx]\^?(?P<deg>\d+)*)|([+-]?\d+\.?\d*)"
USAGE = "Usage: python3 computor.py \"[EQUATION]\""
EGALE_ERR = "Equation must have one '='"
FORMAT_ERR = "Equation Format is Wrong"
DEG_ERR = "The polynomial degree is stricly greater than 2, I can't solve."

class Term:
    def __init__(self, coeff, deg):
         self.coef = coeff
         self.deg = deg
        
    def __str__(self):
        return f'Coef: {self.coef} -- Deg: {self.deg}'

class Complex:
    def __init__(self, real, imag):
         self.real = real
         self.imag = imag

def sqrt(x, precision):
    res = 0
    pas = 1
    while (pas > precision):
        if (res * res == x):
            break
        elif (res * res > x):
            res -= pas
            pas /= 10
        res += pas
    return(res)

def terms_checker(part):
    if len(part) == 0:
        return False
    for term in part:
        if (len(term) != 4):
            return False
        if (term[0] == "" and term[3] == ""):
            return False
    return True

def deg_checker(term):
    if term == "":
        return 1
    return int(term)

def coefs_degs_checker(part):
    terms = []
    for term in part:
        if (term[0] != ""):
            if (term[1] == ""):
                terms.append(Term(float(1), deg_checker(term[2])))
            elif (float(term[1]) == 0):
                continue
            else:
                terms.append(Term(float(term[1]), deg_checker(term[2])))
        else:
            terms.append(Term(float(term[3]), 0))
    return terms


def parser(str):
    first_part = re.findall(RE, str[0].replace(" ",""))
    second_part = re.findall(RE, str[1].replace(" ",""))

    # ********
    # print(first_part)
    # print(second_part, "\n")
    # ********
    
    # CHECKS
    if not(terms_checker(first_part) and terms_checker(second_part)):
        sys.exit(FORMAT_ERR)
    second_part = coefs_degs_checker(second_part)
    for _ in second_part:
        _.coef *= -1    
    eq = coefs_degs_checker(first_part) + second_part
    equation = [Term(0, 0), Term(0, 1), Term(0, 2)]
    superior_degs = []
    for term in eq:
        if term.deg == 0:
            equation[0].coef += term.coef
        elif term.deg == 1:
            equation[1].coef += term.coef
        elif term.deg == 2:
            equation[2].coef += term.coef
        else:
            superior_degs.append(term)
    
    ### Polynom Degree ####
    i = 0
    j = 0
    while i < len(superior_degs):
        j = i + 1
        while j < len(superior_degs):
            if superior_degs[i].deg == superior_degs[j].deg:
                superior_degs[i].coef += superior_degs[j].coef
                superior_degs.pop(j)
            else:
                j += 1
        i += 1
    superior_degs.sort(key=attrgetter('deg'), reverse=True)

    poly_deg = 0
    for _ in superior_degs+equation:  
        if _.deg > poly_deg and _.coef != 0:
            poly_deg = _.deg

    print('**************')
    print("Polynomial degree: ",poly_deg)
    print('**************')
    print_reduced_form(equation, superior_degs)
    print('**************')
    
    return equation, poly_deg


def print_reduced_form(equation, sup):
    print("Reduced form:", end=" ")
    for _ in sup:
        if _.coef == 0:
            continue
        if _.coef < 0:
            print('-', (_.coef) * -1, end=" ")
        else:
            print('+', _.coef, end=' ')
        print(f'* X^{_.deg}', end=' ')

    for _ in reversed(equation):
        if _.coef == 0:
            continue
        if _.coef < 0:
            print('-', (_.coef) * -1, end=" ")
        else:
            print('+', _.coef, end=' ')
        if _.deg != 0:
            print(f'* X^{_.deg}', end=' ')    
    print("= 0")

def solve_2nd_deg(equation):
    a = equation[2].coef
    b = equation[1].coef
    c = equation[0].coef
    delta = b * b - 4 * a * c
    if delta == 0:
        print(f'Discriminat is null; The solution is: \'{"{:.6f}".format(-b / (2*a))}\'')
    elif delta > 0:
        x1 = (-b + sqrt(delta, 0.00000001))/ (2*a)
        x2 = (-b - sqrt(delta, 0.00000001))/ (2*a)
        print(f'Discriminat is strictly positive; The solutions are:', end=' ')
        print(f'\'{"{:.6f}".format(x1)}\' and \'{"{:.6f}".format(x2)}\'')
    else:
        print('Discriminat is strictly negative; The solutions are:', end=" ")
        re = -b / (2*a)
        im = sqrt(-delta, 0.00000001)/(2*a)
        if re!=0:
            print(f'\'{float("{:.6f}".format(re))} + i*{float("{:.6f}".format(im))}\' and \'{float("{:.6f}".format(re))} - i*{float("{:.6f}".format(im))}\'')
        else:
            print(f'\'i*({float("{:.6f}".format(im))})\' and \'-i*({float("{:.6f}".format(im))})\'')

        

def main(argv):
    argc = len(argv)
    if argc != 2:
        sys.exit(USAGE)
    str = argv[1].split('=')
    if (len(str) != 2):
       sys.exit(EGALE_ERR)
    equation, poly_deg = parser(str)

    if poly_deg > 2:
        sys.exit(DEG_ERR)

    if poly_deg == 0:
        if equation[0].coef == 0:
            print("All Real numbers are Solutions.")
        else:
            print("There are No possible Solutions!")
    elif poly_deg == 1:
        sol = equation[0].coef / equation[1].coef * (-1)
        print(f'The solution is: \'{"{:.6f}".format(sol)}\'')
    else:
        solve_2nd_deg(equation)
        
main(sys.argv)