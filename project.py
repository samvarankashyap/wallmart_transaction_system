import sys
import math
import pdb
def main_menu():
    #Main menu function for menu. 
    while True:
        print "====================================================\n"
        print "====================================================\n"
        print "Welcome to W Mart\n"
        print "Please choose an option from the followings.\n"
        print "<A>dd a new transaction of a customer to the database\n"
        print "<D>elete the last transaction from the database for a given customer\n"
        print "<Q>uit\n"
        input_text = raw_input("Please enter input in given options [A,D,Q]:\n")
        if (input_text in ['A','D','Q']):
            if input_text == 'A':
                print "Adding a new transction\n"
                add_new_transaction()
            elif input_text =='D':
                print "Deleting Last transaction\n"
                delete_last_transaction()
            elif input_text== 'Q':
                print "Quiting ..."  
                sys.exit(0) 
        else:
            print "Invalid input Please enter again\n"

def add_new_transaction():
    print "new transaction added\n"
    cust_id = raw_input("Enter customer id:\n")
    total_sale_amt = raw_input("Enter total Sale amount")
    discount_amount = calculate_discount(total_sale_amt)
    discount_sale_amt = total_sale_amt - discount_amount
    reward_points = calculate_reward_points(total_sale_amt)
    additional_discount = calculate_additional_discount(cust_id,reward_points)
    sale_after_add_disc = discount_sale_amt-additional_discount
    cu_sale_for_reward = next_reward_sale(cust_id)
    final_sale_amount = sale_after_add_disc
    write_to_transactions(cust_id,total_sale_amt,discount_amount,discount_sale_amt,reward_points,additional_discount, sale_after_add_disc,cu_sale_for_reward, final_sale_amount)
    

def delete_last_transaction(cust_id):
    print "delete last transaction\n"
    #pdb.set_trace()
    fd = open("sales.txt","r")
    lines = fd.readlines()
    fd.close()
    line_count =0
    counter =0
    lines_to_remove=[]
    for x in lines:
        s1 = x.split(":")
        line_count+=1
        if s1[0]=="Customer ID" and s1[1].strip("\n").strip()==str(cust_id):
            lines_to_remove.append(line_count)
            counter +=1
    pdb.set_trace()
    new_lines1 = lines[0:lines_to_remove[-1]-1]
    new_lines2 = lines[lines_to_remove[-1]-1:lines_to_remove[-1]+8]
    new_lines3 = lines[lines_to_remove[-1]+8:line_count]
    lines = []
    for x in new_lines1:
        lines.append(x)
    for x in new_lines3:
        lines.append(x)
    fd = open("sales.txt","w")
    fd.writelines(lines)
    fd.close()

def calculate_discount(total_sale_amt):
    print "calculating discount\n"
    #pdb.set_trace()
    discount =0 
    discount_details = get_discount_details()
    for x in discount_details:
        s1 = x.split(" ")
        if "Less" == s1[0]:
            if total_sale_amt < int(s1[2].strip("$")):
                discount = int(s1[4].strip("\n").strip("%"))
        if "From" == s1[0]:
            if total_sale_amt < int(s1[6].strip("$").replace(",","")) and total_sale_amt >= int(s1[1].strip("$").replace(",","")):
                if len(s1)== 9:
                    discount = total_sale_amt * int(s1[8].strip('\n').strip("%"))/100
                else:
                    discount = total_sale_amt * int(s1[10].strip('\n').strip("%"))/100
                    discount+= int(s1[8].strip("$"))
        if "above" in s1:
            if total_sale_amt >= int(s1[0].strip("$").replace(",","")):
                discount = total_sale_amt * int(s1[6].strip('\n').strip("%"))/100
                discount+= int(s1[4].strip("$"))
    print discount
    return discount

def calculate_reward_points(total_sale_amt):
    print "calculating reward points"
    reward = total_sale_amt/10
    reward = math.ceil(reward)
    print reward

def write_to_transactions(cust_id,total_sale_amt,discount_amount,discount_sale_amt,reward_points,additional_discount, sale_after_add_disc,cu_sale_for_reward, final_sale_amount):
    print "writing to file"

def get_discount_details():
    fd = open("discount.txt",'r')
    lines = fd.readlines()
    return lines

def calculate_additional_discount(cust_id,reward_points):
    r_points = 0 
    fd = open("sales.txt","r")
    lines = fd.readlines()
    i =0
    d_line =0
    while (i<len(lines)):
       s1= lines[i]
       s1 = s1.split(":")
       if s1[0]=="Customer ID" and s1[1].strip("\n").strip()==str(cust_id):
           pdb.set_trace()
           r_line = i+4
           s2 = lines[r_line]
           s2 = s2.split(":")
           r_point = s2[1].strip("\n")
           r_points += int(r_point)
       i+=1
    print r_points       
    return r_points

#calculate_reward_points(2340)
#get_discount_details()
#main_menu()
#delete_last_transaction(1)
calculate_additional_discount(3,233)
