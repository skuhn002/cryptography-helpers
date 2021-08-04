def find_mlt_inv(cur_mult="input", mod_max="input"):
    """ Find the multiplicative inverse of a current multiplier(mod "mod_max")
    --------------------------------------------------------------------------
    Parameters:
        cur_mult: int
            The current multiplier
        mod_max: int
            The current divisor inside the modulus
                i.e. 10 + 7(mod 5) where 5 would be mod_max
    Return:
        mlt_inv : int
            The multiplicative inverse of cur_mult(mod_max)
    """
    import numpy as np
    import easygui

    if cur_mult == "input":
        cur_mult = easygui.integerbox("What is the current multiplier you want to get rid of?")
    if mod_max == "input":
         mod_max = easygui.integerbox("What is the number in parenthesis after the word \'mod\'?")

    if type(cur_mult) != int or type(mod_max) != int:
        print("One of the inputs isn't an interger")
        print("cur_mult is of type:" + str(type(cur_mult)))
        print("mod_max is of type:" + str(type(mod_max)))
        return None

    mod_max = [i for i in range(mod_max)]

    mltpls = np.array([])

    for i in mod_max:
        show = i * cur_mult % 26
        print(str(i) + " x 7 % 26   =  " + str(show))

        if show == 1:
            mlt_inv = i
            print("The multiplicative inverse is: \t" + str(mlt_inv))
            return mlt_inv

    er_no_inv = "There was no multiplicative inverse found"

    return er_no_inv

class crp:
    """ An object for handling Cryptography based manipulations
    --------------------------------------------------------
    """
    def __init__(self, ctx="", ptx="", nvl_elms=[]):
        self.cyphertext = ctx
        self.plaintext = ptx
        self.nvl_elms = nvl_elms
        if len(ctx) > 0:
            self.n_elms = len(ctx)
        if len(ptx) > 0:
            self.n_elms = len(ptx)

    def update_ctx(self, ctx):
        self.cyphertext = ctx

    def update_ptx(self, ptx):
        self.plaintext = ptx

    def find_elms(self):
        #elms in ctx

        for i in range(len(self.cyphertext)):
            if self.cyphertext[i] not in self.nvl_elms:
                self.nvl_elms.append(self.cyphertext[i])
                print(self.cyphertext[i])

    def frqnc_of_elm(self, elm):
        e_cnt = 0

        for i in range(len(self.cyphertext)):
            if self.cyphertext[i] == elm:
                e_cnt+= 1

        frq = e_cnt / self.n_elms

        return frq*100

    def show_elm_frqs(self):
        self.frqnc_dict = {}

        if len(self.nvl_elms) == 0:
            self.find_elms()

        for i in range(len(self.nvl_elms)):
            elm = str(self.nvl_elms[i])
            frqnc_of_elm = self.frqnc_of_elm(self.nvl_elms[i])

            iPair = {elm : frqnc_of_elm}

            self.frqnc_dict.update(iPair)

            print(elm + ": " + str(frqnc_of_elm))
        print(self.frqnc_dict)

    def frqnc_order(self):
        elms_cpy = self.nvl_elms.copy()

        for i in range(len(elms_cpy)):
            cur_high_frqnc = -1

            j = i

            for j in range(len(elms_cpy)):
                check_elm = elms_cpy[j]
                check_frqnc = self.frqnc_dict[check_elm]

                if check_frqnc >= cur_high_frqnc:
                    cur_high_frqnc = check_frqnc
                    high_frqnc_indx = j

            #remove an elm from elms_cpy
            if len(elms_cpy) > 0:
                elm_2_rmv = elms_cpy[high_frqnc_indx]
                elms_cpy.remove(elm_2_rmv)
                #print("removed " + elm_2_rmv)


            print(str(elm_2_rmv) + ": " + str(cur_high_frqnc))

    def test_shift(self, shift=0):
        self.testtext = ''
        for i in range(len(self.cyphertext)):
            ascii = ord(self.cyphertext[i])
            new_ascii = ascii + shift
            if new_ascii > 122:
                new_ascii -= 26

            new_chr = chr(new_ascii)
            self.testtext = self.testtext + (new_chr)

    def chk_all_shifts(self):
        for i in range(26):
            self.test_shift(i)
            print("shift " + str(i) + " : " + self.testtext)

def fast_mod_exp(base, power, modulus=-1):
    """ A function to do fast modular exponentiation.
    ------------------------------------------------
    Parameters:
        base
            - int : base number
        power
            - int : power to raise base todo
        modulus
            - int : modulus
            - in the case of Fermat's Little Theroem, the modulus will be equal to the power
            - Set to -1 as default
                - if modulus is set to -1 then modulus is set equal to power
    Return:
        answer
            - int : represents base to the power (mod modulus)
    """
    import math

    if modulus == -1:
        modulus = power

    modular_equivalents = [] #these are the modular equivalents of powers of the base

    max_pow_2chk = 1

    while max_pow_2chk < power :
        modular_equivalents.append(pow(base, max_pow_2chk) % modulus)
        max_pow_2chk = max_pow_2chk * 2

    #if max_pow_2chk > power :
        #print("The highest power of " + str(base) + " neccesary to represent " + str(base) + "^" + str(power) + " is " + str(max_pow_2chk/2))


    max_pow = max_pow_2chk/2
    max_pow_copy = max_pow

    coef_4_binary_expand = [] #the zero-th coeficcient corresponds to the largest power in the decomposition

    answer = -1 #default for error detection

    sum_pows_of_bases = 0

    solution = ""

    while max_pow_copy >= 1 and sum_pows_of_bases != power:
        index_of_power = int(math.log(max_pow_copy, 2)) #this index of power can also be thought of as how many doublings the current max_pow_copy represents
        if answer == -1:
            answer = modular_equivalents[index_of_power]
            sum_pows_of_bases = max_pow_copy
            solution = str(base) + "^" + str(int(max_pow_copy))

        if power - sum_pows_of_bases - max_pow_copy >= 0:
            if answer != -1:
                answer = answer * modular_equivalents[index_of_power] % modulus
                sum_pows_of_bases += max_pow_copy
                solution = solution + " * " + str(base) + "^" + str(int(max_pow_copy))
        max_pow_copy = max_pow_copy / 2




    high_rmndr = modular_equivalents[int(math.log(max_pow, 2))]

    #print("The remainder of the highest power, smaller than " + str(power) + ", moduluo " + str(power) + ", is " + str(high_rmndr))

    problem = str(base) + "^" + str(power) + " (mod " + str(modulus) + ")"

    answer = str(answer)

    print("The answer is: " + answer)
    print(problem + " = " + solution + " (mod "+ str(power) +") = " + answer + " (mod " + str(modulus) + ")")


    return int(answer)
