from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.db.models import Count
import os
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.forms import modelformset_factory


def imp_check(user):
    return user.useraccept.imp == True

def login_view(request):
    form = LoginImpForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            auth_login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'authentication_login.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None,auto_id=False)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email=form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.username = username
        new_user.set_password(password)
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            auth_login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'register_form.html', context)

def save_comment_form(new_comment,comment_text,files,rating,init_user,adition_user,employee,competence,another_employee):
    new_comment.comment_text = comment_text
    new_comment.files = files
    new_comment.rating = rating
    new_comment.init_user = init_user
    new_comment.save()
    for user in adition_user:
        new_comment.recipient_user.add(user)
    for user in employee:
        new_comment.employee.add(user)
    for user in competence:
        new_comment.competence.add(user)
    for user in another_employee:
        new_comment.another_employee.add(user)
    for user in another_employee:
        new_comment.recipient_user.add(user)
    for user in employee:
        new_comment.recipient_user.add(user)

def comment_counter(user):
    return Comment.objects.filter(user=user.id).count() + Comment.objects.filter(recipient_user=user.id).count()

# Create your views here.

def base(request):
    return render(request, 'coming.html',)

@login_required
@user_passes_test(imp_check)
def create_employee_view(request):
    form_user = RegistrationEmployeeMainForm(request.POST or None, request.FILES or None,prefix='user')
    form_useraccept = RegistrationEmployeeAdditionForm(request.POST or None, request.FILES or None, prefix='useraccept')
    if form_user.is_valid() and form_useraccept.is_valid():
        new_user = form_user.save(commit=False)
        username = form_user.cleaned_data['username']
        first_name = form_user.cleaned_data['first_name']
        last_name = form_user.cleaned_data['last_name']
        email=form_user.cleaned_data['username']
        new_user.email = email
        new_user.username = username
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.set_password(form_user.cleaned_data['password'])
        new_user.save()
        user_company = form_useraccept.save(commit=False)
        user_company.user = new_user
        user_company.company = request.user.useraccept.company
        user_company.gov = form_useraccept.cleaned_data['gov']
        user_company.phone_number = form_useraccept.cleaned_data['phone_number']
        user_company.date_birth = form_useraccept.cleaned_data['date_birth']
        user_company.social_net = form_useraccept.cleaned_data['social_net']
        user_company.position = form_useraccept.cleaned_data['position']
        user_company.avatar = form_useraccept.cleaned_data['avatar']
        user_company.save()
        return HttpResponseRedirect(reverse('employee_list'))
    context = {
        'form_user': form_user,'form_useraccept': form_useraccept
    }
    return render(request, 'create-employee.html', context)

def registration_employee_view(request):
    form = RegistrationEmployeeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user = request.user
        email=form.cleaned_data['username']
        new_user.email = email
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        user_company=UserAccept(user=User.objects.get(id = new_user.id),company=user.useraccept.company)
        user_company.save()
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    context = {
        'form': form
    }
    return render(request, 'register_form.html', context)


@login_required
@user_passes_test(imp_check)
def edit_employee_view(request,user_id):
    user = User.objects.get(id=user_id)
    useraccept = UserAccept.objects.get(id=user.useraccept.id)
    form_user = EmployeeMainForm(request.POST or None, request.FILES or None, initial=model_to_dict(user), instance=user,prefix='user')
    form_useraccept = EmployeeAdditionForm(request.POST or None, request.FILES or None, initial=model_to_dict(useraccept), instance=useraccept,prefix='useraccept')
    if form_user.is_valid() and form_useraccept.is_valid():
        new_user = form_user.save(commit=False)
        username = form_user.cleaned_data['username']
        first_name = form_user.cleaned_data['first_name']
        last_name = form_user.cleaned_data['last_name']
        email=form_user.cleaned_data['username']
        new_user.email = email
        new_user.username = username
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        user_company = form_useraccept.save(commit=False)
        user_company.gov = form_useraccept.cleaned_data['gov']
        user_company.phone_number = form_useraccept.cleaned_data['phone_number']
        user_company.date_birth = form_useraccept.cleaned_data['date_birth']
        user_company.social_net = form_useraccept.cleaned_data['social_net']
        user_company.position = form_useraccept.cleaned_data['position']
        user_company.avatar = form_useraccept.cleaned_data['avatar']
        user_company.save()
        return HttpResponseRedirect(reverse('employee_list'))
    context = {
        'form_user': form_user,'form_useraccept': form_useraccept,'user': user,'useraccept': useraccept
    }
    return render(request, 'edit-employee.html', context)

