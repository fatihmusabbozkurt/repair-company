import sqlite3
import PySimpleGUI as sg
from datetime import datetime

con = sqlite3.connect('URANUS2017_DATABASE.db.db')
cur = con.cursor()

login_user_E_Mail = -1
login_user_name = -1
login_user_type = -1


def window_login():
    
    layout = [[sg.Text('Welcome to the URANUS2017 Repair Company System. Please enter your information.')],
              [sg.Text('E Mail:',size=(50,1)), sg.Input(size=(50,1), key='E_Mail')],
              [sg.Text('Password:',size=(50,1)), sg.Input(size=(50,1), key='Password')],
              [sg.Button('Login')]]

    return sg.Window('Login Window', layout)

def window_customer():
    
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Button('My Addresses')],
              [sg.Button('Create a New Service Request')],
              [sg.Button('My Service Records')],
              [sg.Button('Logout')]]

    return sg.Window('Customer Window', layout)


def window_technician():
    
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Button('My Service Requests')],
              [sg.Button('Create a New Repair Record')],
              [sg.Button('Add Spare Part to Repair Record')],
              [sg.Button('Approved Reviews')],
              [sg.Button('Logout')]]

    return sg.Window('Technician Window', layout)
    

def window_manager():
    
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Button('Forward Requests')],
              [sg.Button('Pending Reviews')],
              [sg.Button('Create a New Spare Part')],
              [sg.Button('Logout')]]

    return sg.Window('Manager Window', layout)       
    

def window_adding_spare_tech():
    global spare_parts
    global rec_no
    
    spare_parts=[]
    rec_no=[]
    
    
    for row in cur.execute('''SELECT Spare_Part.ModelNo, Spare_Part.Description, Spare_Part.ManufName
                        FROM Spare_Part'''):

        spare_parts.append(row)
        
    for row in cur.execute('''SELECT Use.RecordNo
                        FROM Spare_Part,Use
                        WHERE Use.ManufName=Spare_Part.ManufName
                        AND Use.ModelNo=Spare_Part.ModelNo'''):

        rec_no.append(row)
        
    layout=[[sg.Text('Add Spare Parts:')],
            [sg.Listbox(spare_parts, size=(50, 5), key='Spare')],
            [sg.Listbox(rec_no, size=(50, 5), key='RecNo')],
            [sg.Text('Amount:',size=(50,1)), sg.Input(size=(50,1), key='Amountt')],
            [sg.Button('Add Spare Part'),sg.Button('Return To Main')]]
            


    return sg.Window('Add Spare Part Window', layout) 







def button_add_spare_tech(values):



    
    
    
    if len(values['Spare'])==0:

        sg.popup('Spare Part selection should not be empty.')
    
    elif len(values['RecNo'])==0:
        sg.popup('Record number should not be empty.')
        
    elif len(values['Amountt'])==0:
        sg.popup('Amount should not be empty.')
    
    elif not values['Amountt'][0].isnumeric():
        sg.popup('Amount should be numeric.')
        
        
      
        
     
    
        
        
        
        
        
    
    
    
    else:
        
        
        
        
        
        
        modelNo=values['Spare'][0][0]
        manufName=values['Spare'][0][2]
        amountt=values['Amountt']
        rec_no=values['RecNo'][0][0]
        
        cur.execute('SELECT Use.ManufName,Use.ModelNo,Use.RecordNo FROM Use WHERE ManufName = ? AND ModelNo = ? AND RecordNo = ?', (manufName,modelNo,rec_no))
        row = cur.fetchone()
    
        if row is not None:
            sg.popup('This selected spare part with model no  ' + str(modelNo) + "  and manufacturer name "+ str(manufName) + " " + 'is already added to this record number' + " " +str(rec_no))
            
            
        else:
            stock=[]
            
            for row in cur.execute('''SELECT Spare_Part.StockAmount 
                                    FROM Spare_Part 
                                    WHERE Spare_Part.ManufName = ? AND Spare_Part.ModelNo= ?''',(manufName,modelNo, )):
                stock.append(row)
              
                print(stock[0][0])
                print(amountt)
            
            if int(amountt) > int(stock[0][0]):
                sg.popup('There is not enough spare part stock')
            
            else:
                cur.execute('INSERT INTO Use Values (?,?,?,?)',(manufName,modelNo,rec_no,amountt))
                remaining= int(stock[0][0])- int(amountt)
                cur.execute('UPDATE Spare_Part SET StockAmount = ? WHERE ManufName = ? AND ModelNo = ?', (remaining, manufName,modelNo))
            
                
                sg.popup('Spare part is successfully inserted to record: ' + str(rec_no)+ "model number   " + str(modelNo) + "manufacturer name    " + str(manufName) + "amount=    " +str(amountt))
                sg.popup('Remaining stock = '+ str(remaining))
     
    con.commit()
    
    
