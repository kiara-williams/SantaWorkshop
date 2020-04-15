from array_queue import ArrayQueue


def assign(queue, days, assignments, cost, choice=0):
    instance = queue.first()
    if instance[-1] + days(instance[choice]) > 300:
        return assign(queue, days, assignments, cost, choice + 1)
    else:
        assignments.append(instance[0], instance[choice])
        queue.dequeue()
        if choice >= 0:
            cost += calculate_costs(choice, instance[-1])


def calculate_costs(c, p):
    if c == 1:
        return 50
    elif 1 < c <= 4:
        return (50 * (2 ^ (c-2))) + 9 * p
    # continue from here


def main():
    queue = ArrayQueue()
    cost = 0
    assignments = list()
    days = {k: 0 for k in range(1, 101)}
    while len(queue) > 0:
        assign(queue, days, assignments, cost)