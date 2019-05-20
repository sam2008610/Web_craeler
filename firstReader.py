import threading
import time
import random


def writer(name,  re_wr_lock):
    global start_time
    global write_counter
    global data
    global time_ex
    while 1 == 1:
        re_wr_lock.acquire()
        print(name, "enter critical section.")
        data += random.randint(1, 5)
        write_counter += 1
        print(name, "write data to ", data, ".")
        sleep_time = random.randint(1, 3)
        print(name, "sleep for ", sleep_time, " seconds.")
        time.sleep(sleep_time)
        print(name, "....Wake up! Exit critical section.")
        re_wr_lock.release()
        if time.time()-start_time > time_ex:
            break
        time.sleep(sleep_time)


def reader(name, mutex, re_wr_lock):
    global start_time
    global read_counter
    global data
    global time_ex
    global readernum
    while 1 == 1:
        if mutex._value == readernum:
            re_wr_lock.acquire()
        mutex.acquire()
        re_wr_lock.locked()
        print(name, "enter critical section.")
        read_counter += 1
        print(name, "read data ", data, ".")
        sleep_time = random.randint(1, 3)
        print(name, "sleep for ", sleep_time, " seconds.")
        time.sleep(sleep_time)
        print(name, "....Wake up! Exit critical section.")

        mutex.release()
        if mutex._value == readernum and re_wr_lock.locked():
            re_wr_lock.release()
        if time.time()-start_time > time_ex:
            break
        time.sleep(sleep_time)


data = 5
print("How many reader ?")
readernum = int(input())
print("How many writer ?")
writernum = int(input())
print("First reader-writer problem start!!")
print("Intnitial Data :", data)
print("===============================================")
now_time = 0
start_time = time.time()
time_ex = 120
write_counter = 0
read_counter = 0
rethread = []
wrthread = []
mutex = threading.Semaphore(readernum)
re_wr_lock = threading.Lock()

for i in range(writernum):
    wrthread.append(threading.Thread(
        target=writer, args=("Writer["+str(i+1)+"]",  re_wr_lock)))
    wrthread[i].start()
for i in range(readernum):
    rethread.append(threading.Thread(
        target=reader, args=("    [Reader"+str(i+1)+"]", mutex, re_wr_lock)))
    rethread[i].start()
for i in range(writernum):
    wrthread[i].join()
for i in range(readernum):
    rethread[i].join()

print("===============================================")
print("First reader-writer problem stop!!")
print("Total writer count", write_counter)
print("Total reader count", read_counter)