@login_required
@user_passes_test(imp_check)
def employee_list(request):
    user=request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    employee_list = UserAccept.objects.select_related('user').filter(company=user.useraccept.company)
    return render(request, 'employees-table.html',{'employee_list':employee_list,'comment_count':comment_count,'accept_count':accept_count})


def lichniy_kabinet(request):
    user = request.user
    comment_list_in = Comment.objects.prefetch_related('user','competence').filter(user=user.id)
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    comment_list_out = Comment.objects.prefetch_related('user','competence').filter(recipient_user=user.id)
    context = {
    'comment_list_in':comment_list_in,
    'comment_list_out':comment_list_out,
    'comment_count':comment_count,
    'accept_count':accept_count
    }
    return render(request, 'lk_comment_list.html', context)


def competence_list(request):
    user = request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    competence_list=Competence.objects.all()
    form = CompetenceForm(request.POST or None)
    if form.is_valid():
        new_competence = form.save(commit=False)
        competence_name = form.cleaned_data['competence_name']
        new_competence.competence_name = competence_name
        new_competence.owner=request.user
        new_competence.save()
        return HttpResponseRedirect(reverse('competence_list'))
    return render(request, 'competence_form.html',{'form': form,'competence_list':competence_list,'comment_count':comment_count,'accept_count':accept_count})


def delete_comment(request, comment_id):
    author_id = request.user
    Comment.objects.get(user=author_id,id=comment_id,accept=False).delete()
    return HttpResponseRedirect(reverse('lichniy-kabinet'))


def lk_comment(request, comment_id):
    user = request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    comment = Comment.objects.get(user=user.id,id=comment_id)
    form = CommentEditForm(request.POST or None, request.FILES or None, initial=model_to_dict(comment), instance=comment)
    if form.is_valid():
        new_comment = form.save(commit=False)
        implementer_flag = form.cleaned_data['implementer_flag']
        customer_flag = form.cleaned_data['customer_flag']
        implementer = form.cleaned_data['implementer']
        init_user = form.cleaned_data['init_user']
        competence = form.cleaned_data['competence']
        employee = form.cleaned_data['employee']
        rating = form.cleaned_data['rating']
        files = form.cleaned_data['files']
        comment_text = form.cleaned_data['comment_text']
        adition_user = form.cleaned_data['adition_user']
        another_employee = form.cleaned_data['another_employee']
        if implementer_flag == True:
            new_comment.implementer = init_user
            new_comment.customer = implementer
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))    
        if customer_flag == True:
            new_comment.implementer = implementer
            new_comment.customer = init_user
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})
    return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})


def add_comment(request):
    user = request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    form = CommentEditForm(request.POST or None, request.FILES or None, auto_id=False)
    if form.is_valid():
        new_comment = form.save(commit=False)
        implementer_flag = form.cleaned_data['implementer_flag']
        customer_flag = form.cleaned_data['customer_flag']
        implementer = form.cleaned_data['implementer']
        init_user = form.cleaned_data['init_user']
        competence = form.cleaned_data['competence']
        employee = form.cleaned_data['employee']
        rating = form.cleaned_data['rating']
        files = form.cleaned_data['files']
        comment_text = form.cleaned_data['comment_text']
        adition_user = form.cleaned_data['adition_user']
        another_employee = form.cleaned_data['another_employee']
        if implementer_flag == True:
            new_comment.implementer = init_user
            new_comment.customer = implementer
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))    
        if customer_flag == True:
            new_comment.implementer = implementer
            new_comment.customer = init_user
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})
    return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})


def lk_accept(request):
    user = request.user
    comment_list = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).select_related('user')
    comment_count = comment_counter(user=user) 
    accept_count = Comment.objects.filter(recipient_user=request.user.id,accept=False,failure=False).count()
    return render(request, 'lk_accept.html',{'comment_list':comment_list,'comment_count':comment_count,'accept_count':accept_count})


