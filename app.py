from flask import Flask, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)
    # app.run(host='192.168.18.117')

# Define the input variables
oxygen_rate = ctrl.Antecedent(np.arange(0, 120, 1), 'oxygen_rate')
heart_rate = ctrl.Antecedent(np.arange(0, 201, 1), 'heart_rate')

# Define the output variable
hypoxia = ctrl.Consequent(np.arange(0, 150, 1), 'hypoxia')

# Define the fuzzy sets for each input and output variable
oxygen_rate ['severe_oxygen'] = fuzz.trapmf(oxygen_rate.universe, [0, 0, 70, 80])
oxygen_rate ['moderate_oxygen'] = fuzz.trapmf(oxygen_rate.universe, [70, 80, 90, 95])
oxygen_rate ['mild_oxygen'] = fuzz.trapmf(oxygen_rate.universe, [90, 95, 100, 100])
oxygen_rate ['normal_oxygen'] = fuzz.trimf(oxygen_rate.universe, [95, 100, 100])

# Membership functions for heart rate
heart_rate ['bradycardia'] = fuzz.trimf(heart_rate.universe, [0, 60, 80])
heart_rate ['normal_heart_rate'] = fuzz.trimf(heart_rate.universe, [70, 90, 100])
heart_rate ['tachycardia'] = fuzz.trimf(heart_rate.universe, [120, 140, 200])

# heart_rate['low'] = fuzz.trimf(heart_rate.universe, [0, 0, 100])
# heart_rate['medium'] = fuzz.trimf(heart_rate.universe, [0, 100, 200])
# heart_rate['high'] = fuzz.trimf(heart_rate.universe, [100, 200, 200])

hypoxia ['mild_hypoxia'] = fuzz.trimf(hypoxia.universe, [0, 30, 60])
hypoxia ['bradycardia_hr']= fuzz.trapmf(hypoxia.universe, [20, 40, 60, 80])
hypoxia ['moderate_hypoxia'] = fuzz.trimf(hypoxia.universe, [40, 70, 100])
hypoxia ['severe_hypoxia'] = fuzz.trimf(hypoxia.universe, [70, 100, 100])
hypoxia ['tachycardia_hr']= fuzz.trapmf(hypoxia.universe, [90, 110, 130, 150])

# Define the rules for the fuzzy logic system
rule1 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['severe_oxygen'], hypoxia['severe_hypoxia'])
rule2 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['moderate_oxygen'], hypoxia['moderate_hypoxia'])
rule3 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['mild_oxygen'], hypoxia['mild_hypoxia'])
rule4 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['normal_oxygen'], hypoxia['mild_hypoxia'])

rule5 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['severe_oxygen'], hypoxia['severe_hypoxia'])
rule6 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['moderate_oxygen'], hypoxia['moderate_hypoxia'])
rule7 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['mild_oxygen'], hypoxia['mild_hypoxia'])
rule8 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['normal_oxygen'], hypoxia['mild_hypoxia'])

rule9 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['severe_oxygen'], hypoxia['severe_hypoxia'])
rule10 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['moderate_oxygen'], hypoxia['moderate_hypoxia'])
rule11 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['mild_oxygen'], hypoxia['moderate_hypoxia'])
rule12 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['normal_oxygen'], hypoxia['mild_hypoxia'])

# Create the control system and pass the rules to it
hypoxia_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])

# Create the simulation using the control system
hypoxia_sim = ctrl.ControlSystemSimulation(hypoxia_ctrl)

@app.route('/hypoxia', methods=['POST'])
def calculate_hypoxia():
    # Get the input values from the request
    data = request.get_json()
    oxygen = data['oxygen']
    heart = data['heart']

    # Set the input values
    hypoxia_sim.input['oxygen_rate'] = oxygen
    hypoxia_sim.input['heart_rate'] = heart

    # Evaluate the output value
    hypoxia_sim.compute()

    # Get the output value
    hypoxia_level = hypoxia_sim.output['hypoxia']

    #kategory
    category = 'null'
    # if(hypoxia_sim.input['oxygen_rate'] > 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = 'Tachycardia'
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }elif(hypoxia_sim.input['oxygen_rate'] < 100 and hypoxia_sim.input['heart_rate'] > 95){
    #     category = ''   
    # }else:
        
    # Return the output value as a JSON response
    return {'hypoxia': hypoxia_level, 'category' : category}

if __name__ == '__main__':
    app.run()
