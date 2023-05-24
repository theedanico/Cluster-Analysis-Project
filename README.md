# clusterAnalysis

The aim of the project is to create a desktop application that reads in the input data, clusters them with a method choosed by the user and returns results in a form of a graph or a report.

## How to run

Install dependecies:

```
pip install numpy
pip install pandas
pip install PyQt5
pip install sklearn

```

Copy `.csv` file to project folder

Run program by:

```
python Window.py
```

## Dataset used in a draft of application

Index Gini. The file is available on the internet (https://www.gks.ru). Gini index is a measure of population differentiation by income level. As of now, I am using data from 1995 to 2018. 80 regions. The task is being regarded as Time series clustering. So one region is a serie of 24 time points.
