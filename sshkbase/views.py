import django.contrib.auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import User, SSHKey

PERMISSION_NAMES = ['read', 'write']
PERMISSION_LABELS = {'read': 'Read', 'write': 'Write'}


# Other / utility functions
def isNicknameValid(nickname):
    if len(nickname) == 0 or str.isspace(nickname):
        return False

    validList = [c for c in "abcdefghijklmnopqrstuvwxyz0123456789-_"]
    for c in nickname:
        if c not in validList:
            return False
    return True


def isNicknameUnique(nickname):
    for u in User.objects.all():
        if nickname == u.nickname:
            return False
    return True


# === BASIC VIEW FUNCTIONS ===

# Each one of these functions returns a HttpResponse containing the HTML and CSS
# to be displayed by the browser
# Functions ending with 'View' just get the values to be used inside the HTML templates,
# and render their respective template.

def indexView(request):
    # ???
    user = request.user
    if user is None or not user.is_authenticated:
        return render(request, 'sshkbase/index-anonymous.html', {})

    ctx = {
        'user': user,
    }
    return render(request, 'sshkbase/index.html', ctx)


def listView(request):
    userList = User.objects.order_by('nickname')
    ctx = {
        'userList': userList
    }
    return render(request, 'sshkbase/list.html', ctx)


def userAddView(request):
    return render(request, 'sshkbase/userAdd.html', {})


def userLoginView(request):
    return render(request, 'sshkbase/userLogin.html', {})


def userDetailView(request, userNickname):
    user = get_object_or_404(User, pk=userNickname)
    ctx = {
        'user': user,
        'self': request.user
    }
    return render(request, 'sshkbase/userDetail.html', ctx)


def userUpdateView(request):
    user = request.user
    ctx = {
        'user': user,
    }
    return render(request, 'sshkbase/userUpdate.html', ctx)


def userKeysView(request):
    user = request.user
    keys = SSHKey.objects.filter(user__nickname=user.nickname)
    ctx = {
        'user': user,
        'keys': keys
    }
    return render(request, 'sshkbase/userKeys.html', ctx)


def userDeleteView(request):
    user = request.user
    ctx = {
        'user': user
    }
    return render(request, 'sshkbase/userDelete.html', ctx)


def keyAddView(request):
    user = request.user
    ctx = {
        'user': user,
    }
    return render(request, 'sshkbase/keyAdd.html', ctx)


# View details about a key
def keyDetailView(request, keyId):
    sshkey = get_object_or_404(SSHKey, pk=keyId)
    permInt = sshkey.permissions
    perms = dict()

    for n in PERMISSION_NAMES:
        perms[n] = bool(permInt & 1)
        permInt >>= 1
    ctx = {
        'sshkey': sshkey,
        'perms': perms,
        'perm_labels': PERMISSION_LABELS
    }

    return render(request, 'sshkbase/keyDetail.html', ctx)


def keyDeleteView(request, keyId):
    sshkey = get_object_or_404(SSHKey, pk=keyId)
    ctx = {
        'sshkey': sshkey
    }
    return render(request, 'sshkbase/keyDelete.html', ctx)


# === POST REQUEST HANDLERS ===

# Functions like this one are used when the browser sends a POST request containing information.
# The browsers send a POST request when it is necessary to send data to the server (and change some things
# in the database)
# This function adds a new user in the database
def addUser(request):
    # We gather the information sent with the request
    nickname = request.POST['nickname']
    full_name = request.POST['full-name']
    email = request.POST['email']
    password = request.POST['password']
    # Perform some checks to see if the given data is correct
    if not isNicknameValid(nickname):
        # If not, send a HTTP response to display whatever page we want (in this case the same page),
        # but with an error message attached
        return render(request, 'sshkbase/userAdd.html', {
            'nickname_try': nickname,
            'name_try': full_name,
            'email_try': email,
            'error_msg': "Your nickname may only contain lowercase letters, digits, dashes and underscores."
        })

    if not isNicknameUnique(nickname):
        return render(request, 'sshkbase/userAdd.html', {
            'nickname_try': nickname,
            'name_try': full_name,
            'email_try': email,
            'error_msg': "This nickname is already used."
        })

    # Create the object to be stored in the DB, give it all its values and save it
    user = User.objects.create_user(nickname=nickname, name=full_name, email=email, password=password)
    try:
        validate_password(password, user)
    except ValidationError as err:
        user.delete()
        return render(request, 'sshkbase/userAdd.html', {
            'nickname_try': nickname,
            'name_try': full_name,
            'email_try': email,
            'error_msg': "Your password is invalid :",
            'passwd_errors': err.error_list
        })

    print("Added user " + user.nickname)
    # Finally send a HTTP response to redirect the user to a different page
    return HttpResponseRedirect(reverse('sshkbase:index'))


