from unittest import TestCase

from income_calculator import EmployeeSalaryInfo, FloatSuccessType


class ClassTypesTests(TestCase):
    """Class to test custom types used"""
    def test_FloatSuccessType_Print_Value(self):
        """Test __str__ element of FloatSuccessType"""
        t = FloatSuccessType(123, True)
        self.assertEqual(
            t.__str__(),
            "123",
            msg="__str__ method returned incorrect value with "\
                "success = True"
        )

        t = FloatSuccessType(123, False)
        self.assertEqual(
            t.__str__(),
            "Value error: 123 with no message",
            msg="__str__ method returned incorrect value with "\
                "success = False"
        )

        t = FloatSuccessType(123, False, 'error message')
        self.assertEqual(
            t.__str__(),
            "Value error: 123, error message",
            msg="__str__ method returned incorrect value with "\
                "success = False + message"
        )

    def test_FloatSuccessType_Repr_Value(self):
        """Test __repr__ element of FloatSuccessType"""
        t = FloatSuccessType(123, True)
        self.assertEqual(
            t.__repr__(),
            "123",
            msg="__repr__ method returned incorrect value with "\
                "success = True"
        )

        t = FloatSuccessType(123, False)
        self.assertEqual(
            t.__repr__(),
            "Value error: 123 with no message",
            msg="__repr__ method returned incorrect value with "\
                "success = False"
        )

        t = FloatSuccessType(123, False, 'error message')
        self.assertEqual(
            t.__repr__(),
            "Value error: 123, error message",
            msg="__repr__ method returned incorrect value with "\
                "success = False"
        )


class ClassInitialisationTests(TestCase):
    """Class to test initialisation of employee class"""
    def test_gross_income_initialisation_no_income(self):
        """Test gross income value with no income defined"""
        e = EmployeeSalaryInfo("testname")
        grossIncome = e.getGrossIncome()
        self.assertTrue(
            grossIncome.status,
            msg="Method status did not return True"
        )
        self.assertEqual(
            grossIncome.value,
            0.0,
            msg="Gross income value should be 0.0 when no income defined"
        )

    def test_taxable_income_initialisation(self):
        """Test various initialisations of taxable income"""
        e = EmployeeSalaryInfo("testname")
        self.assertFalse(
            e.addTaxableIncome([123, 168, "string"]),
            msg="String taxable income was incorrectly added"
        )
        e.resetTaxableIncome()
        self.assertEqual(
            e.getGrossIncome().value,
            0.0,
            msg="Taxable income list not reset to 0.0"
        )

        self.assertFalse(
            e.addTaxableIncome([123, 168687, -4332]),
            msg="Negative taxable income was incorrectly added"
        )
        e.resetTaxableIncome()

        self.assertTrue(
            e.addTaxableIncome([27000, 15000]),
            msg="Taxable income with ok input returned false"
        )
        e.resetTaxableIncome()
    
    def test_non_taxable_income_initialisation(self):
        """Test various initialisations of non_taxable income"""
        e = EmployeeSalaryInfo("testname")
        self.assertFalse(
            e.addNonTaxableIncome([123, 168, "string"]),
            msg="String non-taxable income was incorrectly added"
        )
        e.resetNonTaxableIncome()
        self.assertEqual(
            e.getGrossIncome().value,
            0.0,
            msg="Non-taxable income list not reset to 0.0"
        )

        self.assertFalse(
            e.addNonTaxableIncome([123, 168687, -4332]),
            msg="Negative non-taxable income was incorrectly added"
        )
        e.resetNonTaxableIncome()

        self.assertTrue(
            e.addNonTaxableIncome([27000, 15000]),
            msg="Non-taxable income with ok input returned false"
        )
        e.resetNonTaxableIncome()


