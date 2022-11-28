import random
import math
import numpy as np

#hűtés
def annealing(temp, old_time, new_time):
        return math.exp((old_time - new_time) / temp)

#kiszámolja meddig tart a sorrend alapján a meló, visszaküldi a sorrendet és az időt
def makespan(order, tasks, machines_val):
    times = []
    for i in range(0, machines_val):
        times.append(0)
    for j in order:
        times[0] += tasks[j][0]
        for k in range(1, machines_val):
            if times[k] < times[k-1]:
                times[k] = times[k-1]
            times[k] += tasks[j][k]
    return max(times), order

#új munka sorrend
def get_new_seq_2(sequence):
    i1, i2 = random.sample(sequence, 2)
    new_seq = sequence[:]
    new_seq[i1], new_seq[i2] = new_seq[i2], new_seq[i1]
    return new_seq

#iterálás a munka sorrendeken
def sim_anneal(sequence, jobs,num_of_jobs, num_of_machines, time, temperature, iter):
    prev_sequence = sequence
    best_sequence = sequence
    prev_time = time
    iteration = iter
    #lower_temp = 0.99
    best_time = prev_time
    iteration_counter = 1

    #Napló adatok kitörlése és új napló kezdése
    file = open("makespan_log.txt", "w")
    file.write("New makespan:\n")
    file.close
    

    while(iteration > 0):
        # x -> x'
        new_sequence = get_new_seq_2(prev_sequence)
        # c(x')
        new_time, new_sequence = makespan(new_sequence, jobs, num_of_machines) 
        
        #logolás
        file = open("makespan_log.txt", "a")
        log = "*** Time:"+str(new_time)+"***\t\t*** Sequence:"+ str(new_sequence)+ "***\t\t***"+"Iteration:"+ str(iteration_counter)+ " ***\n"
        file.write(log)

        if new_time < best_time:
            # x = x'
            best_time = new_time
            best_sequence = new_sequence
            prev_sequence = new_sequence
            iteration -= 1
            iteration_counter += 1
            #temperature *= lower_temp
        else:
            if annealing(temperature, prev_time, new_time) > random.random():
                # x = x' p eséllyel
                prev_sequence = new_sequence 
            iteration -= 1
            iteration_counter += 1
            #temperature *= lower_temp
        
    file.close()   
    return best_time, best_sequence

#Részfeladat számítás gantt ábra rajzoláshoz:
def get_detailed_subtask(timetable,t0, d, i_masina, i_feladat):
    #részfeladat szótar
    #reszfeladat = {'kezdes_ideje' : t0, 'munka_hossza': d, 'gep_azonsitoja': "M"+str(i_masina), 'feladat_azonositoja':i_feladat} 
    subtask = {'t0' : t0, 'd': d, 'masina_index': i_masina, 'munka_index':i_feladat}
    timetable.append(subtask)

#Részletes munkaterv gantt ábrához:
def get_detailed_schedule(task_times, masinak_szama, feladatok_szama, sequence):
    timetable = []

    #részfeladat idők
    subtask_done_time = [0]*len(masinak_szama)

    #A sorrend minden egyes feladathoz:
    for i_task in sequence:
        #a feladat minden részfeladatához:
        for i_machine, d_subtask in enumerate(task_times[i_task]):
            prev_machine_done_time = subtask_done_time[i_machine-1]
            current_machine_done_time = subtask_done_time[i_machine]

            #t0 beállítás:
            if(i_machine > 0) & (prev_machine_done_time > current_machine_done_time):
                t0 = prev_machine_done_time
            else:
                t0 = current_machine_done_time

            #részfeladat adatok hozzáadása a munkatervhez:
            get_detailed_subtask(timetable, t0, d_subtask, i_machine, i_task)

            #végzési idő = kezdeti időpont + a munka ideje
            subtask_done_time[i_machine] = t0 + d_subtask

    return timetable



if __name__ == "__main__":

    #Kiindulási adatok
    num_of_jobs = 10
    num_of_machines = 10
    np.random.seed(333)
    jobs = np.random.randint(1, 10, size=(num_of_jobs, num_of_machines))    #numpy generálja a munkák mátrixot
    sequence = list(range(0, num_of_jobs))                                  #a kezdeti munkasorrend
    temp = 1                                                                #hűtéshez
    iterations = 1000                                                       #kilépési feltételhez

    #Gantt ábrához:
    #Erőforrás nevek
    machine_names = []
    for i in range(num_of_machines):
        machine_names.append("M"+str(i))  
    #Munka nevek
    job_names = []
    for i in range(num_of_jobs):
        job_names.append("J"+str(i))

    #kezdeti értékek az iterációhoz
    c, nsequence = makespan(sequence, jobs, num_of_machines)
    old_c = c

    #iterálás
    print("Program started!\nCalculating...")
    c, nsequence = sim_anneal(sequence, jobs, num_of_jobs, num_of_machines, c, temp, iterations)
    print("Done!\nClose diagram to exit program.")

    #kiszámított legjobb időhöz tartozó sorrend részletesen
    best_sequence_schedule = get_detailed_schedule(jobs, machine_names, num_of_jobs, nsequence)
   
    #best sequence külön fájlba
    with open('best_sequence_log.txt', 'w') as f:
        f.write("Best sequence step-by-step:\n")
        for line in best_sequence_schedule:
            f.write(f"{line}\n")
    
    #Összegzés egy másik fájlba
    with open('report.txt', 'w') as f:
        f.write("Array of Jobs:\n")
        for line in jobs:
            f.write(f"{line}\n")
        f.write(f"Initial time: {old_c}\n")
        f.write(f"Initial sequence: {sequence}\n")
        f.write(f"Best time found: {c}\n")
        f.write(f"Best sequence found: {nsequence}\n")
    
    from gantt import gantt_megrajzol
    gantt_megrajzol(best_sequence_schedule, machine_names, job_names)