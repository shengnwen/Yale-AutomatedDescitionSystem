__author__ = 'shengwen'


class option(object):
    """An option object

    Attributes:
        location: where you are building the factory.
        cost: construction costs.
        yearstocomplere: years to build factory
        discount: the interest rate for NPV calculation
        union: true or false
        costpercar: labor cost for this option
        revenuepercar: not including labor costs
        monthlyoutput: how many cars you build each month
        npv: the calculated net present value
    """

    def __init__(self, location, cost, yearstocomplete,
                lifetime, discount, union, costpercar,
                revenuepercar, monthlyoutput):
        """Return an option object
        with the given parameters initialized
        """
        self.location = location
        self.cost = cost
        self.yearstocomplete = yearstocomplete
        self.lifetime = lifetime
        self.discount = discount
        self.union = union
        self.costpercar = costpercar
        self.revenuepercar = revenuepercar
        self.monthlyoutput = monthlyoutput


    def __str__(self):
        return ("#<option location: " + self.location +
            " cost: " + str(self.cost) + ">")

    def get_location(self): return self.location
    def get_cost(self): return self.cost
    def get_yearstocomplete(self): return self.yearstocomplete
    def get_lifetime(self): return self.lifetime
    def get_discount(self): return self.discount
    def get_union(self): return self.union
    def get_costpercar(self): return self.costpercar
    def get_revenuepercar(self): return self.revenuepercar
    def get_monthlyoutput(self): return self.monthlyoutput

    def getInfo(self):
        return ("Option Info:[" +
                str(self.get_location()) + "," +
                str(self.get_cost()) + "," +
                str(self.get_yearstocomplete()) + "," +
                str(self.get_lifetime()) + "," +
                str(self.get_discount()) + "," +
                str(self.get_union()) + "," +
                str(self.get_costpercar()) + "," +
                str(self.get_revenuepercar()) + "," +
                str(self.get_monthlyoutput()) + "]")


class decision(object):
    """A decision object

    Attributes:
        options: a list of option object
        stakeholders: a list of stakeholder
        choice: the selected option
        explanation: the justification for the decision
    """

    def __init__(self, options, stakeholders):
        """Return a decision object
        with the given option list and stakeholder list
        """
        self.options = options
        self.stakeholders = stakeholders
        self.decision = None
        self.choice = None
        self.explanation = ""

    def __str__(self):
        return ("#<decision options: " + str(self.options) +
            " stakeholders: " + str(self.stakeholders) + ">")

    def get_options(self):
        return self.options

    def get_stakeholders(self):
        return self.stakeholders

    def generateChoice(self):
        self.choice = []
        for stakehd in self.stakeholders:
            if stakehd == 'stockholders':
                #find largest value
                self.choice.append(decide(self.options))
            elif stakehd == 'unions':
                # find one with union or with largest value
                bestVal = ""
                bestOption = ""
                for cur_option in self.options:
                    if cur_option.get_union() == False:
                        continue
                    option_npv = npv(cur_option)
                    if bestVal == "" or bestVal < option_npv:
                        bestVal = option_npv
                        bestOption = cur_option
                if bestVal == "" or bestVal < 0:
                    self.choice.append(decide(self.options))
                else:
                    self.choice.append(bestOption)
            elif stakehd == 'OH':
                bestVal = ""
                bestOption = ""
                for cur_option in self.options:
                    if cur_option.get_location() != 'OH':
                        continue
                    option_npv = npv(cur_option)
                    if bestVal == "" or bestVal < option_npv:
                        bestVal = option_npv
                        bestOption = cur_option
                if bestVal == "" or bestVal < 0:
                    self.choice.append(decide(self.options))
                else:
                    self.choice.append(bestOption)
            else:
                bestVal = ""
                bestOption = ""
                for cur_option in self.options:
                    if cur_option.get_location() != 'SC':
                        continue
                    option_npv = npv(cur_option)
                    if bestVal == "" or bestVal < option_npv:
                        bestVal = option_npv
                        bestOption = cur_option
                if bestVal == "" or bestVal < 0:
                    self.choice.append(decide(self.options))
                else:
                    self.choice.append(bestOption)

    def get_explanation(self):
        self.explanation = ""
        if len(self.stakeholders) == 0:
            self.choice = decide(self.options)
            self.explanation = "There are no potential stakeholders, so we choose the direct highest option: " \
                               + self.choice.getInfo() + " \nNPV" + str(self.choice)
        i = 0
        while i < len(self.stakeholders):
            the_explation = "Dear " + self.stakeholders[i] +", we choose the best option for you: " + self.choice[i].getInfo() + "\n"
            if self.stakeholders[i] == 'stockholders':
                the_explation += "For your best interest, this option has the highest NPV value!\n"
            elif self.stakeholders[i] == 'unions':
                the_explation += "We try to find the highest option with union member for you!\n"
                if self.choice[i].get_union() == False:
                    the_explation += "However among all the options, there are no one with union members. So we choose the" \
                                     "highest interests option for you! \n"
            elif self.stakeholders[i] == 'OH':
                the_explation += "We try to find the highest option inside OH !\n"
                if self.choice[i].get_location() != "OH":
                    the_explation += "However among all the options, there are no one inside OH. So we choose the" \
                                     "highest interests option for you! \n"
            elif self.stakeholders[i] == 'SC':
                the_explation += "We try to find the highest option inside SC !\n"
                if self.choice[i].get_location() != "SC":
                    the_explation += "However among all the options, there are no one inside SC. So we choose the" \
                                     "highest interests option for you! \n"
            the_explation + "\n"
            self.explanation += the_explation
            i = i + 1
        return self.explanation






