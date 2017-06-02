from django.http import JsonResponse


def read_highlow_contract(request):
    f = open("contracts/HighLowBet.sol", "r")
    contract = f.read()

    return JsonResponse({'data': contract})
