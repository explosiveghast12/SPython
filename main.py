# Based on the Spice3 source code, may have to adapt it for low memory.
# Link: https://github.com/pickleburger/spice3f5/tree/master
# Basically we are making something that can do nodal analysis
# Trying to make this compatible with MicroPython for Casio GFX-9750iii
import math
# may also need cmath for complex numbers

# Constants included in math module

# Not adding transistors yet since I don't need that functionality right now

# global variables
inp = "" # input

nets = {} # nets are stored in a dictionary by net name, this is a dictionary of arrays
components = {} # component names and values, the value is a string and contains Ohms, Henries, Volts, Whatever other info is needed.
undefined_pins = [] # list of pins that are unconnected, add when we add components
equations = []

supported_components = ["r", "i", "c", "v"]

def main():
    print("SPython interface:")
    # Unnecessary if using this as a library for other things

# net/circuit functions

def reset_circuit():
    nets = {} # reset net dictionary

def add_component():
    unit = ""
    print("component to add: ")
    # print supported components?
    for component in supported_components:
        print(component)
    inp = input()

    if inp in supported_components: # we are checking because we need to skip this code otherwise
        match inp:
            case "r":
                unit = "o" # trying to keep these to one character to make life easy
            case "i":
                unit = "h"
            case "c":
                unit = "f"
            case "v":
                unit = "v"
            case _:
                println("you should not be able to read this")
        print("component name: ") # currently there is no function that allows you to change name later
        name = input()
        print("component value: ") # we know based on what they previously chose
        value = input()
        components[name] = value + unit #concatanates string, or at least it is supposed to
        # This will be good enough for basic things, but if you add a voltage source we need to know more.
        # which would be a different case for the component
        # Also, here we need to add unused pins to the list
        # Which we should support pin# instead of just +-
        # Most will only have two pins
        # 0 default is + 1 is -
        undefined_pins.append(name + "-" + 0) # As you can see, we should update this to a for loop
        undefined_pins.append(name + "-" + 1)
        println("component added") # in order to save me some time, they have to define the connections later
        # we also have to keep track of components and values
    

def add_net():
    print("net name: ") # if users want to define nets manually
    temp_net = input()

    if not nets[temp_net]:
        nets[temp_net] = [] # defines net to prevent errors
    
    done = False
    while !done:
        # show current components which can be added to a net, which are just unconnected components
        for i, undef in enumerate(undefined_pins):
            println(f"{i}. {undef}")

        inp = input()
        if inp == "q":
            done = True
        else:
            try:
                nets[temp_net].append(undefined_pins[inp])
            except:
                println("invalid input")
            

def run_rpn(expr):
    # RPN expression evaluator, intellisense made this, it appears to be taken from some other code
    # Add support for constants/variables, if they are grouped together like "jwl" they are multiplied
    # Also keep in mind S = jw or something
    stack = []
    tokens = expr.split()
    for token in tokens:
        if is_operator(token):
            # need to add functions that keep this as a string
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(add(a, b))
            elif token == '-':
                stack.append(subtract(a, b))
            elif token == '*':
                stack.append(mult(a, b))
            elif token == '/':
                stack.append(divide(a, b))
            elif token == '^':
                stack.append(power(a, b))
            else:
                raise ValueError(f"Unknown operator: {token}") # This will never happen
        else:
            stack.append(float(token)) # if this isn't an operator it is either a variable or a number
    return stack[0]

def is_operator(token):
    return token in ['+', '-', '*', '/', '^'] # more intellisense code
    # Also, we should make a array with the tokens, then maybe we don't need this function

def create_nodal():
    system_of_equations = []
    # Current in = current out
    # For AC analysis convert all sources to their phasor equivalents
    # We will have an input, which names nets, and tells what is connected to said nets
    # example: (net1 <= v1+ r1+),(gnd <= r1- v1-)
    # as you can see, all components have a positive and negative terminal at least
    # this is so we can determine which side is connected to which net
    # which will help when determining sign with
    for i, net_name, p in enumerate(nets): # hopefully enumerate works with dictionaries
        for pin in p:
            system_of_equations[i] += component_equation(pin)

def component_equation(component):
    # this just connects functions to return equation to any component, so this function is general.
    # I should check spice to see how they handle this stuff before I continue this way
    # Because this does not seem better
    # need to parse component (which is really just the pin in the net) first
    # which should be given as componentName-pin#
    parts = component.split("-")
    comp_name = parts[0]
    pin_num = parts[1]
    comp_type = components[comp_name][-1] # last character in string of the components value is the unit, which tells how we treat this component
    match comp_type:
        case "r":
            pass
        case "i":
            pass
        case "c":
            pass
        case "v":
            pass
        case _:
            pass

def capacitor_impedence(C, w):
    return "1 jwC /"
    # maybe we need to use strings and evaluate them later
    # or we can have people enter w if it isn't complex, then we will evaluate it as far as possible
    # we should use different functions for known vs unknown capacitance/frequency

def inductor_impedence(L, w):
    return "jwL"

def evaluate_nodes():
    pass

# normal math

def add(x, y):
    # How do we add variables?
    # If both are (complex or normal) numbers
    return x + y
    # else just return "x y +"

def subtract(x, y):
    # if both numbers
    return x - y
    # else return "x y -"

def mult(x, y):
    # if both numbers
    return x * y
    # else return "xy"

def divide(x, y):
    # if both numbers
    return x / y
    # else return "x y /"

def power(x, y):
    # if both numbers
    return x ** y
    # else return "x y ^"

def factorial(x):
    #idk

# Math approximations

def opto_power(x):
    # Approximate 10^x using e^(x * ln(10)), intellisense power
    ln10 = 2.302585092994046
    return exp(x * ln10)

def fast_power(x):
    # Using

def exp(x): # intellisense wrote this
    # Taylor series expansion for e^x
    n_terms = 20  # Number of terms in the series, increase if not accurate enough
    result = 0
    factorial = 1
    for n in range(n_terms):
        if n > 0:
            factorial *= n  # n!
        result += (x ** n) / factorial
    return result

def fast_exp(x):
    # Faster exponentials using continued fractions
    depth = 10  # Depth of the continued fraction
    approximation = 1
    # If you trust intellisense this works
    # I'm making tests so we will see
    for n in range(depth, 0, -1):
        approximation = 1 + (x / n) * approximation
    return approximation

# Math with imagination support, nevermind, apparently python already supports out imagination

# Matrix data structure (define with array and row size) (if we need weird matrices we can add that later)
# This is here for reference

# (numbers[], rowsize)

# Laplace transform

# Tables ;)

# We are using RPN for the simplification table

simplification_table = [
    ("t dd", "1"), # dd means dirac-delta
    ("t tau - dd", "e -s tau * ^"),
    ("t u", "1 s /"), # u means unit step
    ("t tau - u", "e -s tau * ^"),
    ("t t u *", "1 s 2 ^ /"),
    ("", ""),
]

def laplace():
    pass

# DFT

def dft():
    # Sum array of arr[n] * e^((-2pi i kn)/N) for k = 0 to N-1. Wow, intellisense knows.

def inv_dft():
    pass

# FFT
# https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html

def fft():
    pass

# Parsing

# Matrix operations
# which ones do we need?

def rref():
    pass

def mat_mult():
    pass

def determinant():
    pass