def window_forward_man():

    global requesst
        
    global technicianss
    global specialities
    
    
    technicianss=[]
    
    specialities=[]
    
    
    requesst=[]
    
    
    for row in cur.execute('''SELECT ServiceReqAssociation.ReqNum, ServiceReqAssociation.AssocAdrNo, ServiceReqAssociation.AssocCus_Mail,ServiceReqAssociation.Description,ServiceReqAssociation.ReqDate
                            FROM ServiceReqAssociation'''):
    
        requesst.append(row)
   

    
    
    
    
    for row in cur.execute('''SELECT DISTINCT Speciality.TypeNum,ServiceType.TypeName,ServiceType.Description
                            FROM Speciality,ServiceType
                            WHERE Speciality.TypeNum=ServiceType.TypeNum'''):
        specialities.append(row)
    

    

    
    
    
    for row in cur.execute('''SELECT User.E_Mail, User.Name,User.Surname
                            FROM User,Technician,Speciality
                            WHERE User.E_Mail=Technician.Tech_Mail
                            AND Speciality.Tech_Mail=Technician.Tech_Mail'''):
    
        technicianss.append(row)
        
     
      
    
    layout = [[sg.Text('Forward Requests:')],
              [sg.Listbox(specialities, size=(50, 5), key='Sppec')],
              [sg.Listbox(technicianss, size=(50, 5), key='TechMail')],
              [sg.Listbox(requesst, size=(50, 5), key='ReqNum')],
              [sg.Button('Forward'),sg.Button('Filter'),sg.Button('Return To Main')]]


    
    return sg.Window('Forward Requests Window', layout)
        
    

    
def window_pending_reviews_man():
    
    global revieww
    
    revieww=[]
    
    for row in cur.execute('''SELECT Review.RecordNo,Review.Comment,Review.Score
                            FROM Review
                            WHERE Review.RecordNo NOT IN(SELECT Approve.RecordNo
                                                        FROM Approve,Review
                                                        WHERE Approve.RecordNo=Review.RecordNo)'''):
        revieww.append(row)
    

    layout = [[sg.Text('Pending Reviews:')],
          [sg.Listbox(revieww, size=(50, 5), key='Rew')],
          [sg.Button('Approve'),sg.Button('Return To Main')]]
    
    
    return sg.Window('Pending Review Window',layout)
    
    
    

    
    
    
def window_create_spare_man():
    
    
    
    layout = [[sg.Text('Create Spare Part:')],
              [sg.Text('Stock Amount:',size=(50,1)), sg.Input(size=(50,1), key='StockAmountM')],
              [sg.Text('Description:',size=(50,1)), sg.Input(size=(50,1), key='DescriptionM')],
              [sg.Text('Manufacturer Name:',size=(50,1)), sg.Input(size=(50,1), key='ManufNameM')],
              [sg.Text('Model Number:',size=(50,1)), sg.Input(size=(50,1), key='ModelNoM')],
              [sg.Text('Unit Price:',size=(50,1)), sg.Input(size=(50,1), key='UnitPriceM')],
              [sg.Button('Create Spare Part'),sg.Button('Return To Main')]]

    return sg.Window('Create Spare Part Window', layout)
    