class GrossIncomeUnitTests(TestCase):
    """Class to test calculation methods of gross income method"""    
    def test_gross_income_return_valid(self):
        """Test gross income returned correctly"""
        e = EmployeeSalaryInfo("testname")
        incomeTaxable = 27000
        incomeNonTaxable = 3000
        self.assertTrue(
            e.addTaxableIncome([incomeTaxable]),
            msg="Valid taxable income did not return True"
        )
        self.assertTrue(
            e.addNonTaxableIncome([incomeNonTaxable]),
            msg="Valid non-taxable income did not return True"
        )
        grossIncome = e.getGrossIncome()
        self.assertTrue(
            grossIncome.status,
            msg="Valid incomes did not return True"
        )
        self.assertEqual(
            grossIncome.value,
            incomeTaxable + incomeNonTaxable,
            msg="Incomes summed incorrectly"
        )

        e.resetNonTaxableIncome()
        grossIncome = e.getGrossIncome()
        self.assertTrue(
            grossIncome.status,
            msg="Valid incomes did not return true when nontaxable reset"
        )
        self.assertEqual(
            grossIncome.value,
            incomeTaxable,
            msg="Incomes summed incorrectly"
        )

        e.resetTaxableIncome()
        self.assertTrue(
            e.addNonTaxableIncome([incomeNonTaxable]),
            msg="Valid non-taxable income did not return True"
        )
        grossIncome = e.getGrossIncome()
        self.assertTrue(
            grossIncome.status,
            msg="Valid incomes did not return true when nontaxable reset"
        )
        self.assertEqual(
            grossIncome.value,
            incomeNonTaxable,
            msg="Incomes summed incorrectly"
        )
    
    def test_add_taxable_income_value_after_init(self):
        """Test adding values to the income list post init"""
        e = EmployeeSalaryInfo("testname")
        income1 = 27000
        income2 = 3000
        e.addTaxableIncome([income1])
        grossIncome = e.getGrossIncome()
        self.assertEqual(
            grossIncome.value,
            income1,
            msg="Gross income value incorrect"
        )

        e.addTaxableIncome([income2])
        grossIncome = e.getGrossIncome()
        self.assertEqual(
            grossIncome.value,
            income1 + income2,
            msg="Gross income value incorrect after adding"
        )
    
    def test_add_non_taxable_income_value_after_init(self):
        """Test adding values to the income list post init"""
        e = EmployeeSalaryInfo("testname")
        income1 = 27000
        income2 = 3000
        e.addNonTaxableIncome([income1])
        grossIncome = e.getGrossIncome()
        self.assertEqual(
            grossIncome.value,
            income1,
            msg="Gross income value incorrect"
        )

        e.addNonTaxableIncome([income2])
        grossIncome = e.getGrossIncome()
        self.assertEqual(
            grossIncome.value,
            income1 + income2,
            msg="Gross income value incorrect after adding"
        )
    
    def test_force_income_list_invalid(self):
        """Tests forcing invalid values into the income list"""
        e = EmployeeSalaryInfo("testname")
        e.incomeTaxable = "teststring"
        grossIncome = e.getGrossIncome()

        self.assertFalse(
            grossIncome.status,
            msg="Gross income did not return false with forced bad values"
        )
        self.assertEqual(
            grossIncome.message,
            "Value not valid",
            msg="Error message did not return as expected"
        )
    
    def test_force_income_list_invalid_2(self):
        """Tests forcing invalid values into the income list"""
        e = EmployeeSalaryInfo("testname")
        e.incomeTaxable = -63300
        grossIncome = e.getGrossIncome()

        self.assertFalse(
            grossIncome.status,
            msg="Gross income did not return false with forced bad values"
        )


class PAYEUnitTests(TestCase):
    """Class to test PAYE calculation methods"""
    def test_valid_2021_2022(self):
        """Test valid output for 2021-2022"""
        testvalues = {
            'A':{
                'income': 29864.12,
                'tax': 3457.02
            },
            'B':{
                'income': 5451,
                'tax': 0.0
            },
            'C':{
                'income': 57012.28,
                'tax': 10233.31
            },
            'D':{
                'income': 165245.25,
                'tax': 54288.76
            },
        }
            
        e = EmployeeSalaryInfo("testname")

        for testcase in testvalues:
            e.addTaxableIncome([testvalues[testcase]['income']])
            payePaid = e.getPAYEPaid('2021-2022')
            self.assertTrue(
                payePaid.status,
                msg="getPAYEPaid method did not return true"
            )
            self.assertEqual(
                payePaid.value,
                testvalues[testcase]['tax'],
                msg=f"PAYE incorrectly calculated for income of "\
                    f"{testvalues[testcase]['income']}"
            )

            e.resetTaxableIncome()

    def test_force_income_list_invalid(self):
        """Tests forcing invalid values into the income list"""
        e = EmployeeSalaryInfo("testname")
        e.incomeTaxable = ["teststring"]
        payePaid = e.getPAYEPaid('2021-2022')
        self.assertFalse(
            payePaid.status,
            msg="getPAYEPaid method did not return false with bad input"
        )
    
    def test_force_income_list_invalid_2(self):
        """Tests forcing invalid values into the income list"""
        e = EmployeeSalaryInfo("testname")
        e.incomeTaxable = -23400
        payePaid = e.getPAYEPaid('2021-2022')
        self.assertFalse(
            payePaid.status,
            msg="getPAYEPaid method did not return false with bad input"
        )
        self.assertEqual(
            payePaid.message,
            "Taxable income invalid",
            msg="Error message did not return expected text"
        )
    
    def test_invalid_year(self):
        """Test invalid year input"""
        e = EmployeeSalaryInfo("testname")
        e.addTaxableIncome([30000])
        payePaid = e.getPAYEPaid('')
        self.assertFalse(
            payePaid.status,
            msg="Invalid year did not return False"
        )
        self.assertEqual(
            payePaid.message,
            "Year not valid",
            msg="Error message did not return expected text"
        )
        

