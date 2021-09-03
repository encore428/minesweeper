import random
import math
from functools import reduce


# this method of definition serves these purposes:
# 1. when I have a flag value, I can validated it against this with val in flag_symbols
# 2. I can translate flag values into symbols and descriptions
# 3. description is a useful form of documentaion describing the meansing of flag value
# However, if I want to compare a flag value again something, I have two choices:
# 1. if flag == 3, versus
# 2. if flag_symbols[flag][1] == 'implied mine'
# The second method is more descriptive, but a typo can really ruin the program
# but if description is swapped with index, we can partially overcome the
# typo issue with if flag == flag_symbols['implied mine'][1]
# Partially because the code if not executed may not reveal the mistake.
# However, i do not know how to achieve the original purpose 1 of validating
# a value.
flag_symbols = {
    0: [' ', 'none'],
    1: ['c', 'confirmed'],
    2: ['p', 'proposed'],
    3: ['m', 'implied mine'],
    4: ['s', 'implied safe']
}


class Slate:
    def __init__(self, idx, tools):
        self.__idx = idx        # This is needed for debug tracing
        self.__mined = False    # True if slate has a mine
        self.__exposed = False  # True if slate has been uncovered
        self.__intel = 0  # number of mines in the neighborhood
        self.__flag = 0  # 0=no flag, 1=Confirmed flag, 2=Proposed flag, 3=Implied mine, 4=Implied safe
        self.__neighborhood = []  # points to neighborhood Slates
        self.__tools  = tools # this is propagated from the Canvas and duplicated in all slates on the Canvas
                              # this is for use by the method intelViolated()

    @property
    def idx(self):
        return self.__idx

    @property
    def mined(self):
        if self.exposed:
            return self.__mined

    def plant_mine(self, cap):
        # Plant a mine into sub-neighbor of this slate.
        # The game is designed to hide the location of the mines.
        # This mothod is called from Canvas class which nominats a slate.
        # To ensure secrecy, this method will pick one of its neighbors
        # to plant the mine.
        # To further ensure secrecy, this process of finding a random neighbor
        # is repeated a random number of time to ensure Canvas class has no
        # clue of knowing where the mine is planted.
        sub_neighbor_steps = random.randint(0,int(math.sqrt(cap))) + 3
        curSlate = self
        for i in range(sub_neighbor_steps):
            curSlate = curSlate.neighborhood[random.randint(0,len(curSlate.neighborhood)-1)]
        while curSlate.__mined:
            curSlate = curSlate.neighborhood[random.randint(0,len(curSlate.neighborhood)-1)]
        curSlate.__mined = True
        for each_slate in curSlate.neighborhood:
            each_slate.intelInc()

    @property
    def exposed(self):
        return self.__exposed

    @property
    def intel(self):
        if self.exposed:
            return self.__intel

    def intelInc(self):
        self.__intel = self.__intel + 1

    @property
    def flag(self):
        return self.__flag

    @flag.setter
    def flag(self, val):
        if isinstance(val, int) and (val in flag_symbols):
            if not self.exposed:
                self.__flag = val

    @property
    def flagCIntel(self):
        return sum(map(lambda slate: flag_symbols[slate.flag][1]=='confirmed', self.neighborhood))

    @property
    def flagPIntel(self):
        return sum(map(lambda slate: flag_symbols[slate.flag][1]=='proposed', self.neighborhood))

    @property
    def flagMIntel(self):
        return sum(map(lambda slate: flag_symbols[slate.flag][1]=='implied mine', self.neighborhood))

    @property
    def flagSIntel(self):
        return sum(map(lambda slate: flag_symbols[slate.flag][1]=='implied safe', self.neighborhood))

    @property
    def unexposedIntel(self):
        return sum(map(lambda slate: not slate.exposed, self.neighborhood))


    @property
    def tools(self):
        return self.__tools

    @property
    def intelViolated(self):
        ## True if flags around this slate violates its intel
        if self.tools != 2:
            # if game is not played under assisted mode, always not violated
            return False
        pass
        if not self.exposed:
            # if slate is not exposed, no violation can be detected
            return False
        pass
        if self.unexposedIntel == 0:
            # if all slates in the neighborhood are exposed, there can be no violation
            return False
        pass
        # count flags in the neighborhood that suggest mines. If that count exceeds intel, this is violation
        countMinedFlag = 0
        for slate in self.neighborhood:
            if (flag_symbols[slate.flag][1] == 'confirmed') or (flag_symbols[slate.flag][1] == 'proposed') or (flag_symbols[slate.flag][1] == 'implied mine'):
                countMinedFlag = countMinedFlag + 1
        if countMinedFlag > self.intel:
            return True
        pass
        # count flags in the neighborhood that suggest safe. If that leaves insufficient slates to meet intel, this is violation
        countMinedFlag = self.unexposedIntel
        for slate in self.neighborhood:
            if  flag_symbols[slate.flag][1] == 'implied safe':
                countMinedFlag = countMinedFlag - 1
        if countMinedFlag < self.intel:
            return True
        pass
        return False

    @property
    def slateSymbol(self):
        # translate slate properties into char symbol for display on canvas
        if self.exposed:
            if self.mined:
                return '*', 'bomb'
            if self.intelViolated:
                return chr(64+self.intel), f"err{str(self.intel)}"
            else:
                return chr(48+self.intel), f"intel{str(self.intel)}"
        else:
            return flag_symbols[self.flag]
        return " ", "undefined"


    def addNeighbor(self, another_slate):
        self.__neighborhood.append(another_slate)

    @property
    def neighborhood(self):
        return self.__neighborhood

    def __str__(self):
        result = f"Slate[{self.__idx}] is {' exposed' if self.exposed else 'unexposed'}, "
        if self.exposed:
            result = result + f" and {'mined' if self.mined else 'safe'} and Intel is {self.Intel}; "
        result = result + f"has {flag_symbols[self.flag][1] + ' flag; ' if self.flag!=0 else ''}"
        result = result + f"{self.unexposedIntel} unexposed slates and {self.flagCIntel} {flag_symbols[1][1]} flags in the neighborhood."
        return result

    ## to clear flag on this unexposed slate
    def flagClear(self):
        ## return True if there is changes, False if none
        if self.exposed:
            return False
        if self.flag == 0:
            return False
        flagWas = self.flag
        print(f"    clear flag({flagWas}) at slate[{self.__idx}]")
        self.flag = 0;
        return True

    def flagImpliedMine(self):
        ## return True if there is changes, False if none
        if self.exposed:
            return False
        # already the right flag, do nothing
        if flag_symbols[self.flag][1] == 'implied mine':
            return False
        if self.flag != 0:
            return False
        print(f"    plant Implied mine flag at slate[{self.__idx}]")
        self.flag = 3  # Implied mine flag
        return True

    def flagImpliedSafe(self):
        ## return True if there is changes, False if none
        if self.exposed:
            return False
        # already the right flag, do nothing
        if flag_symbols[self.flag][1] == 'implied safe':
            return False
        if self.flag != 0:
            return False
        print(f"    plant Implied safe flag at slate[{self.__idx}]")
        self.flag = 4  # Implied safe flag
        return True

    ## to plant a propose flag on this unexposed slate
    ## return True if there is changes, False if none
    def flagPropose(self):
        if self.exposed:
            ## flag is not applicable to exposed slates
            return False
        # already a Propose flag, no need to do anything
        if flag_symbols[self.flag][1] == 'proposed':
            return False
        if self.flag != 0:
            self.flagClear()
        print(f"    plant Propose flag at slate[{self.__idx}]")
        self.flag = 2  # Proposed flag
        return True

    ## to plant a confirm flag on this unexposed slate
    ## return True if there is changes, False if none
    def flagConfirm(self):
        ## return True if there is changes, False if none
        if self.exposed:
            return False
        # already a Confirm flag, no need to do anything
        if flag_symbols[self.flag][1] == 'confirmed':
            return False
        if self.flag != 0:
            self.flagClear()
        self.flag = 1  # Confirmed flag
        return True

    def seek2Confirm(self):
        # plant Confirm flags around an exposed slate
        # if neighborhood unexposed slates match intel
        if (not self.exposed) or (self.intel == 0):
            return False
        if self.unexposedIntel == self.intel:
            for neighbor in self.neighborhood:
                if not neighbor.exposed and flag_symbols[neighbor.flag][1] != 'confirmed':
                    print(f"    plant Confirm flag at slate[{neighbor.__idx}] because slate[{self.__idx}]intel=neighborhood unexposed slates")
                    neighbor.flagConfirm()
            return True
        return False


    ## If player Cracked a mined slate, all slates are checked and the mine if present will go ogg
    def lit(self):
        if self.__mined:
            self.__exposed = True

    ## For unexposed slates, player can tap to crack it open.  Each cracking tap is handled by this method
    ## the method returns true if a mine has gone off
    def crack(self):
        # For slate already exposed, if the neighborhood has confirmed flag count matching the intel,
        # the method will craking open all unexposed slates in the neighborhood that has no confirmed flag.
        # If the confirmed flag has been planted incorrectly, this will cause a hidden mine to go off
        if self.exposed:
            exploded = False
            if self.flagCIntel == self.intel:
                for neighbor in self.neighborhood:
                    if (not neighbor.exposed) and (flag_symbols[neighbor.flag][1] != 'confirmed'):
                        exploded = exploded or neighbor.crack()
            return exploded
        pass
        # cracking open a Slate with confirmed flag is not allowed
        if flag_symbols[self.flag][1] == 'confirmed':
            return False
        pass
        # if the Slate has a flag, clear it first
        if self.flag != 0:
            self.flagClear()
        pass
        # now expose this Slate
        self.__exposed = True
        # if this Slate has a mine, it explodes and game is over
        if self.mined:
            return True
        pass
        # now that this Slate is exposed, if its intel is = 0, all its neigborhood slates can be cracked open
        if self.intel == 0:
            for neighbor in self.neighborhood:
                if not neighbor.exposed:
                    print(f"    Crack slate[{neighbor.__idx}] because slate[{self.__idx}]intel=0")
                    neighbor.crack()
        # That's all for opening the Slate
        if self.tools != 2:
            return False
        pass
        ### The following is for games in Auto mode
        # Check if neighborhood unexposed Slates count matches Intel, and
        # flag all exposed slate with Confirm flag
        self.seek2Confirm()
        # For each Slate in the neighborhood
        # Check if its neighborhood unexposed Slates count matches Intel, and
        # flag all exposed slate with Confirm flag
        for neighbor in self.neighborhood:
            neighbor.seek2Confirm()
        # Check if neighborhood Confirmed flag count matches Intel,
        # and crack open all unflagged slates
        if (self.intel > 0) and (self.intel == self.flagCIntel):
            for neighbor in self.neighborhood:
                if (not neighbor.exposed) and (flag_symbols[neighbor.flag][1] != 'confirmed'):
                    print(f"    Crack neighbor slate[{neighbor.__idx}] because slate[{self.__idx}] flag count = Intel")
                    neighbor.crack()
        # Repeat for each neighborhood Slate
        for neighbor in self.neighborhood:
            if (neighbor.exposed) and (neighbor.intel > 0) and (neighbor.intel == neighbor.flagCIntel):
                for sub_neighbor in neighbor.neighborhood:
                    if (not sub_neighbor.exposed) and (flag_symbols[sub_neighbor.flag][1] != 'confirmed'):
                        print(f"    Crack sub-neighborSlate[{sub_neighbor.__idx}] of slate[{neighbor.__idx}] with flag count = intel")
                        sub_neighbor.crack()
        return False


    ## For unexposed slates, player can tap to alter the flag on it.  Each tap is handled by this method
    ## the alteration goes in cycles depending on the mode of the game
    def cycleFlag(self):
        # slate already exposed, flagging is not applicable
        if self.exposed:
            return False
        # cracking open a Slate with confirmed flag is not allowed
        flagWas = self.flag
        if self.tools == 0:
            ## for Basic mode. the flag toggles between none and confirmed
            if flagWas == 0:
                return self.flagConfirm()
            else:
                return self.flagClear()
        elif self.tools == 1:
            ## for Assisted mode. the flag cycles from none to confirmed to proposed and back to none
            if flagWas == 0:
                return self.flagConfirm()
            elif flag_symbols[flagWas][1] == 'confirmed':
                return self.flagPropose()
            else:
                return self.flagClear()
        elif self.tools == 2:
            ## for Auto mode. the flag cycles toggles between none and proposed
            if (flagWas == 0) or (flag_symbols[flagWas][1] == 'implied mine') or (flag_symbols[flagWas][1] == 'implied safe'):
                ## for the purpose of flag alternation, implied flag is treated same as none
                return self.flagPropose()
            elif flag_symbols[flagWas][1] == 'confirmed':
                ## confirmed flag cannot be altered
                return False
            elif flag_symbols[flagWas][1] == 'proposed':
                ## proposed flag can be toggled to none
                return self.flagClear()
            else:
                return False
        else:
            return False

        ## end
