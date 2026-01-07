from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


# 🔹 INDEX VIEW – Question list
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, "polls/index.html", context)


# 🔹 DETAIL VIEW – Single question + form
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


# 🔹 VOTE VIEW – POST request handle
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"]
        )
    except (KeyError, Choice.DoesNotExist):
        # Agar user ne choice select nahi ki
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # Vote increment karo
        selected_choice.votes += 1
        selected_choice.save()

        # POST ke baad redirect (BEST PRACTICE)
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )


# 🔹 RESULTS VIEW – Result page
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
