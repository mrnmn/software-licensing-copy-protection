# all functions 
# handling statement after statement.
from verification import new_client
from verification import activate_license
from verification import change_device
from verification import is_mac_exist
from verification import is_email_exist
from verification import set_trial_columns
from verification import set_trial
from verification import trial_expired
from verification import trial_to_paid
from verification import activate_license_after_trial
from verification import clear_periods
from queue import Queue
#usage:
#running in backend.

if __name__ == '__main__':
    #set_trial_columns('tablename') Add the columns for the trial period to your table. (for the first time only)


    #a customer buy the product. Add a customer , mac always NULL.
    #Processing more than 1..
    q = Queue()
    try:
        q.put('user@gmail.com')
    #add clinets
        while not q.empty():
            new_client('tablename',q.get(),None)
    except:
        print("oops!")
    print("added seccessfully!")

    #The customer uses the license to activate the product
    #Receive the Mac and e-mail from the license
    #Processing more than 1..
    if activate_license('tablenale','user@gmail.com',9999999999999): # the mac converted from hexa to int.
        #return true Activation was successful, or determine a trial period according to customer type
        #determine a trial period
        if set_trial('tablenale','user@gmail.com', 30): # trial period in days.
            # return true, the trial period is activated.
        


    #Protect your software from copying. Every time the software is launched, the Mac is sent.
    #Receive the Mac from the software
    #Processing more than 1..
    if is_mac_exist('tablename',9999999999999):
        #return true to the lifetime client (It does not have a trial period.)
    

    #clinets with trial period
    #Every time the software is launched, the Mac is sent.
    #Check if the trial period has expired.
    #Processing more than 1..
    if is_mac_exist('tablename',9898989898989) and not trial_expired('tablename',9898989898989):
        #return true (can use the software)
    else:
        #return false (cant use the software, the trial period has expired.)


    #Change status for customers with an expired trial period.
    # change the status for a clinet from trial to paid. (true to false)
    if trial_to_paid('tablename','user@gmail.com'):
        # the status changed. do something.


   #clear start date and end date (trial period), works after the trial period ends.
   clear_periods('tablename','user@gmail.com') #return true if if done correctly.
    

        


    
     


    
        
    


    
    

    
    

    
    
    
    
    
      


        
        



    



