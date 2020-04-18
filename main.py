from array_queue import ArrayQueue
from operator import itemgetter


def initial_pass(queue, days, assignments):
    instance = queue.dequeue()
    first_choice = instance[2]
    assigned = [instance[0], first_choice]
    assignments.append(assigned)
    days[first_choice] += instance[1]
    while queue.front() != 0:
        instance = queue.dequeue()
        first_choice = instance[2]
        if instance[1] + days[first_choice] < 150:
            print(instance[0], instance[1], days[instance[2]])
            assigned = [instance[0], first_choice]
            assignments.append(assigned)
            days[first_choice] += instance[1]
        else:
            queue.enqueue(instance)


def assign(queue, days, assignments, cost, choice=2):
    # there's issues with this. Fix.
    instance = queue.first()
    if instance[1] + days[instance[choice]] >= 300:
        # print(instance[0], choice, instance[choice], days[instance[choice]])
        return assign(queue, days, assignments, cost, choice + 1)
    else:
        assigned = [instance[0], instance[choice]]
        assignments.append(assigned)
        days[instance[choice]] += instance[1]
        if choice >= 0:
            cost += calculate_costs(choice, instance[1])
        queue.dequeue()


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
        family_number = new_line.pop()
        new_line.insert(1, family_number)
        temp_list.append(new_line)
    in_file.close()
    temp_list.sort(key=itemgetter(1), reverse=True)
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
    initial_pass(queue, days, assignments)
    while queue.is_empty() == False:
        assign(queue, days, assignments, cost, 2)
    print(days)
    write_file("submission_file.csv", assignments)


main()