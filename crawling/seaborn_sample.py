import seaborn as sns
from matplotlib import pyplot as plt

x = [1, 3, 2, 5]
y = [4, 3, 2, 1]

# 꺽은선 그래프
sns.lineplot(x=x, y=y)
plt.show()

# 막대 그래프
sns.barplot(x=x, y=y)
plt.show()

# 그래프 꾸미기
sns.lineplot(x=x, y=y)

plt.title("Line Plot")
plt.xlabel("X Label")
plt.xlabel("Y Label")

plt.ylim(0, 10)
plt.show()
