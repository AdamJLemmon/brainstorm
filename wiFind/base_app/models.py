from django.db import models

# Create your models here.


# each user account matches one model in db and may be associated with many nodes
# each user account also has an associated eth account auto created
class UserAccount(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    eth_account_address = models.CharField(max_length=42)

    # useful string that is returned when entry found in db
    def __str__(self):
        return self.user_name


# each registered node creates a model and is associate to an eth contract
class Node(models.Model):
    node_id = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    eth_contract_address = models.CharField(max_length=42)
    # one to many relation from user accounts to nodes
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, default=None)

    # useful string that is returned when entry found in db
    def __str__(self):
        return self.node_id
