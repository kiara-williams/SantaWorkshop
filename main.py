from array_queue import ArrayQueue
from operator import itemgetter
from time import time

N = 5000


def single_pass(queue, days, assignments, choice):
    """Makes an final pass over the data and assigns all families their preferred choice where that choice does not
    exceed 300 people"""
    cost = 0
    instance = queue.dequeue()
    if instance == None:
        pass
    else:
        assigned = [instance[0], instance[choice]]
        assignments.append(assigned)
        days[instance[choice]] += instance[1]
        cost += calculate_costs(choice, instance[1])
    while queue.front() != 0:
        instance = queue.dequeue()
        if instance == None:
            pass
        elif instance[1] + days[instance[choice]] <= 300:
            assigned = [instance[0], instance[choice]]
            assignments.append(assigned)
            days[instance[choice]] += instance[1]
            cost += calculate_costs(choice, instance[1])
        else:
            queue.enqueue(instance)
    return cost


def first_pass(queue, days, assignments, choice):
    """Makes an initial pass over data and assigns all families to their first choice, where that choice has less than 125
    people assigned to it"""
    cost = 0
    instance = queue.dequeue()
    if instance[1] + days[instance[choice]] <= 126:
        assigned = [instance[0], instance[choice]]
        assignments.append(assigned)
        days[instance[choice]] += instance[1]
        cost += calculate_costs(choice, instance[1])
    else:
        queue.enqueue(instance)
    while queue.front() != 0:
        instance = queue.dequeue()
        if instance[1] + days[instance[choice]] <= 126:
            assigned = [instance[0], instance[choice]]
            assignments.append(assigned)
            days[instance[choice]] += instance[1]
            cost += calculate_costs(choice, instance[1])
        else:
            queue.enqueue(instance)
    return cost


def calculate_costs(c, p):
    """Calculates additional costs if first choice not assigned"""
    choice = c-2
    if choice == 0:
        return 0
    elif choice == 1:
        return 50
    elif 2 <= choice < 5:
        return (50 * (2 ^ (choice-2))) + 9 * p
    elif 5 <= choice < 7:
        return (100 * (c - 3)) + 18 * p
    elif 7 <= choice < 9:
        return (100 * (c - 4)) + 36 * p
    else:
        return 500 + (36 * p) + ((choice - 8) * 199)


def read_file(f, q):
    """Reads data csv, reorders data for processing, and queues data"""
    in_file = open(f, 'r')
    next(in_file)
    for line in in_file:
        new_line = [int(x) for x in line.strip().split(',')]
        family_number = new_line.pop()
        new_line.insert(1, family_number)
        q.enqueue(new_line)
    in_file.close()


def write_file(f, a):
    """Writes day assignments to submission file"""
    out_file = open(f, 'w')
    a.sort(key=itemgetter(0))
    out_file.write("family_id,assigned_day\n")
    for item in a:
        line = "{},{}\n".format(item[0], item[1])
        out_file.write(line)
    out_file.close()


def calc_accounting_penalty(days, start, previous):
    """Applies accounting penalty to day count"""
    if start == 0:
        return 0
    else:
        penalty = (days[start]-125.0) / 400.0 * days[previous]**(0.5)
        return penalty + calc_accounting_penalty(days, start - 1, previous - 1)


def sort_list(queue, i):
    """Sorts list according to choice in ascending order"""
    temp_list = []
    while queue.is_empty == False:
        instance = queue.dequeue()
        temp_list.append(instance)
    temp_list.sort(key=itemgetter(i))
    for item in temp_list:
        queue.enqueue(item)


def main():
    """Pulls data from file, assigns days and writes to submission file"""
    queue = ArrayQueue()
    cost = 0
    assignments = []
    days = {k: 0 for k in range(1, 101)}
    read_file("family_data.csv", queue)
    for i in range(2, 12):
        sort_list(queue, i)
        cost += first_pass(queue, days, assignments, i)
    while queue.first() != None:
        for i in range(2, 12):
            sort_list(queue, i)
            cost += single_pass(queue, days, assignments, i)
    cost += (days[100]-125.0) / 400.0 * days[100]**(0.5)
    cost += calc_accounting_penalty(days, 99, 100)
    write_file("submission_file.csv", assignments)
    print('${:.2f}'.format(cost))


main()