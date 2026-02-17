import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Voter, Candidate, Vote



# ---------- PAGE VIEWS ----------
from django.db.models import Count

def login_view(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')


def voting(request):
    voter_id = request.session.get("voter_id")
    if not voter_id:
        return redirect("/")

    voter = Voter.objects.get(id=voter_id)

    # 🔒 Option 1 UX fix: block voting page after vote
    if voter.has_voted:
        return redirect("/results/")

    candidates = Candidate.objects.all()
    return render(request, 'voting.html', {'candidates': candidates})


def results(request):
    # ✅ OPTION 1: dynamic vote counting
    results = Candidate.objects.annotate(
        total_votes=Count("votes")
    ).order_by("-total_votes")

    return render(request, 'results.html', {
        'results': results
    })
# ---------- API VIEWS ----------
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import Voter

def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    data = request.POST

    govt_voter_id = data.get('govt_voter_id')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # 1️⃣ Required field check
    if not govt_voter_id:
        return JsonResponse({
            'success': False,
            'message': 'Govt Voter ID is required'
        })

    # 2️⃣ Password match check
    if password != confirm_password:
        return JsonResponse({
            'success': False,
            'message': 'Passwords do not match'
        })

    # 3️⃣ Duplicate voter check
    if Voter.objects.filter(govt_voter_id=govt_voter_id).exists():
        return JsonResponse({
            'success': False,
            'message': 'Govt Voter ID already registered'
        })

    # 4️⃣ Safe creation
    Voter.objects.create(
        full_name=data.get('full_name'),
        govt_voter_id=govt_voter_id,
        username=data.get('username'),
        gender=data.get('gender'),
        constituency=data.get('constituency'),
        dob=data.get('dob'),
        password=make_password(password)
    )

    return JsonResponse({
        'success': True,
        'message': 'Registration successful'
    })

from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .models import Voter

def login_user(request):
    if request.method == "POST":
        data = request.POST

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({
                "success": False,
                "message": "Username and password required"
            })

        try:
            voter = Voter.objects.get(username=username)
        except Voter.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Invalid username or password"
            })

        if not check_password(password, voter.password):
            return JsonResponse({
                "success": False,
                "message": "Invalid username or password"
            })

        # ✅ STEP-2 FIX: store voter identity in session
        request.session["voter_id"] = voter.id
        request.session["username"] = voter.username
        request.session["is_logged_in"] = True

        return JsonResponse({
            "success": True, 
            "message": "Login successful"
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid request"
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Voter, Candidate, Vote

def submit_vote(request):
    if request.method == "POST":

        voter_id = request.session.get("voter_id")
        if not voter_id:
            return JsonResponse({
                "status": "error",
                "message": "User not logged in"
            })

        voter = Voter.objects.get(id=voter_id)

        if voter.has_voted:
            return JsonResponse({
                "status": "error",
                "message": "You have already voted"
            })

        candidate_id = request.POST.get("candidate_id")
        if not candidate_id:
            return JsonResponse({
                "status": "error",
                "message": "Invalid candidate"
            })

        candidate = get_object_or_404(Candidate, id=candidate_id)

        try:
            Vote.objects.create(
                voter=voter,
                candidate=candidate
            )
            voter.has_voted = True
            voter.save()

            return JsonResponse({
                "status": "success",
                "message": "Vote submitted successfully"
            })

        except IntegrityError:
            return JsonResponse({
                "status": "error",
                "message": "You have already voted"
            })

def dashboard(request):
    voter_id = request.session.get("voter_id")

    if not voter_id:
        return redirect("/")

    voter = Voter.objects.get(id=voter_id)

    has_voted = Vote.objects.filter(voter=voter).exists()

    return render(request, "dashboard.html", {
        "voter": voter,
        "has_voted": has_voted
    })
