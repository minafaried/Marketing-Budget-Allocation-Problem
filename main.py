import random


def reuse_the_nonallocated_budget(chromosome,marketing_channels_num,tempbudged,ROI,investment_lower_upper):
        allmax = []
        # print(chromosome)
        while (tempbudged != 0):
            max = -1
            index = 0
            for k in range(marketing_channels_num):
                if (ROI[k] > max) and (ROI[k] not in allmax):
                    index = k
                    max = ROI[k]
            # print(tempbudged+chromosome[index],investment_lower_upper[index][1])
            if investment_lower_upper[index][1] >= tempbudged + chromosome[index]:
                print("before :", tempbudged, chromosome, tempbudged)
                chromosome[index] += tempbudged
                allmax.append(ROI[index])
                tempbudged = 0
            else:
                print("before :",tempbudged, chromosome,investment_lower_upper[index][1]-chromosome[index])
                temp = investment_lower_upper[index][1] - chromosome[index]
                chromosome[index] += temp
                tempbudged -= temp
                allmax.append(ROI[index])
            print("after :",tempbudged, chromosome)
            # print(allmax)

            if len(allmax) == marketing_channels_num and tempbudged != 0:
                print("can not use all budget population :")
                print(tempbudged)
                break
        return chromosome


def init(population_num, marketing_channels_num,budget,ROI,investment_lower_upper):  #mina
    population = []
    for i in range(0, population_num):
        chromosome = []
        tempbudged=budget
        for j in range(0, marketing_channels_num):
            r = random.uniform(investment_lower_upper[j][0], investment_lower_upper[j][1])
            if tempbudged-r>=0:
                tempbudged-=r
                chromosome.append(r)
            elif tempbudged<r and tempbudged !=0:
                chromosome.append(tempbudged)
                tempbudged=0
            else:
                chromosome.append(0)
        chromosome=reuse_the_nonallocated_budget(chromosome,marketing_channels_num,tempbudged,ROI,investment_lower_upper)
        population.append(chromosome)
    return population


def check(population, marketing_channels_num,budget,investment_lower_upper): #mustafa
    pass


def fitness_and_selection(population, marketing_channels_num, ROI, selectionNumber): #mustafa
    pass


def crossover(selection,marketing_channels_num): #mina

    r1=random.randrange(0,marketing_channels_num-1)
    r2=random.randrange(0,marketing_channels_num-1)
    while(r2==r1):
        r2=random.randrange(0,marketing_channels_num-1)
    if r1>r2:
        r1, r2 = r2, r1
    print(r1, r2)
    crossover=[]
    for i in range (0,len(selection),2):
        newchromosom1=[]
        newchromosom2=[]
        for j in range(0,r1+1):
            newchromosom1.append(selection[i][j])
            newchromosom2.append(selection[i+1][j])
        for j in range(r1+1,r2+1):
            newchromosom1.append(selection[i+1][j])
            newchromosom2.append(selection[i][j])
        for j in range(r2+1,marketing_channels_num):
            newchromosom1.append(selection[i][j])
            newchromosom2.append(selection[i+1][j])
        crossover.append(newchromosom1)
        crossover.append(newchromosom2)
    return crossover


def mutation_uniform(crossover,investment_lower_upper): #peter
    for i in range(0,len(crossover)):
        delta_lower = 0
        delta_upper = 0
        delta = 0
        for j in range(0,len(crossover[i])):
            delta_lower = crossover[i][j] - investment_lower_upper[j][0]
            delta_upper = investment_lower_upper[j][1] - crossover[i][j]
            r1 = random.uniform(0, 1)
            if r1 <= 0.5:
                delta = delta_lower
            elif r1 > 0.5:
                delta = delta_upper
            r2 = random.uniform(0, delta)
            if delta == delta_lower:
                crossover[i][j] = crossover[i][j] - r2
            elif delta == delta_upper:
                crossover[i][j] = crossover[i][j] + r2
    return crossover

def mutation_non_uniform(bit_filp, crossover,marketing_channels_num, investment_lower_upper): #peter
    pass

def replacement(population, mutation,marketing_channels_num,investment_lower_upper,budget): #mina
    pass


def select_the_fittest(population,marketing_channels_num,investment_lower_upper,budget):  #peter
    pass


def genetic_algo(budget, marketing_channels_num, marketing_channels, ROI, investment_lower_upper): #mina
    pass

def MBAP_input(): #mustafa
    pass

def MBAP(): #mustafa
    pass

def final_result(): #mustafa
   pass
