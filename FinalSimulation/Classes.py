class InteractionGroup:

    def __init__(self, group, baseInteractions = 4):
        self.group = group

        if group == 1:
            self.interactions = baseInteractions
        elif group == 2:
            self.iteractions = baseInteractions * 2
        elif group == 3:
            self.iteractions = baseInteractions * 4
        else:
            raise ValueError("Group number can be 1, 2 or 3. Nothing else!")

class Person:

    def __init__(self, interactionGroup: InteractionGroup, age: int, isVaccinated = False):
        self.interactionGroup = interactionGroup
        self.age = age
        self.isVaccinated = isVaccinated
        self.isInfected = False
        self.recovered = False

    def getNumberOfInteractions(self):
        return self.InteractionGroup.interactions
    
    def returnAge(self):
        return self.age
    
    def setVaccination(self):
        self.isVaccinated = True

    def getIsVaccinated(self):
        return self.isVaccinated
    
    def setInfected(self):
        self.isInfected = True

    def setRecovered(self):
        self.isInfected = False
        self.recovered = True

    def getInfected(self):
        return self.isInfected

    def getRecovered(self):
        return self.recovered