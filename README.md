# Intentclassification

### **Install**
```bash
pip install intentclassification
```

### **About**
Intentclassification AI in python, easy to use intentclassifier package.

### **How to use**
**Import:**
```py
from intentclassification import IntentClassifier
```

**Intents Structure:**
```json
{
    "intents": [
        {
            "tag": "lights_on",
            "patterns": ["Turn the light on", "Turn on the light", "Lights on"]
        },
        {
            "tag": "lights_off",
            "patterns": ["Turn the light off", "Turn off the light", "Lights off"]
        },
        {
            "tag": "fan_on",
            "patterns": ["Turn the fan on", "Turn on the fan", "Fan on"]
        },
        {
            "tag": "fan_off",
            "patterns": ["Turn the fan off", "Turn off the fan", "Fan off"]
        }
    ]
}
```

**Example:**
```py
from intentclassification import IntentClassifier

#Initialise intentclassifier (Intents path being the path to the intents.json file) (Output path being the path to the folder the model will be saved in)
IC = IntentClassifier(intents_path="./intents.json", output_path="./intentclassification")

#Fit the model Aka. train the model on the data in intents.json
IC.fit_model()
#Save the model after fitting
IC.save_model()

#Loading a previously fitted/trained model
#When you have a trained model you dont have to retrain everytime you run the program, just simply load the model like so
IC.load_model()

#Using the model is as simple as parsing a sentence to the predict function
result = IC.predict(input_text="Turn the lights on!")

#The predict function will return a json object including the name of the intent and the probability of that intent
print(result) # Example: {"intent": "lights_on", "probability": "0.999256"}

#Now how about we use this intent for something useful?
#We can define a function that will run whenever the lights_on intent reaches a certain probability
#Remember to give the functions and the intents the same name otherwise the triggerhandler wont work
def lights_on():
    print("Turning lights on!")
    #Run code for turning on your light here!
    #If anything in here is returned it will be parsed through the handleTrigger() function
    return "Lights have been turned on!"

def lights_off():
    print("Turning lights off!")
    #Run code for turning on your light here!
    #If anything in here is returned it will be parsed through the handleTrigger() function
    return "Lights have been turned off!"

def fan_on():
    print("Turning fan on!")
    #Run code for turning on your light here!
    #If anything in here is returned it will be parsed through the handleTrigger() function
    return "Fan has been turned on!"

def fan_off():
    print("Turning fan off!")
    #Run code for turning on your light here!
    #If anything in here is returned it will be parsed through the handleTrigger() function
    return "Fan has been turned off!"

#Create an array with all the trigger functions, this is how the handleTrigger() function accesses them.
trigger_functions = [lights_on]

#Handletrigger takes 2 arguments, the result from the IC.predict() function and a probability threshold value for activating the trigger functions
#The probability_threshold can be changed to accomodate any missfires, the threshold might have to be changed depending on the size of intents.json
returned_value = IC.handleTriggers(prediction=result, probability_threshold=0.75, trigger_functions=trigger_functions)

#The returned value will be None by default depending on if the triggered trigger function returns anything, otherwise it will be the returned value
print(returned_value)

# The printed results of this full program will be the following:
# {'intent': 'lights_on', 'probability': '0.9999784'}
# Turning lights on!
# Lights have been turned on!
```