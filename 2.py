import numpy
import wget
import csv
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
from scipy import special, constants
from numpy import arange, abs, sum
from matplotlib import pyplot as plt

url = "https://jenyay.net/uploads/Student/Modelling/task_02.csv"
var = 1
if os.path.exists("test.txt") == 0:
    wget.download(url, r"test.txt")
with open("test.txt", "r") as file:
    for i in range(0, var, 1):
        next(file)

    line = next(file)
    arr = list(map(float, line.split()))
    arr.pop(0)
print(arr)

"Присвоение значений диаметру сферы, а также минимальной и максимальной частоте соответсвенно"
D = float(arr[0])
fmin = float(arr[1])
fmax = float(arr[2])

# задаем константы для рассчетов
n_end = 10
dx = 100000
r = D / 2
f_arange = arange(fmin, fmax, dx)
wavelength_arange = constants.c / f_arange
k_arange = 2 * constants.pi / wavelength_arange


# h
def f4(n, x):
    return special.spherical_jn(n, x) + 1j * special.spherical_yn(n, x)


# b
def f3(n, x):
    return (x * special.spherical_jn(n - 1, x) - n * special.spherical_jn(n, x)) / (
        x * f4(n - 1, x) - n * f4(n, x)
    )


# a
def f2(n, x):
    return special.spherical_jn(n, x) / f4(n, x)


# ЭПР
rcs_arange = (
    (wavelength_arange**2)
    / numpy.pi
    * (
        abs(
            sum(
                [
                    ((-1) ** n)
                    * (n + 0.5)
                    * (f3(n, k_arange * r) - f2(n, k_arange * r))
                    for n in range(1, n_end)
                ],
                axis=0,
            )
        )
        ** 2
    )
)


counter = 0

# Создаем корневой элемент xml документа с атрибутом version и encoding
root = ET.Element("data")


for f, lambda1, rcs in zip(f_arange, wavelength_arange, rcs_arange):
    row = ET.SubElement(root, "row")
    ET.SubElement(row, "freq").text = str(f) + " Гц"
    ET.SubElement(row, "lambda").text = str(lambda1) + " м"
    ET.SubElement(row, "rcs").text = str(rcs) + " м^2"

tree = ET.ElementTree(root)

# Преобразуем XML в строку с отступами и переводами строк
xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
dom = xml.dom.minidom.parseString(xml_string)
formatted_xml = dom.toprettyxml(indent="  ")  # два пробела для отступ

with open("./result/data.xml", "w", encoding="utf-8") as file:
    file.write(formatted_xml)

# Строим график
plt.xlabel("$f, Гц*10^8$")
plt.ylabel(r"$\sigma, м^2$")
plt.plot(f_arange, rcs_arange)
plt.grid()
plt.show()
