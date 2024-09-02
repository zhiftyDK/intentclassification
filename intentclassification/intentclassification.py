import os
import json
import random
import pickle
import nltk
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

class IntentClassifier:
    def __init__(self, intents_path, output_path, model_name="classifier"):

        model_path = os.path.join(output_path, model_name)

        nltk.download("punkt", quiet=True)
        nltk.download("wordnet", quiet=True)

        if os.path.exists(intents_path):
            with open(intents_path, "r") as f:
                self.intents_data = json.load(f)
        else:
            raise FileNotFoundError
        
        self.model = None
        self.model_path = model_path
        self.history = None
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.words = []
        self.intents = []
        self.training_data = []

    def _prepare_training_data(self, ignore_letters=("!", "?", ",", ".")):
        documents = []

        for intent in self.intents_data["intents"]:
            if intent["tag"] not in self.intents:
                self.intents.append(intent["tag"])

            for pattern in intent["patterns"]:
                pattern_words = nltk.word_tokenize(pattern)
                self.words += pattern_words
                documents.append((pattern_words, intent["tag"]))

        self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words if w not in ignore_letters]
        self.words = sorted(set(self.words))

        empty_output = [0] * len(self.intents)

        for document in documents:
            bag_of_words = []
            pattern_words = document[0]
            pattern_words = [self.lemmatizer.lemmatize(w.lower()) for w in pattern_words]
            for word in self.words:
                bag_of_words.append(1 if word in pattern_words else 0)

            output_row = empty_output.copy()
            output_row[self.intents.index(document[1])] = 1
            self.training_data.append([bag_of_words, output_row])

        random.shuffle(self.training_data)
        self.training_data = np.array(self.training_data, dtype="object")

        X = np.array([data[0] for data in self.training_data])
        y = np.array([data[1] for data in self.training_data])

        return X, y

    def fit_model(self, epochs: int = 200):
        X, y = self._prepare_training_data()

        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(128, input_shape=(X.shape[1],), activation = "relu"))
        self.model.add(tf.keras.layers.Dropout(0.5))
        self.model.add(tf.keras.layers.Dense(64, activation = "relu"))
        self.model.add(tf.keras.layers.Dropout(0.5))
        self.model.add(tf.keras.layers.Dense(y.shape[1], activation="softmax"))

        sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        self.model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

        self.history = self.model.fit(X, y, epochs=epochs, batch_size=5, verbose=1)

    def save_model(self):
        self.model.save(f"{self.model_path}.keras", self.history)
        pickle.dump(self.words, open(f"{self.model_path}_words.pkl", "wb"))
        pickle.dump(self.intents, open(f"{self.model_path}_intents.pkl", "wb"))
    
    def load_model(self):
        self.model = tf.keras.models.load_model(f"{self.model_path}.keras")
        self.words = pickle.load(open(f"{self.model_path}_words.pkl", "rb"))
        self.intents = pickle.load(open(f"{self.model_path}_intents.pkl", "rb"))

    def predict(self, input_text: str):
        input_words = nltk.word_tokenize(input_text)
        input_words = [self.lemmatizer.lemmatize(w.lower()) for w in input_words]

        input_bag_of_words = [0] * len(self.words)

        for input_word in input_words:
            for i, word in enumerate(self.words):
                if input_word == word:
                    input_bag_of_words[i] = 1

        input_bag_of_words = np.array([input_bag_of_words])
        predictions = self.model.predict(input_bag_of_words, verbose=0)[0]
        predicted_intent = self.intents[np.argmax(predictions)]
        return {"intent": predicted_intent, "probability": str(predictions[np.argmax(predictions)])}