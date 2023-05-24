import pandas as pd
from sklearn import preprocessing
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout,QHBoxLayout, QGridLayout, QSplitter, QFrame, QLineEdit, QPlainTextEdit, QComboBox, QFileDialog, QGroupBox,QMessageBox, QLabel, QRadioButton, QTextEdit, QDialog)
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering as AggCluster
import Plot
import Dendrogram


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.CSV_DATA = None
        self.start_box()

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        grid = QGridLayout(self.centralwidget)
        grid.addWidget(self.analysis_box(), 0, 0)
        grid.addWidget(self.description_box(), 1, 0)
        grid.addWidget(self.preview_box(), 0, 1, 2, 1)
        self.setLayout(grid)

        self.setGeometry(350, 175, 1200, 800)
        self.setWindowTitle('Clusterics. Program for cluster analysis.')

    def file_open(self):
        dataFilePath, _ = QFileDialog.getOpenFileName(self, 'Clusterics. Upload a file', '', 'All Files (*);;Text Files (*.csv)', options=QFileDialog.DontUseNativeDialog)

        if _:
            self.dataEdt.setText(str(dataFilePath))
        self.dataFileName = str(dataFilePath.split('/')[-1])

        print(self.dataFileName, ' uploaded!')

        df = pd.read_csv(dataFilePath, sep='[;\t,]', engine='python')
        df = self.standarize(df)
        self.CSV_DATA = df.iloc[:, 1:].values.tolist()
        print(self.CSV_DATA)


    def method_input(self):
        self.method_input = self.comboBox1.currentText()
        return self.method_input

    def metric_input(self):
        self.metric_input = self.comboBox2.currentText()
        return self.metric_input

    def cluster_numb_input(self):
        self.cluster_numb_input = self.clustersEdt.text()
        return self.cluster_numb_input

    def title_input(self):
        self.title_input = self.titleEdt.text()
        return self.title_input

    def author_input(self):
        self.author_input = self.authorEdt.text()
        return self.author_input

    def desc_input(self):
        self.desc_input = self.descEdt.toPlainText()
        return self.desc_input

    # def plot_choice(self):
    #     if self.radiobtn1.isChecked():
    #         return 'Dendrogram'
    #     elif self.radiobtn2.isChecked():
    #         return 'Scatter plot'

    def run_analysis(self):
        # self.clusters = self.clustersEdt.textChanged.connect(self.cluster_numb_input)

        print('Method: ', self.method_input)
        print('Metric: ', self.metric_input)
        print('Number of clusters: ', self.cluster_numb_input())
        # print('Type of chart: ', self.plot_choice())

        if self.method_input == 'k-means':
            return self.k_mean(self.CSV_DATA)
        elif self.method_input == 'Hierarchical agglomeration method':
            return self.agnes(self.CSV_DATA)
        elif self.method_input == 'Method of Wrocław taxonomy':
            return self.slink(self.CSV_DATA)


    def metadata(self):
        self.title = ('Title:', str(self.title_input()))
        self.author = ('Author:', str(self.author_input()))
        self.desc = ('Description:', str(self.desc_input()))

        # print(title)
        # print(author)
        # print(desc)

    def start_box(self):
        startInfo = QMessageBox()
        startInfo.setText('\nIt is a program for analyzing concentrations using the methods of your choice. After the analysis, you will receive a graphical representation of your data in the form of a graph or a ready-made Report.\n')
        startInfo.setWindowTitle('Welcome to Clusterics!')
        startInfo.exec_()

    def analysis_box(self):
        """ Adding data to analysis. Choice of method of analysis. """
        groupBox = QGroupBox('Analysis')

        # labels
        dataLbl = QLabel('Load data', self)
        methodLbl = QLabel('Choose a method of analysis', self)
        metricLbl = QLabel('Choose a measure of distance', self)
        clustersLbl = QLabel('Specify the number of clusters to create', self)
        # plotLbl = QLabel('Select chart type', self)

        # layout labels
        self.layoutT = QGridLayout()
        self.layoutT.addWidget(dataLbl)
        self.layoutT.addWidget(methodLbl)
        self.layoutT.addWidget(metricLbl)
        self.layoutT.addWidget(clustersLbl)
        # self.layoutT.addWidget(plotLbl)
        self.layoutV = QVBoxLayout()

        # data loading field
        self.dataEdt = QLineEdit()
        self.dataEdt.setText('Select data...')
        self.addBtn = QPushButton('&Add', self)
        self.addBtn.clicked.connect(self.file_open)
        self.clustersEdt = QLineEdit(self)


        # drop-down lists
        self.comboBox1 = QComboBox()
        self.comboBox1.setObjectName('Methods')
        self.comboBox1.addItem('k-means')
        self.comboBox1.addItem('Hierarchical agglomeration method')
        self.comboBox1.addItem('Method of Wrocław taxonomy')

        self.comboBox2 = QComboBox()
        self.comboBox2.setObjectName('Measure')
        self.comboBox2.addItem('Euclidean distance')
        self.comboBox2.addItem('Cosine similarity')
        self.comboBox2.addItem('Manhattan distance')

        self.comboBox1.activated.connect(self.method_input)
        self.comboBox2.activated.connect(self.metric_input)

        # # checkbox
        # self.radiobtn1 = QRadioButton('Dendrogram', self)
        # # self.checkbox1.stateChanged.connect(self.dzialanie)
        # self.radiobtn2 = QRadioButton('Dot plot', self)
        # # self.checkbox2.stateChanged.connect(self.dzialanie)
        # self.radiobtn1.setChecked(True)

        # layout element
        self.layoutT.addWidget(self.dataEdt, 0, 1)
        self.layoutT.addWidget(self.addBtn, 0, 2)
        self.layoutT.addWidget(self.comboBox1, 1, 1, 1, 1)
        self.layoutT.addWidget(self.comboBox2, 2, 1, 1, 1)
        self.layoutT.addWidget(self.clustersEdt, 3, 1)
        # self.layoutT.addWidget(self.radiobtn1, 4, 1, 1, 1)
        # self.layoutT.addWidget(self.radiobtn2, 5, 1, 1, 1)
        self.layoutV.addLayout(self.layoutT)

        # button
        self.startBtn = QPushButton('&Start', self)
        self.startBtn.clicked.connect(self.run_analysis)
        self.layoutV.addWidget(self.startBtn)

        groupBox.setLayout(self.layoutV)

        return groupBox


    def description_box(self):
        """ Add title, author and data description. Optional. """
        groupBox = QGroupBox('Report data')

        # labels
        titleLbl = QLabel('Title', self)
        authorLbl = QLabel('Author', self)
        descLbl = QLabel('Description', self)

        # layout labels
        self.layoutT = QGridLayout()
        self.layoutT.addWidget(titleLbl)
        self.layoutT.addWidget(authorLbl)
        self.layoutT.addWidget(descLbl)
        self.layoutV = QVBoxLayout()

        # edit fields
        self.titleEdt = QLineEdit(self)
        self.authorEdt = QLineEdit(self)
        self.descEdt = QPlainTextEdit(self)
        self.descEdt.resize(50, 100)

        # layout editing fields
        self.layoutT.addWidget(self.titleEdt, 0, 1)
        self.layoutT.addWidget(self.authorEdt, 1, 1)
        self.layoutT.addWidget(self.descEdt, 2, 1)
        self.layoutV.addLayout(self.layoutT)

        # button
        self.createBtn = QPushButton('&Create', self)
        # self.createBtn.resize(320, 20)
        # self.createBtn.move(50, 50)
        self.createBtn.clicked.connect(self.metadata)
        self.layoutV.addWidget(self.createBtn)

        groupBox.setLayout(self.layoutV)

        return groupBox

    def preview_box(self):
        """ creating charts/report """
        groupBox = QGroupBox('Preview')

        # creating"charts" tabs and "report"
        self.tabs = QTabWidget()
        self.tab1()
        self.tab2()

        # self.tabs.addTab(self.tab1, 'Charts')
        # self.tabs.addTab(self.tab2, 'Report')

        # create "save", "print", "new session"buttons
        saveBtn = QPushButton('&Save', self)
        printBtn = QPushButton('&Print', self)
        newSessionBtn = QPushButton('&New session', self)

        # add widgets to layout
        self.layoutT = QGridLayout()
        self.layoutT.addWidget(self.tabs, 1, 3, 100, 95)

        layoutH = QHBoxLayout()
        layoutH.addWidget(saveBtn)
        layoutH.addWidget(printBtn)
        layoutH.addWidget(newSessionBtn)

        layoutV = QVBoxLayout()
        layoutV.addLayout(self.layoutT)
        layoutV.addLayout(layoutH)
        groupBox.setLayout(layoutV)

        return groupBox

    def tab1(self):
        tab1 = QWidget()
        tab1.layout = QHBoxLayout()

        plotDataBtn = QPushButton('Plot original dataset')
        plotDataBtn.clicked.connect(self.plot_data)

        '''Button layout section'''
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(plotDataBtn)
        btn_layout.addStretch(1)

        '''Page layout section '''
        left = QFrame()
        left.setLayout(btn_layout)
        left.setLayout(btn_layout)

        self.figure = Plot.Plot()

        # combine the buttons and the canvas in a splitter layout
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(left)
        self.splitter1.addWidget(self.figure)
        self.splitter1.setSizes([10, 800])

        # add the last splitter to the layout
        tab1.layout.addWidget(self.splitter1)
        tab1.setLayout(tab1.layout)
        self.tabs.addTab(tab1, 'Charts')

    def tab2(self):
        tab2 = QWidget()
        tab2.layout = QHBoxLayout()

        self.editor = QPlainTextEdit()
        print(self.metadata())
        # print(self.title_input)
        # self.editor.insertPlainText('loremipsum')
        # self.editor.document().setPlainText(self.metadata())
        # self.editor = QTextEdit(self)
        # self.editor.textChanged.connect(

        print(self.title_input)

        self.editor.setReadOnly(True)
        tab2.layout.addWidget(self.editor)

        tab2.setLayout(tab2.layout)
        self.tabs.addTab(tab2, 'Report')


    def plot_data(self):
        print('Data to plot: \n', self.CSV_DATA)
        if self.CSV_DATA:
            print('Ploting ... ')
            self.figure.plot(self.CSV_DATA)


    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Communication', 'Are you sure you want to exit the program?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # def saveFileDialog(self):
    #     options = QFileDialog.Options()

    #     options |= QFileDialog.DontUseNativeDialog
    #     fileName, _ = QFileDialog.getSaveFileName(self, "Clusterics. Save a file", "", "All Files (*);;Text Files (*.csv)", options=options)
    #     if fileName:
    #         print(fileName)

    def standarize(self, x):

        standscaler = preprocessing.StandardScaler()
        standscaler_df = standscaler.fit_transform(x)
        st_df = pd.DataFrame(standscaler_df)
        return st_df
        # print("Standarized data: \n", st_df)
        # print("Average: ", st_df.mean(axis=0))
        # print("Standard deviation: \n", st_df.std(axis=0))

    def k_mean(self, name):

        cluster_num = int(self.cluster_numb_input)
        self.kmeans = KMeans(n_clusters=cluster_num, init='k-means++', max_iter=300, n_init=10, random_state=0)
        self.y_kmeans = self.kmeans.fit_predict(name)
        print(self.kmeans)
        print(self.y_kmeans)

        self.figureK = Dendrogram.Dendrogram()
        self.figureK.plot_kmean(name, k=cluster_num)
        self.splitter1.addWidget(self.figureK)

    def agnes(self, name):

        cluster_num = int(self.cluster_numb_input)

        if self.metric_input == 'Euclidean distance':
            self.agnes = AggCluster(n_clusters=cluster_num, affinity='euclidean', compute_full_tree='auto', linkage='average')
        elif self.metric_input == 'Cosine similarity':
            self.agnes = AggCluster(n_clusters=cluster_num, affinity='cosine', compute_full_tree='auto',
                                    linkage='average')
        elif self.metric_input == 'Manhattan distance':
            self.agnes = AggCluster(n_clusters=cluster_num, affinity='manhattan', compute_full_tree='auto',
                                    linkage='average')

        self.y_agnes = self.agnes.fit_predict(name)
        print(self.agnes)
        print(self.y_agnes)

        self.figureA = Dendrogram.Dendrogram()
        self.figureA.plot_agnes(name)
        self.splitter1.addWidget(self.figureA)

    def slink(self, name):

        cluster_num = int(self.cluster_numb_input)

        if self.metric_input == 'Euclidean distance':
            self.slink = AggCluster(n_clusters=cluster_num, affinity='euclidean', compute_full_tree='auto', linkage='single')

        elif self.metric_input == 'Cosine similarity':
            self.slink = AggCluster(n_clusters=cluster_num, affinity='cosine', compute_full_tree='auto',
                                    linkage='single')
        elif self.metric_input == 'Manhattan distance':
            self.slink = AggCluster(n_clusters=cluster_num, affinity='manhattan', compute_full_tree='auto',
                                linkage='single')

        self.y_slink = self.slink.fit_predict(name)
        print(self.slink)
        print(self.y_slink)

        self.figureS = Dendrogram.Dendrogram()
        self.figureS.plot_slink(name)
        self.splitter1.addWidget(self.figureS)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())