from django.test import TestCase
from accounts.models import (
    AdminUser,
    Company,
    Factory,
    Complainer,
    CaseReporter,
    FactoryAdmin,
    Case,
    CaseManager,
    CaseTroubleShooter,
)

# Create your tests here.
# from model_bakery import baker


class AdminUserTest(TestCase):
    def setUp(self):
        AdminUser.objects.create(
            name="admin", password="admin", email="123@gmail.com", role="ADMIN"
        )

    def test_name(self):
        user1 = AdminUser.objects.get(name="admin")
        self.assertEqual(user1.name, "admin")


class FactoryAdminTest(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="testcom",
            Address="address",
            POC="person",
            Email="email@email.com",
            PhoneNo=2323131,
        )
        company.save()

        com = Company.objects.get(Legalcompanyname="testcom")
        Factory.objects.create(
            Company=com,
            Code=234,
            Location="Delhi",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )
        fac = Factory.objects.get(Code="234")
        FactoryAdmin.objects.create(
            name="fac_admin",
            password="admin",
            email="F_A@gmail.com",
            role="Factory_ADMIN",
            factoryemployeeid=123,
            Company=com,
            Factory=fac,
        )

    def test_name(self):
        user1 = FactoryAdmin.objects.get(factoryemployeeid=123)
        self.assertEqual(user1.name, "fac_admin")


class CRTest(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="testcom",
            Address="address",
            POC="person",
            Email="email@email.com",
            PhoneNo=2323131,
        )
        company.save()

        com = Company.objects.get(Legalcompanyname="testcom")
        Factory.objects.create(
            Company=com,
            Code=234,
            Location="Delhi",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )
        fac = Factory.objects.get(Code="234")
        CaseReporter.objects.create(
            name="CR",
            password="caserep",
            email="CR@gmail.com",
            role="CR",
            factoryemployeeid=234,
            Company=com,
            Factory=fac,
        )

    def test_name(self):
        user1 = CaseReporter.objects.get(factoryemployeeid=234)
        self.assertEqual(user1.name, "CR")


class CMTest(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="testcom",
            Address="address",
            POC="person",
            Email="email@email.com",
            PhoneNo=2323131,
        )
        company.save()

        com = Company.objects.get(Legalcompanyname="testcom")
        Factory.objects.create(
            Company=com,
            Code=234,
            Location="Delhi",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )
        fac = Factory.objects.get(Code="234")
        CaseManager.objects.create(
            name="CM",
            password="caseman",
            email="CM@gmail.com",
            role="CM",
            factoryemployeeid=345,
            Company=com,
            Factory=fac,
        )

    def test_name(self):
        user1 = CaseManager.objects.get(factoryemployeeid=345)
        self.assertEqual(user1.name, "CM")


class CTTest(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="testcom",
            Address="address",
            POC="person",
            Email="email@email.com",
            PhoneNo=2323131,
        )
        company.save()

        com = Company.objects.get(Legalcompanyname="testcom")
        Factory.objects.create(
            Company=com,
            Code=234,
            Location="Delhi",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )
        fac = Factory.objects.get(Code="234")
        CaseTroubleShooter.objects.create(
            name="CT",
            password="caseman",
            email="CT@gmail.com",
            role="CT",
            factoryemployeeid=456,
            Company=com,
            Factory=fac,
        )

    def test_name(self):
        user1 = CaseTroubleShooter.objects.get(factoryemployeeid=456)
        self.assertEqual(user1.name, "CT")


class ComplainerTest(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="testcom",
            Address="address",
            POC="person",
            Email="email@email.com",
            PhoneNo=2323131,
        )
        company.save()

        com = Company.objects.get(Legalcompanyname="testcom")
        Factory.objects.create(
            Company=com,
            Code=234,
            Location="Delhi",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )
        fac = Factory.objects.get(Code="234")
        Complainer.objects.create(PhoneNo=23456, Company=com, Factory=fac)

    def test_name(self):
        user1 = Complainer.objects.get(PhoneNo=23456)
        self.assertEqual(user1.Company.Legalcompanyname, "testcom")


class FactoryTest(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="company",
            Address="address",
            POC="person",
            Email="email",
            PhoneNo=2323131,
        )
        company.save()
        com = Company.objects.get(Legalcompanyname="company")
        Factory.objects.create(
            Company=com,
            Code=123,
            Location="Bangalore",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )

    def test_code(self):
        fac = Factory.objects.get(Code="123")
        self.assertEqual(str(fac), "Bangalore 123")
        print("passed")


class CompanyTest(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="company",
            Address="address",
            POC="person",
            Email="email",
            PhoneNo=2323131,
        )
        company.save()

    def test_code(self):
        company = Company.objects.get(Legalcompanyname="company")
        self.assertEqual(str(company), "company")
        print("passed")


# class FactoryUserTest(TestCase):
#     def setUp(self):
#         FactoryUser.objects.create(Name='user', Designation='user',  Email='user@gmail.com',
#                                    EmployeeId=123,
#                                    PasswordHash='123',
#                                    Roles='admin')

#     def test_Email(self):
#         user1 = FactoryUser.objects.get(EmployeeId=123)
#         self.assertEqual(user1.Email, 'user@gmail.com')


# class FeedbackTicketsTest(TestCase):
#     def test_Ticket_model(self):
#         feed = baker.make(FeedbackTickets, Title="New req")
#         self.assertEqual(str(feed), 'New req')


# class ComplainerTest(TestCase):
#     def test_Complain_model(self):
#         comp = baker.make(Complainer, PhoneNumber="989", ComplainerID=123)

#         self.assertEqual(str(comp), '123 Complained from 989')


# class CaseReporterTest(TestCase):
#     def setUp(self):
#         CaseReporter.objects.create(ReportedID=10,
#                                     ListCases='["New","Old"]', ListClosedCases='["New","old"]')

#     def test_CaseReporter_model(self):
#         cr = CaseReporter.objects.get(
#             ReportedID=10)

#         self.assertListEqual(cr.get_ListCases(), ['New', 'Old'])

#     def test_CasereporerClose_model(self):
#         cr = CaseReporter.objects.get(ReportedID=10)
#         print(type(cr.get_ListClosedCases()), "closer hu me")
#         self.assertListEqual(cr.get_ListClosedCases(), ['New', 'old'])


# class FactoryAdminTest(TestCase):
#     def test_FactoryAdmin_model(self):
#         fa = baker.make(FactoryAdmin, Name='admin')
#         self.assertEqual(str(fa), 'admin')


# class CaseTest(TestCase):
#     def test_CaseModel(self):
#         case = baker.make(Case, CaseNumber=123)

#         self.assertEqual(str(case), '123')


# class CaseManagerTest(TestCase):
#     def test_CaseManager_model(self):
#         case = baker.make(CaseManager, Name='manager')
#         self.assertEqual(str(case), 'manager')


# class CaseTroubleShooterTest(TestCase):
#     def test_CaseTroubleShooter_model(self):
#         case = baker.make(CaseTroubleShooter, Name='troubleshooter')
#         self.assertEqual(str(case), 'troubleshooter')


# class UnassignedUserTest(TestCase):
#     def test_UnassignedUser_model(self):
#         case = baker.make(UnassignedUser, Name='Unassigned')
#         self.assertEqual(str(case), 'Unassigned')
