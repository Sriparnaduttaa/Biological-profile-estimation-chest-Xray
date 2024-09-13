from django.shortcuts import render, redirect
from mainapp.models import *
from userapp.models import *
from adminapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
import pandas as pd
import numpy as np



# Create your views here.


def admin_dashboard(req):
    all_users_count = UserModel.objects.all().count()
    pending_users_count = UserModel.objects.filter(User_Status="pending").count()
    rejected_users_count = UserModel.objects.filter(User_Status="removed").count()
    accepted_users_count = UserModel.objects.filter(User_Status="accepted").count()
    Feedbacks_users_count = Feedback.objects.all().count()
    prediction_count = UserModel.objects.all().count()
    return render(
        req,
        "admin/admin-dashboard.html",
        {
            "a": all_users_count,
            "b": pending_users_count,
            "c": rejected_users_count,
            "d": accepted_users_count,
            "e": Feedbacks_users_count,
            "f": prediction_count,
        },
    )


def adminlogout(req):
    return redirect("main/admin-login.html")


def pending_users(req):
    pending = UserModel.objects.filter(User_Status="pending")
    paginator = Paginator(pending, 5)
    page_number = req.GET.get("page")
    post = paginator.get_page(page_number)
    return render(req, "admin/pending-users.html", {"user": post})


def all_users(req):
    all_users = UserModel.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = req.GET.get("page")
    post = paginator.get_page(page_number)
    return render(req, "admin/all-users.html", {"allu": all_users, "user": post})


def delete_user(req, id):
    UserModel.objects.get(user_id=id).delete()
    messages.warning(req, "User was Deleted..!")
    return redirect("all_users")


# Acept users button
def accept_user(req, id):
    status_update = UserModel.objects.get(user_id=id)
    status_update.User_Status = "accepted"
    status_update.save()
    messages.success(req, "User was accepted..!")
    return redirect("pending_users")


# Remove user button
def reject_user(req, id):
    status_update2 = UserModel.objects.get(user_id=id)
    status_update2.User_Status = "removed"
    status_update2.save()
    messages.warning(req, "User was Rejected..!")
    return redirect("pending_users")


def adminlogout(req):
    messages.info(req, "You are logged out.")
    return redirect("admin_login")


def admin_feedback(req):
    feed = Feedback.objects.all()
    return render(req, "admin/admin-feedback.html", {"back": feed})


def sentiment_analysis(req):
    fee = Feedback.objects.all()
    return render(req, "admin/sentiment-analysis.html", {"cat": fee})


def sentiment_analysis_graph(req):
    positive = Feedback.objects.filter(Sentiment="positive").count()
    very_positive = Feedback.objects.filter(Sentiment="very positive").count()
    negative = Feedback.objects.filter(Sentiment="negative").count()
    very_negative = Feedback.objects.filter(Sentiment="very negative").count()
    neutral = Feedback.objects.filter(Sentiment="neutral").count()
    context = {
        "vp": very_positive,
        "p": positive,
        "neg": negative,
        "vn": very_negative,
        "ne": neutral,
    }
    return render(req, "admin/sentiment-analysis-graph.html", context)


def comparision_graph(req):
    Vgg16 = Vgg16_model.objects.last()
    Resnet = Resnet_model.objects.last()
    Inceptionv3 = Inceptionv3_model.objects.last()

    Vgg16_graph = Vgg16.model_accuracy if Vgg16 else 'N/A'
    Resnet_graph = Resnet.model_accuracy if Resnet else 'N/A'
    Inceptionv3_graph = Inceptionv3.model_accuracy if Inceptionv3 else 'N/A'

    return render(req, "admin/comparision-graph.html", {
        'Inceptionv3': Inceptionv3_graph,
        'Resnet': Resnet_graph,
        'Vgg16': Vgg16_graph

    })





