#!/usr/bin/python3
"""Try to connect to database"""

from models import general_injector, injector, initModelsAndStorage, storage


initModelsAndStorage()

User = injector['User']

user = User()
print(user.getRequiredAttributes())

# for item in storage.all(User).values():
#     if item.last_name != 'davenchy':
#         continue
#     item.last_name = 'a7a'
#     item.save()

# print(obj)