def accept_comment(request, comment_id):
    user = request.user
    comment_count = comment_counter(user=user) 
    accept_count = Comment.objects.filter(recipient_user=request.user.id,accept=False,failure=False).count()
    comment = Comment.objects.get(recipient_user=request.user.id,id=comment_id,accept=False)
    form = AcceptForm(request.POST or None,instance=comment)
    if form.is_valid():
        new_accept = form.save(commit=False)
        accept = form.cleaned_data['accept']
        failure = form.cleaned_data['failure']
        if failure == True:
        	return HttpResponseRedirect(f'../lk-failure/failure-{comment_id}-comment')
        if accept == True:
            user=User.objects.get(id=request.user.id)
            user.useraccept.accept=True
            user.useraccept.save()
            for user in comment.recipient_user.all():
                users=User.objects.get(id=user.id)
                if users.useraccept.accept == False:
                    print("Fail!")
                    break
            else:
                new_accept.accept = accept
                recipient_users=''
                for user in comment.recipient_user.all():
                    recipient_users+=(user.last_name + user.first_name + user.useraccept.company +',')
                    user=User.objects.get(id=user.id)
                    user.useraccept.accept=False
                    user.useraccept.save()
                data_comment=f'''"
                    Status - accepted, user - {comment.user}, recipient_users - {recipient_users}, 
                    comment - {comment.comment_text}"'''
                command=r'''curl -H "Content-type:application/json" --data '{"data":'''+data_comment+r'''}' http://localhost:3001/mineBlock'''
                print(data_comment,command)
                os.system(command)
                new_accept.save()
                return HttpResponseRedirect(reverse('lichniy-kabinet'))
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    return render(request, 'accept_form.html', {'form': form,'comment':comment,'comment_count':comment_count,'accept_count':accept_count})



def lk_failure(request,comment_id):
    user=request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    comment = Comment.objects.get(recipient_user=user.id,id=comment_id,failure=False)
    form = AcceptForm(request.POST or None,initial=model_to_dict(comment),instance=comment)
    if form.is_valid():
        new_failure = form.save(commit=False)
        failure_text = form.cleaned_data['failure_text']
        new_failure.failure_text = failure_text
        new_failure.save()
        user=User.objects.get(id=request.user.id)
        user.useraccept.failure=True
        user.useraccept.save()
        for user in comment.recipient_user.all():
            users=User.objects.get(id=user.id)
            if users.useraccept.failure == False:
                break
        else:
            new_failure.failure=True
            recipient_users=''
            for user in comment.recipient_user.all():
                recipient_users+=(user.last_name + user.first_name + user.useraccept.company +',')
                user=User.objects.get(id=user.id)
                user.useraccept.failure=False
                user.useraccept.save()
            data_comment=f'''"
                Status - failure, user - {comment.user}, recipient_users - {recipient_users}, comment - {comment.comment_text}, 
                reason - {failure_text}"'''
            command=r'''curl -H "Content-type:application/json" --data '{"data":'''+data_comment+r'''}' http://localhost:3001/mineBlock'''
            os.system(command)
            new_failure.save()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    return render(request, 'failure_form.html', {'form': form,'comment':comment,'comment_count':comment_count,'accept_count':accept_count})


def comment_info(request, comment_id):
    user=request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    disputs = Disputs.objects.filter(comment=comment_id)
    comment = Comment.objects.get(id=comment_id)
    form = DisputForm(request.POST or None)
    if form.is_valid():
        new_disput = form.save(commit=False)
        text = form.cleaned_data['text']
        new_disput.text = text
        new_disput.user = user
        new_disput.comment = comment
        new_disput.save()
        return HttpResponseRedirect(f'../lk-accepted-list/info-{comment_id}-comment')
    return render(request, 'comment_info.html', {'form': form,'disputs':disputs,'comment':comment,'comment_count':comment_count,'accept_count':accept_count})

