from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse,request
from myapp.models import register,foodlist
from .models import user_details,user_command,WaterIntake
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import json
import requests
from datetime import date
from datetime import timedelta,datetime
from .utils import greeting,size,unique,gem_res,summ,calcare,needed_days,calculate_protein,calculate_potassium
from .email_util import email_verifi
import os
# from .encrytion import hash_password,verify_password
import secrets
#secure_id = secrets.token_hex(16)  # 16 bytes = 32 hex characters
flag ="none"
def regist(request):
    import secrets
    if request.method =="POST":
        names =request.POST.get('name')
        emails =request.POST.get('email')
        pass_words =request.POST.get('password')
        temp1 =register.objects.filter(email = emails)
        request.session['email']=emails
        request.session['name']=names
        request.session['password']=pass_words


        if temp1:
            error="emails is exists"
            return render(request,"registation.html",{'error':error})
        else :
            otp =email_verifi(emails)
            request.session['otp_created_time']=datetime.now().isoformat()
            request.session['otp']=otp
            # new = register(name =names,email =emails,password =pass_words,unique_id=secure_ids)
            # new.save()
            return redirect('verify_otp_view')
    
    return render(request,"registation.html")


def resend_otp(request):
    email=request.session.get('email')
     
    
    otp =email_verifi(email)
    request.session['otp']=otp
    request.session['otp_created_time']=datetime.now().isoformat()
    return redirect('verify_otp_view')


def verify_otp_view(request):
    otp =request.session.get('otp')
    otp_created_time_str =str(request.session.get('otp_created_time'))
    otp_created_time = datetime.fromisoformat(otp_created_time_str)
    otp_expiry_time =otp_created_time+timedelta(minutes=10)
    
    secure_ids = secrets.token_hex(16)
    flag =False
    if request.method == "POST":
        entered_otp = int(request.POST.get("otp", 0))
        if datetime.now()>otp_expiry_time:
            return render(request,'verify_otp_view.html',{'err':"TIME OUT"})
        else:
            if entered_otp ==int(otp):
                usename=request.session.get('name')
                email=request.session.get('email')
                password=request.session.get('password')
                # hashed_pw = hash_password(password)
                new = register(name =usename,email =email,password =password,unique_id=secure_ids)
                new.save()
                flag=True
                return redirect('login')
            elif flag ==False:
                return render(request,'verify_otp_view.html',{'err':"OTP IS INVALIDE"})
    return render(request,'verify_otp_view.html',{'otp':otp,'error':secure_ids})




def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password =request.POST.get('password')
        try:
            temp2 =register.objects.filter(email =email).first()
            true_passs=temp2.password
        except:    
            return render (request,"login.html",{'erorr2':"enter correct email_id"})
        # temp3 =register.objects.filter(password =verify_password(password))
        # temp3 =register.objects.filter(password =password)
        # temp4 =register.objects.filter(name =email,password=password)
        # temp5 =register.objects.all()


        # request.session['myvariable']=password
        request.session['email']=email

    
        
        if password==true_passs:
            return redirect (index)
        
        else:
            return render(request,'login.html',{'erorr':"enter correct password"})
        
    return render(request,"login.html")    
                 
def find(request):
    email =request.session.get('email')
    register_instance = get_object_or_404(register, email=email)
    if request.method == 'POST':
        # Get input values from the form
        weight = float(request.POST['weight'])
        height = float(request.POST['height'])
        age = int(request.POST['age'])
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']
        goal = request.POST['goal']
        # protein = calculate_protein(weight, goal)
        # Calculate BMR using Mifflin-St Jeor equation
        protien= calculate_protein(weight,str(goal))
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Define activity multipliers
        activity_factors = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'super_active': 1.9
        }

        tdee = bmr * activity_factors[activity_level]

        # Calculate calories for goal
        if goal == 'maintain':
            calories_for_goal = tdee
        elif goal == 'lose_weight':
            calories_for_goal = tdee - 500  # 500 calorie deficit
        elif goal == 'gain_weight':
            calories_for_goal = tdee + 500  # 500 calorie surplus
        # request.session['yourcalories']=calories_for_goal  
        lower_fat=(calories_for_goal*0.20)/9
        upper_fat=(calories_for_goal*0.35)/9
        fiber ="none"
        suger = round((tdee*0.05)/4 ,2)
        if age <= 50 and age>=18 and gender =='male':
            fiber ="30 - 38"
        elif age <= 50 and age>=18 and gender =='female':
            fiber ="21 - 25"
        elif age >= 50 and gender =='male':
            fiber ="28"
        elif age >=50 and gender == 'female':
            fiber ="21"
        elif age <=18:
            fiber ="14 - 31"    
        potassim =calculate_potassium(age,gender,weight) 
    
        if user_details.objects.filter(email=register_instance).first():
            user_details.objects.filter(email=register_instance).update(
            weight=weight,height=height,
            age =age,gender =gender,activity_level=activity_level,
            goal=goal,bmr=round(bmr,2),tdee=round(tdee,2),
            your_calorie_goal =round(calories_for_goal,4),
            protien_min =protien[0],protien_max=protien[1],
            lower_fat=round(lower_fat,2),upper_fat=round(upper_fat,2),
            potassium=potassim,fiber=fiber,suger=suger
            )
        else:
            new_user_details =user_details(email =register_instance,weight=weight,height=height,age =age,gender =gender,activity_level=activity_level,goal=goal,bmr=round(bmr,2),tdee=round(tdee,2),your_calorie_goal =round(calories_for_goal,4),protien_min =protien[0],protien_max=protien[1],lower_fat=round(lower_fat,2),upper_fat=round(upper_fat,2),potassium=potassim,fiber=fiber,suger=suger)
            new_user_details.save()
        return render(request, 'find.html', {'bmr': bmr,'tdee': tdee,'calories_for_goal': calories_for_goal,
                                             'protien_min':protien[0],'protien_max':protien[1],
                                             'lower_fat':round(lower_fat,2),'upper_fat':round(upper_fat,2),
                                             'potassim':potassim,'fiber':fiber,'suger':suger})
    
    return render(request,"find.html")