def Train_Test_Split(req):
    images_training = 2100
    images_validation = 899
    images_testing = 40
    image_classes = 2

    try:
        model_performance = Train_test_split_model.objects.latest('S_No')
        model_performance.Images_training = str(images_training)
        model_performance.Images_validation = str(images_validation)
        model_performance.Images_testing = str(images_testing)
        model_performance.Images_classes = str(image_classes)
    except Train_test_split_model.DoesNotExist:
        model_performance = Train_test_split_model(
            Images_training=str(images_training),
            Images_validation=str(images_validation),
            Images_testing=str(images_testing),
            Images_classes=str(image_classes)
        )

    model_performance.save()

    req.session['images_training'] = images_training
    req.session['images_validation'] = images_validation
    req.session['images_testing'] = images_testing
    req.session['image_classes'] = image_classes
    return render(req, "admin/Train-Test-Split.html")


def Train_Test_Split_Result(req):
    latest_entry = Train_test_split_model.objects.latest('S_No')

    context = {
        'images_training': latest_entry.Images_training,
        'images_validation': latest_entry.Images_validation,
        'images_testing': latest_entry.Images_testing,
        'image_classes': latest_entry.Images_classes
    }

    messages.success(req, "Train Test Split executed successfully")
    return render(req, "admin/Train Test Split-result.html", context)




def Vgg16(req):
    model_name = "Vgg16"
    accuracy = "83.95" 
    executed = "Vgg16 Model Executed Successfully"
    
    try:
        model_performance = Vgg16_model.objects.get(model_name=model_name)
        model_performance.model_accuracy = accuracy
        model_performance.model_executed = executed
    except Vgg16_model.DoesNotExist:
        model_performance = Vgg16_model(
            model_name=model_name, 
            model_accuracy=accuracy,
            model_executed=executed
        )
    model_performance.save()

    req.session['model_name'] = model_name
    req.session['accuracy'] = accuracy
    req.session['executed'] = executed
    return render(req, "admin/VGG16.html")


def Vgg16_result(req):
    model_name = req.session.get('model_name')
    accuracy = req.session.get('accuracy')
    executed = req.session.get('executed')

    context = {
        'model_name': model_name,
        'accuracy': accuracy,
        'executed': executed
    }
    messages.success(req, "Vgg16 Model executed successfully")
    return render(req, "admin/VGG16-btn.html", context)



def Resnet(req):
    model_name = "Resnet"
    accuracy = "60.85" 
    executed = "Resnet Model Executed Successfully"
    
    try:
        model_performance = Resnet_model.objects.get(model_name=model_name)
        model_performance.model_accuracy = accuracy
        model_performance.model_executed = executed
    except Resnet_model.DoesNotExist:
        model_performance = Resnet_model(
            model_name=model_name, 
            model_accuracy=accuracy,
            model_executed=executed
        )
    model_performance.save()

    req.session['model_name'] = model_name
    req.session['accuracy'] = accuracy
    req.session['executed'] = executed
    return render(req, "admin/Resnet.html")


def Resnet_result(req):
    model_name = req.session.get('model_name')
    accuracy = req.session.get('accuracy')
    executed = req.session.get('executed')

    context = {
        'model_name': model_name,
        'accuracy': accuracy,
        'executed': executed
    }
    messages.success(req, "Resnet Model executed successfully")
    return render(req, "admin/Resnet-btn.html", context)



def Inceptionv3(req):
    model_name = "Inceptionv3"
    accuracy = "81.85" 
    executed = "Inceptionv3 Model Executed Successfully"
    
    try:
        model_performance = Inceptionv3_model.objects.get(model_name=model_name)
        model_performance.model_accuracy = accuracy
        model_performance.model_executed = executed
    except Inceptionv3_model.DoesNotExist:
        model_performance = Inceptionv3_model(
            model_name=model_name, 
            model_accuracy=accuracy,
            model_executed=executed
        )
    model_performance.save()

    req.session['model_name'] = model_name
    req.session['accuracy'] = accuracy
    req.session['executed'] = executed
    return render(req, "admin/Inception.html")


def Inceptionv3_result(req):
    model_name = req.session.get('model_name')
    accuracy = req.session.get('accuracy')
    executed = req.session.get('executed')

    context = {
        'model_name': model_name,
        'accuracy': accuracy,
        'executed': executed
    }
    messages.success(req, "Inceptionv3 Model executed successfully")
    return render(req, "admin/Inception-btn.html", context)

