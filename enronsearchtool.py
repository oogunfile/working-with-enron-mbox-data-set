import mailbox
import os
import re
#################################################################################
# FUNCTION 1
# searching for a word or phrase in an mbox file that avoids repetitive words and makes the phrase an exact match(no partial matches)
def enron_search_term(searchWord):
    #split the words and call set function to remove duplicate words
    word_split= set(searchWord.lower().split())
    #join words and any white space inbetween. Use word boundaries to ensure exact search
    word_join = r"\b" + r"\b\s*".join(word_split) + r"\b"
    #check:print(word_join)
    # make an object called pattern so you can use the search() with it
    pattern = re.compile(word_join , re.IGNORECASE)
    num = 0
    # iterate through mailbox files in directory
    for filename in os.listdir("filepath"):
        mbox_path = os.path.join("filepath", filename)
        # create mbox object
        mbox = mailbox.mbox(mbox_path)
        for message in mbox:
            email = message.get_payload(decode = True).decode(errors = "ignore")
            sender = message["From"]
            date = message["Date"]
            #name_email = message["x-From"]
            if re.search(pattern,email):
                num+=1
                print(num, " : ", sender , date)
                # check: print(email)
    if num==0:
            print("Not found")
    print("Results found: ", num)

searchWord = input("enron_search term_search term:....  ")
enron_search_term(searchWord)
#################################################################################
#FUNCTION 2
#searching for mails sent and received by a particular person. using their full name as the search term. 
def enron_Name_search(prompt):
     num = 0 
     #to ensure both last and first name are entered
     if len(prompt)<2:
         print("Enter both surname and first name please")
         return
     else: 
         name = prompt.split()
         #exchange first and last names and ignore dots 
         #The assignment says to enter last and first name but the name header 
         #fields have first and last names
         fullName1 = r"\b" + name[1] + r"[^a-zA-Z]*"  + name[0]+ r"\b"
         fullName2 =  r"\b" + name[0] + r"[^a-zA-Z]*" + name[1]+ r"\b"
         #pattern_Fullname = re.compile(fullName1 + r"|" + fullName2, re.IGNORECASE, )
         # iterate through mailbox files in directory
         for filename in os.listdir("filepath"):
             mbox_path = os.path.join("filepath", filename)
             # create mbox object
             mbox = mailbox.mbox(mbox_path)
             for message in mbox:
                # if message.get("From") and re.search(name_phrase, message["x-From"], re.IGNORECASE):
                 sender = message["From"]
                 receiver = message["To"]
                 if sender is not None and receiver is not None:
                     # i decided to search for either last and first name or first and last name
                     if re.search(fullName1,  str(sender)) or re.search(fullName2,  str(sender)):
                         num+=1
                         #
                         print(num, sender) 
                     if re.search(fullName1, str(receiver)) or re.search(fullName2, str(receiver)):
                         num+=1
                         print(num, receiver)
         if num==0:
             print("No match")
     print("Results found: ", num)

prompt = input("enron_search address_search last_name first_name: ")
enron_Name_search(prompt)

#################################################################################
#FUNCTION 3
#searching for mails exchanged between two people. 
def search_Addresses(addy1, addy2):
    #escape() use special xters in re library as string,
    addy_pattern1 = re.compile(r"\b" + re.escape(addy1) + r"\b", re.IGNORECASE)
    addy_pattern2 = re.compile(r"\b" + re.escape(addy2) + r"\b", re.IGNORECASE)
    count =0
    for filename in os.listdir("filepath"):
        mbox_path = os.path.join("filepath", filename)
        # create mbox object
        mbox = mailbox.mbox(mbox_path)
        for message in mbox:
            subject = message["subject"]
            sender = message["From"]
            receiver = message["To"]
            date = message["Date"]
            # to omit header fields that are absent
            if sender is not None and receiver is not None:
                if (re.search(addy_pattern1, sender) and re.search(addy_pattern2, receiver)) or (re.search(addy_pattern2, sender) and re.search(addy_pattern1, receiver)) :
                    count+=1
                    print(count, " : ", sender, "  -->  ", receiver, subject, date)
    if count==0:
        print("No match")
    print("Results found", count)
addy1 = input("enron_search interaction_search address_1..  ")
addy2 = input("enron_search interaction_search address_2..  ") 
search_Addresses(addy1, addy2)
