"""
Program description:
This program should calculate the total take home salary given
certain parameters about the employee. 
The calculation methods should be in class form so an object
can be created for each employee

INPUTS:
✓ Name or id - str
✓ Base Salary - float
✓ Tax Free Income - float
Pension contribution - float
Salary sacrifice - pct/float
Year - int
Tax Free Allowance - float, default set by year lookup
Other expenses pre tax - float
Other expenses post tax - float
Days holiday - float

OUTPUTS/ACCESSIBLE METHODS:
✓ Gross annual income - float
✓ PAYE paid - float
✓ NI paid - float
Pension deducted - float
Gross deductions - float
Net take home year - float
Net take home month - float
Net take home day - float
Net take home hour - float

"""


pensionBands = {
    '2021-2022':{
        'lower_level': 6240.0,
        'higher_level': 50270.0
    },
    '2020-2021':{
        'lower_level': 6240.0,
        'higher_level': 50000.0
    },
    '2019-2020':{
        'lower_level': 6136.0,
        'higher_level': 50000.0
    },
    '2018-2019':{
        'lower_level': 6032.0,
        'higher_level': 46350.0
    },
}


taxRates = {
    '2021-2022':{
        'PAYE_rate1':{
            'threshold': 12579.0,
            'rate_pct': 20.0
        },
        'PAYE_rate2':{
            'threshold': 50279.0,
            'rate_pct': 40.0,
        },
        'PAYE_rate3':{
            'threshold': 150000.0,
            'rate_pct': 45.0
        },
        'NI_rate1':{
            'threshold': 9568.0,
            'rate_pct': 12.0
        },
        'NI_rate2':{
            'threshold': 50270.0,
            'rate_pct': 2.0
        },
    },
    '2020-2021':{
        'PAYE_rate1':{
            'threshold': 12500.0,
            'rate_pct': 20.0
        },
        'PAYE_rate2':{
            'threshold': 50000.0,
            'rate_pct': 40.0,
        },
        'PAYE_rate3':{
            'threshold': 150000.0,
            'rate_pct': 45.0
        },
        'NI_rate1':{
            'threshold': 9500.0,
            'rate_pct': 12.0
        },
        'NI_rate2':{
            'threshold': 50000.0,
            'rate_pct': 2.0
        },
    },
    '2019-2020':{
        'PAYE_rate1':{
            'threshold': 12500.0,
            'rate_pct': 20.0 
        },
        'PAYE_rate2':{
            'threshold': 50000.0,
            'rate_pct': 40.0,
        },
        'PAYE_rate3':{
            'threshold': 150000.0,
            'rate_pct': 45.0
        },
        'NI_rate1':{
            'threshold': 8632.0,
            'rate_pct': 12.0
        },
        'NI_rate2':{
            'threshold': round(4167.0 * 12, 2),
            'rate_pct': 2.0
        },
    },
    '2018-2019':{
        'PAYE_rate1':{
            'threshold': 11850.0,
            'rate_pct': 20.0
        },
        'PAYE_rate2':{
            'threshold': 46350.0,
            'rate_pct': 40.0,
        },
        'PAYE_rate3':{
            'threshold': 150000.0,
            'rate_pct': 45.0
        },
        'NI_rate1':{
            'threshold': 8424.0,
            'rate_pct': 12.0
        },
        'NI_rate2':{
            'threshold': round(3863.0 * 12, 2),
            'rate_pct': 2.0
        },
    },
}


def isFloatValid(value):
        """
        Check value is float and positive
        """
        try:
            value * 1.0 # check input is a value

            if value < 0: # check input is positive
                return False

        except TypeError:
            return False

        return True


class FloatSuccessType:
    def __init__(self, value, status, message=''):
        self.value = round(value, 2)
        self.status = status
        self.message = message
    
    def __str__(self):
        if self.status:
            return f'{self.value}'
        else:
            if self.message == '':
                return f'Value error: {self.value} with no message'
            else:
                return f'Value error: {self.value}, {self.message}'
    
    def __repr__(self):
        if self.status:
            return f'{self.value}'
        else:
            if self.message == '':
                return f'Value error: {self.value} with no message'
            else:
                return f'Value error: {self.value}, {self.message}'


