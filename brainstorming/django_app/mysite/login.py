from django.http import JsonResponse
from django.http import HttpResponseRedirect
# from django.urls import reverse
from django.urls import resolve
from .mongo_storage_api import StorageManager
from .constants import *


storage_manager = StorageManager('localhost', 27017, 'lt_game')


def attempt_login(request):

    username = request.GET.get(USERNAME, None)
    password = request.GET.get(PASSWORD, None)

    # init return data
    data = {
        REQ_STATE: 'success',
        USERNAME: username
    }

    # query users to find username
    cursor = storage_manager.find(USERS_COLLECTION, {USERNAME: username})

    # if there is an item in the cursor than name exits
    if cursor.count():

        # check to see if password is incorrect
        if username + password != cursor[0][USERNAME] + cursor[0][PASSWORD]:
            data[REQ_STATE] = 'Incorrect password'

    # user name does not exist
    else:
        data[REQ_STATE] = 'Username does not exist'

    return JsonResponse(data)


def create_user(request):

    username = request.GET.get(USERNAME, None)
    password = request.GET.get(PASSWORD, None)
    email = request.GET.get(EMAIL, None)

    # init return data
    data = {
        REQ_STATE: 'success',
        USERNAME: username
    }

    # query users to see username already exists
    cursor = storage_manager.find(USERS_COLLECTION, {USERNAME: username})

    # if there is an item in the cursor than name exits
    if cursor.count():
        data[REQ_STATE] = 'Username already exists'

    # new user, create
    else:
        storage_manager.insert(USERS_COLLECTION,
                               {
                                   USERNAME: username,
                                   PASSWORD: password,
                                   EMAIL: email,
                                   BALANCE: 0
                               })

    return JsonResponse(data)


def update_user(request):
    username = request.GET.get(USERNAME, None)
    action = request.GET.get('action', None)
    attr = request.GET.get('attr', None)
    new_account = request.GET.get('accountAddr', None)

    response = storage_manager.update(USERS_COLLECTION, {USERNAME: username}, {action: {attr: new_account}})

    return JsonResponse({REQ_STATE: str(response)})


def change_password(request):
    print("CHANGING PASSWORD!")
    print("Mongo entry...")
    print("Redirecting...")
    return HttpResponseRedirect("/dashboard/")

def get_account_address(request):
    print("getting address")
    username = request.GET.get(USERNAME, None)

    print(username)

    # init return data
    data = {
        REQ_STATE: 'success',
        USERNAME: username,
        ACCOUNT_ADDRESS: None
    }

    # query users to find username
    cursor = storage_manager.find(USERS_COLLECTION, {USERNAME: username})

    print(cursor.count())

    # if there is an item in the cursor than name exits
    if cursor.count():
        print("got cursor")
        data[ACCOUNT_ADDRESS] = cursor[0][ACCOUNT_ADDRESS]
        print(cursor[0][ACCOUNT_ADDRESS])

    return JsonResponse(data)

def update_balance(request):
    print("updating balance")
    username = request.GET.get(USERNAME, None)
    balance = request.GET.get(BALANCE, None)

    print(username)

    # init return data
    data = {
        REQ_STATE: 'success',
        USERNAME: username,
        BALANCE: 0
    }

    # query users to find username
    cursor = storage_manager.update(USERS_COLLECTION, {USERNAME: username}, {'$set': {BALANCE: balance}})

    if 'ok' in cursor and cursor['ok'] == '1.0':
        data[BALANCE] = cursor[0][BALANCE]
        print(cursor[0][ACCOUNT_ADDRESS])

    return JsonResponse(data)



