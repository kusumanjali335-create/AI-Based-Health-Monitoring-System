from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import HealthHistory
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

import joblib
import pandas as pd

heart_model = joblib.load("ml/models/heart_model.pkl")


# ---------------- HOME ---------------- #

def home(request):
    return render(request, "home.html")


# ---------------- REGISTER ---------------- #

def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")

            return redirect("register")

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Registration Successful")

        return redirect("login")

    return render(request, "register.html")


# ---------------- LOGIN ---------------- #

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


# ---------------- DASHBOARD ---------------- #

def dashboard(request):

    if not request.user.is_authenticated:

        return redirect("login")

    return render(request, "dashboard.html")


# ---------------- LOGOUT ---------------- #

def logout_view(request):

    logout(request)

    return redirect("home")


# ---------------- HEALTH MONITOR ---------------- #

def health_monitor(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        name = request.POST["name"]
        age = int(request.POST["age"])
        gender = request.POST["gender"]

        heart_rate = int(request.POST["heart_rate"])
        bp_sys = int(request.POST["bp_sys"])
        bp_dia = int(request.POST["bp_dia"])

        temperature = float(request.POST["temperature"])
        spo2 = int(request.POST["spo2"])
        blood_sugar = int(request.POST["blood_sugar"])

       # ---------------- AI HEART PREDICTION ---------------

        try:

            input_data = pd.DataFrame({
                "age": [age],
                "resting_blood_pressure": [bp_sys],
                "Max_heart_rate": [heart_rate]
            })

            prediction = heart_model.predict(input_data)

            if prediction[0] == 1:
                heart = "High Risk"
            else:
                heart = "Low Risk"

        except Exception as e:

            print("Heart Model Error:", e)

            if bp_sys > 140 or heart_rate > 110:
                heart = "High Risk"
            else:
                heart = "Low Risk"

        # ---------------- DIABETES ----------------

        if blood_sugar >= 126:
            diabetes = "High Risk"
        else:
            diabetes = "Low Risk"

        # ---------------- STROKE ----------------

        if age >= 60 or bp_sys > 150:
            stroke = "Medium Risk"
        else:
            stroke = "Low Risk"

        # ---------------- KIDNEY ----------------

        if bp_sys > 140 and blood_sugar > 140:
            kidney = "Medium Risk"
        else:
            kidney = "Low Risk" 

        # ---------------- HEALTH SCORE ----------------

        score = 100

        # Heart
        if heart == "High Risk":
            score -= 30

        # Diabetes
        if diabetes == "High Risk":
            score -= 25

        # Kidney
        if kidney == "Medium Risk":
            score -= 20

        # Stroke
        if stroke == "Medium Risk":
            score -= 20

        # Heart Rate
        if heart_rate < 60 or heart_rate > 100:
            score -= 5

        # Blood Pressure
        if bp_sys > 140 or bp_dia > 90:
            score -= 5

        # Oxygen Level
        if spo2 < 95:
            score -= 5

        # Temperature
        if temperature > 38 or temperature < 35:
            score -= 5

        # Keep score between 0 and 100
        score = max(0, min(score, 100))

        # ---------------- HEALTH STATUS ----------------

        if score >= 90:
            status = "Excellent"

        elif score >= 75:
            status = "Good"

        elif score >= 50:
            status = "Moderate Risk"

        else:
            status = "Critical Condition"

        
        # ---------------- SAVE TO DATABASE ----------------

        HealthHistory.objects.create(
            user=request.user,
            name=name,
            age=age,
            heart=heart,
            diabetes=diabetes,
            kidney=kidney,
            stroke=stroke,
            score=score
        )

        return render(request, "result.html", {

            "name": name,
            "heart": heart,
            "diabetes": diabetes,
            "stroke": stroke,
            "kidney": kidney,
            "score": score,
            "status": status,

            "age": age,
            "gender": gender,
            "heart_rate": heart_rate,
            "bp_sys": bp_sys,
            "bp_dia": bp_dia,
            "temperature": temperature,
            "spo2": spo2,
            "blood_sugar": blood_sugar,

        })

    return render(request, "health_monitor.html")

def history(request):

    if not request.user.is_authenticated:
        return redirect("login")

    reports = HealthHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "history.html",
        {
            "reports": reports
        }
    )

def about(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "about.html")

def tips(request):

    if not request.user.is_authenticated:
        return redirect("login")

    tips_list = [

        "💧 Drink at least 2–3 litres of water every day.",

        "🚶 Walk or exercise for 30 minutes daily.",

        "🥗 Eat more fruits and green vegetables.",

        "😴 Sleep 7–8 hours every night.",

        "❤️ Check your blood pressure regularly.",

        "🩸 Monitor your blood sugar if you are diabetic.",

        "🚭 Avoid smoking and excessive alcohol consumption.",

        "🧘 Reduce stress through yoga or meditation.",

        "🥜 Eat healthy foods and avoid junk food.",

        "👨‍⚕ Visit your doctor regularly for health check-ups."

    ]

    return render(
        request,
        "tips.html",
        {
            "tips": tips_list
        }
    )

def emergency(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "emergency.html")

def profile(request):

    if not request.user.is_authenticated:
        return redirect("login")

    reports = HealthHistory.objects.filter(user=request.user)

    last_report = reports.order_by("-created_at").first()

    return render(request, "profile.html", {

        "reports": reports.count(),

        "last_report": last_report,

    })

def download_report(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="AI_Health_Report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI BASED HEALTH MONITORING SYSTEM</b>", styles['Title']))
    story.append(Paragraph("<br/>", styles['Normal']))

    story.append(Paragraph(f"<b>Name:</b> {request.GET.get('name')}", styles['Normal']))
    story.append(Paragraph(f"<b>Age:</b> {request.GET.get('age')}", styles['Normal']))
    story.append(Paragraph(f"<b>Gender:</b> {request.GET.get('gender')}", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    story.append(Paragraph("<b>AI Prediction Results</b>", styles['Heading2']))

    story.append(Paragraph(f"Heart Disease : {request.GET.get('heart')}", styles['Normal']))
    story.append(Paragraph(f"Diabetes : {request.GET.get('diabetes')}", styles['Normal']))
    story.append(Paragraph(f"Stroke : {request.GET.get('stroke')}", styles['Normal']))
    story.append(Paragraph(f"Kidney Disease : {request.GET.get('kidney')}", styles['Normal']))
    story.append(Paragraph(f"Overall Health Score : {request.GET.get('score')}%", styles['Normal']))

    story.append(Paragraph("<br/>", styles['Normal']))
    story.append(Paragraph("<b>AI Recommendations</b>", styles['Heading2']))

    story.append(Paragraph("• Drink 2-3 litres of water daily.", styles['Normal']))
    story.append(Paragraph("• Exercise for 30 minutes.", styles['Normal']))
    story.append(Paragraph("• Eat healthy food.", styles['Normal']))
    story.append(Paragraph("• Sleep 7-8 hours.", styles['Normal']))
    story.append(Paragraph("• Visit your doctor regularly.", styles['Normal']))

    doc.build(story)

    return response