import datetime

def menu():
    
    """ Displays Menu and Gives Menu Options to User """
    
    
    #welcome message
    welcome = 'Welcome to the Small Business Delivery Program'
    
    #print welcome board
    print('*' * len(welcome))
    print(welcome)
    print('*' * len(welcome))
    
    #input menu choice
    choice = input('What would you like to do? \n 1. Display DELIVERY SUMMARY TABLE for this week \n 2. Display and save DELIVERY ORDER for specific address \n 3. Quit \n > ')
    
    #invalid entries
    while choice not in ['1', '2', '3']:
        #ask for valid input
        choice = input('Sorry, invalid entry. Please enter a choice from 1 to 3. \n > ')
    
    #return choice
    return choice


def option1():
    
    
    """ Displays Delivery Summary Table"""
    
    #open files
    zones = openZones()
    orders = openOrders()
    products = openProducts()
    
    #find areas delivered to 
    totalNum = {}
    addressCode = []
    totalPrice = 0

    #get order address
    for item in orders:
        #gets time in specific area
        times = int(item['amount'].strip()) #used for price later
        addressCode.append(item['address'])
        productID = item['product']
        totalPrice += int(products[productID][2].strip()) * times
        
    #in dollars    
    totalPrice = totalPrice/100
    
    #each unique address delivered to
    uniqueAddress = []
    
    #remove duplicates
    for i in addressCode:
        if i not in uniqueAddress:
            uniqueAddress.append(i)
            
    #dictionary for total amount to each areaCode
    for i in range(len(uniqueAddress)):
        #not in dict = 1
        if uniqueAddress[i][-7:-4] not in totalNum:
            totalNum[uniqueAddress[i][-7:-4]] = 1
        #+1 for every new time
        else:
            totalNum[uniqueAddress[i][-7:-4]] += 1
                  
    #amount of deliveries to each area name
    delivery = {}
    for key in zones:
        for item in zones[key]:
            if item in totalNum:
                if key not in delivery:
                    delivery[key] = totalNum[item]
                else:
                    delivery[key] += totalNum[item]
                
    #drivers needed
    drivers = {}
    for key in delivery:
        #not multiple of 10
        if delivery[key]%10 != 0:
            drivers[key] = int(delivery[key]//10) + 1
        else:
            drivers[key] = delivery[key]//10
            
    #format display
    deliveryzoneLength = len(' Delivery Zone ') * '-'
    deliveriesLength = len(' Deliveries ') * '-'
    driversLength = len('  Drivers  ' ) * '-'
    print('+%s+%s+%s+'%(deliveryzoneLength,deliveriesLength,driversLength))
    print('| Delivery Zone | Deliveries |  Drivers  |')
    print('+%s+%s+%s+'%(deliveryzoneLength,deliveriesLength,driversLength))
    
    #count drivers and deliveries
    totalDrivers = 0
    totalDeliveries = 0
    deliveryPrice = 12
    
    #print each area in alphabetical
    for i in sorted(delivery.keys()):
        print('| {:<13s} | {:^10} | {:^9} |'.format(i,delivery[i],drivers[i]))
        totalDrivers += drivers[i]
        totalDeliveries += delivery[i]
        
    #print displays
    print('+%s+%s+%s+'%(deliveryzoneLength,deliveriesLength,driversLength))
    print('| Total drivers needed {:>17} |'.format(totalDrivers))
    print('| Total delivery cost%11s%8.2f |'%('$',deliveryPrice*totalDeliveries))
    print('| Delivery cost/purchasess {:12.1f}% |'.format(((deliveryPrice*totalDeliveries)/totalPrice)*100))
    print('+%s-%s-%s+\n'%(deliveryzoneLength,deliveriesLength,driversLength))
    
    
    
def option2():
    
    """Displays Delivery Order and Saves Invoice"""
    
    
    #list of addresses from order
    orderAddress = []
    
    #find order addresses
    orders = openOrders()
    products = openProducts()
    
    #dictionary of months
    months = {'01':'JAN', '02': 'FEB' , '03':'MAR' , '04':'APR' , '05':'MAY', '06':'JUN', '07':'JULY', '08':'AUG', '09':'SEPT', '10':'OCT', '11':'NOV', '12':'DEC'}
    
    #open invoice file
    
    file = open('invoice.txt', 'w')
    
    
    for item in orders:
        orderAddress.append(item['address'])
        
    #enter address
    address = input('Address: ')
    
    #valid address
    if address in orderAddress:

        deliveryMessage = 'Delivery for:'
        
        #format address size
        if len(address) > 30:
            address = address[:29] + '*'        
        
        #format invoice 
        file.write('{:18}{:>29s}\n'.format(deliveryMessage, address))
        file.write('=' * 47)
        file.write('\n{:<7} {:<27}   {}\n'.format('Date', 'Item', 'Price'))
        file.write('{:<7} {} {:>12}\n'.format(('-'*6), ('-'*26), ('-'*9)))
        
        #total price counter
        totalPrice = 0
        #nested list of invoice info
        invoice = []
        for item in orders:
            #list of info of each order
            info = []
            #find purchases for address
            if item['address'] == address:
                date = item['date']
                
                #convert date into month letters
                monthNum = date[5:7]
                datetime_object = datetime.datetime.strptime(monthNum, '%m')
                monthName = datetime_object.strftime('%b').upper() + ' ' + date[8:]
                
                #find product name and quantity
                product = item['product']
                amount = (item['amount']).strip()
                
                #iterate through products for price and name
        
                for key in products:
                    
                    #find purchsed product
                    if product == key:
                        #find price
                        price = float(products[key][2])*float(amount)/100.00
                        totalPrice += price 
                        
                        #format product size
                        if len(products[key][1]) > 20:
                            productName = products[key][1][:19] + '*'
                        elif len(products[key][1]) <= 20:
                            productName = products[key][1]
                        
                        #print
                        #print('%s %s %s %20.2f'%(monthName, amount, productName, price))
                        
                #create nested list
                        info.extend([monthName, amount, productName, price])
                invoice.append(info)
        #sort relative to date
        invoice = sorted(invoice)            
        
        #print invoice
        for item in invoice:
            file.write('{:6s}  {:03d} x {:<20s}{:>5}{:>8.2f}\n'.format(item[0],int(item[1]),item[2],'$',item[3]))
        
        #print total
        file.write('{:>47}\n'.format('-'*9))
        file.write('{:>39}{:>8.2f}\n\n'.format('$',totalPrice))
        file.close()
        
        #read and print invoice
        f = open('invoice.txt','r')
        print(f.read())
        
        #prompt menu
        menu()
        
    #invalid address
    else:
        #redirect back to menu
        print('Invalid address.\n')


def option3():
    
    
    """Exits Application"""
    
    
    print('\nThank you for using the Small Business Delivery Program! Goodbye.')

def openOrders():
    
    """ Opens and Reads Orders Text File
    
    Returns List of Orders in a Dictionary"""
    
    orders = []
    #open and read order file
    filename = 'orders.txt'
    for line in open(filename):
        
        orderList = line.split('%')
    
        orderDict = {'date':'', 'name':'', 'address':'','product':'','amount':''}
    
        orderDict['date'] = orderList[0]
        orderDict['name'] = orderList[1]
        orderDict['address'] = orderList[2]
        orderDict['product'] = orderList[3]
        orderDict['amount'] = orderList[4]
    
        orders.append(orderDict)
        
    return orders
        

def openProducts():
    
    """ Opens and Reads Products Text File
    
    Returns Dictionary of Products"""
    
    #open and read products file
    
    productDict = {}
    
    filename = 'products.txt'
    for line in open(filename):
        productList = line.split(';')
        productDict[productList[0]] = productList
        
    return productDict

def openZones():
    
    """ Opens and Reads Zones Text File
    
    Returns Dictionary of Zones"""
    
    zoneDict = {}
    
    #open and read zones file
    filename = 'zones.txt'
    for line in open(filename):
        zoneList = line.split('#')
        zoneDict[zoneList[0]] = zoneList[1]
        
    #remove \n from values    
    for key in zoneDict:
        zoneDict[key] = zoneDict[key].replace('\n','')
        zoneDict[key] = zoneDict[key].split(',')
    
    return zoneDict


def main():
    
    #open menu
    option = menu()
    
    while option != '3':
    
    #different options
        if option == '1':
            option1()
            #go back to menu
        
        elif option == '2':
            option2()   
            #go back to menu
            
        option = menu()
        
    if option == '3':
        option3()
        
main()