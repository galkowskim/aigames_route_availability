import pandas as pd
import pickle
import warnings
from sklearn.model_selection import train_test_split
from preprocessor.preprocessor import Preprocessor
from preprocessor.dataextracter import DataExtracter
from model.model import Model

warnings.filterwarnings('ignore')

data_extractor = DataExtracter()

train = data_extractor.train()
test = data_extractor.test()

preprocessor_train = Preprocessor(train)
preprocessor_test = Preprocessor(test)

train = preprocessor_train.preprocess_train()
test = preprocessor_test.preprocess_test()

model = Model(learning_rate=0.1)
y_train = train['status']
X_train = train.drop(['status'], axis=1)

# X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.8, random_state=420)
model.train(X_train, y_train)

y_pred_train = model.predict(X_train)
# y_pred_val = model.predict(X_val)

print(f'Training data:')
model.calculate_f1(y_pred_train, y_train)
print()

# print(f'Validation data:')
# model.calculate_f1(y_pred_val, y_val)
# print()

# Save csv output into results.csv
test = model.onehot(test)
y_pred = model.predict_and_save(test)


# Saving model
model_path = 'data/model/finalized_model.sav'
print(f'Dumping model into {model_path}')
pickle.dump(model, open(model_path, 'wb'))