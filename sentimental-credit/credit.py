import cs50
import re

number = cs50.get_int('Number: ')
match = re.match(r'^\d{13,16}$', str(number))

if match:
    # Get number of digits
    start = str(match).find('(0, ') + 4
    end = str(match).find(')')
    digits = int(str(match)[start: end])
else:
    print('INVALID')
    exit()


def main():
    num = str(number)
    if (luhn(number, digits) and digits == 15 and (num[0:2] == '34' or num[0:2] == '37')):
        # AMEX
        print('AMEX')
    elif (luhn(number, digits) and (digits == 13 or digits == 16) and num[0] == '4'):
        # VISA 13 and 16
        print('VISA')
    elif (luhn(number, digits) and digits == 16 and int(num[0:2]) in range(51, 56)):
        # MASTERCARD
        print('MASTERCARD')
    else:
        # INVALID
        print('INVALID')


def luhn(number, Length):
    # Checks Luhn's algorithm to number
    List = list(str(number))
    a = []
    b = []

    # Sum of second to last * 2 evens
    for i in range(Length - 2, -1, -2):
        x = str(2 * int(List.pop(i)))
        x = list(x)
        for j in range(len(x)):
            a.append(int(x[j]))
    sum_a = sum(a)

    # Sum of odds
    for i in range(len(List)):
        b.append(int(List[i]))
    sum_b = sum(b)

    if ((sum_a + sum_b) % 10 == 0):
        return True
    return False


if __name__ == "__main__":
    main()

