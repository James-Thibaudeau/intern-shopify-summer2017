import time
import internProblem, internProblemAsync

'''
I wrote this to test the time each version of the Shopify
Internship problem, when running this file one can clearly
see the difference in time between the two solutions.
'''

print("\n********** Testing Synchronous ****************\n")
time_start = time.clock()
internProblem.start('count', 'orders')
time_end = (time.clock() - time_start) *1000
print("\n**************************\n")
print("Done in %d ms." %(time_end))

print("\n********** Testing Asynchronous ****************\n")
time_start = time.clock()
internProblemAsync.start('count', 'orders')
time_end = (time.clock() - time_start) *1000
print("\n**************************\n")
print("Done in %d ms." %(time_end))