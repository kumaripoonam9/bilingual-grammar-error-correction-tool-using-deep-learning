from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random, os, json

from .models import Room, Message, ExpertLanguage, PendingExpertReview
from expert.forms import ExpertLanguageForm, InputMessageForm

from spellcheck.forms import FileUploadForm





# ------- edit room name
def edit_room_name(request, room_name):
    
    data = json.loads(request.body)
    print(data)
    print(room_name)

    edited_room_name = data['edited_room_name'].strip()

    user_profile = request.user.profile.user_type
    # success = room.edit_room_name(edited_room_name, user_profile)

    room = Room.objects.get(room_name=room_name)

    if user_profile == "Expert user":
        room.expert_room_name = edited_room_name
    else:
        room.user_room_name = edited_room_name
        
    room.save()

    context = {}
    return render(request, "expert/chat.html", context)




# --------- shows all the rooms on side -----------
@login_required(login_url='login')
def chat(request):
    username = request.user
    get_messages = Message.objects.filter(sender=username)

    # print(username)
    
    room_user_map = {
        # room: user,
        
    }

    get_rooms = []
    allusers = []

    for msg in get_messages:
        if msg.room.room_name not in get_rooms:
            room = msg.room.room_name
            get_rooms.append(msg.room.room_name)
            
            get_room_msg_list = Message.objects.filter(room=msg.room)

            for m in get_room_msg_list:
                if m.sender != request.user.username:
                    room_user_map[room] = m.sender

                if m.sender != request.user.username and m.sender not in allusers:
                    allusers.append(m.sender)

    allrooms = Room.objects.filter(room_name__in=get_rooms)
    
    print(allrooms)

    print(get_rooms, allusers)

    context = {
        'convo': False,
        'rooms': get_rooms,
        'allrooms': allrooms,
        'allusers': allusers
    }
    
    return render(request, "expert/chat.html", context)




# ------- finding expert --------
@login_required(login_url='login')
def expert_review(request):
    secret_code = ''

    if request.method == 'POST':
        if 'secret_code_button' in request.POST:

            username = request.user
            room = request.POST['room']

            try:
                get_room = Room.objects.get(room_name=room)
                return redirect('room', room_name=room)

            except Room.DoesNotExist:
                new_room = Room(room_name=room)
                new_room.save()

                return redirect('room', room_name=room)
        
        elif 'expert_lang_requested_button' in request.POST:

            expert_lang_requested = request.POST.get('expert_lang_requested')
            
            get_experts = ExpertLanguage.objects.filter(languages_known=expert_lang_requested, verified=True).values() | ExpertLanguage.objects.filter(languages_known='Both hindi and english', verified=True).values()

            random_expert = random.choice(get_experts)     # random selection of an expert
            
            random_expert_username = User.objects.get(id=random_expert['user_id']).username
            random_expert_userid = random_expert['user_id']
            username = request.user.username
            userid = request.user.id
            # creating secret key (room name)
            secret_code = f'{username[0]}{username[-1]}-{userid}-{random_expert_userid}-{random_expert_username[0]}{random_expert_username[-1]}'

            print(f'room name = {secret_code}\nuser = {username}\nexpert = {random_expert_username}')

            # saving new rooms to pending room
            try:
                get_room = Room.objects.get(room_name=secret_code)                
            except Room.DoesNotExist:
                new_room = Room(room_name=secret_code)
                new_room.save()
                new_room = Room.objects.get(room_name=secret_code)
                try:
                    get_room = PendingExpertReview.objects.get(pending_room=new_room)
                except PendingExpertReview.DoesNotExist:
                    random_expert = User.objects.get(id=random_expert['user_id'])
                    new_pending_room = PendingExpertReview(expert=random_expert, pending_room=new_room)
                    new_pending_room.save()

            # context = {'secret_code': secret_code}
            # return render(request, "expert/expertreview.html", context)
    
    pending_rooms = PendingExpertReview.objects.filter(expert=request.user)
    # print(pending_rooms)
    context = {
        'secret_code': secret_code,
        'pending_rooms': pending_rooms,
    }
    return render(request, "expert/expertreview.html", context)




#---- to display messages in the inbox ----
@login_required(login_url='login')
def messaging(request, room_name):

    # file_form = FileUploadForm()
    input_form = InputMessageForm()

    # for side list
    username = request.user
    get_messages = Message.objects.filter(sender=username)
    
    get_rooms = []
    allusers = []
    for msg in get_messages:
        if msg.room not in get_rooms:
            get_rooms.append(msg.room)
            get_msg_list = Message.objects.filter(room=msg.room)
            for m in get_msg_list:
                if m.sender != username and m.sender not in allusers:
                    allusers.append(m.sender)
    # end-- for side list
    allrooms = Room.objects.filter(room_name__in=get_rooms)


    
    get_room = Room.objects.get(room_name=room_name)

    if request.method == "POST":
        # print(bool(request.POST.get('message')), request.FILES.get('attachment'))

        if request.FILES.get('attachment') or bool(request.POST.get('message'))==True:
            input_form = InputMessageForm(request.POST, request.FILES)
            
            if input_form.is_valid():
                new_message = input_form.save(commit=False)
                new_message.room = get_room
                new_message.sender = request.user
                new_message.save()

                input_form = InputMessageForm()

                if request.user.profile.user_type == "Expert user":
                    # expert = request.user
                    # room = Room.objects.get(room_name=get_room)
                    try:
                        pending_room = PendingExpertReview.objects.get(pending_room=get_room)
                        pending_room.delete()
                    except PendingExpertReview.DoesNotExist:
                        pass
    # else:
    #     expertlangform = ExpertLanguageForm()


    # if request.method == 'POST':
    #     message = request.POST['message']
    #     message = message.strip()
    #     username = request.user

    #     new_message = Message(room=get_room, sender=username, message=message)
    #     new_message.save()

    #     if request.user.profile.user_type == "Expert user":
    #         # expert = request.user
    #         # room = Room.objects.get(room_name=get_room)
    #         try:
    #             pending_room = PendingExpertReview.objects.get(pending_room=get_room)
    #             pending_room.delete()
    #         except PendingExpertReview.DoesNotExist:
    #             pass

    get_messages = Message.objects.filter(room=get_room)
    get_sender = request.user

    for msg in get_messages:
        if msg.sender!=get_sender:
            get_sender = msg.sender
            break

    # print(get_sender)

    

    context = {
        'convo': True, 
        'messages': get_messages,

        'user': request.user,
        'sender': get_sender,

        'room_name': room_name,
        'current_room': get_room,

        'rooms': get_rooms,
        'allrooms': allrooms,
        'allusers': allusers,

        # 'file_form': file_form,
        'input_form': input_form,
    }
    
    return render(request, "expert/chat.html", context)



@login_required(login_url='login')
def verification(request):

    if request.method == "POST":
        expertlangform = ExpertLanguageForm(request.POST, request.FILES) 
        if expertlangform.is_valid():
            expertlangs = expertlangform.save(commit=False)
            expertlangs.user = request.user
            expertlangs.save()
            return redirect('profile')
        
    else:
        expertlangform = ExpertLanguageForm()

    context = {
        'expertlangform': expertlangform
    }
    return render(request, "expert/expert_verification.html", context)




