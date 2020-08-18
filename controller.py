listItem = {}

def listingSelectedItem(data):
    # create new dictionary index
    newKey = len(listItem)+1
    listItem[newKey] = {}
    # adding data to dictionary
    listItem[newKey]['itemName'] = data['itemName']
    listItem[newKey]['price'] = int(data['price'])
    listItem[newKey]['numberOfItem'] = int(data['numberOfItem'])
    listItem[newKey]['subTotal'] = int(data['numberOfItem'])*int(data['price'])
    return listItem

def getAllItem():
    allData=""
    for index, data in listItem.items():
        allData = allData + listItem[index]["itemName"] +" x "+ str(listItem[index]["numberOfItem"])+" , "
    return allData

def getTotal():
    total = 0
    for index, data in listItem.items():
        total += listItem[index]["subTotal"]
    return total