def button_create_spare_man(values):
    
    
    stock=values['StockAmountM']
    despM=values['DescriptionM']
    manufM=values['ManufNameM']
    modM=values['ModelNoM']
    unpric=values['UnitPriceM']
    
    
    if stock=='':
        sg.popup('Stock amount cannot be empty')
    
        
    elif not stock.isnumeric():
        sg.popup('Stock amount should be numeric')
        
    elif despM=='':
        sg.popup('Description cannot be empty')
        
    elif manufM=='':
        sg.popup('Manufacturer name cannot be empty')
        
    elif modM=='':
        sg.popup('Model number cannot be empty')
        
    elif not modM.isnumeric():
        sg.popup('Model number should be numeric')
        
    elif unpric=='':
        sg.popup('Unit price cannot be empty')
        
    elif not unpric.isnumeric():
        sg.popup('Unit price should be numeric')
        
    else:
        
        cur.execute('SELECT Spare_Part.StockAmount,Spare_Part.Description,Spare_Part.ManufName,Spare_Part.ModelNo,Spare_Part.UnitPrice FROM Spare_Part WHERE StockAmount = ? AND Description = ? AND ManufName = ? AND ModelNo = ? AND UnitPrice = ?', (stock,despM,manufM,modM,unpric))
        row = cur.fetchone()

        if row is not None:
            sg.popup('There is already a spare part with stock amount '+str(stock)+' despriction '+ str(despM)+ ' manufacturer name ' + str(manufM)+ ' model number '+str(modM)+' unit price '+ str(unpric))
    

        else:
        
   
            cur.execute('INSERT INTO Spare_Part Values (?,?,?,?,?)',(stock,despM,manufM,modM,unpric))

            sg.popup('Spare part with stock amount '+str(stock)+' despriction '+ str(despM)+ ' manufacturer name ' + str(manufM)+ ' model number '+str(modM)+' unit price '+ str(unpric))

    con.commit()
    
    
    
    
    
def window_request():    
    global address
    global type_name
    global description
    
    address = []
    type_name = []
    description = []
    
    for row in cur.execute('''SELECT AddNum,BuildNum,StreetName,CityName
                            FROM AddressHas,Customer
                            WHERE AddressHas.Cus_Mail=Customer.Cus_Mail
                            AND AddressHas.Cus_Mail = ?''',(login_user_E_Mail,)):
        
        address.append(row)
        
        
        
    for row in cur.execute(''' SELECT DISTINCT TypeName
                            FROM ServiceType'''):
        
        type_name.append(row)
        
        
        
        
    for row in cur.execute(''' SELECT DISTINCT Description
                            FROM ServiceType'''):
        description.append(row)
    
    
    layout = [[sg.Text('Your Service Request:')],
              [sg.Listbox(address, size=(50, 5), key='AddNum')],
              [sg.Text('Type Name:'), sg.Combo(type_name, size=(25,7), key='TypeNum')],
              [sg.Text('Type Description:'), sg.Combo(description, size=(25,7), key='Description')],
              [sg.Button('Create Request'),sg.Button('Return To Main')]]

    return sg.Window('Request Window', layout)


def window_request_tech():
    
    
    serv_req_tech=[]
    
    
    for row in cur.execute('''SELECT Forward.ReqNum,AssocAdrNo,AssocCus_Mail,Description,ReqDate
                            FROM Forward,ServiceReqAssociation
                            WHERE Forward.ReqNum=ServiceReqAssociation.ReqNum
                            AND Forward.Tech_Mail = ?''',(login_user_E_Mail,)):
       
        serv_req_tech.append(row)
    
    
    
    
    
    
    
    layout = [[sg.Text('Your Service Requests:')],
              [sg.Listbox(serv_req_tech, size=(50, 5), key='ReqNum')],
              [sg.Button('Return To Main')]]
    
    
    
    return sg.Window('Request Technician Window', layout)
    
    
    
    
    
