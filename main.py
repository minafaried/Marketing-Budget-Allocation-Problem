import random

population_num = 5
iteration_num = 3
selectionNumber = 2
crossover_probability = .7
kConstant = 2
def checkIfDuplicates(listOfElems):
    res = []
    sum = 0
    for elem in listOfElems:
        if elem not in res:
            res.append(elem)
            sum += 1

    return sum,res

def all_equal(iterable):

    res = []
    sum = 0
    for elem in iterable:
        if elem not in res:
            res.append(elem)
            sum += 1

    if sum==1:
        return True
    else:
        return False


def reuse_the_nonallocated_budget(chromosome, marketing_channels_num, tempbudged, ROI, investment_lower_upper):
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
            # print("before :", tempbudged, chromosome)
            chromosome[index] += tempbudged
            allmax.append(ROI[index])
            tempbudged = 0
        else:
            # print("before :",tempbudged, chromosome,investment_lower_upper[index][1]-chromosome[index])
            temp = investment_lower_upper[index][1] - chromosome[index]
            chromosome[index] += temp
            tempbudged -= temp
            allmax.append(ROI[index])
        # print("after :",tempbudged, chromosome)
        # print(allmax)

        if len(allmax) == marketing_channels_num and tempbudged != 0:
            print("can not use all budget population :")
            print(tempbudged)
            break
    return chromosome


def fix_over_allocated_budget(chromosome, marketing_channels_num, tempbudged, ROI, investment_lower_upper):
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
        if investment_lower_upper[index][0] <= chromosome[index] + tempbudged:
            # print("before1 :", tempbudged, chromosome)
            chromosome[index] += tempbudged
            allmin.append(ROI[index])
            tempbudged = 0
        else:
            # print("before2 :", tempbudged, chromosome, investment_lower_upper[index][1] - chromosome[index])
            temp = chromosome[index] - investment_lower_upper[index][0]
            chromosome[index] -= temp
            tempbudged += temp
            allmin.append(ROI[index])
        # print("after :", tempbudged, chromosome)
        # print(allmax)

        if len(allmin) == marketing_channels_num and tempbudged != 0:
            print("can not use all budget population :")
            print(tempbudged)
            break
    return chromosome


def init(population_num, marketing_channels_num, budget, ROI, investment_lower_upper):  # mina
    population = []
    for i in range(0, population_num):
        chromosome = []
        tempbudged = budget
        for j in range(0, marketing_channels_num):
            r = random.uniform(investment_lower_upper[j][0], investment_lower_upper[j][1])
            chromosome.append(r)
        # print(chromosome)
        sumofchromosome = sum(chromosome)
        if sumofchromosome > budget:
            # print("over budget")
            chromosome = fix_over_allocated_budget(chromosome, marketing_channels_num, budget - sumofchromosome, ROI,
                                                   investment_lower_upper)
        elif sumofchromosome < budget:
            # print("reuses budget")
            chromosome = reuse_the_nonallocated_budget(chromosome, marketing_channels_num, budget - sumofchromosome,
                                                       ROI, investment_lower_upper)
        # print(chromosome)
        population.append(chromosome)
    return population


def check(population, marketing_channels_num, ROI, budget, investment_lower_upper):
    for i in range(0, len(population)):  # loop for all population
        chromosomeValue = 0
        for j in range(0, len(population[i])):  # loop for all boundries in each chromosome
            if (population[i][j] > investment_lower_upper[j][1]):  # if cell is greater than upper
                population[i][j] = investment_lower_upper[j][1]  # cell = upper
                chromosomeValue += population[i][j]  # calculate chromsome's buget
            elif (population[i][j] < investment_lower_upper[j][0]):  # if cell is smaller than lower
                population[i][j] = investment_lower_upper[j][0]  # cell = lower
                chromosomeValue += population[i][j]
            else:  # if cell is smaller than upper and greater than lower
                chromosomeValue += population[i][j]  # calculate chromsome's buget
        if chromosomeValue == budget:  # budget full used
            continue
        elif chromosomeValue < budget:  # still there are budgets
            population[i] = reuse_the_nonallocated_budget(population[i], marketing_channels_num,
                                                          budget - chromosomeValue, ROI, investment_lower_upper)
        else:  # if chromosome has buget more than mine
            population[i] = fix_over_allocated_budget(population[i], marketing_channels_num, budget - chromosomeValue,
                                                      ROI, investment_lower_upper)
    return population