def index(request):
    Greeting = greeting()
    
    today =datetime.now().date()
    email=request.session.get('email')
    user=register.objects.get(email=email)
    unique_id=user.unique_id
    names =user.name
    unique =register.objects.get(unique_id=unique_id)
    food =foodlist.objects.filter(unique=unique,date =today)
    tot =summ(unique,today)


    if request.method =='POST':
        query =request.POST.get('query')
        si =int(request.POST.get('size'))
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        response = requests.get(api_url + query, headers={'X-Api-Key': os.getenv('X-Api-Key')})
        try:
            api = json.loads(response.content)
            item =api['items'][0]
            name =item['name']
            calo =size(si,item['calories'])
            fat =size(si,item['fat_total_g'])
            fat_saturated =size(si,item['fat_saturated_g'])
            protein =size(si,item['protein_g'])
            sodium =size(si,item['sodium_mg'])
            potassium =size(si,item['potassium_mg'])
            cholesterol =size(si,item['cholesterol_mg'])
            carbohydrates =size(si,item['carbohydrates_total_g'])
            fiber =size(si,item['fiber_g'])
            sugar =size(si,item['sugar_g'])
            all =[calo,fat,fat_saturated,protein,sodium,potassium,cholesterol,carbohydrates,fiber,sugar]

            allname =["calories","fat","fat_saturated","protein","sodium",
                      "potassium","cholesterol","carbohydrates","fiber","sugar"]
            
            
            
            newfood = foodlist(unique=unique,date=today,item=name,
                               calories=calo,fat=fat,fat_saturated=fat_saturated,
                               protein=protein,sodium=sodium,potassium=potassium,
                               cholesterol=cholesterol,carbohydrates=carbohydrates,
                               fiber=fiber,sugar=sugar)
            newfood.save()
            
            tot =summ(unique,today)
            tot_float = [float(value) for value in tot] 
            gem =gem_res(f"{name} this is best for my diet")
            query="none"
            return render(request,'home.html',{'greeting':Greeting,'all':all,'allname':allname,'tot1':tot_float,'query':query,
                                               'api':api,'name':names,'food':food,'tot':tot_float,'allnames1': json.dumps(allname),
                                               'gem':gem})    
            
        except:
            return render(request,'home.html',{'greeting':Greeting,'query':"Please Enter Valid Food ",'wel':Greeting})
    
    

    allname =["calories","fat","fat_saturated","protein","sodium",
              "potassium","cholesterol","carbohydrates","fiber","sugar"]
    
    tot_float = [float(value) for value in tot]

    return render(request,"home.html",{'food':food,'greeting':Greeting,'email':email,'tot':tot,
                                       'gem':"gem",'allname':allname,'tot1': tot_float,'name':names,
                                       'allnames1': json.dumps(allname)})
               


def about(request):
    num =0
    return render(request,'about.html',{'num':num})
def contact(request):
    return render(request,'contact.html')
