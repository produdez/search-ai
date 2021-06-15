
# class Dick:
#     def __init__(self,a,b):
#         self.a = a
#         self.b = b
#     def __eq__(self, o) :
#         return self.a == o.a and self.b == o.b
#     def __str__(self):
#         return '({},{})'.format(self.a, self.b)

# l1 = [Dick(1,2), Dick(2,3), Dick(4,5)]
# l2 = [Dick(1,2), Dick(1,2)]
# obj = Dick(1,2)
# print(obj in l1)

# l1.remove(obj)
# print([str(x) for x in l1])

# l2.remove(obj)
# print([str(x) for x in l2])


from scipy.stats import rv_discrete  
import numpy
values = numpy.array([1.1, 2.2, 3.3])
probabilities = [0.2, 0.5, 0.3]

distrib = rv_discrete(values=(range(len(values)), probabilities))  # This defines a Scipy probability distribution

print(distrib.rvs(size=1))  # 10 samples from range(len(values))
