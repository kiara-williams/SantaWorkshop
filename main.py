from array_queue import ArrayQueue
from operator import itemgetter


def assign(queue, days, assignments, cost, choice):
    instance = queue.first()
    try:
        if instance[-1] + days[instance[choice]] > 125:
            return assign(queue, days, assignments, cost, choice + 1)
        else:
            assigned = [instance[0], instance[choice]]
            assignments.append(assigned)
            cur_num = days[instance[choice]]
            new_num = cur_num + instance[-1]
            days[instance[choice]] = new_num
            print(days)
            print(assigned, instance[-1])
            queue.dequeue()
            if choice >= 0:
                cost += calculate_costs(choice, instance[-1])
    except:
        if instance[-1] + days[instance[choice]] >= 300:
            return assign(queue, days, assignments, cost, choice + 1)
        else:
            assigned = [instance[0], instance[choice]]
            assignments.append(assigned)
            cur_num = days[instance[choice]]
            new_num = cur_num + instance[-1]
            days[instance[choice]] = new_num
            print(days)
            print(assigned, instance[-1])
            queue.dequeue()
            if choice >= 0:
                cost += calculate_costs(choice, instance[-1])


def calculate_costs(c, p):
    if c == 1:
        return 50
    elif 1 < c <= 4:
        return (50 * (2 ^ (c-2))) + 9 * p
    else:
        return 0


def read_file(f, q):
    temp_list = []
    in_file = open(f, 'r')
    next(in_file)
    for line in in_file:
        new_line = [int(x) for x in line.strip().split(',')]
        temp_list.append(new_line)
    in_file.close()
    temp_list.sort(key=itemgetter(2))
    print(temp_list)
    for item in temp_list:
        q.enqueue(item)


def write_file(f, a):
    out_file = open(f, 'w')
    for item in a:
        line = "{}\n".format(item)
        out_file.write(line)
    out_file.close()


def main():
    queue = ArrayQueue()
    cost = 0
    assignments = []
    days = {k: 0 for k in range(1, 101)}
    read_file("family_data.csv", queue)
    while len(queue) > 0:
        assign(queue, days, assignments, cost, 1)
    print(days)
    write_file("submission_file.csv", assignments)


main()