def myaccount(request):
    from django.utils.dateparse import parse_date
    date =datetime.now().date()
    # request.session['date']=str(date)
    email=request.session.get('email')
    user_detail1=register.objects.get(email=email)
    user_info ={}
    waterlimit=WaterIntake.objects.filter(email=email).last()
    limit = waterlimit.glasses_drank *100
    remainig =2000-limit
    if request.method =="POST":
        selected_date = request.POST.get("date")
        request.session['date']=selected_date
        return redirect(myaccount)
    try:
        if user_detail1 and email:
            user_detail =user_details.objects.get(email=email)
            user_info={'name':user_detail1.name,'email':user_detail1.email,
                    'weight':user_detail.weight,'height':user_detail.height,
                    'age':user_detail.age,'gender':user_detail.gender,
                    'activity_level':user_detail.activity_level,'goal':user_detail.goal,
                    'bmr':user_detail.bmr,'tdee':user_detail.tdee,
                    'your_calorie_goal':user_detail.your_calorie_goal,'protien_min':user_detail.protien_min,
                    'protien_max':user_detail.protien_max,'lower_fat':user_detail.lower_fat,
                    'upper_fat':user_detail.upper_fat,'potassium':user_detail.potassium,
                    'fiber':user_detail.fiber,'suger':user_detail.suger
                    }
    except:
        user_info ={}        

    
    date =str(request.session.get('date'))
    
    # date1 = datetime.fromisoformat(date).date() 
    parsed_date = parse_date(date)
    
    # selected_date = datetime.fromisoformat(date).date()
    today=datetime.now().date()
    yester =datetime.now().date() - timedelta(days=1)
    email=request.session.get('email')
    user=register.objects.get(email=email)
    unique_id=user.unique_id
    unique =register.objects.get(unique_id=unique_id)
    food_today =foodlist.objects.filter(unique=unique,date =today)
    food =foodlist.objects.filter(unique=unique,date =parsed_date)
    tot =summ(unique,parsed_date)
    
    allname =["calories","fat","fat_saturated","protein","sodium",
              "potassium","cholesterol","carbohydrates","fiber","sugar"]
    
    input ="calories"
    if date:
        food =food
        tot=tot
    

    else:
        food =food_today
        tot =summ(unique,today)

    tot_float = [float(value) for value in tot]
    
    return render(request,'myaccount.html',{'tot1':tot_float,'food':food,'input':input,
                                            'tot':tot,'allnames1': json.dumps(allname),
                                            'email':email,'date':date,'today':today,'user_info':user_info,'water':limit,'remain':remainig})


    

def deep(request):
    if request.method =="POST":
        needed_nutrition=request.POST.get("needed_nutrition").lower()
        needed_dates=int(request.POST.get("needed_dates", 0))
        email=request.session.get('email')
        user=register.objects.get(email=email)
        unique_id=user.unique_id
        unique =register.objects.get(unique_id=unique_id)
        try:
            tot3 =calcare(unique,needed_dates)
            x=needed_days(needed_dates)
            calories =tot3[0]
            fat =tot3[1]
            fat_saturated =tot3[2]
            protein =tot3[3]
            sodium =tot3[4]
            potassium =tot3[5]
            cholesterol =tot3[6]
            carbohydrates =tot3[7]
            fiber =tot3[8]
            sugar =tot3[9]
            all ={'calories':calories,'fat':fat,'fat_saturated':fat_saturated,'protein':protein,'sodium':sodium,'potassium':potassium,'cholesterol':cholesterol,'carbohydrates':carbohydrates,'fiber':fiber,'sugar':sugar}
            
            for i in all:
                if needed_nutrition==i:
                    need = all[i]
                    need =[float(value) for value in need]
                    return render(request,'deep_analysis.html',{'need':need,'needed_days': json.dumps(x),'needed_nutrition':json.dumps(needed_nutrition)})
                elif needed_nutrition =="all":
                    return render(request,'deep_analysis.html',{'need':all,'needed_days':x,'needed_nutrition':needed_nutrition})
        except:
             return render(request,'deep_analysis.html',{'error':"Please enter valied food"})
    return render(request,'deep_analysis.html')

def user_commands(request):
    email=request.session.get('email')
    regist =register.objects.get(email=email)
    name =regist.name
    
    if request.method =="POST":
        user_commands=request.POST.get("user_command")
        regist =register.objects.get(email=email)
        user =user_command(name =regist.name,email=regist.email,command=user_commands) 
        user.save()
        request.session['test']=user_commands
    user_commands=request.session.get('test')
    contest ={'name':name,'email':email,'command':user_commands}

    user =user_command.objects.get(user_commands_by_email=email)
    return render(request,'about.html',{'your':user})



def water(request):
    today = date.today()
    email=request.session.get('email')
    regist =register.objects.get(email=email)
    entry, created = WaterIntake.objects.get_or_create(email=regist.email, date=today)

    if request.method == 'POST':
        if entry.glasses_drank < 20:
            entry.glasses_drank += 1
            entry.save()
        return redirect('water')
    # list=[1,2,3,4,5,6,7,8]
    # remain =8 - 
    # for i in range(remain):
    #     list[i]=1

    context = {
        'entry': entry,
        'remaining':range(20- entry.glasses_drank),
        'range_list': range(entry.glasses_drank),
        'your' :entry.glasses_drank*100,
        'need':(20- entry.glasses_drank)*100

    }
    

    return render(request,"water.html",context)
