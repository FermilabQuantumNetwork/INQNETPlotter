import csv

#############################
####CSV 2 column parser######
#############################
#useful for data in x,y
#format. will return a list
#with x and y values for your
#plot
#############################
def csv_parser( filename ):
    x = []
    y = []
    try:
        print("[INFO] Reading CSV file -->", filename)
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #next(csv_reader, None)
            line_count = 0
            keys = (0,0)
            for row in csv_reader:
                if line_count == 0:
                    keys = list (row)
                    print("[INFO] CSV keys in file: ", filename , " are --> ", keys)
                    #print (row[keys[0]],row[keys[1]])
                    x.append(float(row[keys[0]]))
                    y.append(float(row[keys[1]]))
                    line_count += 1
                else:
                    #print (row[keys[0]],row[keys[1]])
                    x.append(float(row[keys[0]]))
                    y.append(float(row[keys[1]]))
                    line_count += 1
            print("[INFO]",f'Processed {line_count} lines in -->', filename)
    except KeyboardInterrupt:
        print("Quit")
    return x,y