def window_create_record_tech():    
    global record
    global service_fee
    global descriptionT
    

    
   
    
    request = []
    


    for row in cur.execute(    '''SELECT Forward.ReqNum,AssocAdrNo,AssocCus_Mail,Description,ReqDate
                                FROM Forward,ServiceReqAssociation
                                WHERE Forward.ReqNum=ServiceReqAssociation.ReqNum
                                AND Forward.ReqNum NOT IN(SELECT Createe.ReqNum
                                                                FROM Createe)
                                AND Forward.Tech_Mail = ?''',(login_user_E_Mail,)):
                            
        
        request.append(row)
        
        
     

    
        
    
    layout = [[sg.Text('Your Service Request:')],
              [sg.Listbox(request, size=(50, 5), key='ReqNum')],
              [sg.Text('Service Fee:',size=(50,1)), sg.Input(size=(50,1), key='ServiceFee')],
              [sg.Text('Description:',size=(50,1)), sg.Input(size=(50,1), key='DescriptionT')],
              [sg.Text('Date of Resolution:', size=(15,1)), sg.Input(key='dateofres', size=(15,1)), sg.CalendarButton('Choose Date', format='%Y-%m-%d')],
              [sg.Button('Create Record'),sg.Button('Return To Main')]]

    return sg.Window('Record Window', layout)


 
def window_approved_reviews():
    
    approved = []
    

    for row in cur.execute('''SELECT Approve.RecordNo,Review.Comment,Review.Score
                            FROM Approve,Review,Createe, Repair_Record
                            WHERE Approve.RecordNo=Review.RecordNo
                            AND Repair_Record.RecordNo=Createe.RecordNo
                            AND Review.RecordNo= Repair_Record.RecordNo
                            AND Createe.Tech_Mail = ?''',(login_user_E_Mail,)):
        
        approved.append(row)
        
        
    layout = [[sg.Text('Approved Reviews:')],
              [sg.Listbox(approved, size=(50, 5), key='RecordNo,Man_Mail')],
              [sg.Button('Return To Main')]]
    
    
    return sg.Window('Approved Reviews Window', layout)
    
    

def window_my_addresses():
    address = []
    for row in cur.execute('''SELECT AddNum,BuildNum,StreetName,CityName
                            FROM AddressHas,Customer
                            WHERE AddressHas.Cus_Mail=Customer.Cus_Mail
                            AND AddressHas.Cus_Mail = ?''',(login_user_E_Mail,)):
        address.append(row)
      
    
    layout = [[sg.Text('My Addresses:')],
              [sg.Listbox(address, size=(50, 5), key='AddNum,Cus_Mail')],
              [sg.Button('Return To Main')]]


    
    return sg.Window('My Addresses Window', layout)


def window_records():
    records = []
    
    for row in cur.execute('''SELECT Repair_Record.RecordNo, Repair_Record.ResolveDate, Repair_Record.Description
                            FROM Repair_Record, Createe, ServiceReqAssociation
                            WHERE Repair_Record.RecordNo = Createe.RecordNo
                            AND Createe.ReqNum = ServiceReqAssociation.ReqNum
                            AND Repair_Record.RecordNo NOT IN (SELECT Review.RecordNo
                                                                FROM Review)
                            AND ServiceReqAssociation.AssocCus_Mail = ?''',(login_user_E_Mail,)):
        records.append(row)


    
    
    

    layout = [[sg.Text('My Records:')],
              [sg.Listbox(records, size=(50, 5), key='RecordNo')],
              [sg.Text('Comment:')], 
              [sg.Input(key='comment')],
              [sg.Text('Score(1-100):')], 
              [sg.Input(key='score')],
              [sg.Button('Add Review'),sg.Button('Return To Main')]]
    

    
    
    
        
    return sg.Window('Records Window', layout)