def npv(this_option):
    q = 1 / (this_option.get_discount() + 1)
    #print("q:" + str(q))
    constructYear = this_option.get_yearstocomplete()
    #print("year" + str(constructYear))
    constructionCost = (this_option.get_cost() / constructYear) * q * (1 - pow(q, constructYear)) / (1 - q)
    #print("constructionCost:%f"%constructionCost)
    profitYear = this_option.get_lifetime() - constructYear
    profitAnual = (this_option.get_revenuepercar() - this_option.get_costpercar()) * this_option.get_monthlyoutput() * 12
    profitTotal = profitAnual * pow(q, constructYear) * q * (1 - pow(q, profitYear))/ (1 - q)
    #print("profitCost: %f" %profitTotal)
    return profitTotal - constructionCost


def decide(option_list):
    # use npv to calculate
    # return best option
    bestVal = ""
    bestOption = ""
    for cur_option in option_list:
        option_npv = npv(cur_option)
        #print(cur_option.getInfo() + ":" + str(option_npv))
        if bestVal == "" or bestVal < option_npv:
            bestVal = option_npv
            bestOption = cur_option
    if bestVal=="" or bestVal < 0:
        #print("no positive option exist!")
        return None
    else:
        return bestOption

def sensitivity(option_list):
    if len(option_list) == 0:
        return None
    generatedOptions = []
    optionScore = []
    optionWeight = [0.08, 0.12, 0.10, 0.10, 0.09, 0.11, 0.10, 0.10, 0.12, 0.08]
    for cur_option in option_list:
        score = 0
        # low cost * weight 0.08

        lowCostOption = option(cur_option.get_location(), cur_option.get_cost() * 0.8, cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar(),
                                       cur_option.get_monthlyoutput())
        score += npv(lowCostOption) * optionWeight[0]
        generatedOptions.append(lowCostOption)
        # hight cost weight 0.12
        highCostOption = option(cur_option.get_location(), cur_option.get_cost() * 1.2, cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar(),
                                       cur_option.get_monthlyoutput())
        score += npv(highCostOption) * optionWeight[1]
        generatedOptions.append(highCostOption)

        # low discount 0.10
        lowDiscountOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount()*0.8, cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar(),
                                       cur_option.get_monthlyoutput())
        score += npv(lowDiscountOption) * optionWeight[2]
        generatedOptions.append(lowDiscountOption)

        # high discount 0.10
        highDiscountOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount()*1.2, cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar(),
                                    cur_option.get_monthlyoutput())
        score += npv(highDiscountOption) * optionWeight[3]
        generatedOptions.append(highDiscountOption)

        # low cost per car 0.09
        lowCostPerCarOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar() * 0.8, cur_option.get_revenuepercar(),
                                       cur_option.get_monthlyoutput())
        score += npv(lowCostPerCarOption) * optionWeight[4]
        generatedOptions.append(lowCostPerCarOption)
        # high cost per car 0.11
        highCostPerCarOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar() * 1.2, cur_option.get_revenuepercar(),
                                       cur_option.get_monthlyoutput())
        score += npv(highCostPerCarOption) * optionWeight[5]
        generatedOptions.append(highCostPerCarOption)
        # low revenue per car 0.10
        lowRevenueOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar() * 0.8,
                                       cur_option.get_monthlyoutput())
        score += npv(lowRevenueOption) * optionWeight[6]
        generatedOptions.append(lowRevenueOption)
        # high revenue per car 0.10
        highRevenueOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar() * 1.2,
                                       cur_option.get_monthlyoutput())
        score += npv(highRevenueOption) * optionWeight[7]
        generatedOptions.append(highRevenueOption)
        # low monthly output 0.12
        lowOutputOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar(),
                                       cur_option.get_monthlyoutput() * 0.8)
        score += npv(lowOutputOption) * optionWeight[8]
        generatedOptions.append(lowOutputOption)
        # high monthly output 0.08
        highOutputOption = option(cur_option.get_location(), cur_option.get_cost(), cur_option.get_yearstocomplete(),
                                       cur_option.get_lifetime(), cur_option.get_discount(), cur_option.get_union(),
                                       cur_option.get_costpercar(), cur_option.get_revenuepercar(),
                                       cur_option.get_monthlyoutput() * 1.2)
        score += npv(highOutputOption) * optionWeight[9]
        generatedOptions.append(highOutputOption)
        optionScore.append(score)
    i = 0
    bestOption = 0
    bestScore = optionScore[0]
    while(i < len(optionScore)):
        #print("option:" + str(i) + ":" + str(optionScore[i]))
        if bestScore < optionScore[i]:
            bestScore = optionScore[i]
            bestOption = i
        i = i + 1
    return option_list[bestOption]
    #return decide(generatedOptions)

def explain(option_list, stakeholder_list = ""):
    des = decision(option_list, stakeholder_list)
    des.generateChoice()
    return des


# for test npv
# optOH = option("OH", 40000000, 2, 12, .05, True, 6500,
#                     10000, 1000)
# optSC = option("SC", 20000000, 2, 10, .05, False, 4000,
#                     10000, 500)
# print (str(optOH) + optOH.getInfo())
# print (str(optSC) + optSC.getInfo())
#
# s = ["stockholders", "unions", "OH", "SC"]
# opt = [optOH, optSC]
# d = decision(opt, s)
# print(d)
#
# print ("npv:%f", npv(optOH))
# print ("npv:%f", npv(optSC))
# print(decide(opt))
# best = sensitivity(opt)
# print("\n" + best.getInfo() + ":" + str(npv(best)))
# print(explain(opt, s).get_explanation())



