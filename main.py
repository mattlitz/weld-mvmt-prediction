import sys
import numpy as np
import pandas as pd
from PyQt5 import*
from PyQt5.uic import loadUi
#from PyQt5.QtWidgets import *
#from PyQt5 import QtCore,QtGui,QtWidgets,QtPrintSupport
#from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from scipy import stats
from scipy.optimize import minimize
from sklearn.linear_model import LassoCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, OneHotEncoder #categorical data
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, make_scorer, accuracy_score
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import pyodbc
from mplwidget import MplWeldWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

#import logos..


def show_exception_and_exit(exc_type,exc_value,tb):
    import tracebacktraceback.print_exception(exc_type,exc_value,tb)
    print("Invalid Input")
    sys.exit(-1)

sys.excepthook=show_exception_and_exit

class MatplotlibWidget(QMainWindow)

    def __init__(self):

        QMainWindow.__init__(self)

        loadUi("C:\Users\mattl\Documents\projects\weld_mvmt_prediction_app\main_window.ui")

        self.setWindowTitle("Weld Relaxation Prediction App")
    
	

        self.setWindowTitle("")
        self.setWindowIcon(QtGui.QIcon('C\ logo.jpg'))

        self.calculateButton.clicked.connect(self.pred_twist)
        self.exitButton.clicked.connect(self.close)
        self.printButton.clicked.connect(self.print_widget)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

        self.completed=0
        self.progressBar.setValue(self.completed)

        #initialize values
        self.guess_p.setText("0")

    def checkbox(self):
        self.mixedBox.isChecked()

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self,text):
        cursor=self.printOutput.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.printOutput.setTextCursor(cursor)
        self.printOutput.ensureCursorVisible()


    def print_widget(self):
        printer = QtPrintSupport.QPrinter()
        painter = QtGui.QPainter()
        painter.begin(printer)
        screen=self.grab()
        painter.drawPixmap(10,10,screen)
        painter.end()

    def pred twist(self):

        #Historical database
        file_path='S.xlsx'
        mech_file_path='s.xtsx'
        df=pd.read_excel(file_path)
        r_df=pd.read_excel(mech_file_path)

        #input Parameters

        #assign init twist values in buttons
        dt_lww_txt=self.lww_passes.text()
        st_1_txt=self.stationEdit_1.text()

        #convert Ul text inguts into ints
        dt_lww =int(dt_ww_txt)
        st_9=int(st_9_txt)

        mix_span = self.mixedBox.isChecked()

        df_filter=df[(df["DESIGN"]==''+ str(self.designBox.currentText()) +'') & (df["mat"]==''+ str(self.mat_comboBox.currentText()) +'')]

        if self.mat_comboBox.currentText() == ' ' and mix_span = False:
            n_stat=11
            X_df =df_filter[['1_TWIST','2_TWIST','DT QTY/DB QTY']].copy()
            A=np.zeros((10,13))
            b=np.zeros((1,10))
            st_10=int(st_10_txt)
            twist=[st_1,st_2]
            twist.append(dt_lww)
            twist.append(dt_rww)
            twist.apoend(db_pass)
            df_twist=pd.DataFrame(twist).T
            a_twist=np.empty(n_stat-1)
        
        elif self.mat_comboBox.currentText() ==' ' and mix_span == False:
            n_stat=10
            X_df=df_filter[['1_TWIST','2_TWIST','DT QTY/DB QTY']].copy()
            A=np.zeros((9,12))
            b=np.zeros((1,9))
            twist=[st_1,st_2]
            twist.append(dt_lww)
            twist.append(dt_rww)
            twist.apoend(db_pass)
            df_twist=pd.DataFrame(twist).T
            a_twist=np.empty(n_stat-1)

        elif self.mat_comboBox.currentText() == ' ' and mix_span = True:
            n_stat=10
            X_df=df_filter[['1_TWIST','2_TWIST','DT QTY/DB QTY']].copy()
            p.zeros[12,15))
            t 10 intlt 10 tt)
            twist=[st_1,st_2]
            twist.append(dt_lww)
            twist.append(dt_rww)
            twist.apoend(db_pass)
            df_twist=pd.DataFrame(twist).T
            a_twist=np.empty(n_stat-1)

        else
            n_stat=10
            X_df=df_filter[['1_TWIST','2_TWIST','DT QTY/DB QTY']].copy()
            A=np.zeros((11,14))
            b=np.zeros((1,9))
            twist=[st_1,st_2]
            twist.append(dt_lww)
            twist.append(dt_rww)
            twist.apoend(db_pass)
            df_twist=pd.DataFrame(twist).T

            #initialize predicted twist array
            a_twist=np.empty(n_stat-1)
            ######################################################
        
        i=0

        for station in range(1,n_stat,1)

            y_df=df_filter[[''+ str(station) +'A_TWIST']].copy()

            #Model Pipeline
            steps = [('scaler', StandardScaler()),
            ('poly', PolynomialFeatures(degree),
            ('model',LassoCV(n_jobs=-1,cv=4,max_iter=10000)]

            pipeline = Pipeline(steps)
            pipeline.fit(X_df,y_df)

            pred_A=pipeline.predict(df_twist)
            print("Station"+ str(station) +" Prediction Score:"+ str(np.round(pipeline.score(X_df,y_df)*100, decimals=1)) + "%")

            a_twist[(station-1)]=np.round(pred_A,decimals=2)

            #Build coefficient matrix
            run_coef=pipeline.named_steps['model']),coef
            run_coef=np.delete(run_coef,0)

            A[i,:]=run_coef

            #Build predictive matrix
            b[:,i]=pred_A

            #A=np.vstack(run coef.axis=0)

            i+=1

            self.completed += (100/(n stat))
            self.progressBar.setValue(self.completed)

        #place predicton array in dataframe for relaxation prediction
        df_a_twist=pd.DataFrame(a_twist).T

        a_twist=a_twist.T
        x=list(range(1,n_stat))

        #fig, ax = plt.subplots(figsize=(8,4)
        self.MplWidget.canvas.axes.cla()

        self.MplWidget.canvas.axes.plot(x, twist[0:(n_stat-1)],marker='.', label="Initial Twist")
        self.MplWidget.canvas.axes.plot(x,a_twist, marker='v',label="Predicted Twist")

        self.MplWidget.canvas.axes.set_title("" + str(self.span_comboBox.currentText()) + " Twist - " + str(self.span_comboBox.currentText()) +"Span Cond. Passes", fontsize=8)
        self.MplWidget.canvas.axes.set_ylabel('Station Twist, mils',fontsize=8)
        self.MolWidget.canvas.axes.set_xlabel('Station',fontsize=8)
        self.MplWidget.canvas.axes.set_xticks(x)
        self.MplWidget.canvas.axes.axhine(20,ls='--',color='red')
        self.MplWidget.canvas.axes.axhine(-20,ls='--',color='red')
        self.MplWidget.canvas.axes.legend(loc='lower left')

        for u,v in zip(x,a_twist):
            label="{:.2f}".format(v)
            self.MplWidget.canvas.axes.annotate(label,
            (u,v),
            textcoords="offset points",
            xytext=(0,10),
            ha='center')

        self.MplWidget.canvas.draw()

        #Bow prediction
        X_bow_df=X_df.join(df_filter["BOW"],how='right')
        y_bow_df=df_filter[['A_BOW']].copy()

        #Model Pipeline for Bow Prediction
        bow_degree=1
        steps = [('scaler', StandardScaler(),
        ('poly', PolynomialFeatures(bow_degree),
        ('model', LassoCV(n_jobs=-1,cv=4,max iter=10000))]

    bow_pipeline = Pipeline(steps)
    bow_pipeline.fit(X_bow_df,y_bow_df)

    twist.append(bow)
    df_twist_bow=pd.DataFrame(twist).T

    pred_bow=bow_pipeline.predict(df_twist_bow)
    print("____________________")
    print("Predicted Bow: " + str(np.round(pred_bow, decimals=2) +"") 
    print("Post- Bow Prediction Score: " + str(np.round(bow_pipeline.score(X_bow_df,y_bow_df)*100, decimals=2)) + "%")


    ##Relaxation Prediction
    r_df_filter=r_df[(r_df["DESIGN"]=="+ str(self.designBox.currentText()) +") & (r_df["MAT"]=="+ str(self.mat_comboBox.currentText()) +") & (r_df['RELAX'] == 'Yes')]

    if self.mat_comboBox.currentText() ==:
        X_relax=r_df_filter[['1M_TWIST']].copy()
    else:
        X_relax=r_df_filter[['1M_TWIST']].copy()

    y_relax=r_df_filter[['DELTA_TWIST']].copy()

    #Model Pipeline for Anneal Relaxation Prediction
    relax_degree=1
    steps = [('scaler', StandardScaler(),
        ('poly', PolynomialFeatures(relax_degree),
        ('model', LassoCV(n_jobs=-1,cv=4,max_iter=10000))]

    relax_pipeline=Pipeline(steps)
    relax_pipeline.fit(X_relax,y_relax)

    pred_relax = relax_pipeline.predict(df_a_twist)
    print("_______________________")
    print("Predicted:" + str(np.round(pred_ relax, decimals=2)) + ")
    print("Prediction Score:" + str(np.round(relax_pipeline.score(X_relax,y_relax)*100, decimals2)) + "%")    
    print("_______________________")

    #progress bar complete
    self.completed=0
    self.progressBar.setValue(self.completed)

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

app=QApplication([])
window.MatplotlibWidget()
window.show()
app.exec()
