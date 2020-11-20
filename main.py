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
                #print("before :", tempbudged, chromosome)
                chromosome[index] += tempbudged
                allmax.append(ROI[index])
                tempbudged = 0
            else:
                #print("before :",tempbudged, chromosome,investment_lower_upper[index][1]-chromosome[index])
                temp = investment_lower_upper[index][1] - chromosome[index]
                chromosome[index] += temp
                tempbudged -= temp
                allmax.append(ROI[index])
            #print("after :",tempbudged, chromosome)
            # print(allmax)

            if len(allmax) == marketing_channels_num and tempbudged != 0:
                print("can not use all budget population :")
                print(tempbudged)
                break
        return chromosome

def fix_over_allocated_budget(chromosome,marketing_channels_num,tempbudged,ROI,investment_lower_upper):
    allmin = []
    # print(chromosome)
    while (tempbudged != 0):
        min = 1000000000
        index = 0
        for k in range(marketing_channels_num):
            if (ROI[k] < min) and (ROI[k] not in allmin):
                index = k
                min = ROI[k]
        # print(tempbudged+chromosome[index],investment_lower_upper[index][1])
        if investment_lower_upper[index][0] <= chromosome[index]+tempbudged:
            #print("before1 :", tempbudged, chromosome)
            chromosome[index] += tempbudged
            allmin.append(ROI[index])
            tempbudged = 0
        else:
            #print("before2 :", tempbudged, chromosome, investment_lower_upper[index][1] - chromosome[index])
            temp = chromosome[index]-investment_lower_upper[index][0]
            chromosome[index] -= temp
            tempbudged += temp
            allmin.append(ROI[index])
        #print("after :", tempbudged, chromosome)
        # print(allmax)

        if len(allmin) == marketing_channels_num and tempbudged != 0:
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
            r =random.uniform(investment_lower_upper[j][0], investment_lower_upper[j][1])
            chromosome.append(r)
        #print(chromosome)
        sumofchromosome=sum(chromosome)
        if sumofchromosome>budget:
            #print("over budget")
            chromosome=fix_over_allocated_budget(chromosome,marketing_channels_num,budget-sumofchromosome,ROI,investment_lower_upper)
        elif sumofchromosome<budget:
            #print("reuses budget")
            chromosome=reuse_the_nonallocated_budget(chromosome,marketing_channels_num,budget-sumofchromosome,ROI,investment_lower_upper)
        #print(chromosome)
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

def mutation_non_uniform(crossover,investment_lower_upper ,max_num_generation , current_generation): #peter
    t = current_generation
    T = max_num_generation
    b = 1.5  #dependency factor
    for i in range(0,len(crossover)):
        delta_lower = 0
        delta_upper = 0
        y = 0
        for j in range(0,len(crossover[i])):
            delta_lower = crossover[i][j] - investment_lower_upper[j][0]
            delta_upper = investment_lower_upper[j][1] - crossover[i][j]
            r1 = random.uniform(0, 1)
            if r1 <= 0.5:
                y = delta_lower
            elif r1 > 0.5:
                y = delta_upper
            R = random.uniform(0, 1)
            crossover[i][j] = y * (1 - pow(R, pow(1-t/T ,b)))
    return crossover

def replacement(population, mutation,ROI): #mina
    # success_prop [.3,.3,.5,.2,.2]
    new_gen = []
    mProp = []
    for x in range(0, len(mutation)):
        mSum = 0
        for y in range(0, len(mutation[x])):
            mSum += mutation[x][y] * (ROI[y]/100)
        mProp.append(mSum)
    for i in range(0, len(population)):
        pSum = 0
        for j in range(0, len(population[i])):
            pSum += population[i][j] * (ROI[j]/100)
        flag = False
        for j in range(0, len(mProp)):
            if mProp[j] > pSum and mutation[j] not in new_gen:
                new_gen.append(mutation[j])
                flag = True
                break
        if flag == False:
            new_gen.append(population[i])
    return new_gen

def select_the_fittest(population,ROI):  #peter
    fittest_index = 0
    for i in range(0,len(population)):
        tempSum =0
        geneSum =0
        for j in range(0,len(population[i])):
            tempSum += population[i][j] * (ROI[j]/100)
        if tempSum > geneSum:
            fittest_index = i
    return population[fittest_index]

def genetic_algo(budget, marketing_channels_num, marketing_channels, ROI, investment_lower_upper): #mina
    pass

def MBAP_input(): #mustafa
    pass

def MBAP(): #mustafa
    pass

def final_result(): #mustafa
   pass
