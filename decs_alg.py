import csv, re
import itertools
AUTHOR_CSV = "Author.csv"
OUTPUT_CSV = "output_45.csv"
PAPERAUTHOR_CSV= "PaperAuthor.csv"
PAPER_CSV= "PaperAuthor.csv"

def getData():
    order_list = list()
    author_name = dict()
    set_author_name = dict()
    paper_author_dict = dict()
    co_author_dict = dict()
    papers_list = set()
    auth_paper_list = dict()
    with open(AUTHOR_CSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next()
        total_num = 0
        for row in reader:
            order_list.append(int(row[0]))
            co_author_dict[row[0]] = set()
            author_name[row[0]] = row[1].lower()
            set_author_name[row[0]] = set()
            spaces = row[1].split(" ");
            for space in spaces:
                set_author_name[row[0]].add(space.lower())
    csvfile.close()
    order_list.sort()
    with open(PAPERAUTHOR_CSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next()
        total_num = 0
        for row in reader:
            papers_list.add(str(row[1]))
            print "done with first pass"
            if not (row[1] in auth_paper_list):
                auth_paper_list[row[1]] = set()
            auth_paper_list[row[1]].add(row[0])
    csvfile.close()

    
  
#print co_author_dict['521630']
#order_list.sort()

    c_dict,nc_dict = get_stored_data()
    f = open(OUTPUT_CSV, 'w')
    f.write('AuthorId,DuplicateAuthorIds'+'\n')
    for row in order_list:
        if str(row) in nc_dict:
            f.write(str(row)+ ',')
            
            for nc in nc_dict[str(row)]:
                if str(row) == nc:
                    f.write(nc + ' ')
                elif str(row) in papers_list and nc in papers_list:
                    if match_funs_nc(set_author_name[str(row)],set_author_name[nc],author_name[str(row)],author_name[nc],auth_paper_list[str(row)],auth_paper_list[nc]):
                        f.write(nc + ' ')
             
        elif str(row) in c_dict:
            f.write(str(row)+ ',')
            
            for c in c_dict[str(row)]:
                if str(row) == c:
                    f.write(c + ' ')
                elif str(row) in papers_list and c in papers_list:
                    if match_funs_c(set_author_name[str(row)],set_author_name[c],author_name[str(row)],author_name[c],auth_paper_list[str(row)],auth_paper_list[c]):
                        f.write(c + ' ')
                
        else:
            f.write(str(row)+ ',' + str(row))
        f.write('\n')
            


    print "DONE WITH PREPROC"
def match_funs_nc(set1,set2,name1,name2,pap1,pap2):
    if (match_fun_2(set1,set2) or match_fun_1(set1,set2)) or (match_fun_4(name1,name2) and match_fun_3(set1,set2) or match_fun_5(pap1,pap2)):
        return True
    else:
        return False

def match_funs_c(set1,set2,name1,name2,pap1,pap2):
    if match_fun_1(set1,set2) or (match_fun_4(name1,name2) and match_fun_3(set1,set2) or match_fun_5(pap1,pap2)):
        return True
    else:
        return False

def match_fun_6(set1,set2):
    ret_boolean = False
    if len(set1) > 2 and len(set2) > 2:
        ret_boolean = set1.issubset(set2)
        if not ret_boolean:
            ret_boolean = set2.issubset(set1)

    return ret_boolean

def match_fun_7(pap1,pap2):
    if len(pap1.intersection(pap2)) > ((2*len(pap1))/3):
        return True
    else:
        return False

def match_fun_5(pap1,pap2):
    if len(pap1.intersection(pap2)) > int(2*float(len(pap1)+len(pap2))/float(3)):
        return True
    else:
        return False

def match_fun_4(name1,name2):
    spaces1= name1.split(" ")
    spaces2= name2.split(" ")
    if spaces1[-1] == spaces2[-1]:
        return True
    else:
        return False
#check if authors have same words in their names
def match_fun_1(set1,set2):
    dist = jdist(set1,set2)
    #print dist
    if dist > .95:
        return True

def match_fun_2(set1,set2):
    flag = 0
    temp1 = set1.difference(set2)
    temp2 = set2.difference(set1)
    if len(temp2) == 1 and len(temp1) == 1:
        elem1= temp1.pop()
        elem2 = temp2.pop()
        elem2 = elem2.replace('.','')
        elem1 = elem1.replace('.','')
        if elem1.startswith(elem2) or elem2.startswith(elem1):
            return True
    return False

def match_fun_3(set1,set2):
    ret_boolean = False
    ret_boolean = set1.issubset(set2)
    if not ret_boolean:
        ret_boolean = set2.issubset(set1)
    if ret_boolean:
        print set1
        print set2
    return ret_boolean

def get_stored_data():
    nc_dict = dict()
    nc33_f = open('out_nc4.csv','r')
    nc33_lines = nc33_f.readlines()
    counter = 0
    for l in nc33_lines:
        counter +=1
        #print counter
        comma = l.split(',')
        eval_str= l.replace(comma[0]+',','')
        nc_dict[comma[0]] = eval(eval_str)

    c_dict = dict()
    c33_f = open('out_c4.csv','r')
    c33_lines = c33_f.readlines()
    
    for l in c33_lines:
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
    
