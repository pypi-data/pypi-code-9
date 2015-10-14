import types
  

class MockModule(object):
    """For mocking module"""
        
    def __init__(self, moduleNameOrModule):
        """Module can be given as string or the module itself"""
        if type(moduleNameOrModule) is types.StringType:
            self._module = __import__(moduleNameOrModule, globals(), locals(), [], -1)
        else:
            self._module = moduleNameOrModule
        self._mock = Mock()

    def __getattr__(self, name):
        mockedAttr = getattr(self._mock, name)
        setattr(self._module, name, mockedAttr)
        return mockedAttr

    def verify(self):
        self._mock.verify()

class Mock(object):
    """Mock object"""
    
    def __init__(self):
        self._mockMethods = {}

    def verify(self):
        """Verifies that all expectation are met. Raises exception
           when expectations are not met."""
        [method.verify() for method in self._mockMethods.values()]

    def __getattr__(self, name):
        return self._getMockMethod(name)
        
    def __call__(self, *args, **kwargs):
        return self
    
    def _getMockMethod(self, name):    
        if name not in self._mockMethods:
            self._createMockMethod(name)
        return self._mockMethods[name]

    def _createMockMethod(self, name):
        mockMethod = MockMethod(name)
        self._mockMethods[name] = mockMethod
        
class Proxy(object):
    
    def __init__(self, subjects):
        self.subjects = subjects
        
    def __getattr__(self, name):
        newSubjects = [subject.__getattr__(name) for subject in self.subjects]
        return Proxy(newSubjects)
        
    def __call__(self, *args, **kwargs):
        [subject(*args, **kwargs) for subject in self.subjects]
        
class MockArray(Mock):
    "Array of same mock objects"
    
    def __init__(self, numberOfMocks):
        Mock.__init__(self)
        assert numberOfMocks > 0, "Mock count must be > 0"
        self._mocks = [Mock() for i in range(numberOfMocks)]
        
    def __getitem__(self, index):
        if index > len(self):
            raise IndexError()
        return self._mocks[index]
        
    def __len__(self):
        return len(self._mocks)
        
    def __getattr__(self, name):
        return Proxy([mock.__getattr__(name) for mock in self._mocks])

    def __call__(self, *args, **kwargs):
        return Proxy(self._mocks)
        
    def verify(self):
        for mock in self._mocks: mock.verify()
        
class Expectation(object):
    """Base class for expectation classes"""
    def __init__(self, mockMethod):
        self.mockIsCalled = False
        self.mockMethod = mockMethod      


class CallExpectation(Expectation):
    
    def __init__(self, mockMethod):
        Expectation.__init__(self, mockMethod)
        self.mockExpectedArgs = None
        self.mockExpectedKwargs = None
        self.mockExpectedCallCount = None
        self.mockReceivedCalls = 0

    def mockVerify(self):   
        assert self.mockIsCalled, 'Method %s(%s,%s) was not called' \
            % (self.mockMethod.mockMethodName, self.mockExpectedArgs,self.mockExpectedKwargs)
        
        self.mockVerifyCallCount()


    def mockSetExpectedArgs(self, *args, **kwargs):
        self.mockExpectedArgs = args
        self.mockExpectedKwargs = kwargs
        return self

    def mockSetExpectedCallCount(self, count):
        self.mockExpectedCallCount = count
        return self

    def mockVerifyCallCount(self):
        assert 'FAILURE: verify call count not set'

    def mockVerifyCallCountExactly(self):
        if self.mockExpectedCallCount:
            assert self.mockReceivedCalls == self.mockExpectedCallCount, \
                'Method %s was called %d times, but expectations was %d times' \
                    % (self.mockMethod.mockMethodName, self.mockReceivedCalls, self.mockExpectedCallCount)

    def mockVerifyCallCountAtLeast(self):
        if self.mockExpectedCallCount:
            assert self.mockReceivedCalls >= self.mockExpectedCallCount, \
                'Method %s was called %d times, but expectations was at least %d times' \
                    % (self.mockMethod.mockMethodName, self.mockReceivedCalls, self.mockExpectedCallCount)

    def __getattr__(self,name):

        if name == 'withArgs':
            return self.mockSetExpectedArgs
        elif name == 'once':
            self.mockVerifyCallCount = self.mockVerifyCallCountExactly
            return self.mockSetExpectedCallCount(1)
        elif name == 'times':
            self.mockVerifyCallCount = self.mockVerifyCallCountExactly
            return self.mockSetExpectedCallCount
        elif name == 'atLeastTimes':
            self.mockVerifyCallCount = self.mockVerifyCallCountAtLeast
            return self.mockSetExpectedCallCount
        else:
            return self.mockMethod.__getattr__(name)

    def __call__(self, *args, **kwargs):
        if self.mockExpectedArgs:
            if self.mockExpectedArgs != args:
                return
        if self.mockExpectedKwargs:
            if self.mockExpectedKwargs != kwargs:
                return
        self.mockIsCalled = True
        self.mockReceivedCalls += 1

class CallNotExpected(Expectation):
    
    def __init__(self, mockMethod):
        Expectation.__init__(self, mockMethod)

    def mockVerify(self):   
        assert not self.mockIsCalled, "Method %s was called" % (self.mockMethod.mockMethodName)

    def mockIsOk(self):
        return not self.mockIsCalled

    def __getattr__(self,name):
        return self.mockMethod.__getattr__(name)

    def __call__(self, *args, **kwargs):
        self.mockIsCalled = True

    

class MockMethod(object):
    
    def __init__(self, methodName=None):
        self.mockMethodName = methodName
        self.mockExpectations = []
        self.mockMethodCallable = self._nullCallable
        self.mockArgumentHistory = []

    def verify(self):
        map(lambda expectation: expectation.mockVerify(), self.mockExpectations)

    def mockSetReturnValue(self, value):
        self.returnValue = value
    
    def mockMethodToBeCalled(self, method):
        self.mockMethodCallable = method

    def __getattr__(self,name):
        if name == 'mustBeCalled':
            return self._addExpectation(CallExpectation)          
        elif name == 'mustNotBeCalled':
            return self._addExpectation(CallNotExpected)
        elif name == 'returns':
            return self.mockSetReturnValue
        elif name == 'execute':
            return self.mockMethodToBeCalled
        elif name == 'history':
            return self.mockArgumentHistory

    def __call__(self, *args, **kwargs):
        self.mockArgumentHistory.append((args,kwargs))
        for expectation in self.mockExpectations:
            expectation(*args, **kwargs)

        self.mockMethodCallable(*args, **kwargs)
        return self.returnValue

    def _addExpectation(self, expectation):
        expectation = expectation(self)
        self.mockExpectations.append(expectation)
        return expectation

    def _nullCallable(self, *args, **kwargs):
        pass
