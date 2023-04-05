class Event:
    def __init__(self, type, subtype, trigger, expected, nrExpected, testNumber) -> None:
        self.type = type
        self.subtype = subtype
        self.trigger = trigger
        self.gotten = ""
        self.expected = expected
        self.nrGotten = ""
        self.nrExpected = nrExpected
        self.success = ""
        self.testNumber = testNumber
