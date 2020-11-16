import sys
import numpy as np
import pandas as pd
import seaborn as sns
import pyodbc

from PyQt5 import*
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import*
from PyQt5 import QtCore,QtGui,QtWidgets,QtPrintSupport
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#from scipy import stats
#from scipy.optimize import minimize
from sklearn.linear_model import LassoCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures #OneHotEncoder #categorical data
#from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, make_scorer, accuracy_score
import warnings
warnings.filterwarnings('ignore')
from mplweldwidget import MplWeldWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

#detail resource file detail.py
import detail


def show_exception_and_exit(exc_type,exc_value,tb):
    import traceback
    traceback.print_exception(exc_type,exc_value,tb)
    print("Invalid Input")
    sys.exit(-1)

sys.excepthook=show_exception_and_exit

class WeldPredictionMain(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        loadUi(r"C:\Users\mattl\Documents\projects\weld-mvmt-prediction\main_window.ui",self)

        self.setWindowTitle("Weld Movement Prediction")
        #self.setWindowIcon(QtGui.QIcon('C:\logo.jpg'))

        self.calculateButton.clicked.connect(self.pred_twist)
        self.exitButton.clicked.connect(self.close)
        self.printButton.clicked.connect(self.print_widget)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

        self.completed=0
        self.progressBar.setValue(self.completed)

        #initialize alloy options
        self.alloy_comboBox.addItem("Ti-6Al-4V")
        self.alloy_comboBox.addItem("Mg AZ80A")

    
    def __del__(self):
        sys.stdout = sys.__stdout__

    
    #function for output to "printOutput" label
    def normalOutputWritten(self,text):
        cursor=self.printOutput.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.printOutput.setTextCursor(cursor)
        self.printOutput.ensureCursorVisible()

    #prints screenshot of app
    def print_widget(self):
        printer = QtPrintSupport.QPrinter()
        painter = QtGui.QPainter()
        painter.begin(printer)
        screen=self.grab()
        painter.drawPixmap(10,10,screen)
        painter.end()

    #main function
    def pred_twist(self):

        #Access historical database - the following code enables access to an existing s
        #username = "_______"
        #password = "_______"

        #sql = ("SELECT * FROM Table")
        #cnxn = pyodbc.connect('Driver={database};SERVER=server; Uid=username;Pwd=password')
        #df = pd.read_sql(sql, cnxn)

        #Historical data located in excel spreadsheet
        file_path=r'C:\Users\mattl\Documents\projects\historical_data.csv'
        df=pd.read_csv(file_path)

        #Input parameters

        #assign initial twist values from UI inputs
        passQty_txt=self.passQtyEdit.text()
        seg1_txt=self.seg1Edit.text()
        seg2_txt=self.seg2Edit.text()
        seg3_txt=self.seg3Edit.text()
        seg4_txt=self.seg4Edit.text()
        seg5_txt=self.seg5Edit.text()
        seg6_txt=self.seg6Edit.text()
        seg7_txt=self.seg7Edit.text()

        #convert UI text inputs into floats
        passQty = int(passQty_txt)
        seg1=float(seg1_txt)
        seg2=float(seg2_txt)
        seg3=float(seg3_txt)
        seg4=float(seg4_txt)
        seg5=float(seg5_txt)
        seg6=float(seg6_txt)
        seg7=float(seg7_txt)

        #build input list and transform into dataframe
        twist=[seg1,seg2,seg3,seg4,seg5,seg6,seg7,passQty]
        df_twist=pd.DataFrame(twist).T

        #filters historical data by alloy selected
        alloy_filter=df[(df['ALLOY']==''+ str(self.alloy_comboBox.currentText()) +'')]

        #creates "X" dataframe for future regression
        X_df = alloy_filter[['SEG1','SEG2','SEG3','SEG4','SEG5','SEG6','SEG7','PASS_QTY']].copy()

        #number of segments with measurements
        n_seg = 7          

        #initialize predicted twist array
        a_twist=np.empty(n_seg)
      
        i=0

        #iterates over each station to predict twist using historic data
        for segment in range(1,n_seg+1,1):

            y_df=alloy_filter[['A_SEG' + str(segment) +'']].copy()


            #number of polynomial degrees
            degree = 2 

            #Model Pipeline
            steps = [('scaler', StandardScaler()),
            ('poly', PolynomialFeatures(degree)),
            ('model',LassoCV(n_jobs=-1,cv=4,max_iter=10000))]

            pipeline = Pipeline(steps)
            pipeline.fit(X_df,y_df)

            pred_A = pipeline.predict(df_twist)
            print("Segment "+ str(segment) +" Prediction Score:"+ str(np.round(pipeline.score(X_df,y_df)*100, decimals=1)) + "%")

            a_twist[(segment-1)]=np.round(pred_A,decimals=2)

            #Build coefficient matrix
            run_coef=pipeline.named_steps['model'].coef_
            run_coef=np.delete(run_coef,0)

            i+=1

            self.completed += (100/(n_seg))
            self.progressBar.setValue(self.completed)

        

        a_twist=a_twist.T
        x=list(range(1,n_seg+1))

        #fig, ax = plt.subplots(figsize=(8,4))
        self.MplWeldWidget.canvas.axes.cla()
        self.MplWeldWidget.canvas.axes.plot(x, twist[0:(n_seg)],marker='.', label="Initial Twist")
        self.MplWeldWidget.canvas.axes.plot(x,a_twist, marker='v',label="Predicted Twist")
        self.MplWeldWidget.canvas.axes.set_title("Predicted Twist per Segment", fontsize=10)
        self.MplWeldWidget.canvas.axes.set_ylabel('Twist, mm',fontsize=8)
        self.MplWeldWidget.canvas.axes.set_xlabel('Segment',fontsize=8)
        self.MplWeldWidget.canvas.axes.set_xticks(x)
        self.MplWeldWidget.canvas.axes.axhline(0.75,ls='--',color='red')
        self.MplWeldWidget.canvas.axes.axhline(-0.75,ls='--',color='red')
        self.MplWeldWidget.canvas.axes.legend(loc='lower left')

        for u,v in zip(x,a_twist):
            label="{:.2f}".format(v)
            self.MplWeldWidget.canvas.axes.annotate(label,
            (u,v),
            textcoords="offset points",
            xytext=(0,10),
            ha='center')

        self.MplWeldWidget.canvas.draw()

        #progress bar completion update
        self.completed=0
        self.progressBar.setValue(self.completed)

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

app=QApplication([])
window=WeldPredictionMain()
window.show()
app.exec()