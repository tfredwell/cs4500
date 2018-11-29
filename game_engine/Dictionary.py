#   Team Cosmosis
#   Group Project: taste game remodel
#   contained class: Dictionary
#       Goal: A simple class to read and setup lists for each of the different food groups in a list of
#       triplets (RFID code, food item name, taste attribute)
#       Constructor:
#           init(self)
#               sets variable lists for fruit, protein, grain, dairy, and vegetable
#               calls update method
#       Methods:
#           update(self):
#               reads in a file for each food type variable list
#               line by line and separates the line into a list of words
#           display(self):
#               displays what is in each food type list and numbers the entries of each list in sequential order
#           clear(self):
#                clears all *table.txt files
#           getveg(self)|getprotein(self)|getfruit(self)|getgrain(self)|getdairy(self):
#               returns the respective food item list
# needed/contained files:
#       proteintable.txt
#       fruittable.txt
#       dairytable.txt
#       graintable.txt
#       vegtable.txt
#
#       All Files should have lines in the format: rfidKey foodItem tasteAttribute

class Dictionary:
    def __init__(self):
        self.veg = []
        self.protein = []
        self.fruit = []
        self.grain = []
        self.dairy = []

        self.update()

    def update(self):
        vegf = open("vegtable.txt", "r")

        for line in vegf:
            line = line.split(" ")
            line[2] = line[2].rstrip('\n')
            self.veg.append(line)
        vegf.close()

        proteinf = open("proteintable.txt", "r")

        for line in proteinf:
            line = line.split(" ")
            line[2] = line[2].rstrip('\n')
            self.protein.append(line)

        proteinf.close()

        fruitf = open("fruittable.txt", "r")

        for line in fruitf:
            line = line.split(" ")
            line[2] = line[2].rstrip('\n')
            self.fruit.append(line)

        fruitf.close()

        grainf = open("graintable.txt", "r")

        for line in grainf:
            line = line.split(" ")
            line[2] = line[2].rstrip('\n')
            self.grain.append(line)

        grainf.close()

        dairyf = open("dairytable.txt", "r")

        for line in dairyf:
            line = line.split(" ")
            line[2] = line[2].rstrip('\n')
            self.dairy.append(line)

        dairyf.close()


    def display(self):
        count = 0
        for obj in self.veg:
            print(count, '\t', self.veg[count])
            count = count + 1

        count = 0
        for obj in self.dairy:
            print(count, '\t', self.dairy[count])
            count = count + 1

        count = 0
        for obj in self.protein:
            print(count, '\t', self.protein[count])
            count = count + 1

        count = 0
        for obj in self.fruit:
            print(count, '\t', self.fruit[count])
            count = count + 1

        count = 0
        for obj in self.grain:
            print(count, '\t', self.grain[count])
            count = count + 1

    def clear(self):
        f = open("proteintable.txt", "w")
        f.close()

        f = open("dairytable.txt", "w")
        f.close()

        f = open("graintable.txt", "w")
        f.close()

        f = open("vegtable.txt", "w")
        f.close()

        f = open("fruittable.txt", "w")
        f.close()

    def getveg(self):
            return self.veg

    def getdairy(self):
        return self.dairy

    def getprotein(self):
        return self.protein

    def getfruit(self):
        return self.fruit

    def getgrain(self):
        return self.grain


#   test Code: (just proof of concept)
test = Dictionary()
test.display()
#   veg = test.getveg()
#   dairy = test.getdairy()
#   protein = test.getprotein()
#   grain = test.getgrain()
#   fruit = test.getfruit()
#   print(veg)
#   print(dairy)
#   print(protein)
#   print(grain)
#   print(fruit)
#   test.clear()