@login_required
@user_passes_test(imp_check)
def employee_info(request, user_id):
    user = User.objects.get(id=user_id)
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    verify_count = Comment.objects.filter(recipient_user=user.id,accept=True).count() + Comment.objects.filter(user=user.id,accept=True).count() 
    return render(request, 'employee.html', {'user':user,'comment_count':comment_count,'accept_count':accept_count,'verify_count':verify_count})

@login_required
@user_passes_test(imp_check)
def appeal_info(request, appeal_id):
    appeal = Appeal.objects.get(id=appeal_id,accepter=request.user.useraccept.company)
    messeges = MessegesAppeal.objects.prefetch_related('user','accepter').filter(appeal=appeal)
    rubricator = appeal.rubricator.get_ancestors(ascending=False, include_self=True)
    form = MessegesAppealForm(request.POST or None)
    if form.is_valid():
        new_disput = form.save(commit=False)
        text = form.cleaned_data['text']
        new_disput.text = text
        new_disput.user = request.user
        new_disput.accepter = appeal.accepter
        new_disput.appeal = appeal
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'appeal-card.html', {'rubricator':rubricator,'appeal':appeal,'messeges':messeges,'form': form})

@login_required
@user_passes_test(imp_check)
def appeal_list(request):
    appeals = Appeal.objects.prefetch_related('user').filter(accepter=request.user.useraccept.company)
    return render(request, 'appeal-table.html', {'appeals':appeals})

@login_required
@user_passes_test(imp_check)
def appeal_accept(request, appeal_id):
    appeal = Appeal.objects.get(id=appeal_id,accepter=request.user.useraccept.company)
    if appeal.accept == True:
        return HttpResponseRedirect(reverse('appeal_list'))
    appeal.accept = True
    new_order = Order()
    new_order.company = request.user.useraccept.company
    new_order.appeal = appeal
    new_order.rubricator = appeal.rubricator
    new_order.save()
    if appeal.failure == True:
        appeal.failure = False
    appeal.save()
    return HttpResponseRedirect(reverse('appeal_list'))

@login_required
@user_passes_test(imp_check)
def appeal_failure(request, appeal_id):
    appeal = Appeal.objects.get(id=appeal_id,accepter=request.user.useraccept.company)
    if appeal.failure == True:
        return HttpResponseRedirect(reverse('appeal_list'))
    appeal.failure = True
    if appeal.accept == True:
        appeal.accept = False
    appeal.save()
    return HttpResponseRedirect(reverse('appeal_list'))

@login_required
@user_passes_test(imp_check)
def order_list(request):
    orders = Order.objects.prefetch_related('company','appeal').filter(company=request.user.useraccept.company)
    return render(request, 'orders-list.html', {'orders':orders})

@login_required
@user_passes_test(imp_check)
def card_list(request,rubricator_id):
    rubricator = Rubricator.objects.get(id=rubricator_id)
    qs = []
    for i in rubricator.get_children():
        for j in i.get_children():
            qs.append(Card.objects.prefetch_related('company','rubricator').filter(rubricator=j.id))
    cards = qs
    return render(request, 'catalog-sections.html', { 'rubricator':rubricator,'cards':cards})

@login_required
def landing(request):
    rubricator = Rubricator.objects.get(id=5)
    return render(request, 'landing.html', { 'rubricator':rubricator})

@login_required
@user_passes_test(imp_check)
def card_info(request,rubricator_id, card_id):
    card = Card.objects.get(id=card_id)
    rubricator = card.rubricator
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        new_appeal = Appeal()
        new_appeal.size = int(form.cleaned_data['size'])
        new_appeal.user = request.user
        new_appeal.accepter = card.company
        new_appeal.rubricator = rubricator
        new_appeal.save()
        new_order = Order()
        new_order.cost = int(form.cleaned_data['size'])*card.cost_size
        new_order.company = card.company
        new_order.appeal = new_appeal
        new_order.rubricator = rubricator
        new_order.save()
        return HttpResponseRedirect(reverse('order_list'))
    return render(request, 'catalog-card.html', { 'rubricator':rubricator,'card':card,'form':form})

@login_required
@user_passes_test(imp_check)
def stage_accept(request,order_id, stage_id):
    order = Order.objects.get(id=order_id,company=request.user.useraccept.company)
    stage = Stage.objects.get(id=stage_id,order=order)
    stage.accept = True
    stage.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@user_passes_test(imp_check)
