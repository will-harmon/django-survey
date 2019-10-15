from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import SurveyForm, ChoiceFormSet
from .models import Survey, Choice, User

class IndexView(generic.ListView):
    template_name = 'surveys/index.html'
    # instead of using object_list
    context_object_name = 'survey_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Survey.objects.all()

class DetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/detail.html'

class ResultsView(generic.DetailView):
    model = Survey
    template_name = 'surveys/results.html'

# class CreateView(generic.CreateView):
#     model = Question
#     template_name = 'polls/create.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

class CreateView(generic.CreateView):
    model = Survey
    template_name = 'surveys/create.html'
    form_class = SurveyForm
    success_url = 'surveys/index/'

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = SurveyForm(self.request.POST)
            context['formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['form'] = SurveyForm()
            context['formset'] = ChoiceFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        formset = context['formset']
        if all([form.is_valid(), formset.is_valid()]):
            form.instance.created_by = self.request.user
            survey = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    choice = inline_form.save(commit=False)
                    choice.survey = survey
                    choice.save()
            return HttpResponseRedirect(reverse('surveys:index',))

def vote(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    try:
        selected_choice = survey.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'surveys/detail.html', {
            'survey': survey,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('surveys:results', args=(survey.id,)))