class NIUnitTests(TestCase):
    """Class to test NI calculation methods"""
    def test_valid_2021_2022(self):
        """Test valid output for 2021-2022"""
        
        testvalues = {
            'A':{
                'income': 5168.56,
                'tax': 0.0
            },
            'B':{
                'income': 10298.98,
                'tax': 87.72
            },
            'C':{
                'income': 32875.21,
                'tax': 2796.87
            },
            'D':{
                'income': 75846.94,
                'tax': 5395.78
            },
        }
        
        e = EmployeeSalaryInfo("testname")

        for testcase in testvalues:
            e.addTaxableIncome([testvalues[testcase]['income']])
            niPaid = e.getNIPaid('2021-2022')
            self.assertTrue(
                niPaid.status,
                msg="getNIPaid method did not return true"
            )
            self.assertEqual(
                niPaid.value,
                testvalues[testcase]['tax'],
                msg=f"NI incorrectly calculated for income of "\
                    f"{testvalues[testcase]['income']}"
            )

            e.resetTaxableIncome()
        
    def test_force_income_list_invalid(self):
        """Tests forcing invalid values into the income list"""
        e = EmployeeSalaryInfo("testname")
        e.incomeTaxable = ["teststring"]
        niPaid = e.getNIPaid('2021-2022')
        self.assertFalse(
            niPaid.status,
            msg="getNIPaid method did not return false with bad input"
        )
    
    def test_force_income_list_invalid_2(self):
        """Tests forcing invalid values into the income list"""
        e = EmployeeSalaryInfo("testname")
        e.incomeTaxable = -23400
        niPaid = e.getNIPaid('2021-2022')
        self.assertFalse(
            niPaid.status,
            msg="getNIPaid method did not return false with bad input"
        )
        self.assertEqual(
            niPaid.message,
            "Taxable income invalid",
            msg="Error message did not return expected text"
        )
    
    def test_invalid_year(self):
        """Test invalid year input"""
        e = EmployeeSalaryInfo("testname")
        e.addTaxableIncome([30000])
        niPaid = e.getNIPaid('')
        self.assertFalse(
            niPaid.status,
            msg="Invalid year did not return False"
        )
        self.assertEqual(
            niPaid.message,
            "Year not valid",
            msg="Error message did not return expected text"
        )


class DeductionsUnitTests(TestCase):
    """Class to test the deductions methods"""
    year = '2021-2022'
    testvalues = {
        'A':{
            'incomeTaxable': 24000,
            'incomeNonTaxable': 0,
            'pensionPct': 5,
            'pensionType': 'post_tax',
            'netIncome': 19273.56,
        },
        'B':{
            'incomeTaxable': 24000,
            'incomeNonTaxable': 0,
            'pensionPct': 5,
            'pensionType': 'pre_tax',
            'netIncome': 19380.12,
        },
        'C':{
            'incomeTaxable': 24000,
            'incomeNonTaxable': 3000,
            'pensionPct': 5,
            'pensionType': 'pre_tax',
            'netIncome': 22380.12,
        },
        'D':{
            'incomeTaxable': 27000,
            'incomeNonTaxable': 3000,
            'pensionPct': 6,
            'pensionType': 'post_tax',
            'netIncome': 24027.48,
        },
        'D':{
            'incomeTaxable': 38254.54,
            'incomeNonTaxable': 1685,
            'pensionPct': 6,
            'pensionType': 'pre_tax',
            'netIncome': 30055.86,
        },
    }
    
    def test_ideal_cases(self):
        """Ideal case test"""
        for testcase in self.testvalues:
            
            if self.testvalues[testcase]['pensionType'] == 'pre_tax':
                pre_tax_status = True
                post_tax_status = False
            elif self.testvalues[testcase]['pensionType'] == 'post_tax':
                pre_tax_status = False
                post_tax_status = True
            else:
                self.assertFalse(
                    True, 
                    msg=f"Pension type set incorrectly in test case {testcase}"
                )

            e = EmployeeSalaryInfo("testname")
            e.addTaxableIncome([self.testvalues[testcase]['incomeTaxable']])
            e.addNonTaxableIncome([self.testvalues[testcase]['incomeNonTaxable']])
            e.addPension(
                year=self.year,
                percentage=self.testvalues[testcase]['pensionPct'],
                pre_tax=pre_tax_status,
                post_tax=post_tax_status
            )
            net_income = e.getNetIncome(year=self.year)

            self.assertTrue(
                net_income.status,
                msg=f"Net income calculation did not return True in test case {testcase}"
            )

            self.assertEqual(
                net_income.value,
                self.testvalues[testcase]['netIncome'],
                msg="Net income calculation did not return "\
                    f"pre-calculated value in test case {testcase}"
            )