class taxRateBandType:
    def __init__(self, threshold, rate_pct):
        self.threshold = threshold
        self.rate_pct = rate_pct


class EmployeeSalaryInfo(object):
    """An object containing salary information for an employee"""
    def __init__(self, employee_name):
        self.employee_name = employee_name
        self.resetTaxableIncome()
        self.resetNonTaxableIncome()
        self.resetPreTaxExpense()
        self.resetPostTaxExpense()
    
    def resetTaxableIncome(self):
        """Clears taxable income list"""
        self.incomeTaxable = 0.0
        return True
    
    def resetNonTaxableIncome(self):
        """Clears non-taxable income list"""
        self.incomeNonTaxable = 0.0
        return True
    
    def resetPreTaxExpense(self):
        """Clears pre tax expense list"""
        self.expensePreTax = 0.0
        return True
    
    def resetPostTaxExpense(self):
        """Clears pre tax expense list"""
        self.expensePostTax = 0.0
        return True

    def addTaxableIncome(self, incomeList):
        """Define the taxable income for the employee"""
        for input in incomeList:

            if isFloatValid(input):
                self.incomeTaxable += input
            else:
                return False
        
        return True

    def addNonTaxableIncome(self, incomeList):
        """Define the non-taxable income for the employee"""
        for input in incomeList:

            if isFloatValid(input):
                self.incomeNonTaxable += input
            else:
                return False
        
        return True
    
    def addPreTaxExpense(self, expenseList):
        """Define pre tax expense i.e. reduces gross income"""
        expense = 0.0

        for input in expenseList:
        
            if isFloatValid(input):
                expense += input
            else:
                return False

        if expense < self.incomeTaxable:
            self.expensePreTax = expense
            return True
        else:
            return False

    def addPostTaxExpense(self, expenseList):
        """Define post tax expense i.e. reduces net income"""
        for input in expenseList:

            if isFloatValid(input):
                self.expensePostTax += input
            else:
                return False
        
        return True

    def getGrossIncome(self):
        """Returns gross income with success flag at .value and .status"""
        grossIncome = 0.0

        if isFloatValid(self.incomeTaxable) and \
            isFloatValid(self.incomeNonTaxable):
            grossIncome = self.incomeTaxable + self.incomeNonTaxable
        else:
            return FloatSuccessType(0.0, False, "Value not valid")
        
        return FloatSuccessType(grossIncome, True)
    
    def getPAYEPaid(self, year):
        """Return PAYE paid"""
        taxPaid = 0.0
        incomeTaxable = 0.0

        if isFloatValid(self.incomeTaxable) and \
            isFloatValid(self.expensePreTax) and \
                self.incomeTaxable > self.expensePreTax:
            incomeTaxable = self.incomeTaxable - self.expensePreTax
        else:
            return FloatSuccessType(0.0, False, "Taxable income invalid")

        try:
            rate1 = taxRateBandType(
                taxRates[year]['PAYE_rate1']['threshold'],
                taxRates[year]['PAYE_rate1']['rate_pct'],
            )
            rate2 = taxRateBandType(
                taxRates[year]['PAYE_rate2']['threshold'],
                taxRates[year]['PAYE_rate2']['rate_pct'],
            )
            rate3 = taxRateBandType(
                taxRates[year]['PAYE_rate3']['threshold'],
                taxRates[year]['PAYE_rate3']['rate_pct'],
            )

        except KeyError:
            return FloatSuccessType(0.0, False, "Year not valid")

        if incomeTaxable <= rate1.threshold:
            taxPaid = 0.0
        elif incomeTaxable <= rate2.threshold:
            taxPaid = (incomeTaxable - rate1.threshold) * (rate1.rate_pct/100)
        elif incomeTaxable <= rate3.threshold:
            taxPaid = (rate2.threshold - rate1.threshold) * (rate1.rate_pct/100) \
                      + (incomeTaxable - rate2.threshold) * (rate2.rate_pct/100)
        else:
            taxPaid = (rate2.threshold - rate1.threshold) * (rate1.rate_pct/100) \
                      + (rate3.threshold - rate2.threshold) * (rate2.rate_pct/100) \
                      + (incomeTaxable - rate3.threshold) * (rate3.rate_pct/100)

        taxPaid = round(taxPaid, 2)

        return FloatSuccessType(taxPaid, True)
    
    def getNIPaid(self, year):
        """Return NI paid"""
        taxPaid = 0.0
        incomeTaxable = 0.0

        if isFloatValid(self.incomeTaxable) and \
            isFloatValid(self.expensePreTax) and \
                self.incomeTaxable > self.expensePreTax:
            incomeTaxable = self.incomeTaxable - self.expensePreTax
        else:
            return FloatSuccessType(0.0, False, "Taxable income invalid")

        try:
            rate1 = taxRateBandType(
                taxRates[year]['NI_rate1']['threshold'],
                taxRates[year]['NI_rate1']['rate_pct'],
            )
            rate2 = taxRateBandType(
                taxRates[year]['NI_rate2']['threshold'],
                taxRates[year]['NI_rate2']['rate_pct'],
            )

        except KeyError:
            return FloatSuccessType(0.0, False, "Year not valid")

        if incomeTaxable <= rate1.threshold:
            taxPaid = 0.0
        elif incomeTaxable <= rate2.threshold:
            taxPaid = (incomeTaxable - rate1.threshold) * (rate1.rate_pct/100)
        else:
            taxPaid = (rate2.threshold - rate1.threshold) * (rate1.rate_pct/100) \
                      + (incomeTaxable - rate2.threshold) * (rate2.rate_pct/100)

        taxPaid = round(taxPaid, 2)

        return FloatSuccessType(taxPaid, True)
    
    def addPension(self, year, percentage, pre_tax=False, post_tax=False):
        """Adds pension to expenses"""
        pension = 0.0

        if post_tax == pre_tax:
            return FloatSuccessType(
                0.0, 
                False, 
                "Pension must be either pre OR post tax"
            )
        
        if not (percentage >= 0 and percentage <= 100):
            return FloatSuccessType(
                0.0,
                False,
                "Percentage must be within 0 - 100 range"
            )
        
        try:
            upper_band = pensionBands[year]['higher_level']
            lower_band = pensionBands[year]['lower_level']

        except KeyError:
            return FloatSuccessType(0.0, False, "Year not valid")

        if isFloatValid(self.incomeTaxable):
            incomeTaxable = self.incomeTaxable
        else:
            return FloatSuccessType(0.0, False, "Taxable income invalid")
        
        if incomeTaxable <= lower_band:
            pensionable_earnings = 0.0
        elif incomeTaxable <= upper_band:
            pensionable_earnings = incomeTaxable - lower_band
        else:
            pensionable_earnings = upper_band - lower_band
        pension = pensionable_earnings * (percentage/100)

        if post_tax:
            pension *= 0.8
            self.addPostTaxExpense([pension])
        else:
            self.addPreTaxExpense([pension])

        return FloatSuccessType(pension, True)

    def getDeductions(self, year):
        """Return total deductions from incomes"""
        getPAYEPaid = self.getPAYEPaid(year)
        if getPAYEPaid.status:
           payePaid = getPAYEPaid.value 
        else:
            return FloatSuccessType(0.0, False, getPAYEPaid.message)
        
        getNIPaid = self.getNIPaid(year)
        if getNIPaid.status:
           niPaid = getNIPaid.value 
        else:
            return FloatSuccessType(0.0, False, getNIPaid.message)
        
        if isFloatValid(self.expensePostTax):
            expensePostTax = self.expensePostTax
        else:
            return FloatSuccessType(0.0, False, 'Post tax expenses invalid')
        
        if isFloatValid(self.expensePreTax):
            expensePreTax = self.expensePreTax
        else:
            return FloatSuccessType(0.0, False, 'Pre tax expenses invalid')
        
        deductions = payePaid + niPaid + expensePostTax + expensePreTax

        return FloatSuccessType(deductions, True)

    def getNetIncome(self, year):
        """Return annual take home pay"""
        income = self.getGrossIncome()
        deductions = self.getDeductions(year)

        if not income.status:
            return FloatSuccessType(
                0.0,
                False,
                income.message
            )
        if not deductions.status:
            return FloatSuccessType(
                0.0,
                False,
                deductions.message
            )
        
        return FloatSuccessType(income.value - deductions.value, True)