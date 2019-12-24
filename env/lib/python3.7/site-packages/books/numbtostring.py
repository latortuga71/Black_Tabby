#!/usr/bin/python

class NumbToString:
    def __init__(self):
        self.TENS = [None, None, "twenty", "thirty", "forty",
               "fifty", "sixty", "seventy", "eighty", "ninety"]
        self.SMALL = ["zero", "one", "two", "three", "four", "five",
                "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen"]
        self.HUGE = [None, None] + [h + "illion" for h in ("m", "b", "tr", "quadr", "quint", "sext","sept", "oct", "non", "dec")]

    def __nonzero(self,c, n, connect=''):
        return "" if n == 0 else connect + c + self.spell_integer(n)

    def __last_and(self,num):
        if ',' in num:
            pre, last = num.rsplit(',', 1)
            if ' and ' not in last:
                last = ' and' + last
            num = ''.join([pre, ',', last])
        return num

    def __big(self,e, n):
        if e == 0:
            return self.spell_integer(n)
        elif e == 1:
            return self.spell_integer(n) + " thousand"
        else:
            return self.spell_integer(n) + " " + self.HUGE[e]

    def __base1000_rev(self,n):
        # generates the value of the digits of n in base 1000
        # (i.e. 3-digit chunks), in reverse.
        while n != 0:
            n, r = divmod(n, 1000)
            yield r

    def spell_integer(self,n):
        if n < 0:
            return "minus " + self.spell_integer(-n)
        elif n < 20:
            return self.SMALL[n]
        elif n < 100:
            a, b = divmod(n, 10)
            return self.TENS[a] + self.__nonzero("-", b)
        elif n < 1000:
            a, b = divmod(n, 100)
            return self.SMALL[a] + " hundred" + self.__nonzero(" ", b, ' and')
        else:
            num = ", ".join([self.__big(e, x) for e, x in
                            enumerate(self.__base1000_rev(n)) if x][::-1])
            return self.__last_and(num)
    def main(self,n):
        self.spell_integer(n)