def button_login(values):
    
    global login_user_E_Mail
    global login_user_name
    global login_user_type
    global window
    
    umail = values['E_Mail']
    upass = values['Password']
    if umail == '':
        sg.popup('E-Mail cannot be empty')
    elif upass == '':
        sg.popup('Password cannot be empty')
    else:
        
        cur.execute('SELECT E_Mail, Name, Surname FROM User WHERE E_Mail = ? AND Password = ?', (umail,upass))
        row = cur.fetchone()
        
             
                    
        
        if row is None:
            sg.popup('E_Mail or password is wrong!')
            
        else:
            
            
            
            login_user_E_Mail = row[0]
            
            
            login_user_name = row[1]
            
            cur.execute('SELECT Cus_Mail FROM Customer WHERE Cus_Mail = ?', (umail,))
            row_customer = cur.fetchone()
            
            
            
            if row_customer is None:
                cur.execute('SELECT Tech_Mail FROM Technician WHERE Tech_Mail = ?', (umail,))
                row_technician = cur.fetchone()
                
                if row_technician is None:
                    cur.execute('SELECT Man_Mail FROM Manager WHERE Man_Mail = ?', (umail,))
                    row_manager = cur.fetchone()
                    
                    if row_manager is None:
                        sg.popup('User is not found!')
                        
                    else:
                        login_user_type = 'Manager'
                        sg.popup('Welcome, ' + login_user_name + ' (Manager)')
                        window.close()
                        window = window_manager()
                    
                else:
                    login_user_type = 'Technician'
                    sg.popup('Welcome, ' + login_user_name + ' (Technician)')
                    window.close()
                    window = window_technician()
                    
            else:
                
                login_user_type = 'Customer'    
                sg.popup('Welcome, ' + login_user_name + ' (Customer)')
                window.close()
                window = window_customer()
                    

                    
                    
def button_approve_man(values):
    
    #FIX EVERYTHING
    
    todaysDate2 = datetime.today().strftime('%Y-%m-%d')
    

    if len(values['Rew']) == 0:
        sg.popup('Choose a review first!')
    else:
        
        new_approved = values['Rew'][0]
        new_approved_code = new_approved[0]
        
        print(new_approved_code)
        
        # now let's insert this to enrolled
        cur.execute('INSERT INTO Approve Values(?,?,?)', (login_user_E_Mail,new_approved_code,todaysDate2))
        
        sg.popup('Successfully approved the review with record number ' + str(new_approved))
        
        # refresh the list so that enrolled course does not appear in combo
        available_reviews = []
        
        
        
        for row in cur.execute('''SELECT Review.RecordNo,Review.Comment,Review.Score
                            FROM Review
                            WHERE Review.RecordNo NOT IN(SELECT Approve.RecordNo
                                                        FROM Approve,Review
                                                        WHERE Approve.RecordNo=Review.RecordNo)'''):
            available_reviews.append(row)
            
        window.Element('Rew').Update(values=available_reviews)
        
        con.commit()

        
        

    
 
    
    
def button_pending_reviews_man(values):
    
    global window
    window.close()
    window=window_pending_reviews_man()
    
    
    
def button_forward_man(values):

    global requ
    global tech
    
    
    requ=values['ReqNum'][0][0]
    tec=values['TechMail'][0][0]

    cur.execute('SELECT Forward.Man_Mail,Forward.Tech_Mail,Forward.ReqNum FROM Forward WHERE Man_Mail = ? AND Tech_Mail = ? AND ReqNum = ?', (login_user_E_Mail,tec,requ))
    row = cur.fetchone()
    
    if row is not None:
        sg.popup('This forward process with request number  ' + str(requ) + "  and technician "+ str(tec) + " " + 'is already done before')


    else:    
        cur.execute('INSERT INTO Forward Values(?,?,?)',(login_user_E_Mail,tec,requ))
        sg.popup('Forward process of request '+str(requ)+' is succesfully done to the techinican '+str(tec))
        con.commit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def button_filter_man(values):
    
    
    chosen_spec=values['Sppec']
    


    
    if chosen_spec =='':
        sg.popup('Please choose a speciality')
        
    else:
        
        specc=chosen_spec[0][0]
        
        
        technicianss=[]
        
            
        for row in cur.execute('''SELECT User.E_Mail, User.Name,User.Surname
                                FROM User,Technician,Speciality
                                WHERE User.E_Mail=Technician.Tech_Mail
                                AND Speciality.Tech_Mail=Technician.Tech_Mail
                                AND Speciality.TypeNum = ?''',(specc,)):

            technicianss.append(row)



        window.Element('TechMail').Update(values=technicianss)

                    
