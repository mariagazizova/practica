import numpy as np
import matplotlib.pyplot as plt

def my_function(x):
    return 10 + x**2 - 10 * np.cos(2 * np.pi * x)

start = -5.12
end = 5.12
step = 0.01

# Создаем массив значений x на указанном интервале
x = np.arange(start, end, step)

# Вычисляем значения функции для каждого значения x
y = my_function(x)

# Сохраняем результаты в текстовый файл
with open("result.txt", "w") as file:
    for i in range(len(x)):
        file.write("{:.4f}    {:.4f}, \n".format(x[i], y[i]))

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('График функции')
plt.grid()
plt.show()

print('Программа завершила работу.')