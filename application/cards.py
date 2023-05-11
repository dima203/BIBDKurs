from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty


class Card(MDCard):
    id = StringProperty('')

    def get_lists(self) -> tuple[list]:
        return ()


class CustomerCard(Card):
    customerCode = StringProperty('')
    customerName = StringProperty('')
    customerLocation = StringProperty('')
    customerPhone = StringProperty('')


class WorkerCard(Card):
    workerCode = StringProperty('')
    workerFIO = StringProperty('')
    professionCode = StringProperty('')
    hireDate = StringProperty('')
    workerLocation = StringProperty('')
    workerPhone = StringProperty('')


class WorkCard(Card):
    workCode = StringProperty('')
    workPrice = NumericProperty(0)
    workTime = NumericProperty(0)


class SPTCard(Card):
    sptCode = StringProperty('')
    sptName = StringProperty('')
    sptIzm = StringProperty('')
    sptPrice = NumericProperty(0)


class SpecificationCard(Card):
    specificationCode = StringProperty('')
    contractCode = StringProperty('')
    customerCode = StringProperty('')
    sptCode = StringProperty('')
    workCode = ListProperty([])
    content = ObjectProperty()
    cost = NumericProperty(0)

    def get_lists(self) -> tuple[list]:
        return self.workCode,


class TaskCard(Card):
    taskCode = StringProperty('')
    contractCode = StringProperty('')
    taskDate = StringProperty('')
    workCode = ListProperty([])
    workerCode = ListProperty([])
    content = ObjectProperty()
    taskCost = NumericProperty(0)

    def get_lists(self) -> tuple[list]:
        return self.workCode, self.workerCode


class CustomerReportCard(Card):
    customerCode = StringProperty('')
    contractNumber = NumericProperty(0)
    contractPrice = NumericProperty(0)


class WorkerReportCard(Card):
    workerCode = StringProperty('')
    workerFIO = StringProperty('')
    taskNumber = NumericProperty(0)
    workPrice = NumericProperty(0)
