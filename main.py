from array_queue import ArrayQueue


def assign(queue, days, assignments, cost, choice=0):
    instance = queue.first()
    if instance == "Empty":
        return False
    elif instance[-1] + days(instance[choice]) > 300:
        return assign(queue, days, assignments, cost, choice + 1)
    else:
        assignments.append(instance[0], instance[choice])
        queue.dequeue()
        if choice >= 0:
            cost += calculate_costs(choice, instance[-1])
        return assign(queue, days, assignments, cost)


