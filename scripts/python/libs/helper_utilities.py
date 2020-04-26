import argparse
import csv

###############################
########command line parser####
###############################
command_line_parser = argparse.ArgumentParser(description='obtain command line input')
#parser.add_argument('--input_file_name', dest='input_file_name', action='store_true', help="provide input file: --input_file_name <path_to_file>")
command_line_parser.add_argument('--input_file_name',  dest='input_file_name',  help="provide input file: --input_file_name <path_to_file>")
command_line_parser.add_argument('--output_file_name', dest='output_file_name', help="provide input file: --output_file_name <path_to_file>")
command_line_parser.add_argument('--teleportation_type', dest='teleportation_type', help="provide teleportation type: --teleportation_type <early,late,plus>")
command_line_parser.add_argument('--spools', dest='spools', help="provide spools or no-spool option: --spools <True,False>")

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


#############################################
####CSV 2 column parser with given keys######
#############################################
#useful for data in x,y
#format. will return a list
#with x and y values for your
#plot
#############################
def csv_parser_keys_xy( filename, key_x, key_y ):
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
                ###################################################################
                #row is Dictionary [(key_1_i,value_1_i), ...,(key_n_i,value_n_i)]
                #in each instance of the loop you get the keys
                #to access the value_x_i do row[key_x]
                ###################################################################
                if line_count == 0:
                    keys = list (row)
                    print("[INFO] CSV keys in file: ", filename , " are --> ", keys)
                    #print (row)
                    #print (row[keys[0]],row[keys[1]])
                    #get key_x
                    if key_x in row:
                        #print('key %s has values %f'%(key_x,float(row[key_x])))
                        x.append(float(row[key_x]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_x)
                        exit()

                    #get key_y
                    if key_y in row:
                        #print('key %s has values %f'%(key_y,float(row[key_y])))
                        y.append(float(row[key_y]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_y)
                        exit()

                    line_count += 1
                else:
                    #get key_x
                    if key_x in row:
                        #print('key %s has values %f'%(key_x,float(row[key_x])))
                        x.append(float(row[key_x]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_x)
                        exit()

                    #get key_y
                    if key_y in row:
                        #print('key %s has values %f'%(key_y,float(row[key_y])))
                        y.append(float(row[key_y]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_y)
                        exit()
                    line_count += 1

            print("[INFO]",f'Processed {line_count} lines in -->', filename)
    except KeyboardInterrupt:
        print("Quit")

    return x,y

#####################################################
#########CSV 3 column parser with given keys#########
#####################################################
#useful for data in x,y,y_unc
#format. will return a list
#with x,y,z values for your
#plot
#############################
def csv_parser_keys_xyz( filename, key_x, key_y, key_z ):
    x = []
    y = []
    z = []#z-could be y uncertainty for example
    try:
        print("[INFO] Reading CSV file -->", filename)
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #next(csv_reader, None)
            line_count = 0
            keys = (0,0)
            for row in csv_reader:
                ###################################################################
                #row is Dictionary [(key_1_i,value_1_i), ...,(key_n_i,value_n_i)]
                #in each instance of the loop you get the keys
                #to access the value_x_i do row[key_x]
                ###################################################################
                if line_count == 0:
                    keys = list (row)
                    print("[INFO] CSV keys in file: ", filename , " are --> ", keys)
                    #print (row)
                    #print (row[keys[0]],row[keys[1]])
                    #get key_x
                    if key_x in row:
                        #print('key %s has values %f'%(key_x,float(row[key_x])))
                        x.append(float(row[key_x]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_x)
                        exit()

                    #get key_y
                    if key_y in row:
                        #print('key %s has values %f'%(key_y,float(row[key_y])))
                        y.append(float(row[key_y]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_y)
                        exit()

                    #get key_z
                    if key_z in row:
                        #print('key %s has values %f'%(key_y,float(row[key_y])))
                        z.append(float(row[key_z]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_y)
                        exit()

                    line_count += 1
                else:
                    #get key_x
                    if key_x in row:
                        #print('key %s has values %f'%(key_x,float(row[key_x])))
                        x.append(float(row[key_x]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_x)
                        exit()

                    #get key_y
                    if key_y in row:
                        #print('key %s has values %f'%(key_y,float(row[key_y])))
                        y.append(float(row[key_y]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_y)
                        exit()

                    #get key_y_unc
                    if key_z in row:
                        #print('key %s has values %f'%(key_y,float(row[key_y])))
                        z.append(float(row[key_z]))
                    else:
                        print ('[ERROR] Did not find key %s in CSV file', key_y)
                        exit()

                    line_count += 1

            print("[INFO]",f'Processed {line_count} lines in -->', filename)
    except KeyboardInterrupt:
        print("Quit")

    return x,y,z
