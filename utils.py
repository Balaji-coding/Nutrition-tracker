import secrets
from myapp.models import register,foodlist

def unique():
    # Generate a secure random hex token
    secure_id = secrets.token_hex(16)  # 16 bytes = 32 hex characters
    # Example: 9a1b3c4d5e6f7a8b9c0d1e2f3g4h5i6j
    return secure_id


from datetime import timedelta,datetime
def greeting():
    
    yester =datetime.now().date() - timedelta(days=1)
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        return "Good Morning"
    elif 12<= current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"
    
def size(a,b):
    kg=a
    calo=b

    if kg ==100:
        calorie =calo
        return round(calorie,2)
    elif kg >=100:
            
        calories =calo/100
        calorie =kg*calories
        return round(calorie,2)
    elif kg <=100:
        calories =calo/100
        calorie = kg*calories
        return round(calorie,2)

    
def summ(unique,today):

    # today =datetime.now().date() - timedelta(days=7)
    food =foodlist.objects.filter(unique=unique,date =today)

    tot =0
    tot1 =0
    tot2 =0
    tot3 =0
    tot4 =0
    tot5 =0
    tot6 =0
    tot7 =0
    tot8 =0
    tot9 =0
    for i in food:
        tot += i.calories 
        
    for i in food:
        tot1 += i.fat 
        
    for i in food:
        tot2 += i.fat_saturated 
        
    for i in food:
        tot3 += i.protein 
        
    for i in food:
        tot4 += i.sodium 
        
    for i in food:
        tot5 += i.potassium 
        
    for i in food:
        tot6 += i.cholesterol 
        
    for i in food:
        tot7 += i.carbohydrates 
        
    for i in food:
        tot8 += i.fiber 
        
    for i in food:
        tot9 += i.sugar 
        
    tot10 =[tot,tot1,tot2,tot3,tot4,tot5,tot6,tot7,tot8,tot9]
    return tot10











import requests
import textwrap
def gem_res(need):
        import os
        import google.generativeai as genai

        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        )

        chat_session = model.start_chat(
        history=[
        ]
        )

        response = chat_session.send_message(need)
        
        formatted_response = response.text.strip().split("\n")

        return(formatted_response)


def calcare(unique,x):
    tot3 =[]
    tot4 =[]
    tot5 =[]
    tot6 =[]
    tot7 =[]
    tot8 =[]
    tot9 =[]
    tot10 =[]
    tot11=[]
    tot12 =[]

    for i in range(x):
        dates =datetime.now().date() - timedelta(days=i)
        tot =summ(unique,dates)
         
        tot3.append(tot[0])
        tot4.append(tot[1])
        tot5.append(tot[2])
        tot6.append(tot[3])
        tot7.append(tot[4])
        tot8.append(tot[5])
        tot9.append(tot[6])
        tot10.append(tot[7])
        tot11.append(tot[8])
        tot12.append(tot[9])
    tot3.reverse()
    tot3 = [float(value) for value in tot3]
    tot4.reverse()
    tot4 = [float(value) for value in tot4]
    tot5.reverse()
    tot5 = [float(value) for value in tot5]
    tot6.reverse()
    tot6 = [float(value) for value in tot6]
    tot7.reverse()
    tot7 = [float(value) for value in tot7]
    tot8.reverse()
    tot8 = [float(value) for value in tot8]
    tot9.reverse()
    tot9 = [float(value) for value in tot9]
    tot10.reverse()
    tot10 = [float(value) for value in tot10]
    tot11.reverse()
    tot11 = [float(value) for value in tot11]
    tot12.reverse()
    tot12 = [float(value) for value in tot12]


    empty_list = [tot3,tot4,tot5,tot6,tot7,tot8,tot9,tot10,tot11,tot12,]


    return empty_list
    

def needed_days(day):
    dates_list =[]
    for i in range(day):
        dates =datetime.now().date() - timedelta(days=i)
        dates_list.append(dates)
    dates_list.reverse()
    date_tuples = [(date.day, date.month, date.year) for date in dates_list]

    return date_tuples


def calculate_protein(weight, goal):
    list1=[]
    protein_factors = {
        "maintain": (1.2, 2.0),
        "lose_weight": (1.6, 2.2),
        "gain_weight": (1.8, 2.5)
    }
    
    if goal in protein_factors:
        min_factor, max_factor = protein_factors[goal]
        min_protein = weight * min_factor
        max_protein = weight * max_factor
        list1 =[round(min_protein, 2),round(max_protein, 2)]
        return list1

def calculate_potassium(age, gender, weight_kg):
    if age >= 18:
        if gender == 'male':
            return 3400
        elif gender == 'female':
            return 2600
    elif age >= 14:
        return 2800 if gender == 'male' else 2600
    elif age >= 9:
        return 2500 if gender == 'male' else 2600
    elif age >= 4:
        return 2300
    elif age >= 1:
        return 2000
    else:
        return 40 * weight_kg 