def fitness_and_selection(population, kConstant, ROI, selectionNumber):  # mustafa
    if (all_equal(population) == True):
        return [population[0], population[1]]
    if selectionNumber % 2 != 0:
        print("Selection Number Must be EVEN")
        return None
    fitness = []
    commulative = []
    take_K_Number = []
    selection = []
    for i in range(0, len(population)):
        fitnessProcess = 0
        for j in range(0, len(population[i])):
            fitnessProcess += ROI[j] * population[i][j]
        fitness.append(fitnessProcess)
    # print("Fintess: ",fitness)
    while (len(selection) != selectionNumber):
        #print(0)
        if len(selection) > selectionNumber:
            print("Error")
            return None
        take_K_Number = []
        while (len(take_K_Number) < kConstant):
            #print("takeNumLength: ", len(take_K_Number))
            #print("takeNumber: ", take_K_Number)
            if (len(take_K_Number) > kConstant):
                print("ERROR")
                return None
            randNum = random.randrange(0, len(fitness))
            #print("Population: ", population)
            #print("Fintess: ", fitness)
            #print("RandNum: ", randNum)
            #print("fitness chosen: ", fitness[randNum])
            if fitness[randNum] in take_K_Number:
                continue
            else:
                take_K_Number.append(fitness[randNum])
        #print("Take K Number:", take_K_Number)
        highest = take_K_Number[0]
        for take in range(1, len(take_K_Number)):
            if take_K_Number[take] > highest:
                highest = take_K_Number[take]
        #print("Highest", highest)
        for pop in range(0, len(fitness)):
            if highest == fitness[pop] and population[pop] not in selection:
                selection.append(population[pop])
            else:
                continue
    return selection


def crossover(selection, marketing_channels_num):  # mina
    if len(selection)<=1:
        return selection
    r1 = random.randrange(0, marketing_channels_num - 1)
    r2 = random.randrange(0, marketing_channels_num - 1)
    while (r2 == r1):
        r2 = random.randrange(0, marketing_channels_num - 1)
    if r1 > r2:
        r1, r2 = r2, r1
    #print(r1, r2)
    crossover = []
    for i in range(0, len(selection), 2):
        newchromosom1 = []
        newchromosom2 = []
        for j in range(0, r1 + 1):
            newchromosom1.append(selection[i][j])
            newchromosom2.append(selection[i + 1][j])
        for j in range(r1 + 1, r2 + 1):
            newchromosom1.append(selection[i + 1][j])
            newchromosom2.append(selection[i][j])
        for j in range(r2 + 1, marketing_channels_num):
            newchromosom1.append(selection[i][j])
            newchromosom2.append(selection[i + 1][j])
        crossover.append(newchromosom1)
        crossover.append(newchromosom2)
    return crossover


def mutation_uniform(crossover, investment_lower_upper):  # peter
    for i in range(0, len(crossover)):
        delta_lower = 0
        delta_upper = 0
        delta = 0
        for j in range(0, len(crossover[i])):
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


def mutation_non_uniform(crossover, investment_lower_upper, max_num_generation, current_generation):  # peter
    t = current_generation
    T = max_num_generation
    b = 1.5  # dependency factor
    for i in range(0, len(crossover)):
        delta_lower = 0
        delta_upper = 0
        y = 0
        for j in range(0, len(crossover[i])):
            delta_lower = crossover[i][j] - investment_lower_upper[j][0]
            delta_upper = investment_lower_upper[j][1] - crossover[i][j]
            r1 = random.uniform(0, 1)
            if r1 <= 0.5:
                y = delta_lower
            elif r1 > 0.5:
                y = delta_upper
            R = random.uniform(0, 1)
            crossover[i][j] = y * (1 - pow(R, pow(1 - t / T, b)))
    return crossover


