import sys
import math
import pdb
def main_menu():
    #Main menu function for menu. 
    while True:
        print("====================================================\n")
        print("====================================================\n")
        print("Welcome to W Mart\n")
        print("Please choose an option from the followings.\n")
        print("<A>dd a new transaction of a customer to the database\n")
        print("<D>elete the last transaction from the database for a given customer\n")
        print("<Q>uit\n")
        input_text = raw_input("Please enter input in given options [A,D,Q]:\n")
        if (input_text in ['A','D','Q']):
            if input_text == 'A':
                print("Adding a new transaction\n")
                add_new_transaction()
            elif input_text =='D':
                print("Deleting Last transaction\n")
                c_id = raw_input("Enter customer id:\n")
                delete_last_transaction(c_id)
            elif input_text== 'Q':
                print("Quiting ...")
                sys.exit(0) 
        else:
            print "Invalid input Please enter again\n"

def add_new_transaction():
    # adding new transaction
    attr_dict = {}
    attr_dict["cust_id"]= raw_input("Enter customer id:\n")
    attr_dict["total_sale_amt"]=  raw_input("Enter total Sale amount:\n")
    attr_dict["discount_amount"]= calculate_discount(attr_dict["total_sale_amt"])
    attr_dict["discount_sale_amt"]= int(attr_dict["total_sale_amt"]) - int(attr_dict["discount_amount"])
    #pdb.set_trace()
    attr_dict["reward_points"]=  calculate_reward_points(attr_dict["total_sale_amt"])
    attr_dict["additional_discount"]= calculate_additional_discount(attr_dict["cust_id"],attr_dict["reward_points"])
    attr_dict["sale_after_add_disc"]=  int(attr_dict["discount_sale_amt"])-int(attr_dict["additional_discount"])
    attr_dict["cu_sale_for_reward"]=  next_reward_sale(attr_dict["cust_id"])
    attr_dict["final_sale_amount"] =  attr_dict["sale_after_add_disc"]
    write_to_transactions(attr_dict)
    

def delete_last_transaction(cust_id):
    # Delete the last trasaction
    print("delete last transaction\n")
    cust_id = int(cust_id)
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
    print("calculating discount\n")
    discount =0 
    total_sale_amt = int(total_sale_amt)
    discount_details = get_discount_details()
    for x in discount_details:
        s1 = x.split(" ")
        if "Less" == s1[0]:
            if total_sale_amt < int(s1[2].strip("$")):
                discount = int(s1[4].strip("\n").strip("%"))
        if "From" == s1[0]:
            if total_sale_amt < int(s1[6].strip("$").replace(",","")) and total_sale_amt >= int(s1[1].strip("$").replace(",","")):
                if len(s1)== 9:
                    discount = (total_sale_amt-int(s1[1].strip('\n').strip("$")))*int(s1[8].strip('\n').strip("%"))/100
                else:
                    discount = (total_sale_amt-int(s1[1].strip('\n').strip("$"))) * int(s1[10].strip('\n').strip("%"))/100
                    discount+= int(s1[8].strip("$"))
        if "above" in s1:
            if total_sale_amt >= int(s1[0].strip("$").replace(",","")):
                discount = (total_sale_amt-int(s1[0].strip('\n').strip("$"))) * int(s1[6].strip('\n').strip("%"))/100
                discount+= int(s1[4].strip("$"))
    print discount
    return discount

def calculate_reward_points(total_sale_amt):
    print("calculating reward points")
    total_sale_amt = int(total_sale_amt)
    reward = total_sale_amt/100
    reward = math.floor(reward)
    return reward

def write_to_transactions(attr_dict):
    fd = open("sales.txt","a")
    p_str = ""
    p_str += "Customer ID: "+str(attr_dict["cust_id"])+"\n"
    p_str += "Total sale amount: "+str(attr_dict["total_sale_amt"])+"\n"
    p_str += "Discount amount: "+str(attr_dict["discount_amount"])+"\n"
    p_str += "Discount sale amount: "+str(attr_dict["discount_sale_amt"])+"\n"
    p_str += "Reward point: "+str(attr_dict["reward_points"])+"\n"
    p_str += "Additional discount: "+str(attr_dict["additional_discount"])+"\n"
    p_str += "Additional discounted sale amount: "+str(attr_dict["sale_after_add_disc"])+"\n"
    p_str += "Cumulative sale amount for the next reward point: "+str(attr_dict["cu_sale_for_reward"])+"\n"
    p_str += "Final sale amount: "+str(attr_dict["final_sale_amount"])+"\n"
    print p_str
    fd.write(p_str)
    fd.close()
    

def get_discount_details():
    fd = open("discount.txt",'r')
    lines = fd.readlines()
    return lines

def calculate_additional_discount(cust_id,reward_points):
    r_points = 0 
    add_discount = 0
    cust_id = int(cust_id)
    reward_points = int(reward_points)
    fd = open("sales.txt","r")
    lines = fd.readlines()
    i =0
    d_line =0
    while (i<len(lines)):
       s1= lines[i]
       s1 = s1.split(":")
       if s1[0]=="Customer ID" and s1[1].strip("\n").strip()==str(cust_id):
           r_line = i+4
           s2 = lines[r_line]
           s2 = s2.split(":")
           r_point = s2[1].strip("\n").strip()
           r_points += int(float(r_point))
       i+=1
    print(r_points)
    if (r_points+reward_points)/100 > 0 :
        add_discount = math.floor(r_points+reward_points/100)*10  
    print(add_discount)   
    return add_discount

def next_reward_sale(cust_id):
    return 10

main_menu()
