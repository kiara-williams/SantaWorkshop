from array_queue import ArrayQueue
from operator import itemgetter


def initial_pass(queue, days, assignments):
    """Makes an initial pass over data and assigns all families to their first choice where possible.
    Minimises the work of the recursion function"""
    instance = queue.dequeue()
    first_choice = instance[2]
    assigned = [instance[0], first_choice]
    assignments.append(assigned)
    days[first_choice] += instance[1]
    while queue.front() != 0:
        instance = queue.dequeue()
        first_choice = instance[2]
        if instance[1] + days[first_choice] < 125:
            assigned = [instance[0], first_choice]
            assignments.append(assigned)
            days[first_choice] += instance[1]
        else:
            queue.enqueue(instance)


def assign(queue, days, assignments, limit, choice=2):
    """Assigns families to days whilst observing set limits to number of people allowed"""
    cost = 0
    instance = queue.first()
    if instance[1] + days[instance[choice]] > limit:
        return assign(queue, days, assignments, limit, choice + 1)
    else:
        assigned = [instance[0], instance[choice]]
        assignments.append(assigned)
        days[instance[choice]] += instance[1]
        if choice >= 0:
            cost += calculate_costs(choice, instance[1])
        queue.dequeue()
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
    for item in temp_list:
        q.enqueue(item)


def write_file(f, a):
    """Writes day assignments to submission file"""
    out_file = open(f, 'w')
    a.sort(key=itemgetter(0))
    out_file.write("family_id,assigned_day\n")
    for item in a:
        line = "{},{}\n".format(item[0], item[1])
        out_file.write(line)
    out_file.close()


def main():
    """Pulls data from file, assigns days and writes to submission file"""
    queue = ArrayQueue()
    cost = 0
    assignments = []
    days = {k: 0 for k in range(1, 101)}
    read_file("family_data.csv", queue)
    initial_pass(queue, days, assignments)
    while queue.is_empty() == False:
        try:
            cost += assign(queue, days, assignments, 126)
        except:
            cost += assign(queue, days, assignments, 300)
    write_file("submission_file.csv", assignments)


main()