def button_My_Addresses(values):
    global window
    window.close()
    window = window_my_addresses()
                

        

def button_My_Service_Requests(values):
    global window
    window.close()
    window = window_request_tech()



def button_Approved_Reviews(values):
    global window
    window.close()
    window = window_approved_reviews()
    
    
    

def button_Create_a_New_Service_Request(values):
    global window
    window.close()
    window = window_request()

    
def button_My_Records(values):
    global window
    window.close()
    window = window_records()
    
    

def button_Create_Request(values):
    global window
    global todaysDate
    
    todaysDate = datetime.today().strftime('%Y-%m-%d')
    
    
    
   
    
    
    
    if len(values['AddNum']) == 0:
        sg.popup('Address cannot be empty!')
    elif len(values['TypeNum']) == 0:
        sg.popup('Type name cannot be empty!')
    elif len(values['Description']) == 0:
        sg.popup('Description name cannot be empty!')
    else:
        cur.execute('SELECT MAX(ReqNum) FROM ServiceReqAssociation')
        row = cur.fetchone()

        if row is None:
            new_reqnum = 1
        else:
            new_reqnum = row[0] + 1
    
    
        address=values['AddNum'][0][0]
        type_name=values['TypeNum'][0]
        description=values['Description'][0]
    
        cur.execute('INSERT INTO ServiceReqAssociation VALUES (?,?,?,?,?)',(new_reqnum,address,login_user_E_Mail,description,todaysDate))
    
        con.commit()
    
        sg.popup('Successfully inserted with request number: ' + str(new_reqnum)+ " address   " + str(address) + " type name  "+ str(type_name) + " description   " +str(description))
            
    
def button_Create_Record_Tech(values):
    global window
    
    
    dateres=values['dateofres']
    
    service_fee=values['ServiceFee']
    descriptionT=values['DescriptionT']
    
    

    
    
    
    date_string = dateres
    format = "%Y-%m-%d"

    
    
    try:
      datetime.strptime(date_string, format)
      x=1
    except ValueError:
      x=0
    
    
    
    
    if len(values['ReqNum']) == 0:
        sg.popup('Request cannot be empty!')
    elif service_fee == '':
        sg.popup('Service fee cannot be empty!')
        
    elif descriptionT == '':
        sg.popup('Description name cannot be empty!')
        
    elif dateres == '':
        sg.popup('Date cannot be empty!')
        
        
        
    elif x==0:
        
    
        sg.popup('Date type should be Year-Month-Day!')
    
    
    
    
    else:
        request=values['ReqNum'][0][0]
        
        cur.execute('SELECT MAX(RecordNo) FROM Repair_Record')
        row = cur.fetchone()

        if row is None:
            new_recno = 1
        else:
            new_recno = row[0] + 1  

    
    
        
        

        cur.execute('INSERT INTO Repair_Record VALUES (?,?,?,?)',(descriptionT,new_recno,dateres,service_fee))
    
        cur.execute('INSERT INTO Createe VALUES(?,?,?)',(login_user_E_Mail,request,new_recno))
        
        
        
        

        
        
    
        sg.popup('Successfully inserted with record number: ' + str(new_recno)+ " service fee   " + str(service_fee) + " date   "+ str(dateres) + " description   " +str(descriptionT))
      
        
        available_requests = []
        
        
        
        for row in cur.execute('''SELECT Forward.ReqNum,AssocAdrNo,AssocCus_Mail,Description,ReqDate
                                FROM Forward,ServiceReqAssociation
                                WHERE Forward.ReqNum=ServiceReqAssociation.ReqNum
                                AND Forward.ReqNum NOT IN(SELECT Createe.ReqNum
                                                                FROM Createe)
                                AND Forward.Tech_Mail = ?''',(login_user_E_Mail,)):
            available_requests.append(row) 
            
        window.Element('ReqNum').Update(values=available_requests)
    
    con.commit()
    
     
            


            
    

