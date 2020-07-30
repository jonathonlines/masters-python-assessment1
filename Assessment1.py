
#Part A

from os import listdir

#creates a list of all the files in results folder (note the results folder must be unzipped and in same directory as py file)
filelst = listdir("results")

#empty list for IP addresses (to use later to avoid duplicates)
IPaddresses = []

#New string with column headings as first row. Will use at end of Part A to add rows for each participants' results
resultsForCsv = "Condition,Name,Age,Gender,Hit_Proportion,NearMiss_Proportion,FullMiss_Proportion,Happiness_Hit_Mean,Happiness_NearMiss_Mean,Happiness_FullMiss_Mean,WantsMore_Hit_Mean,WantsMore_NearMiss_Mean,WantsMore_FullMiss_Mean,Happiness_Min,Happiness_Max\n"

#Count of all files - to use below to define the number of loops and in Part B
fileCount = len(filelst)

# ------ start of loop for each file in results -------

for i in range(0, fileCount):

    #open and reads each file in results (results must be in same directory as this .py file). removes "\n" and replaces with a comma, then creates a list of everything in file
    file_open = open("results/"+filelst[i], "r")
    contents = file_open.read()
    file_all = contents.replace("\n", ",")
    file_all = file_all.split(",")

    #slices ip address from list. Checks if IP address is not already in list, to prevent duplicates
    IPaddress_slice = file_all[2]
    if IPaddress_slice not in IPaddresses:

        #adds IP address to IP address list
        IPaddresses.append(IPaddress_slice)

        # ------ this section slices the participants' details from the file (condition, name, age etc.)-------

        # slices condition from list
        attribute_condition = file_all[0]

        # slices gender from list, converts it all to lower case and then into 1 for male and 2 for female
        attribute_gender = file_all[5].lower()
        if attribute_gender == "male":
            attribute_gender = "1"
        else:
            attribute_gender = "2"

        # slices participant's name and age from list and then joins into a string, separated by comma
        attribute_nameAge = ",".join(file_all[3:5])

        # adds all info about the participant into a string, and deletes the large space in condition
        attributes = attribute_condition + "," + attribute_nameAge + "," + attribute_gender
        attributes = attributes.replace("  ", "")

        # creates a list of the column headings from original file, to use in next section
        dataHeadings = file_all[6:file_all.index("trial")]

        # ------  this section moves onto calculating the relevant proportions, averages etc. we want from the rows of trial results -----
        
        # slices data of all trials, starting from first instance of trial
        trials_slice = file_all[file_all.index("trial"):]

        #loops through all trial data, slices data for each separate trail and then adds to list 'trials'
        trials = []
        trial_index = 0

        for data in trials_slice:
            if data == "trial":
                trial_data = trials_slice[trial_index:trial_index+9]
                trials.append(trial_data)
                trial_index += len(trial_data)

        #empty counters for count of hits,nearMiss and fullMiss outcomes, plus the total number of trials
        hitCount = 0
        nearMissCount = 0
        fullMissCount = 0
        trialsCount = len(trials)

        #empty lists for happiness scores across each outcome
        happiness_hit = []
        happiness_nearMiss = []
        happiness_fullMiss = []

        # empty lists for willingness to continue (i.e. WantsMore) scores across each outcome
        wantsMore_hit = []
        wantsMore_nearMiss = []
        wantsMore_fullMiss = []

        # loop for each row (i.e. every trial for participant)
        for row in trials:

            #adds to counters for each outcome
            if "hit" in row:
                hitCount += 1
            if "nearMiss" in row:
                nearMissCount += 1
            if "fullMiss" in row:
                fullMissCount += 1

            #the index in list for result (i.e. outcome)
            result_index = dataHeadings.index("Result")

            #for each outcome, looks up happiness score, converts to int and adds to list
            happiness_index = dataHeadings.index("Happinness")
            happiness_index_data = int(row[happiness_index])

            if row[result_index] == "hit":
                happiness_hit.append(happiness_index_data)
            elif row[result_index] == "nearMiss":
                happiness_nearMiss.append(happiness_index_data)
            else:
                happiness_fullMiss.append(happiness_index_data)

            # for each outcome, looks up wantsMore score, converts to int and adds to list
            wantsMore_index = dataHeadings.index("WantsMore")
            wantsMore_index_data = int(row[wantsMore_index])

            if row[result_index] == "hit":
                wantsMore_hit.append(wantsMore_index_data)
            elif row[result_index] == "nearMiss":
                wantsMore_nearMiss.append(wantsMore_index_data)
            else:
                wantsMore_fullMiss.append(wantsMore_index_data)

        # now the loop of each trial has finished, calculates the proportions for each outcome
        hit_proportion = hitCount / trialsCount
        nearMiss_proportion = nearMissCount / trialsCount
        fullMiss_proportion = fullMissCount / trialsCount

        #converts proportions into a string separated by commas
        outcome_proportions = str(hit_proportion) + "," + str(nearMiss_proportion) + "," + str(fullMiss_proportion)

        #calculates mean happiness score for each outcome, and converts into a new string separated by commas
        happiness_hit_Mean = sum(happiness_hit) / hitCount
        happiness_nearMiss_Mean = sum(happiness_nearMiss) / nearMissCount
        happiness_fullMiss_Mean = sum(happiness_fullMiss) / fullMissCount

        happiness_Means = str(happiness_hit_Mean) + "," + str(happiness_nearMiss_Mean) + "," + str(happiness_fullMiss_Mean)

        # calculates mean wantsMore score for each outcome, and converts into a new string separated by commas
        wantsMore_hit_Mean = sum(wantsMore_hit) / hitCount
        wantsMore_nearMiss_Mean = sum(wantsMore_nearMiss) / nearMissCount
        wantsMore_fullMiss_Mean = sum(wantsMore_fullMiss) / fullMissCount

        wantsMore_Means = str(wantsMore_hit_Mean) + "," + str(wantsMore_nearMiss_Mean) + "," + str(wantsMore_fullMiss_Mean)

        # adds happiness scores, calculates min and max and converts into a new string separated by commas
        happinessData = happiness_hit + happiness_nearMiss + happiness_fullMiss
        happiness_min = min(happinessData)
        happiness_max = max(happinessData)
        happiness_MinMax = str(happiness_min) + "," + str(happiness_max)

        #adds all the participants' attributes and results into one string
        participantRow = attributes + "," + outcome_proportions + "," + happiness_Means + "," + wantsMore_Means + "," + happiness_MinMax

        # adds participant data to a string, plus a line space so each participant is in a new row, ready to import into csv
        resultsForCsv += participantRow + "\n"

