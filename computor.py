import sys
import re


RE = "((?P<coef>[+-]?\d+\.?\d*)?\*?[Xx]\^?(?P<deg>\d+)*)|([+-]?\d+\.?\d*)"
USAGE = "Usage:"
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

def terms_checker(part):
    if len(part) == 0:
        return False
    for term in part:
        if (len(term) != 4):
            return False
        if (term[1] == "" and term[3] == ""):
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
    print(first_part)
    print(second_part, "\n")
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
        # else:
        #     superior_degs.append(term)
    print("SUP!!", superior_degs[0].deg)
# *************************************
    poly_deg = 0

    for _ in equation:
        if _.deg > poly_deg and _.coef != 0:
            poly_deg = _.deg
    # *************
    print("Equation: ")
    for _ in equation:
        print(_)
    print('\n')
    # *************
    return equation, poly_deg

def print_reduced_form(equation):
    print("**************\nReduced form:", end=" ")
    for _ in reversed(equation):
        if _.coef != 0:
            if _.coef < 0:
                if _.coef == -1:
                    print('-',end=" ")
                else:
                    print(f"- {_.coef*(-1)}", end=" ")
            else:
                if _.deg == 0:
                    print(f"{_.coef}", end=" ")
                elif _.coef == 1:
                    print('+',end=" ")
                else:
                    print(f"+ {_.coef} *", end=" ")
            if _.deg != 0:
                print(f"X^{_.deg}", end=" ")
        elif _.deg == 0:
            print(f"{_.coef}", end=" ")
    print("= 0\n**************")

def main(argv):
    argc = len(argv)
    if argc != 2:
        sys.exit(USAGE)
    str = argv[1].split('=')
    if (len(str) != 2):
       sys.exit(EGALE_ERR)
    equation, poly_deg = parser(str)
    
    print("**************\nPolynomial degree: ",poly_deg)
    if poly_deg > 2:
        sys.exit(DEG_ERR)
    
    # SIMPLIFY
    print_reduced_form(equation)
    # SOLVE

    if poly_deg == 0:
        if equation[0].coef == 0:
            print("All Real numbers are Solutions.")
        else:
            print("There are No possible Solutions!")
    elif poly_deg == 1:
        print("The solution is: ", equation[0].coef / equation[1].coef * (-1))
        



if __name__ == "__main__":
	main(sys.argv)