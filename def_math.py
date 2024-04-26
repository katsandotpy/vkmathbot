import random
import math

class create:
    def plus(mass):
        a = random.randint(mass["plus"][0][0], mass["plus"][0][1])
        b = random.randint(mass["plus"][1][0], mass["plus"][1][1])
        primer_txt = str(a) + "+" + str(b)
        primer_answer = a + b
        return primer_txt, primer_answer

    def multi(mass):
        a = random.randint(mass["multi"][0][0], mass["multi"][0][1])
        b = random.randint(mass["multi"][1][0], mass["multi"][1][1])
        primer_txt = str(a) + "*" + str(b)
        primer_answer = a * b
        return primer_txt, primer_answer

    def minus(mass):
        a = random.randint(mass["minus"][0][0], mass["minus"][0][1])
        b = random.randint(mass["minus"][1][0], mass["minus"][1][1])
        primer_txt = str(a) + "-" + str(b)
        primer_answer = a - b
        return primer_txt, primer_answer

    def div(mass):
        a = random.randint(mass["div"][0][0], mass["div"][0][1])
        b = random.randint(mass["div"][1][0], mass["div"][1][1])
        primer_answer = b
        c = a * b
        primer_txt = str(c) + ":" + str(a)
        return primer_txt, primer_answer

    def sq(mass):
        primer_answer = random.randint(mass["sq"][0][0], mass["sq"][0][1])
        primer_txt = "√" + str(primer_answer ** 2)
        return primer_txt, primer_answer

    def equation(mass):
        x1 = random.randint(-5, 5)
        x2 = random.randint(-5, 5)
        a = random.randint(1, 5)
        b = -a * (x1 + x2)
        c = x1 * x2 * a
        if b > 0:
            btxt = "+"
        else:
            btxt = "-"
        if c > 0:
            ctxt = "+"
        else:
            ctxt = "-"
        equat = str(a) + ("x²") + btxt + str(int(math.fabs(b))) + str("x") + ctxt + str(
            int(math.fabs(c))) + "=0"

        choose_num6 = random.randint(1, 2)
        if choose_num6 == 1:
            primer_answer = max(x1, x2)
            primer_txt = "Найдите наибольший корень квадратного уравнения: \n" + equat
        else:
            primer_answer = min(x1, x2)
            primer_txt = "Найдите наименьший корень квадратного уравнения: \n" + equat
        return primer_txt, primer_answer

    def degree(mass):
        list_stepen = ["\u00b2", "\u00b3", "\u2074", "\u2075", "\u2076", "\u2077"]
        a = random.randint(mass["degree"][0][0], mass["degree"][0][1])
        b = random.randint(mass["degree"][1][0], mass["degree"][1][1])
        primer_txt = str(a) + str(list_stepen[b - 2])
        primer_answer = a ** b
        return primer_txt, primer_answer







