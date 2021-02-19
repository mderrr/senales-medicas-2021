import pandas, numpy
import matplotlib.pyplot as plot

df = pandas.read_csv("./Clase 4/data_example1.csv")

df.plot(x="Time", y=["S1", "S3"], kind="line")
#plot.show()

x = df["S1"]
y = df["S3"]

N = len(x)
rxy = numpy.sum((x - numpy.mean(x)) * (y - numpy.mean(y)))

Prxy = rxy / ((N - 1) * numpy.sqrt(numpy.var(x) * numpy.var(y)))

plot.title("Pearso Coeff" + str(round(Prxy, 2)))

plot.show()

print(Prxy)