def loginUser(request):
    nickname = request.POST['nickname']
    rawPassword = request.POST['password']

    user = authenticate(request, nickname=nickname, password=rawPassword)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('sshkbase:index'))
    else:
        return render(request, 'sshkbase/userLogin.html', {
            'nickname_try': nickname,
            'error_msg': "Unknown password and/or username."
        })


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('sshkbase:index'))


def updateUser(request):
    # For update functions like this one, we get the existing object with the nickname we got from the URL,
    user = request.user
    newName = request.POST['name']
    # Change its name
    user.name = newName
    # And save it again to update the database
    user.save()
    print("Updated user " + user.nickname)
    # Then send a redirect response to redirect the user to the user detail page
    return HttpResponseRedirect(reverse('sshkbase:user-detail', args=(user.nickname,)))


# For deletion, we only need to get the object in the database, call the 'delete()' function.
# then redirect to the previous index page
def deleteUser(request):
    user = request.user
    user.delete()
    print("Deleted user " + user.nickname)
    return HttpResponseRedirect(reverse('sshkbase:index'))


# Functions for keys do basically the same thing as user ones, but on keys.
def addKey(request):
    user = request.user
    print("Received POST request : " + str(request.POST))
    title = request.POST['title']
    if len(title) == 0 or str.isspace(title):
        return render(request, 'sshkbase/keyAdd.html', {
            'user': user,
            'error_msg': "You must specify a title for the key"
        })
    title = str.strip(title)
    key = request.POST['key']
    if len(key) == 0 or str.isspace(key):
        return render(request, 'sshkbase/keyAdd.html', {
            'user': user,
            'error_msg': "The key cannot be empty"
        })
    key = str.strip(key)

    date = timezone.now()
    permissions = 0
    for i in range(len(PERMISSION_NAMES)):
        n = PERMISSION_NAMES[i]
        fullName = 'perm-' + n
        if fullName in request.POST and request.POST[fullName] == 'on':
            permissions |= (1 << i)
    keyObj = SSHKey(user=user, title=title, key=key, addDate=date, permissions=permissions)
    keyObj.save()
    print("Added key #" + str(keyObj.id) + " to user " + user.nickname)
    return HttpResponseRedirect(reverse('sshkbase:user-keys'))


def updateKey(request, keyId):
    sshkey = get_object_or_404(SSHKey, pk=keyId)
    permInt = sshkey.permissions
    perms = dict()

    for n in PERMISSION_NAMES:
        perms[n] = bool(permInt & 1)
        permInt >>= 1
    title = request.POST['title']
    if len(title) == 0 or str.isspace(title):
        return render(request, 'sshkbase/keyDetail.html', {
            'sshkey': sshkey,
            'perms': perms,
            'perm_labels': PERMISSION_LABELS,
            'error_msg': "You must specify a title for the key"
        })
    sshkey.title = str.strip(title)
    key = request.POST['key']
    if len(key) == 0 or str.isspace(key):
        return render(request, 'sshkbase/keyDetail.html', {
            'sshkey': sshkey,
            'perms': perms,
            'perm_labels': PERMISSION_LABELS,
            'error_msg': "The key cannot be empty"
        })
    sshkey.key = str.strip(key)
    sshkey.permissions = 0
    for n in PERMISSION_NAMES:
        sshkey.permissions <<= 1
        fullName = 'perm-' + n
        if fullName in request.POST and request.POST[fullName] == 'on':
            sshkey.permissions |= 1
    sshkey.save()
    print("Updated key #" + str(keyId))
    return HttpResponseRedirect(reverse('sshkbase:user-keys'))


def deleteKey(request, keyId):
    sshkey = get_object_or_404(SSHKey, pk=keyId)
    userNickname = sshkey.user.nickname
    sshkey.delete()
    print("Deleted key #" + str(keyId))
    return HttpResponseRedirect(reverse('sshkbase:user-keys'))
