from VictoryGoals import *
from unittest import *

from inspect import isfunction


class ExtendedTestCase(TestCase):

	def assertType(self, object, expectedType):
		self.assertEqual(type(object), expectedType)


class TestGetNumArgs(ExtendedTestCase):

	def testFunction(self):
		def noargs():
			pass
		def onearg(arg):
			pass
		def twoargs(arg1, arg2):
			pass
		
		self.assertEqual(getnumargs(noargs), 0)
		self.assertEqual(getnumargs(onearg), 1)
		self.assertEqual(getnumargs(twoargs), 2)
	
	def testMethod(self):
		class SomeClass(object):
			def noargs(self):
				pass
			def onearg(self, arg):
				pass
			def twoargs(self, arg1, arg2):
				pass
		
		self.assertEqual(getnumargs(SomeClass.noargs), 1)
		self.assertEqual(getnumargs(SomeClass.onearg), 2)
		self.assertEqual(getnumargs(SomeClass.twoargs), 3)
	
	def testLambda(self):
		self.assertEqual(getnumargs(lambda: 0), 0)
		self.assertEqual(getnumargs(lambda x: x), 1)
		self.assertEqual(getnumargs(lambda x, y: (x, y)), 2)
	
	def testDLLMethods(self):
		self.assertEqual(getnumargs(CyPlot.getX), 1)
		self.assertEqual(getnumargs(CyPlot.getYield), 2)
		self.assertEqual(getnumargs(CyPlot.at), 3)


class PlayerContainer(object):

	def __init__(self, iPlayer):
		self.iPlayer = iPlayer


