import matplotlib.pyplot as plt
import pickle
# Data


f = open('optimal_result2.pckl', 'rb')
obj = pickle.load(f)

#num_areas = [3, 4, 5, 6, 7, 8, 9, 10]
num_developers = [5,6,7,8,9,10]
government_profit = obj

# Creating the plot
plt.figure(figsize=(10, 5))
plt.plot(num_developers, government_profit, marker='o')

# Adding titles and labels
plt.title("Government Profit vs. Number of WSPs")
plt.ylim((0, 700))
plt.xlabel("Number of WSPs")
plt.ylabel("Government Profit")

# Showing grid
plt.grid(True)

# Display the plot
plt.savefig('WSPs.png')
