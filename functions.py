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
