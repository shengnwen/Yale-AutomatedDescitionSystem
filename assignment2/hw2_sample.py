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
        
    def __str__(self):
        return ("#<decision options: " + str(self.options) + 
            " stakeholders: " + str(self.stakeholders) + ">")
        
    def get_options(self):
        return self.options
    
    def get_stakeholders(self):
        return self.stakeholders
    
    
optOH = option("OH", 40000000, 2, 12, .05, True, 6500,
                    10000, 1000)
optSC = option("SC", 20000000, 2, 10, .05, True, 4000,
                    10000, 500)
print (optOH)
print (optSC)

s = ["stockholders", "unions", "OH", "SC"]
opt = [optOH, optSC]
d = decision(opt, s)
print(d)

    