def button_Review(values):
    global window  
    

    
    
   
    
    if len(values['score']) == 0:
        sg.popup('Score cannot be empty!')
    elif not values['score'][0].isnumeric():
        sg.popup('Score should be numeric.')
        
    elif len(values['comment']) == 0:
        sg.popup('Comment cannot be empty!')
        
    elif len(values['RecordNo'])==0:
        sg.popup('Record number cannot be empty!')
        
    else:
        
        comment=values['comment']
        score=values['score']
        RecordNo=values['RecordNo'][0][0]
        
        if int(score) <1 or int(score)>100 :
            sg.popup('Score should be between [1,100] ')
            
        else:

        
        
        
         
            cur.execute('INSERT INTO Review VALUES(?,?,?,?)',(login_user_E_Mail,RecordNo,comment,score))   
            sg.popup('Review is successfully taken:')
       
            available_records = []



            for row in cur.execute('''SELECT Repair_Record.RecordNo, Repair_Record.ResolveDate, Repair_Record.Description
                            FROM Repair_Record, Createe, ServiceReqAssociation
                            WHERE Repair_Record.RecordNo = Createe.RecordNo
                            AND Createe.ReqNum = ServiceReqAssociation.ReqNum
                            AND Repair_Record.RecordNo NOT IN (SELECT Review.RecordNo
                                                                FROM Review)
                            AND ServiceReqAssociation.AssocCus_Mail = ?''',(login_user_E_Mail,)):
        
                available_records.append(row)

                window.Element('RecordNo').Update(values=available_records)
        
    
    con.commit()
    window.close()
    window=window_records()

    


                
                
window = window_login()

while True:
    event, values = window.read()
    if event == 'Login':
        button_login(values) 
    elif event == 'My Addresses':
        window.close()
        button_My_Addresses(values)
    elif event == 'Create a New Service Request':
    
        window.close()
        button_Create_a_New_Service_Request(values)
    elif event == 'Create Request':
        button_Create_Request(values)
    elif event == 'Return To Main':
        if login_user_type == 'Customer':
            window.close()
            window = window_customer()
        elif login_user_type == 'Technician':
            window.close()
            window = window_technician()
        elif login_user_type == 'Manager':
            window.close()
            window = window_manager()
        else:
            window.close()
            window = window_records()

            
    elif event == 'Create a New Spare Part':
        window.close()
        window=window_create_spare_man()
            
    elif event == 'Forward Requests':
        window.close()
        window=window_forward_man()    

    elif event == 'Forward':

        button_forward_man(values)
        
    elif event == 'Filter':
        button_filter_man(values)
        
    elif event == 'Pending Reviews':
        button_pending_reviews_man(values)
        
    elif event == 'Create Spare Part':
        button_create_spare_man(values)
            
            
    elif event == 'My Service Records':
        window.close()
        button_My_Records(values)
        
        
    elif event == 'Create a New Repair Record':
        window.close()
        window=window_create_record_tech()
        
    elif event == 'Create Record':
        
        button_Create_Record_Tech(values)
     
    
    elif event == 'Add Spare Part to Repair Record':
        window.close()
        window=window_adding_spare_tech()
        
        
    elif event == 'Add Spare Part':
        button_add_spare_tech(values)
        
    
    elif event == 'Approved Reviews':
        window.close()
        window = window_approved_reviews()
    
    elif event == 'Approve':
        button_approve_man(values)
    
    
    elif event == 'Add Review':
        window.close()
        button_Review(values)     
    elif event == 'My Service Requests':
        window.close()
        button_My_Service_Requests(values)
        
    elif event == 'Logout':
        login_user_id = -1
        login_user_name = -1
        login_user_type = -1
        window.close()
        window = window_login()
        
        
        
        
        
    elif event == sg.WIN_CLOSED:
        sg.popup('ŞOV BİTTİ HER ŞEY İÇİN TEŞEKKÜRLER SİNAN HOCAM')
        break
    
        
window.close()

con.commit()
con.close()