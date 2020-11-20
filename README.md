# weld-mvmt-prediction
This application predicts the distortion of flat metal stock after welding passes are applied. The inputs of the program are the measurements of the stock along the edge of the stock. The app utilizes machine learning to draw inferences from historical measurements and pass applications. The app is written in python, utilizes scikit-learn for machine learning, and the front end is created with PyQt with matplotlib embedded.

This application predicts the post weld distortion of the stock by using the initial shape data and quantity of passes as inputs.  The application is written in python and utilizes the scikit-learn package to build a regression model using lasso regularization (LassoCV). This is a machine learning application, since new initial shape and post-weld shape data are pulled from a database that is continually updated.  This data is then used to build regression models each time the app is executed.  Thus as more data is added to the database, an increase in the prediction score (coefficient of determination (R^2) ) is anticipated   The front end is created with PyQt 5 with the matplotlib library embedded to provide the user with a visualization of the post-weld condition.  The red dotted line presents the range of acceptable distortion within the part.  The python output is streamed into a PyQt text box and displays the coefficient of determination of the prediction for each segment.  

All units are in millimeters (mm).


![Machine Learning Framework](framework.png)

The following graphic presents a screenshot of the application.

![GUI Front End](front_end.png)
edges
