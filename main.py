from array_queue import ArrayQueue
from operator import itemgetter


def assign(queue, days, assignments, cost, choice=0):
    instance = queue.first()
    if instance[-1] + days(instance[choice]) > 300:
        return assign(queue, days, assignments, cost, choice + 1)
    else:
        assignments.append(set(instance[0], instance[choice]))
        queue.dequeue()
        if choice >= 0:
            cost += calculate_costs(choice, instance[-1])


def calculate_costs(c, p):
    if c == 1:
        return 50
    elif 1 < c <= 4:
        return (50 * (2 ^ (c-2))) + 9 * p
    # continue from here


def read_file(f, q):
    temp_list = []
    in_file = open(f, 'r')
    next(in_file)
    for line in in_file:
        line.strip()
        new_line = list(line.split(','))
        temp_list.append(new_line)
    sorted(temp_list, key=itemgetter(-1))
    for item in temp_list:
        q.enqueue(item)


def main():
    queue = ArrayQueue()
    cost = 0
    assignments = []
    days = {k: 0 for k in range(1, 101)}
    read_file("family_data.csv", queue)
    while len(queue) > 0:
        assign(queue, days, assignments, cost)