class TestEventHandlers(ExtendedTestCase):

	def setUp(self):
		self.handlers = EventHandlers()
		
		self.iCallCount = 0
		self.iIncrement = 0
	
	def trackCall(self, *args):
		self.iCallCount += 1
	
	def increment(self, other, iChange):
		self.iIncrement += iChange
	
	def testGet(self):
		handler_func = self.handlers.get("techAcquired", lambda *args: 0)
		
		self.assert_(isfunction(handler_func))
		self.assertEqual(handler_func.__name__, "techAcquired")
	
	def testGetNonExistent(self):
		self.assertRaises(Exception, self.handlers.get, "someNonexistentEvent", lambda *args: 0)
	
	def testBeginPlayerTurn(self):
		onBeginPlayerTurn = self.handlers.get("BeginPlayerTurn", self.trackCall)
		
		onBeginPlayerTurn(PlayerContainer(0), (100, 0))
		self.assertEqual(self.iCallCount, 1)
		
		onBeginPlayerTurn(PlayerContainer(1), (100, 0))
		self.assertEqual(self.iCallCount, 1)
	
	def testTechAcquired(self):
		onTechAcquired = self.handlers.get("techAcquired", self.trackCall)
		
		onTechAcquired(PlayerContainer(0), (10, 0, 0, False))
		self.assertEqual(self.iCallCount, 1)
		
		onTechAcquired(PlayerContainer(1), (10, 0, 0, False))
		self.assertEqual(self.iCallCount, 1)
	
	def testCombatResult(self):
		onCombatResult = self.handlers.get("combatResult", self.trackCall)
		winningUnit = makeUnit(0, 0, (0, 0))
		losingUnit = makeUnit(1, 0, (0, 1))
		
		onCombatResult(PlayerContainer(0), (winningUnit, losingUnit))
		self.assertEqual(self.iCallCount, 1)
		
		onCombatResult(PlayerContainer(1), (winningUnit, losingUnit))
		self.assertEqual(self.iCallCount, 1)
		
		winningUnit.kill(0, False)
		losingUnit.kill(0, False)
	
	def testPlayerGoldTrade(self):
		onPlayerGoldTrade = self.handlers.get("playerGoldTrade", self.increment)
		
		onPlayerGoldTrade(PlayerContainer(0), (1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onPlayerGoldTrade(PlayerContainer(1), (1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
	
	def testUnitPillage(self):
		onUnitPillage = self.handlers.get("unitPillage", self.increment)
		unit = makeUnit(0, 0, (0, 0))
		
		onUnitPillage(PlayerContainer(0), (unit, 0, -1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onUnitPillage(PlayerContainer(1), (unit, 0, -1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		unit.kill(-1, False)
	
	def testCityCaptureGold(self):
		onCityCaptureGold = self.handlers.get("cityCaptureGold", self.increment)
		city = player(1).initCity(0, 0)
		
		onCityCaptureGold(PlayerContainer(0), (city, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onCityCaptureGold(PlayerContainer(1), (city, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		city.kill()
	
	def testCityAcquired(self):
		onCityAcquired = self.handlers.get("cityAcquired", self.trackCall)
		city = player(1).initCity(0, 0)
		
		onCityAcquired(PlayerContainer(0), (1, 0, city, False, False))
		self.assertEqual(self.iCallCount, 1)
		
		onCityAcquired(PlayerContainer(1), (1, 0, city, False, False))
		self.assertEqual(self.iCallCount, 1)
		
		city.kill()
	
	def testCityBuilt(self):
		onCityBuilt = self.handlers.get("cityBuilt", self.trackCall)
		city = player(0).initCity(0, 0)
		
		onCityBuilt(PlayerContainer(0), (city,))
		self.assertEqual(self.iCallCount, 1)
		
		onCityBuilt(PlayerContainer(1), (city,))
		self.assertEqual(self.iCallCount, 1)
		
		city.kill()
	
	def testBlockade(self):
		onBlockade = self.handlers.get("blockade", self.increment)
		
		onBlockade(PlayerContainer(0), (0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onBlockade(PlayerContainer(1), (0, 100))
		self.assertEqual(self.iIncrement, 100)

	def testCityRazed(self):
		onCityRazed = self.handlers.get("cityRazed", self.trackCall)
		city = player(1).initCity(0, 0)
		
		onCityRazed(PlayerContainer(0), (city, 0))
		self.assertEqual(self.iCallCount, 1)
		
		onCityRazed(PlayerContainer(1), (city, 0))
		self.assertEqual(self.iCallCount, 1)
		
		city.kill()
	
	def testPlayerSlaveTrade(self):
		onPlayerSlaveTrade = self.handlers.get("playerSlaveTrade", self.increment)
		
		onPlayerSlaveTrade(PlayerContainer(0), (0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onPlayerSlaveTrade(PlayerContainer(1), (0, 100))
		self.assertEqual(self.iIncrement, 100)
	
	def testGreatPersonBorn(self):
		onGreatPersonBorn = self.handlers.get("greatPersonBorn", self.trackCall)
		
		onGreatPersonBorn(PlayerContainer(0), (None, 0, None))
		self.assertEqual(self.iCallCount, 1)
		
		onGreatPersonBorn(PlayerContainer(1), (None, 0, None))
		self.assertEqual(self.iCallCount, 1)
	
	def testPeaceBrokered(self):
		onPeaceBrokered = self.handlers.get("peaceBrokered", self.trackCall)
		
		onPeaceBrokered(PlayerContainer(0), (0, 1, 2))
		self.assertEqual(self.iCallCount, 1)
		
		onPeaceBrokered(PlayerContainer(1), (0, 1, 2))
		self.assertEqual(self.iCallCount, 1)
	
	def testEnslave(self):
		onEnslave = self.handlers.get("enslave", self.trackCall)
		
		onEnslave(PlayerContainer(0), (0, None))
		self.assertEqual(self.iCallCount, 1)
		
		onEnslave(PlayerContainer(1), (0, None))
		self.assertEqual(self.iCallCount, 1)


class TestDeferred(ExtendedTestCase):

	def testCapitalWithoutCities(self):
		city = capital()
		self.assertEqual(city(0), None)
		
	def testCapitalAfterCity(self):
		city = player(0).initCity(0, 0)
		city.setHasRealBuilding(iPalace, True)
		
		capital_ = capital()
		
		self.assertEqual(capital_(0).getID(), city.getID())
		
		city.kill()
		
	def testCapitalBeforeCity(self):
		capital_ = capital()
		city = player(0).initCity(0, 0)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(capital_(0).getID(), city.getID())
		
		city.kill()
		
	def testCityVarargs(self):
		city_ = player(0).initCity(0, 0)
		deferredCity = city(0, 0)
		
		self.assertEqual(deferredCity().getID(), city_.getID())
		
		city_.kill()
	
	def testCityWithoutCities(self):
		deferredCity = city((0, 0))
		self.assertEqual(deferredCity(), None)
	
	def testCityAfterCity(self):
		city_ = player(0).initCity(0, 0)
		deferredCity = city((0, 0))
		
		self.assertEqual(deferredCity().getID(), city_.getID())
		
		city_.kill()
	
	def testCityBeforeCity(self):
		deferredCity = city((0, 0))
		city_ = player(0).initCity(0, 0)
		
		self.assertEqual(deferredCity().getID(), city_.getID())
		
		city_.kill()
	
	def testWonderWithoutCities(self):
		city = wonder(iPyramids)
		self.assertEqual(city(), None)
	
	def testWonderWithoutWonder(self):
		city = wonder(iPyramids)
		city_ = player(0).initCity(0, 0)
		
		self.assertEqual(city(), None)
		
		city_.kill()
	
	def testWonderWithWonder(self):
		city = wonder(iPyramids)
		city_ = player(0).initCity(0, 0)
		city_.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(city().getID(), city_.getID())
		
		city_.kill()


class TestAggregate(ExtendedTestCase):

	def testEvalSum(self):
		agg = sum(i for i in xrange(3))
		result = agg.eval(lambda x: x*x)
		
		self.assertEqual(result, 5)
	
	def testEvalAverage(self):
		agg = avg(i for i in xrange(5))
		result = agg.eval(lambda x: x)
		
		self.assertEqual(result, 2.0)
		
	def testEvalAverageEmpty(self):
		agg = avg(i for i in xrange(0))
		result = agg.eval(lambda x: x)
		
		self.assertEqual(result, 0.0)
	
	def testLazyItemsOnEval(self):
		agg = sum(i for i in xrange(3))
		self.assertEqual(agg._items, None)
		
		agg.eval(lambda x: x)
		self.assertEqual(agg._items, [0, 1, 2])
	
	def testLazyItemsOnIter(self):
		agg = sum(i for i in xrange(3))
		self.assertEqual(agg._items, None)
		
		for i in agg:
			continue
		self.assertEqual(agg._items, [0, 1, 2])
	
	def testLazyItemsOnContains(self):
		agg = sum(i for i in xrange(3))
		self.assertEqual(agg._items, None)
		
		contained = 0 in agg
		self.assertEqual(agg._items, [0, 1, 2])


class TestArgumentProcessor(ExtendedTestCase):

	def testReturnsArguments(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,))
		self.assertType(result, Arguments)
	
	def testSubjectNone(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,))
		self.assertEqual(result.subject, None)
		
	def testObjectivesEmptyList(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		result = types.process(city((100, 100)))
		self.assertEqual(result.objectives, [])
	
	def testObjectivesNotList(self):
		self.assertRaises(ValueError, ArgumentProcessor, int)

	def testProcessSingleType(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,))
		self.assertEqual(result.objectives, [(0,)])
	
	def testProcessMultipleSingleTypes(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,), (1,), (2,))
		self.assertEqual(result.objectives, [(0,), (1,), (2,)])
	
	def testProcessMultipleSingleTypesFlat(self):
		types = ArgumentProcessor([int])
		
		result = types.process(0, 1, 2)
		self.assertEqual(result.objectives, [(0,), (1,), (2,)])
	
	def testInvalidType(self):
		types = ArgumentProcessor([str])
		
		self.assertRaises(ValueError, types.process, 0)
	
	def testInvalidTypeAfterValid(self):
		types = ArgumentProcessor([str])
		
		self.assertRaises(ValueError, types.process, "0", "1", 2)
	
	def testInvalidLengthTooLong(self):
		types = ArgumentProcessor([int])
		
		self.assertRaises(ValueError, types.process, (0, 1), (2, 3))
	
	def testEmptyInput(self):
		types = ArgumentProcessor([str])
		
		self.assertRaises(ValueError, types.process)
	
	def testProcessDoubleType(self):
		types = ArgumentProcessor([int, str])
		
		result = types.process((1, "1"), (2, "2"))
		self.assertEqual(result.objectives, [(1, "1"), (2, "2")])
	
	def testProcessInvalidLengthTooShort(self):
		types = ArgumentProcessor([int, str])
		
		self.assertRaises(ValueError, types.process, (0,), (1,))
	
	def testProcessTooShortFlat(self):
		types = ArgumentProcessor([str, str])
		
		self.assertRaises(ValueError, types.process, "0")
	
	def testProcessTooLongFlat(self):
		types = ArgumentProcessor([str, str])
		
		self.assertRaises(ValueError, types.process, "0", "1", "2")
	
	def testDefaultIntValue(self):
		types = ArgumentProcessor([int])
		
		result = types.process()
		self.assertEqual(result.objectives, [(1,)])
	
	def testDefaultIntValueInMultiple(self):
		types = ArgumentProcessor([int, int])
		
		result = types.process((1,), (2,), (3,))
		self.assertEqual(result.objectives, [(1, 1), (2, 1), (3, 1)])
	
	def testDefaultIntValueWhenLonger(self):
		types = ArgumentProcessor([int, int])
		
		self.assertRaises(ValueError, types.process, (1, 2, 3))
		
	def testIntValidTypeForInfoClass(self):
		types = ArgumentProcessor([CvBuildingInfo])
		
		result = types.process(1, 2, 3)
		self.assertEqual(result.objectives, [(1,), (2,), (3,)])
	
	def testAggregateValidTypeForInfoClass(self):
		types = ArgumentProcessor([CvBuildingInfo])
		
		result = types.process(sum(i for i in xrange(3)))
		self.assertType(result, Arguments)
		
		objectives = result.objectives
		self.assertType(objectives, list)
		self.assertEqual(len(objectives), 1)
		self.assertType(objectives[0], tuple)
		self.assertEqual(len(objectives[0]), 1)
		self.assertType(objectives[0][0], Aggregate)
	
	def testDefaultPlayerValue(self):
		types = ArgumentProcessor([Players])
		
		result = types.process()
		self.assertEqual(result.objectives, [(players.major().alive(),)])
	
	def testCityType(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		result = types.process(city((100, 100)))
		self.assertType(result, Arguments)
		self.assertType(result.subject, Deferred)
		
		objectives = result.objectives
		self.assertType(objectives, list)
		self.assertEqual(len(objectives), 0)
	
	def testCityTypeFailsWhenMissing(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		self.assertRaises(ValueError, types.process)
	
	def testCityTypeFailsWithDifferentArgument(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		self.assertRaises(ValueError, types.process, 1)
	
	def testCityOnlyExpectedFirst(self):
		types = ArgumentProcessor([str, int], CyCity)
		
		result = types.process(city((100, 100)), ("1", 1), ("2", 2), ("3", 3))
		self.assertType(result, Arguments)
		self.assertType(result.subject, Deferred)
		
		objectives = result.objectives
		self.assertType(objectives, list)
		self.assertEqual(len(objectives), 3)
		
		for objective in objectives:
			self.assertType(objective[0], str)
			self.assertType(objective[1], int)
	
	def testCityCannotBeSuppliedTwice(self):
		types = ArgumentProcessor([str, int], CyCity)
		
		self.assertRaises(ValueError, types.process, city((100, 100)), city((50, 50)), ("1", 1))
	
	def testObjectiveSplit(self):
		types = ArgumentProcessor([int, int, int], objective_split=1)
		
		result = types.process((1, 2, 3), (4, 5, 6), (7, 8, 9))
		self.assertEqual(result.objectives, [((1, 2), (3,)), ((4, 5), (6,)), ((7, 8), (9,))])
		
	def testObjectSplitDouble(self):
		types = ArgumentProcessor([int, int, int], objective_split=2)
		
		result = types.process((1, 2, 3), (4, 5, 6), (7, 8, 9))
		self.assertEqual(result.objectives, [((1,), (2, 3)), ((4,), (5, 6)), ((7,), (8, 9))])
	
	def testPrefersSingleOverDoubleWithDefault(self):
		types = ArgumentProcessor([str, int])
		
		result = types.process("string", 10)
		self.assertEqual(result.objectives, [("string", 10)])
	
	def testListTransform(self):
		types = ArgumentProcessor([list])
		
		result = types.process([1, 2, 3])
		self.assertEqual(result.objectives, [((1, 2, 3),)])
	
	def testAggregateIsValidForPlots(self):
		types = ArgumentProcessor([Plots])
		
		result = types.process(sum([plots.of([(61, 31)])]))
		self.assertEqual(len(result.objectives), 1)
		self.assertType(result.objectives[0], tuple)
		self.assertEqual(len(result.objectives[0]), 1)
		self.assertType(result.objectives[0][0], Aggregate)


class TestArgumentProcessorBuilder(ExtendedTestCase):

	def setUp(self):
		self.builder = ArgumentProcessorBuilder()

	def testRequiresSetup(self):
		self.assertRaises(ValueError, self.builder.build)
		
	def testUninitialized(self):
		self.assertEqual(self.builder.initialized(), False)
	
	def testInitialized(self):
		self.assertEqual(self.builder.withObjectiveTypes(int).initialized(), True)
	
	def testWithObjectiveType(self):
		types = self.builder.withObjectiveTypes(int).build()
		
		self.assertEqual(types.objective_types, [int])
	
	def testWithObjectiveTypes(self):
		types = self.builder.withObjectiveTypes(int, int).build()
		
		self.assertEqual(types.objective_types, [int, int])
	
	def testWithSubjectType(self):
		types = self.builder.withSubjectType(CyCity).build()
		
		self.assertEqual(types.subject_type, CyCity)
	
	def testWithObjectiveSplit(self):
		types = self.builder.withObjectiveTypes(int, int).withObjectiveSplit(1).build()
		
		self.assertEqual(types.objective_split, 1)


class TestBaseGoal(ExtendedTestCase):

	def setUp(self):
		class DummyProcessor(object):
			def process(self, *args):
				return Arguments([], None)
		
		def condition(self, objective=None):
			return self.condition_value
		
		def display(self):
			return str(self.condition())
		
		BaseGoal._types = DummyProcessor()
		BaseGoal.condition = condition
		BaseGoal.display = display
		
		self.goal = BaseGoal()
		self.goal.condition_value = True
	
	def testInitialState(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		self.assertEqual(self.goal.objectives, [])
		self.assertEqual(self.goal.subject, None)
		self.assertEqual(self.goal.iPlayer, None)
		self.assertEqual(self.goal._player, None)
		self.assertEqual(self.goal._team, None)
		self.assertEqual(self.goal.callback, None)
	
	def testActivate(self):
		self.goal.activate(0)
		
		self.assertEqual(self.goal.iPlayer, 0)
		self.assertEqual(self.goal._player.getID(), 0)
		self.assertEqual(self.goal._team.getID(), 0)
		self.assertEqual(self.goal.callback, None)
	
	def testActivateWithCallback(self):
		def callback():
			pass
		
		self.goal.activate(0, callback)
		
		self.assertEqual(self.goal.callback, callback)
	
	def testPossiblePossible(self):
		self.assertEqual(self.goal.possible(), True)
	
	def testPossibleSucceeded(self):
		self.goal.state = SUCCESS
		self.assertEqual(self.goal.possible(), False)
	
	def testPossibleFailed(self):
		self.goal.state = FAILURE
		self.assertEqual(self.goal.possible(), False)
	
	def testWin(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.win()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFail(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testSetStateUnchanged(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.setState(POSSIBLE)
		self.assertEqual(self.goal.state, POSSIBLE)
	
	def testSetStateChanged(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.setState(SUCCESS)
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testSetStateChangedCallback(self):
		class Callable(object):
			def __init__(self):
				self.called = None
			def call(self, called):
				self.called = called
				
		callable = Callable()
		
		self.goal.activate(0, callable.call)
		self.goal.setState(SUCCESS)
		self.assertEqual(callable.called, self.goal)
	
	def testSetStateUnchangedCallback(self):
		class Callable(object):
			def __init__(self):
				self.called = None
			def call(self, called):
				self.called = called
				
		callable = Callable()
		
		self.goal.activate(0, callable.call)
		self.goal.setState(POSSIBLE)
		self.assertEqual(callable.called, None)

	def testExpirePossible(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.expire()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testExpireSuccess(self):
		self.goal.state = SUCCESS
		self.goal.expire()
		
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testExpireFailure(self):
		self.goal.state = FAILURE
		self.goal.expire()
		
		self.assertEqual(self.goal.state, FAILURE)
	
	def testNonzero(self):
		self.assertEqual(bool(self.goal), True)
	
	def testNonzeroWithFailedCondition(self):
		self.goal.condition_value = False
		
		self.assertEqual(bool(self.goal), False)
	
	def testToString(self):
		self.assertEqual(str(self.goal), "True")
	
	def testCheckPossible(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.check()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testCheckFailure(self):
		self.goal.state = FAILURE
		
		self.goal.check()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testCheckSuccess(self):
		self.goal.state = SUCCESS
		
		self.goal.check()
		self.assertEqual(self.goal.state, SUCCESS)
		
	def testCheckFailingPossible(self):
		self.goal.condition_value = False
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.check()
		self.assertEqual(self.goal.state, POSSIBLE)
	
	def testCheckFailingFailure(self):
		self.goal.condition_value = False
		self.goal.state = FAILURE
		
		self.goal.check()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testCheckFailingSuccess(self):
		self.goal.condition_value = False
		self.goal.state = SUCCESS
		
		self.goal.check()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFinalCheckPossible(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFinalCheckFailure(self):
		self.goal.state = FAILURE
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testFinalCheckSuccess(self):
		self.goal.state = SUCCESS
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFinalCheckFailingPossible(self):
		self.goal.condition_value = False
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testFinalCheckFailingFailure(self):
		self.goal.condition_value = False
		self.goal.state = FAILURE
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testFinalCheckFailingSuccess(self):
		self.goal.condition_value = False
		self.goal.state = SUCCESS
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, SUCCESS)


class TestConditionGoals(ExtendedTestCase):

	def testControlAllCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(0).initCity(65, 31)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlSomeCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlNoCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlEmpty(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testControlOutside(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(0).initCity(59, 31)
		
		self.assertEqual(bool(goal), False)
		
		city.kill()
	
	def testControlAllOfMultiple(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)), plots.rectangle((66, 30), (70, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(69, 31)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
	
	def testControlSomeOfMultiple(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)), plots.rectangle((66, 30), (70, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(69, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()

	def testControlOrVassalizeAllCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(0).initCity(65, 31)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlOrVassalizeSomeCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlOrVassalizeNoCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlOrVassalizeAllVassal(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
		city3.kill()
		
		team(1).setVassal(team(0).getID(), False, False)
	
	def testControlOrVassalizeOneVassal(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(2).initCity(63, 31)
		city3 = player(2).initCity(65, 31)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
		
		team(1).setVassal(team(0).getID(), False, False)
	
	def testSettleWhenFounded(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		self.assertEqual(bool(goal), True)
		
		city.kill()
	
	def testSettleWhenConquered(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		self.assertEqual(city.getOwner(), 0)
		self.assertEqual(bool(goal), False)
		
		city.kill()
	
	def testSettleWhenTraded(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		player(0).acquireCity(city, False, True)
		city = city_(61, 31)
		
		self.assertEqual(city.getOwner(), 0)
		self.assertEqual(bool(goal), False)
		
		city.kill()
	
	def testWonderOwned(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(bool(goal), True)
		
		city.kill()
	
	def testWonderNonExistent(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		
	def testWonderDifferentOwner(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(bool(goal), False)
		
		city.kill()
	
	def testMultipleWondersNone(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testMultipleWondersSome(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		for iWonder in [iPyramids, iParthenon]:
			city.setHasRealBuilding(iWonder, True)
		
		self.assertEqual(bool(goal), False)
		
		city.kill()
	
	def testMultipleWondersAll(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		for iWonder in [iPyramids, iParthenon, iColossus]:
			city.setHasRealBuilding(iWonder, True)
		
		self.assertEqual(bool(goal), True)
		
		city.kill()
	
	def testCityBuildingNoCity(self):
		goal = Condition.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testCityBuildingNoBuilding(self):
		goal = Condition.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		
		self.assertEqual(bool(goal), False)
		
		_city.kill()
	
	def testCityBuildingWithBuilding(self):
		goal = Condition.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), True)
		
		_city.kill()
		
	def testCityBuildingDifferentCity(self):
		goal = Condition.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		_city = player(0).initCity(63, 31)
		_city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), False)
		
		_city.kill()
	
	def testCityMultipleBuildingsSome(self):
		goal = Condition.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks]:
			_city.setHasRealBuilding(iBuilding, True)
		
		self.assertEqual(bool(goal), False)
		
		_city.kill()
	
	def testCityMultipleBuildingsAll(self):
		goal = Condition.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks, iLibrary]:
			_city.setHasRealBuilding(iBuilding, True)
		
		self.assertEqual(bool(goal), True)
		
		_city.kill()
	
	def testCityMultipleBuildingsDifferentCities(self):
		goal = Condition.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city1.setHasRealBuilding(iGranary, True)
		city1.setHasRealBuilding(iBarracks, True)
		city2.setHasRealBuilding(iLibrary, True)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
	
	def testProjectNonExistent(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testProjectCompleted(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		team(0).changeProjectCount(iTheInternet, 1)
		
		self.assertEqual(bool(goal), True)
		
		team(0).changeProjectCount(iTheInternet, -1)
	
	def testProjectCompletedOther(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		team(1).changeProjectCount(iTheInternet, 1)
		
		self.assertEqual(bool(goal), False)
		
		team(1).changeProjectCount(iTheInternet, -1)
	
	def testProjectCompletedMultipleSome(self):
		goal = Condition.project(iTheInternet, iHumanGenome, iSDI)
		goal.activate(0)
		
		team(0).changeProjectCount(iTheInternet, 1)
		team(0).changeProjectCount(iHumanGenome, 1)
		
		self.assertEqual(bool(goal), False)
		
		team(0).changeProjectCount(iTheInternet, -1)
		team(0).changeProjectCount(iHumanGenome, -1)
	
	def testProjectCompletedMultipleAll(self):
		goal = Condition.project(iTheInternet, iHumanGenome, iSDI)
		goal.activate(0)
		
		for iProject in [iTheInternet, iHumanGenome, iSDI]:
			team(0).changeProjectCount(iProject, 1)
		
		self.assertEqual(bool(goal), True)
		
		for iProject in [iTheInternet, iHumanGenome, iSDI]:
			team(0).changeProjectCount(iProject, -1)
	
	def testRouteNone(self):
		goal = Condition.route(plots.of([(60, 30), (61, 30), (62, 30)]), iRouteRoad)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testRouteSome(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.route(area, iRouteRoad)
		goal.activate(0)
		
		for plot in area.without((60, 30)):
			plot.setRouteType(iRouteRoad)
		
		self.assertEqual(bool(goal), False)
		
		for plot in area.without((60, 30)):
			plot.setRouteType(-1)
	
	def testRouteAll(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.route(area, iRouteRoad)
		goal.activate(0)
		
		for plot in area:
			plot.setRouteType(iRouteRoad)
		
		self.assertEqual(bool(goal), True)
		
		for plot in area:
			plot.setRouteType(-1)
	

class TestCountGoals(ExtendedTestCase):

	def testBuildingNone(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 3")
	
	def testBuildingSome(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testBuildingAll(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		for tile in tiles:
			city_(tile).kill()
			
	def testBuildingMore(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testBuildingMultiplePartial(self):
		goal = Count.building((iGranary, 3), (iBarracks, 2))
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iBarracks, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["2 / 3", "2 / 2"]))
		
		for tile in tiles:
			city_(tile).kill()
	
	def testBuildingMultipleAll(self):
		goal = Count.building((iGranary, 3), (iBarracks, 2))
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iBarracks, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 2"]))
		
		for tile in tiles:
			city_(tile).kill()
	
	def testBuildingSum(self):
		goal = Count.building(sum([iGranary, iBarracks, iLibrary]), 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks, iLibrary]:
			city.setHasRealBuilding(iBuilding, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		city.kill()
	
	def testCultureLess(self):
		goal = Count.culture(500)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 500")
	
	def testCultureMore(self):
		goal = Count.culture(500)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.changeCulture(0, 1000, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 500")
		
		city.kill()
	
	def testGoldLess(self):
		goal = Count.gold(500)
		goal.activate(0)
		
		player(0).changeGold(100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "100 / 500")
		
		player(0).changeGold(-100)
	
	def testGoldMore(self):
		goal = Count.gold(500)
		goal.activate(0)
		
		player(0).changeGold(1000)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 500")
		
		player(0).changeGold(-1000)
	
	def testResourceLess(self):
		goal = Count.resource(iGold, 1)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
	
	def testResourceEnough(self):
		goal = Count.resource(iGold, 1)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testResourcesSome(self):
		goal = Count.resource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 0)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "0 / 1"]))
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testResourcesAll(self):
		goal = Count.resource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "1 / 1"]))
		
		city1.kill()
		city2.kill()
		
		plot(61, 31).setBonusType(-1)
		plot(62, 31).setRouteType(-1)
		plot(63, 31).setBonusType(-1)
	
	def testResourceSum(self):
		goal = Count.resource(sum([iGold, iSilver]), 2)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		city1.kill()
		city2.kill()
		
		plot(61, 31).setBonusType(-1)
		plot(62, 31).setRouteType(-1)
		plot(63, 31).setBonusType(-1)
	
	def testControlledResourceLess(self):
		goal = Count.controlledResource(iGold, 1)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
	
	def testControlledResourceEnough(self):
		goal = Count.controlledResource(iGold, 1)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testControlledResourcesSome(self):
		goal = Count.controlledResource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 0)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "0 / 1"]))
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testControlledResourcesAll(self):
		goal = Count.controlledResource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "1 / 1"]))
		
		city1.kill()
		city2.kill()
		
		plot(61, 31).setBonusType(-1)
		plot(62, 31).setRouteType(-1)
		plot(63, 31).setBonusType(-1)
	
	def testControlledResourceVassal(self):
		goal = Count.controlledResource(iGold, 1)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(2).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(2).getNumAvailableBonuses(iGold), 1)
		
		team(2).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(team(2).isVassal(team(0).getID()), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		team(1).setVassal(team(0).getID(), False, False)
		city.kill()
	
	def testImprovementLess(self):
		goal = Count.improvement(iCottage, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		tiles = [(60, 31), (62, 31)]
		for plot in plots.of(tiles):
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		self.assertEqual(player(0).getImprovementCount(iCottage), 2)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city.kill()
		for tile in plots.of(tiles):
			plot.setImprovementType(-1)
	
	def testImprovementMore(self):
		goal = Count.improvement(iCottage, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		tiles = [(60, 31), (62, 31), (61, 30), (61, 32)]
		for plot in plots.of(tiles):
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		self.assertEqual(player(0).getImprovementCount(iCottage), 4)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city.kill()
		for plot in plots.of(tiles):
			plot.setImprovementType(-1)
	
	def testPopulationLess(self):
		goal = Count.population(5)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(3)
		
		self.assertEqual(player(0).getNumCities(), 1)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "3 / 5")
		
		city.kill()
	
	def testPopulationMore(self):
		goal = Count.population(5)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(10)
		
		self.assertEqual(player(0).getNumCities(), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "10 / 5")
		
		city.kill()
	
	def testPopulationMultipleCities(self):
		goal = Count.population(5)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		
		city1.setPopulation(3)
		city2.setPopulation(3)
		
		self.assertEqual(player(0).getNumCities(), 2)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "6 / 5")
		
		city1.kill()
		city2.kill()
	
	def testCorporationLess(self):
		goal = Count.corporation(iSilkRoute, 2)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasCorporation(iSilkRoute, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		city.kill()
	
	def testCorporationMore(self):
		goal = Count.corporation(iSilkRoute, 2)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasCorporation(iSilkRoute, True, False, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 2")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testCorporationsSome(self):
		goal = Count.corporation((iSilkRoute, 2), (iTradingCompany, 2))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		
		city1.setHasCorporation(iSilkRoute, True, False, False)
		city2.setHasCorporation(iSilkRoute, True, False, False)
		
		city1.setHasCorporation(iTradingCompany, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["2 / 2", "1 / 2"]))
		
		city1.kill()
		city2.kill()
	
	def testCorporationsAll(self):
		goal = Count.corporation((iSilkRoute, 2), (iTradingCompany, 2))
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasCorporation(iSilkRoute, True, False, False)
			city.setHasCorporation(iTradingCompany, True, False, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["2 / 2", "2 / 2"]))
		
		for tile in tiles:
			city_(tile).kill()
	
	def testUnitLess(self):
		goal = Count.unit(iSwordsman, 3)
		goal.activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 2)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testUnitMore(self):
		goal = Count.unit(iSwordsman, 3)
		goal.activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 4)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testUnitsSome(self):
		goal = Count.unit((iSwordsman, 3), (iArcher, 3))
		goal.activate(0)
		
		swordsmen = makeUnits(0, iSwordsman, (0, 0), 3)
		archers = makeUnits(0, iArcher, (0, 0), 2)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "2 / 3"]))
		
		for unit in swordsmen:
			unit.kill(False, -1)
		
		for unit in archers:
			unit.kill(False, -1)
	
	def testUnitsAll(self):
		goal = Count.unit((iSwordsman, 3), (iArcher, 3))
		goal.activate(0)
		
		swordsmen = makeUnits(0, iSwordsman, (0, 0), 3)
		archers = makeUnits(0, iArcher, (0, 0), 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 3"]))
		
		for unit in swordsmen:
			unit.kill(False, -1)
		
		for unit in archers:
			unit.kill(False, -1)
	
	def testUnitUnique(self):
		goal = Count.unit(iSwordsman, 3)
		goal.activate(0)
		
		units = makeUnits(0, iLegion, (0, 0), 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testUnitUniqueRequirement(self):
		goal = Count.unit(iLegion, 3)
		goal.activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testNumCitiesLess(self):
		goal = Count.numCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		city.kill()
	
	def testNumCitiesMore(self):
		goal = Count.numCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			player(0).initCity(*tile)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 2")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testNumCitiesSum(self):
		goal = Count.numCities(sum([plots.rectangle((60, 30), (62, 35)), plots.rectangle((63, 30), (65, 35))]), 2)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(64, 31)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		city1.kill()
		city2.kill()
	
	def testSettledCitiesAll(self):
		goal = Count.settledCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			player(0).initCity(*tile)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testSettledCitiesSome(self):
		goal = Count.settledCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		
		city2 = player(1).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		self.assertEqual(player(0).getNumCities(), 2)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		city1.kill()
		city2.kill()
	
	def testOpenBordersLess(self):
		goal = Count.openBorders(players.of(1, 2, 3), 2)
		goal.activate(0)
		
		team(0).setOpenBorders(team(1).getID(), True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		team(0).setOpenBorders(team(1).getID(), False)
	
	def testOpenBordersMore(self):
		goal = Count.openBorders(players.of(1, 2, 3), 2)
		goal.activate(0)
		
		others = [1, 2, 3]
		for iTeam in others:
			team(0).setOpenBorders(team(iTeam).getID(), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 2")
		
		for iTeam in others:
			team(0).setOpenBorders(team(iTeam).getID(), False)
	
	def testOpenBordersDefaultOnlyAlive(self):
		goal = Count.openBorders(2)
		goal.activate(0)
		
		team(0).setOpenBorders(team(10).getID(), True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 2")
		
		team(0).setOpenBorders(team(10).getID(), False)
	
	def testSpecialistLess(self):
		goal = Count.specialist(iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testSpecialistMore(self):
		goal = Count.specialist(iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testSpecialistsSome(self):
		goal = Count.specialist((iSpecialistGreatScientist, 3), (iSpecialistGreatArtist, 3))
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "2 / 3"]))
		
		city.kill()
	
	def testSpecialistsAll(self):
		goal = Count.specialist((iSpecialistGreatScientist, 3), (iSpecialistGreatArtist, 3))
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 3"]))
		
		city.kill()
	
	def testSpecialistSum(self):
		goal = Count.specialist(sum([iSpecialistGreatScientist, iSpecialistGreatArtist]), 4)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 4")
		
		city.kill()
	
	def testAverageCulture(self):
		goal = Count.averageCulture(500)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 500, True)
		city2.setCulture(0, 1000, True)
		city3.setCulture(0, 1500, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 500")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testPopulationCitiesNotEnough(self):
		goal = Count.populationCities(10, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(12)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testPopulationCitiesLess(self):
		goal = Count.populationCities(10, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setPopulation(12)
		city2.setPopulation(10)
		city3.setPopulation(8)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testPopulationCitiesMore(self):
		goal = Count.populationCities(10, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setPopulation(16)
		city2.setPopulation(14)
		city3.setPopulation(12)
		city4.setPopulation(10)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		city4.kill()
	
	def testCultureCitiesNotEnough(self):
		goal = Count.cultureCities(500, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setCulture(0, 600, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testCultureCitiesLess(self):
		goal = Count.cultureCities(500, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 600, True)
		city2.setCulture(0, 500, True)
		city3.setCulture(0, 400, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testCultureCitiesMore(self):
		goal = Count.cultureCities(500, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 800, True)
		city2.setCulture(0, 700, True)
		city3.setCulture(0, 600, True)
		city4.setCulture(0, 500, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		city4.kill()
	
	def testCultureLevelNotEnough(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		city.setCulture(0, 5000, True)
		
		self.assertEqual(player(0).getNumCities(), 1)
		self.assertEqual(city.getCulture(0), 5000)
		self.assertEqual(city.getCultureLevel(), iCultureLevelRefined)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testCultureLevelLess(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelDeveloping), True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testCultureLevelCitiesMore(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		city4.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		city4.kill()
	
	def testCitySpecialistWithoutCity(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 3")
		
	def testCitySpecialistDifferentOwner(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 3")
		
		_city.kill()
	
	def testCitySpecialistEnough(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		_city.kill()
	
	def testCultureLevelNoCity(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1000")
	
	def testCultureLevelDifferentOwner(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined)
		goal.activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setCulture(0, 5000, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1000")
		
		_city.kill()
	
	def testCultureLevelEnough(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setCulture(0, 5000, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "5000 / 1000")
		
		_city.kill()


class TestTrackGoals(ExtendedTestCase):

	def testGoldenAgesOutside(self):
		goal = Track.goldenAges(1)
		goal.activate(0)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 8")
		
		goal.deactivate()
	
	def testGoldenAgesDuring(self):
		goal = Track.goldenAges(1)
		goal.activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 8")
		
		player(0).changeGoldenAgeTurns(-8)
		
		goal.deactivate()
		
	def testGoldenAgesAnarchy(self):
		goal = Track.goldenAges(1)
		goal.activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		player(0).changeAnarchyTurns(8)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 8")
		
		player(0).changeGoldenAgeTurns(-8)
		player(0).changeAnarchyTurns(-8)
		
		goal.deactivate()
	
	def testEraFirsts(self):
		goal = Track.eraFirsts(iClassical, 5)
		goal.activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 5")
		
		team(0).setHasTech(iLaw, False, 0, True, False)
		
		goal.deactivate()
	
	def testEraFirstsDifferentEra(self):
		goal = Track.eraFirsts(iClassical, 5)
		goal.activate(0)
		
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 5")
		
		team(0).setHasTech(iFeudalism, False, 0, True, False)
		
		goal.deactivate()
	
	def testEraFirstsNotFirst(self):
		goal = Track.eraFirsts(iClassical, 5)
		goal.activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 5")
		
		team(0).setHasTech(iLaw, False, 0, False, False)
		team(1).setHasTech(iLaw, False, 1, False, False)
		
		goal.deactivate()
	
	def testEraFirstsMultiple(self):
		goal = Track.eraFirsts((iClassical, 1), (iMedieval, 1))
		goal.activate(0)
		
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["0 / 1", "1 / 1"]))
		
		team(0).setHasTech(iFeudalism, False, 0, True, False)
		
		goal.deactivate()
	
	def testSunkShips(self):
		goal = Track.sunkShips(1)
		goal.activate(0)
		
		ourShip = makeUnit(0, iWarGalley, (3, 3))
		theirShip = makeUnit(1, iGalley, (3, 4))
		
		events.fireEvent("combatResult", ourShip, theirShip)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		ourShip.kill(False, -1)
		theirShip.kill(False, -1)
		
		goal.deactivate()
	
	def testSunkShipWinnerNotUs(self):
		goal = Track.sunkShips(1)
		goal.activate(0)
		
		theirShip = makeUnit(2, iWarGalley, (3, 3))
		thirdShip = makeUnit(1, iGalley, (3, 4))
		
		events.fireEvent("combatResult", theirShip, thirdShip)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		theirShip.kill(False, -1)
		thirdShip.kill(False, -1)
		
		goal.deactivate()
	
	def testSunkShipLandUnits(self):
		goal = Track.sunkShips(1)
		goal.activate(0)
		
		ourUnit = makeUnit(0, iSwordsman, (61, 31))
		theirUnit = makeUnit(1, iArcher, (62, 31))
		
		events.fireEvent("combatResult", ourUnit, theirUnit)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		ourUnit.kill(False, -1)
		theirUnit.kill(False, -1)
		
		goal.deactivate()
	
	def testTradeGoldPlayerGoldTrade(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		events.fireEvent("playerGoldTrade", 1, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		goal.deactivate()
	
	def testTradeGoldPlayerGoldTradeDifferent(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		events.fireEvent("playerGoldTrade", 0, 1, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		goal.deactivate()
	
	def testTradeGoldFromCities(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		city1 = player(0).initCity(57, 50)
		city2 = player(0).initCity(57, 52)
		
		player(0).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(0).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		self.assert_(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0)
		self.assert_(city2.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0)
		
		iExpectedCommerce = city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE)
		iExpectedCommerce *= player(0).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
		iExpectedCommerce /= 100
		
		self.assert_(iExpectedCommerce > 0)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "%d / 100" % iExpectedCommerce)
		
		city1.kill()
		city2.kill()
		
		player(0).setCivics(iCivicsEconomy, iReciprocity)
		player(0).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
		
		goal.deactivate()
		
	def testTradeGoldFromCitiesForeign(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		city1 = player(1).initCity(57, 50)
		city2 = player(1).initCity(57, 52)
		
		player(1).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(1).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		self.assert_(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE))
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		city1.kill()
		city2.kill()
		
		player(1).setCivics(iCivicsEconomy, iReciprocity)
		player(1).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
		
		goal.deactivate()
	
	def testTradeGoldFromDeals(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		player(0).changeGoldPerTurnByPlayer(1, -100)
		
		goal.deactivate()
	
	def testTradeGoldFromDealsForeign(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		player(1).changeGoldPerTurnByPlayer(0, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		player(1).changeGoldPerTurnByPlayer(0, -100)
		
		goal.deactivate()
	
	def testRaidGoldPillage(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testRaidGoldPillageDifferent(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 1, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testRaidGoldConquest(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		events.fireEvent("cityCaptureGold", city, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		city.kill()
		
		goal.deactivate()
	
	def testRaidGoldConquestDifferent(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		
		events.fireEvent("cityCaptureGold", city, 1, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		city.kill()
		
		goal.deactivate()
	
	def testPillage(self):
		goal = Track.pillage(1)
		goal.activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testPillageDifferent(self):
		goal = Track.pillage(1)
		goal.activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 1, 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testAcquiredCitiesAcquired(self):
		goal = Track.acquiredCities(1)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		
		events.fireEvent("cityAcquired", 1, 0, city, True, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testAcquiredCitiesBuilt(self):
		goal = Track.acquiredCities(1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		events.fireEvent("cityBuilt", city)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testPiracyGoldPillage(self):
		goal = Track.piracyGold(100)
		goal.activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testPiracyGoldBlockade(self):
		goal = Track.piracyGold(100)
		goal.activate(0)
		
		events.fireEvent("blockade", 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		goal.deactivate()
	
	def testRazes(self):
		goal = Track.razes(1)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		events.fireEvent("cityRazed", city, 0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testSlaveTradeGold(self):
		goal = Track.slaveTradeGold(100)
		goal.activate(0)
		
		events.fireEvent("playerSlaveTrade", 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		goal.deactivate()
	
	def testGreatGenerals(self):
		goal = Track.greatGenerals(1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		unit = makeUnit(0, iGreatGeneral, (61, 31))
		
		events.fireEvent("greatPersonBorn", unit, 0, city)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testGreatGeneralsOther(self):
		goal = Track.greatGenerals(1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		unit = makeUnit(0, iGreatScientist, (61, 31))
		
		events.fireEvent("greatPersonBorn", unit, 0, city)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		city.kill()
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testResourceTradeGoldFromDeals(self):
		goal = Track.resourceTradeGold(100)
		goal.activate(0)
		
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		player(0).changeGoldPerTurnByPlayer(1, -100)
		
		goal.deactivate()
	
	def testResourceTradeGoldFromDealsForeign(self):
		goal = Track.resourceTradeGold(100)
		goal.activate(0)
		
		player(1).changeGoldPerTurnByPlayer(0, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		player(1).changeGoldPerTurnByPlayer(0, -100)
		
		goal.deactivate()
	
	def testBrokeredPeace(self):
		goal = Track.brokeredPeace(1)
		goal.activate(0)
		
		events.fireEvent("peaceBrokered", 0, 1, 2)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		goal.deactivate()
	
	def testBrokeredPeaceOther(self):
		goal = Track.brokeredPeace(1)
		goal.activate(0)
		
		events.fireEvent("peaceBrokered", 2, 1, 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		goal.deactivate()
	
	def testEnslave(self):
		goal = Track.enslaves(1)
		goal.activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("enslave", 0, unit)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testConquerFrom(self):
		goal = Track.conquerFrom([iBabylonia], 1)
		goal.activate(0)
		
		city = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testConquerFromTrade(self):
		goal = Track.conquerFrom([iBabylonia], 1)
		goal.activate(0)
		
		city = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city, False, True)
		city = city_(61, 31)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testConquerFromMultiple(self):
		goal = Track.conquerFrom([iBabylonia, iHarappa, iGreece], 3)
		goal.activate(0)
		
		city1 = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city1, True, False)
		city1 = city_(61, 31)
		
		city2 = player(iHarappa).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		city3 = player(iGreece).initCity(65, 31)
		player(0).acquireCity(city3, True, False)
		city3 = city_(65, 31)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		
		goal.deactivate()


test_cases = [
	TestGetNumArgs,
	TestEventHandlers,
	TestDeferred,
	TestAggregate,
	TestArgumentProcessor,
	TestArgumentProcessorBuilder,
	TestBaseGoal,
	TestConditionGoals,
	TestCountGoals,
	TestTrackGoals,
]


suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)