# Check the versions of libraries
# Python version
import os
#import joblib
import pickle

from azureml.core import Workspace, Run
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, plot_confusion_matrix)
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import sys

# import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import scipy
import sklearn
import os
from sklearn import model_selection



run = Run.get_context()
if (run.id.startswith('OfflineRun')):
	os.environ['AZUREML_DATAREFERENCE_irisdata'] = '.\sample_data.csv'
	os.environ['AZUREML_DATAREFERENCE_model_output'] = '.\model_output'

print('======================================')
print('Python:      {}'.format(sys.version))
print('scipy:       {}'.format(scipy.__version__))
print('numpy:       {}'.format(np.__version__))
print('matplotlib:  {}'.format(matplotlib.__version__))
print('pandas:      {}'.format(pd.__version__))
print('sklearn:     {}'.format(sklearn.__version__))
print('======================================')


# Load dataset
column_headers = ['sepal-length', 'sepal-width',
                  'petal-length', 'petal-width', 'class']
df = pd.read_csv(os.environ['AZUREML_DATAREFERENCE_irisdata'], names=column_headers)

data = df.values
X = data[:, 0:4]
y = data[:, 4]
validation_size = 0.20
seed = 12345
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(
    X, y, test_size=validation_size, random_state=seed)

# We will use 10-fold cross validation to estimate accuracy.
print('X_train: {}'.format(X_train.shape))
print('X_validation: {}'.format(X_validation.shape))
print('Y_train: {}'.format(Y_train.shape))
print('Y_validation: {}'.format(Y_validation.shape))
print('======================================')

#import models

scoring = 'accuracy'

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

results = []
names = []
best_score = 0
best_model = None

# create a ./outputs folder in the compute target
# files saved in the "./outputs" folder are automatically uploaded into run history
os.makedirs('./outputs', exist_ok=True)

with open('./outputs/output.txt', 'w') as f:
	for name, model in models:
		kfold = model_selection.KFold(n_splits=3, random_state=None)
		cv_results = model_selection.cross_val_score(
			model, X_train, Y_train, cv=kfold, scoring=scoring)
		results.append(cv_results)
		names.append(name)

		#run prediction to get confusion matrix
		mdl = model.fit(X_train,Y_train)
		y_pred = mdl.predict(X_validation)

		conf_mat = confusion_matrix(Y_validation, y_pred)
		accuracy = accuracy_score(Y_validation, y_pred)

		run.log(name+"_accuracy",accuracy)
	
		# confusion matrix log for azureml does not accept ndarray
		# https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.run.run?view=azure-ml-py#log-confusion-matrix-name--value--description----
		# https://stackoverflow.com/questions/62343056/how-to-log-a-confusion-matrix-to-azureml-platform-using-python
		cmtx = {
			"schema_type": "confusion_matrix",
			"data": {"class_labels": ["Iris-setosa", "Iris-versicolor","Iris-virginica"],
					"matrix": [[int(y) for y in x] for x in conf_mat]}
		}
		run.log_confusion_matrix('Confusion matrix '+name, cmtx)

		if accuracy>best_score:
			best_score = accuracy
			best_model = (name, mdl)

		msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
		f.write(msg)
		f.write('\n')
		print(msg)
		print(".")
	
	# +

run.log("accuracy",best_score)


pkl_filename = "model.pkl"
with open(os.path.join('./outputs/', pkl_filename), 'wb') as file:
    pickle.dump(best_model[1], file)

print("retrieving output mount path")
mounted_output_path = os.environ['AZUREML_DATAREFERENCE_model_output']
os.makedirs(mounted_output_path, exist_ok=True)

with open(os.path.join(mounted_output_path, pkl_filename), 'wb') as file:
    pickle.dump(best_model[1], file)


# logging the best model information to properties and tags. 
# Properties are immutable, tags are not. Both can be accessed outside
# of the run.
run.add_properties({'best_model':best_model[0],'accuracy':best_score})
run.tag("best_model",best_model[0])
run.tag("accuracy",best_score)

# also add these properties to the parent run (if offline run parent would be null)
if not(run.id.startswith('OfflineRun')):
	run.parent.add_properties({'best_model':best_model[0],'accuracy':best_score})
	run.parent.tag("best_model",best_model[0])
	run.parent.tag("accuracy",best_score)