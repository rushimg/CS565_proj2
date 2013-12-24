import csv, re
import itertools
AUTHOR_CSV = "Author.csv"
PAPER_AUTHOR_CSV = "PaperAuthor.csv"
OUTPUT_CSV = "output_chinese3.csv"

def getData():
    order_list = list()
    author_name = list()
    with open(AUTHOR_CSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next()
        total_num = 0
        for row in reader:
            order_list.append(int(row[0]))
    #author_name[row[0]] = row[1]
    csvfile.close()
    order_list.sort()

    c_dict,nc_dict = get_stored_data()
                #matching_functs(c_dict,nc_dict,author_name)
    set_output_dicts(c_dict,nc_dict,order_list)

    print "DONE WITH PREPROC"
                #f = open(OUTPUT_CSV, 'w')
                #f.write('AuthorId,DuplicateAuthorIds'+'\n')
  
    '''for row in order_list:
	#if counter < 1000:
        f.write(str(row)+',')
       	for row2 in order_list:
            	sim = jdist(test_vector_author_name[str(row)],test_vector_author_name[str(row2)])
         	if sim > .75:
               		f.write(str(row2)+' ')
	#else:
	#	f.write(str(row)+','+str(row))
            #print sim
	counter += 1
        print counter
        f.write('\n')
        f.flush()
    f.close()'''


def set_output_dicts(c_dict,nc_dict,order_list):
    print "setting output dicts"
    output_dict = dict()
    out = open('out_nc4.csv','w')
    for elem in order_list:
        output_dict[elem] = set()
    counter = 0
    for elem2 in order_list:
        counter +=1
        print counter
        for elem3 in nc_dict:
            #print elem3
            #print c_dict[elem3]
            #print str(elem2) + ' dkaskld'
            if str(elem2) in nc_dict[elem3]:
                output_dict[elem2] = output_dict[elem2].union(nc_dict[elem3])
        if len(output_dict[elem2]) > 0:
                out.write(str(elem2) + ',' + str(output_dict[elem2]))
                out.write('\n')
                     #for elem4 in nc_dict:
                     #if str(elem2) in nc_dict[elem4]:
                     #output_dict[elem2] = output_dict[elem2].union(nc_dict[elem4])
                     
                     #out.write(str(elem2) + ',' + str(output_dict[elem2]))
            #for elem6 in output_dict[elem2]:
#out.write(str(elem6) + ' ')

        
        out.flush()
            #else:
        #out.write(str(elem2) + ',' + str(elem2))
#   out.write('\n')
    out.close()
        #print output_dict




def get_stored_data():
    nc_dict = dict()
    nc33_f = open('nc33.txt')
    nc33_lines = nc33_f.readlines()
    counter = 0
    for l in nc33_lines:
        counter +=1
        print counter
        comma = l.split(',')
        eval_str= l.replace(comma[0]+',','')
        nc_dict[comma[0]] = eval(eval_str)
        print eval_str

    c_dict = dict()
    c33_f = open('c_33.txt')
    c33_lines = c33_f.readlines()
    counter = 0
    for l in c33_lines:
        counter +=1
        print counter
        comma = l.split(',')
        eval_str= l.replace(comma[0]+',','')
        c_dict[comma[0]] = eval(eval_str)
    return c_dict,nc_dict

def jdist(a,b):
    union = a.union(b)
    inter = a.intersection(b)
    len_union = float(len(union))
    len_inter = float(len(inter))
    jsim = len_inter/len_union
    jdist = 1-jsim
    return jsim

if __name__ == "__main__":
    getData();
    