# ------ end of loop for each file in results -------

#opens new csv file and writes all results to it
resultsCsv = open("results.csv" , "w")

resultsCsv.write(resultsForCsv)
resultsCsv.close()

#END of Part A

#-----------------------------------------------------

#Part B

#empty counters for number of participants in experiments A and B
expA_count = 0
expB_count = 0

#new list for all dates
date_lst = []

#loops each filename, adds to counter if expA or expB in first slice. slices date from file name and adds to date_lst
for file in filelst:
    if file[0:4] == "expA":
        expA_count += 1
    else:
        expB_count += 1

    date_lst.append(file[-18:-10])

#text for summary file with total participants, and participants in expA and expB. This only uses info from the file names, so does not remove any duplicate IP addresses.
summary = "There were " + str(fileCount)+ " participants in total. \n"
summary += "There were " + str(expA_count)+ " participants in Experiment A (Lincoln). \n"
summary += "There were " + str(expB_count) + " participants in Experiment B (UCL). \n"

#new dictionary for participants per date
date_dict = {}

#loop for dates in date list, and adds count of dates as values to each key in dictionary
for date in date_lst:
    date_dict[date] = date_lst.count(date)

summary += "The number of participants per date was as follows: \n"

#loop through sorted dates in dictionary, and adds text to summary for each date and number of participants
for date in sorted(date_dict):
    summary += str(date) + ": " + str(date_dict[date]) + "\n"

#opens new txt file and writes summary text to file
results_summary = open("results_summary.txt" , "w")

results_summary.write(summary)
results_summary.close()

#END of Part B