def replacement(population, mutation, ROI):  # mina
    # success_prop [.3,.3,.5,.2,.2]
    new_gen = []
    mProp = []
    for x in range(0, len(mutation)):
        mSum = 0
        for y in range(0, len(mutation[x])):
            mSum += mutation[x][y] * (ROI[y] / 100)
        mProp.append(mSum)
    for i in range(0, len(population)):
        pSum = 0
        for j in range(0, len(population[i])):
            pSum += population[i][j] * (ROI[j] / 100)
        flag = False
        for j in range(0, len(mProp)):
            if mProp[j] > pSum and mutation[j] not in new_gen:
                new_gen.append(mutation[j])
                flag = True
                break
        if flag == False:
            new_gen.append(population[i])
    return new_gen


def select_the_fittest(population, ROI):  # peter
    fittest_index = 0
    for i in range(0, len(population)):
        tempSum = 0
        geneSum = 0
        for j in range(0, len(population[i])):
            tempSum += population[i][j] * (ROI[j] / 100)
        if tempSum > geneSum:
            fittest_index = i
    return population[fittest_index]


def genetic_algo(budget, marketing_channels_num, marketing_channels, ROI, investment_lower_upper):  # mina
    population = init(population_num, marketing_channels_num, budget, ROI, investment_lower_upper)
    for i in range(0, iteration_num):
        #print(population)
        selection_out = fitness_and_selection(population, marketing_channels_num, ROI, selectionNumber)
        crossover_out = crossover(selection_out, marketing_channels_num)
        mutation_out = mutation_uniform(crossover_out, investment_lower_upper)
        population = replacement(population, mutation_out, ROI)
    res= select_the_fittest(population,ROI)
    #print(res)
    return res

def MBAP_input():
    channelsName = []
    ROI = []
    lower_upper = []
    budget = int(input("Enter the marketing budget (in thousands): "))
    channelNumbers = int(input("Enter the number of marketing channels: "))
    for i in range(0, int(channelNumbers)):
        tempLoUp = []
        channelName = str(input("Enter channel Name: "))
        channelROI = int(input("Enter channel ROI: "))
        channelsName.append(channelName)
        ROI.append(channelROI)
        channelLower = str(input("Enter channel Lower Bound: "))
        channelUpper = str(input("Enter channel Upper Bound: "))
        if (channelLower == 'x'):
            channelLower = 0
            tempLoUp.append(channelLower)
        else:
            tempLoUp.append(int(channelLower))
        if channelUpper == 'x':
            channelUpper = 100
            calcChannelUpper = (budget * channelUpper) / 100
            tempLoUp.append(calcChannelUpper)
        else:
            calcChannelUpper = (int(budget) * int(channelUpper)) / 100
            tempLoUp.append(calcChannelUpper)

        if channelLower > channelUpper:
            print("Lower boundry can't be greater than Upper Bound plz try again")
            exit(0)
        lower_upper.append(tempLoUp)
    return budget, channelNumbers, channelsName, ROI, lower_upper


def MBAP():
    #budget, channelNumbers, channelsName, ROI, lower_upper= MBAP_input()
    budget, channelNumbers, channelsName, ROI, lower_upper=100,4,["tv","G","T","F"],[8,12,7,11],[[2.7,58],[20.5,100],[0,18],[10,100]]
    f = open("finalResult.txt", "w")
    f.close()
    f = open("finalResult.txt", "a")
    for i in range(0, 20):
        res=genetic_algo(budget, channelNumbers, channelsName, ROI, lower_upper)
        stringres="iteration number "+str(i+1)+"\n"
        for j in range(0,len(res)):
            stringres+=channelsName[j]+" --> " + str(round(res[j],2))+"K\n"
        f.write(stringres)
    f.close()


MBAP()
