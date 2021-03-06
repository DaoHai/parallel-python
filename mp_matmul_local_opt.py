from multiprocessing import Pool
import numpy
from time import time


def calc_target(id):
    global a,b
    return numpy.dot(a,b)


def update_pool_global(dict):
    globals().update(dict)

def mat_rowrange_mul(a_row):
    global a,b
    print("a_row")
    print(a_row)

    return numpy.dot(a[a_row[0]:a_row[1],:],b) 


def mat_rowcol_mul(a_row):
    global a,b

    return numpy.dot(a[a_row,:],b) 






if __name__ == '__main__':


    x = 4096
    #y = 2048
    y = 256

    num_cpus = 4

    # Create a dictionary with objects to
    # send once to worker
    worker_globals = {}
    a = worker_globals['a'] = numpy.random.uniform(size=(x,y))
    b = worker_globals['b'] = numpy.random.uniform(size=(y,x))

    print("starting.")
    t1 = time()
    ans1 = numpy.dot(a,b)
    print("1 CPU:", time()-t1)
    
    p = Pool(num_cpus,update_pool_global,(worker_globals,))

    #import pdb; pdb.set_trace()

    #domains = ((0,999),(1000,1999),(2000,2999),(3000,3999))
    step = (x + .0) / (num_cpus + .0)


    domains = zip(numpy.arange(0,x,step).astype(int),numpy.arange(0,x,step).astype(int)+round(step))


    t1 = time()
    tmp = p.map(mat_rowrange_mul, domains)

    ans2 = numpy.empty((x,x))



    for i,domain in enumerate(domains):
        
        ans2[domain[0]:domain[1],:] = tmp[i]


    print(ans1)
    print(ans2)
    print("%d CPUs:" % num_cpus, time()-t1)

    

    # ans2 needs a bit of reformatting

    print("Same?:", numpy.alltrue(abs(ans1-ans2)<1e-11))
