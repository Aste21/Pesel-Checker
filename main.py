import time

start = time.time()

PESEL_LENGTH = 11
PESEL_WEIGHT = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
# a list where index is the month number, and the value is the number of days in the month
MONTH_LENGTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

# function checking if the year is a leap year


def leap_year_check(y, m):
    century = m - m % 20
    if y == 0 and century == 20:
        return True
    elif y == 0:
        return False
    elif y % 4 == 0:
        return True
    else:
        return False


file = open("1e6.dat", 'r')

# counters
total = correct = male = female = 0
invalid_length = invalid_digit = invalid_date = invalid_checksum = invalid = 0

for pesel in file:
    is_true = True
    table = 11 * [0]
    pesel = pesel.strip()
    total += 1
    # checking the pesel length
    if len(pesel) != PESEL_LENGTH:
        invalid += 1
        invalid_length += 1
        continue
    # checking if pesel is made only from digits
    for x in range(11):
        if not pesel[x].isdigit():
            invalid_digit += 1
            invalid += 1
            is_true = False
            break
        else:
            table[x] = int(pesel[x])
    if not is_true:
        continue
    # checking the date
    YY = 10 * table[0] + table[1]
    MM = 10 * table[2] + table[3]
    DD = 10 * table[4] + table[5]
    M = MM % 20
    is_leap = leap_year_check(YY, MM)
    if DD == 0:
        invalid_date += 1
        continue
    elif is_leap and M == 2:
        if DD > 29:
            invalid_date += 1
            continue
    elif M > 12 or M < 1:
        invalid_date += 1
        continue
    elif DD > MONTH_LENGTH[M - 1]:
        invalid_date += 1
        continue
    # calculating and checking the checksum
    c = 0
    for x in range(10):
        c += table[x] * PESEL_WEIGHT[x]
    c = (10 - (c % 10)) % 10
    if c != table[10]:
        invalid_checksum += 1
        continue
    # counting correct pesel numbers and counting number of females and males
    correct += 1
    if table[9] % 2 == 0:
        female += 1
    else:
        male += 1

file.close()

# show results
print("TOTAL CORRECT FEMALE MALE")
print(total, correct, female, male)
print("INVALID-LENGTH INVALID-DIGIT INVALID_DATE INVALID-CHECKSUM")
print(invalid_length, invalid_digit, invalid_date, invalid_checksum)

print("Runtime [s]= ", time.time() - start)
