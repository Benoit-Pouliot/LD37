from app.sprites.item.item import Item

class Inventory:
    def __init__(self):
        # Menu list
        self.itemList = []

    def addItem(self,printedName,method):
        self.itemList.append(Item(printedName,method))