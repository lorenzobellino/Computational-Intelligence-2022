import random
from queue import PriorityQueue
import logging

N = 500
SEED = 42

TRESHOLD = 1

logging.basicConfig(format="%(message)s", level=logging.INFO)


class PrioritizedSet:
    def __init__(self, priority: int, s: set):
        self.priority = priority
        self.item = s

    def __lt__(self, other):
        return self.priority < other.priority
    
    def __eq__(self, other):
        return self.priority == other.priority
    
    def __gt__(self, other):
        return self.priority > other.priority

    def __iter__(self):
        return iter((self.priority, self.item))
    
    
def problem(N, seed=None):
    random.seed(seed)
    sets = [set(set(random.randint(0,N-1) for n in range(random.randint(N // 5, N // 2)))) for n in range(random.randint(N,N*5))]
    goal = set(_ for _ in range(N))
    return sets,goal

def calculate_weight(r,g,s = set()):
    # logging.debug(f"tot : {len(goal-s1-s2)}")
    # logging.debug(f"s1 : {s1} s2: {s2} goal: {goal}")
    # return len(goal - s1 - s2)
    logging.debug(f"result: {r} goal: {g} s: {s}")
    
    # if any (x in g-r for x in s):
    #     return 100-int(100*sum(x not in g-r for x in s) / len(s))
    # else:
    #     return 100
    w = int(100*sum(x in g-r for x in s) / len(s))
    if(w>=TRESHOLD*100):
        return 0
    else:
        return 100-w



def goal_test(result,goal):
    return set().union(*result) == goal

def search(sets,goal):
    pq = PriorityQueue()
    for ps in sets:
        pq.put(PrioritizedSet(int(100/(N-len(ps))),ps))
    
    # devi riempire 10 elementi :
    # ordina per dimensione del set
    # prendi per primo il piu grande
    # poi controlla se la dimensione del prossimo set da prender
    # è maggiore del numero di valori ancora da coprire
    # non sceglierlo e passa

    # se devi coprire ancora 3 valori non ha
    # senso prendere un set che copre 5 valori

    # provare a mettere come score una percentuale di copertura
    # rispetto a quanti valoiri sono presenti nel set
    # res = {1,2,3}
    # s1 = {4,5} => 100%
    # s2 = {4,5,1} => 66%
    explored = 0
    result = [pq.get().item]
    result_set = set().union(result[0])
    logging.debug(f"result_set: {result_set}")
    unused = PriorityQueue()
    while result is not None and not goal_test(result,goal):
        # to_cover = calculate_weight(result_set,goal)
        to_cover = len(goal - result_set)
        logging.debug(f"tocover: {to_cover}")
        logging.debug(f"result: {result} \nresult_set: {result_set}\nto_cover: {to_cover}")
        logging.debug(f"{pq.qsize()} sets in queue")
        logging.debug(f"{pq.qsize()}")
        while not pq.empty():
            explored +=1 
            s = pq.get().item
            
            coverage = calculate_weight(result_set,goal,s)
            logging.debug(f"coverage: {coverage}")
            if coverage == 0:
                logging.debug(f"found coverage 100%: {s}")
                result.append(s)
                logging.debug(f"result_set: {result_set}\ns: {s}")
                result_set = result_set.union(s)
                logging.debug(f"result_set: {result_set}")
                while not unused.empty():
                    pq.put(unused.get())
                break
            elif coverage != 100:
                unused.put(PrioritizedSet(coverage,s))
            else:
                logging.debug(f"found coverage 0%: {s}")
        else:
            if unused.empty():
                result = None
                break
            else:
                local_best = unused.get().item
                result.append(local_best)
                result_set = result_set.union(local_best)
                logging.debug(f"{local_best} is the local best")
                logging.debug(f"{result_set} is the result_set")
                #pq = unused
                #unused = PriorityQueue()
                while not unused.empty():
                    pq.put(unused.get())


        #break
    logging.info(f"explored {explored}")
    return result
        

def main():
    sets,goal = problem(N,SEED)
    logging.debug(f"\nsets: {sets}\ngoal: {goal}")
    result = search(sets, goal)
    if result == None:
        logging.info("No solution found")
    else:
        # logging.info(f"the result is:\n{result}")
        logging.info(f"the weight of the solution is:\n{sum(len(s) for s in result)}")

if __name__ == "__main__":

    main()
    