def estimate_accept(request,order_id, estimate_id):
    order = Order.objects.get(id=order_id,company=request.user.useraccept.company)
    estimate = Estimate.objects.get(id=estimate_id,order=order)
    estimate.accept = True
    estimate.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    

@login_required
@user_passes_test(imp_check)
def delete_estimate(request, estimate_id,order_id):
    Estimate.objects.get(order=Order.objects.get(id=order_id,company=request.user.useraccept.company),id=estimate_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@user_passes_test(imp_check)
def order_info(request, order_id):
    order = Order.objects.get(id=order_id,company=request.user.useraccept.company)
    messeges = MessegesAppeal.objects.prefetch_related('appeal','accepter').filter(order=order)
    rubricator = order.rubricator.get_ancestors(ascending=False, include_self=True)
    estimate = order.estimate_set.all().first()
    StageFormSet = modelformset_factory(Stage, form=StageForm, extra=0)
    formset = StageFormSet(request.POST or None,queryset=Stage.objects.filter(order=order),prefix='stage')
    form = MessegesAppealForm(request.POST or None,prefix='mesg')
    form_adress = AdressForm(request.POST or None,prefix='adr')
    form_guaranty = GuarantyForm(request.POST or None, request.FILES or None,prefix='guaranty')
    form_estimate = EstimateForm(request.POST or None, request.FILES or None,prefix='estimate')
    if form.is_valid():
        new_disput = form.save(commit=False)
        text = form.cleaned_data['text']
        new_disput.text = text
        new_disput.user = request.user
        new_disput.accepter = order.company
        new_disput.order = order
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if order.adress and order.guaranty:
        form_adress = AdressForm(request.POST or None, initial=model_to_dict(order.adress), instance=order.adress,prefix='adr')
        form_guaranty = GuarantyForm(request.POST or None, request.FILES or None, initial=model_to_dict(order.guaranty), instance=order.guaranty,prefix='guaranty')
        if form_adress.is_valid() and form_guaranty.is_valid():
            new_addr = form_adress.save()
            new_addr.save()
            new_guaranty = form_guaranty.save()
            new_guaranty.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if order.guaranty:
        form_guaranty = GuarantyForm(request.POST or None, request.FILES or None, initial=model_to_dict(order.guaranty), instance=order.guaranty,prefix='guaranty')
        if form_guaranty.is_valid():
            new_guaranty = form_guaranty.save()
            new_guaranty.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:    
        if form_guaranty.is_valid():
            new_guaranty = form_guaranty.save()
            new_guaranty.save()
            order.guaranty = new_guaranty
            order.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            pass
    if order.adress:
        form_adress = AdressForm(request.POST or None, initial=model_to_dict(order.adress), instance=order.adress,prefix='adr')
        if form_adress.is_valid():
            new_addr = form_adress.save()
            new_addr.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:    
        if form_adress.is_valid():
            new_addr = form_adress.save()
            new_addr.save()
            order.adress = new_addr
            order.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if form_estimate.is_valid():
        new_estimate = form_estimate.save(commit=False)
        new_estimate.files = form_estimate.cleaned_data['files']
        new_estimate.order = order
        new_estimate.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if estimate:
        form_estimate_failure = EstimateFailureForm(request.POST or None, prefix='failure')
        if form_estimate_failure.is_valid():
            new_estimate_failure = Estimate.objects.get(id=estimate.id)
            new_estimate_failure.reason = form_estimate_failure.cleaned_data['reason']
            new_estimate_failure.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {
    'rubricator':rubricator,'order':order,'messeges':messeges,'form': form,'form_adress':form_adress,'form_guaranty':form_guaranty,'formset': formset,
    'form_estimate':form_estimate,
    }
    if estimate:
        context['form_estimate_failure']=form_estimate_failure
    return render(request, 'catalog-card-order.html', context)

def show_genres(request):
    return render(request, "customer.html",)

def customer1(request):
    return render(request, "customer1.html",)

def customer2(request):
    return render(request, "customer2.html",)

def customer3(request):
    return render(request, "customer3.html",)