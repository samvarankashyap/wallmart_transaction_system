import sys
import math
import pdb
def main():
    #Main menu function for menu.
    forever = True 
    while forever:
        print "Welcome to W Mart\n"
        print "Please choose an option from the followings.\n"
        print "<A>dd a new transaction of a customer to the database\n"
        print "<D>elete the last transaction from the database for a given customer\n"
        print "<Q>uit\n"
        option = raw_input("Select input in options A, D, Q :\n")
        if option.upper() == 'A':
            start_transaction()
        elif option.upper() =='D':
            customer_id = raw_input("Enter customer id:\n")
            delete_transaction(customer_id)
        elif option.upper() == 'Q':
            sys.exit(0) 
        else:
            print "Wrong option Enter again\n"

def start_transaction():
    # start a new transaction
    attr_dict = {}
    attr_dict["c_id"] = raw_input("Enter customer id:\n")
    attr_dict["total_sale"] = raw_input("Enter total Sale amount:\n")
    attr_dict["discount_amount"] = get_discount(attr_dict["total_sale"])
    attr_dict["discount_sale_amt"] = int(attr_dict["total_sale"]) - int(attr_dict["discount_amount"])
    attr_dict["reward_points"] = get_reward_points(attr_dict["total_sale"])
    attr_dict["additional_discount"] = get_add_discount(attr_dict["c_id"],attr_dict["reward_points"])
    attr_dict["sale_after_add_disc"] = int(attr_dict["discount_sale_amt"])-int(attr_dict["additional_discount"])
    attr_dict["cu_sale_for_reward"] = 10
    attr_dict["final_sale_amount"] = attr_dict["sale_after_add_disc"]
    sales_file = open("sales.txt","a")
    output = ""
    output += "Customer ID: "+str(attr_dict["c_id"])+"\n"
    output += "Total sale amount: "+str(attr_dict["total_sale"])+"\n"
    output += "Discount amount: "+str(attr_dict["discount_amount"])+"\n"
    output += "Discount sale amount: "+str(attr_dict["discount_sale_amt"])+"\n"
    output += "Reward point: "+str(attr_dict["reward_points"])+"\n"
    output += "Additional discount: "+str(attr_dict["additional_discount"])+"\n"
    output += "Additional discounted sale amount: "+str(attr_dict["sale_after_add_disc"])+"\n"
    output += "Cumulative sale amount for the next reward point: "+str(attr_dict["cu_sale_for_reward"])+"\n"
    output += "Final sale amount: "+str(attr_dict["final_sale_amount"])+"\n"
    print output
    sales_file.write(output)
    sales_file.close()
    

def delete_transaction(cust_id):
    # Delete the last trasaction
    cust_id = int(cust_id)
    sales_file = open("sales.txt","r")
    lines = sales_file.readlines()
    sales_file.close()
    line_count =0
    counter =0
    lines_to_remove=[]
    for x in lines:
        s1 = x.split(":")
        line_count+=1
        if s1[0]=="Customer ID" and s1[1].strip("\n").strip()==str(cust_id):
            lines_to_remove.append(line_count)
            counter +=1
    lines1 = lines[0:lines_to_remove[-1]-1]
    lines2 = lines[lines_to_remove[-1]+8:line_count]
    lines = []
    for x in lines1:
        lines.append(x)
    for x in lines2:
        lines.append(x)
    sales_file = open("sales.txt","w")
    sales_file.writelines(lines)
    sales_file.close()

def get_discount(total_sale_amt):
    discount =0 
    total_sale_amt = int(total_sale_amt)
    discount_file = open("discount.txt",'r')
    discounts = discount_file.readlines()
    discount_file.close()
    for d in discounts:
        s1 = d.split(" ")
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
    return discount

def get_reward_points(total_sale):
    points = int(total_sale)/100
    return points

def get_add_discount(cust_id,reward_points):
    r_points = 0 
    add_discount = 0
    cust_id = int(cust_id)
    reward_points = int(reward_points)
    sales_file = open("sales.txt","r")
    lines = sales_file.readlines()
    sales_file.close()
    i =0
    d_line =0
    while (i<len(lines)):
       s1= lines[i]
       s1 = s1.split(":")
       if s1[0]=="Customer ID" and s1[1].strip("\n").strip()==str(cust_id):
           r_line = i+4
           s2 = lines[r_line]
           s2 = s2.split(":")
           r_point = s2[1].strip("\n")
           r_points += int(r_point.split('.')[0])
       i+=1
    if (r_points+reward_points)/100 > 0 :
        add_discount = math.floor(r_points+reward_points/100)*10  
    return add_discount

main()
