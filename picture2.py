import matplotlib.pyplot as plt
import pickle
# Data


f = open('optimal_result3.pckl', 'rb')
obj = pickle.load(f)

num_areas = [3, 4, 5, 6, 7, 8, 9, 10]
#num_developers = [5,6,7,8,9,10]
government_profit = obj

# Creating the plot
plt.figure(figsize=(10, 5))
plt.plot(num_areas, government_profit, marker='o')

# Adding titles and labels
plt.title("Government Profit vs. Number of Regions")
plt.ylim((0, 700))
plt.xlabel("Number of Regions")
plt.ylabel("Government Profit")

# Showing grid
plt.grid(True)

# Display the plot
plt.savefig('Regions.png')
