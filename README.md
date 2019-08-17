# task-17-aug-2019
[![Build Status](https://travis-ci.org/ihor-nahuliak/task-17-aug-2019.svg?branch=master)](https://travis-ci.org/ihor-nahuliak/task-17-aug-2019)
[![Coverage Status](https://coveralls.io/repos/github/ihor-nahuliak/task-17-aug-2019/badge.svg?branch=master)](https://coveralls.io/github/ihor-nahuliak/task-17-aug-2019?branch=master)

address deduplication task

#### Task:

```python
###### Address deduplication
# Consider an Address model defined as follows:
#
# class UserAddress(models.Model):
#    user = models.ForeignKey(User)
#    name = models.CharField(max_length=255)
#    street_address = models.CharField(max_lenght=255)
#    street_address_line2 = models.CharField(max_lenght=255, blank=True, null=True)
#    zipcode = models.CharField(max_length=12, blank=True, null=True)
#    city = models.CharField(max_length=64)
#    state = models.CharField(max_length=64, blank=True, null=True)
#    country = models.CharField(max_length=2)
#    full_address = models.TextField(blank=True)
#    
#    def save(*args, **kwargs):
#        streetdata = f"{self.street_address}\n{self.street_address_line2}"
#        self.full_address = f"{streetdata}\n{self.zipcode} {self.city} {self.state} {self.country}"
#        super().save(*args, **kwargs)
#
# A UserAddress is saved every time the user changes something in the form, provided the form is valid.
# The task is devising a way of removing partial addresses that are entirely a subset of the current address.
# For example, assuming the following addresses are entered in the form(all belonging to the same user) in sequence:
#
# add1 = UserAddress(name="Max", city="Giventown")
# add2 = UserAddress(name="Max Mustermann", street_address="Randomstreet", city="Giventown")
# add3 = UserAddress(name="Max Mustermann", street_address="456 Randomstreet", city="Giventown")
# add4 = UserAddress(name="Max Mustermann", street_address="789 Otherstreet", city="Giventown", country="NL")
# 
# The expected result would be that only add3 and add4 are left in the DB at the end of the sequence
```

#### Questions:
* Do we need to take the better filled older value as the right filled
  if we try to store the new value that's shortest?
  e.g. what should happen here:
  ```python
  m1 = UserAddress(user_id=1, name='Max Mustermann', city='Giventown')
  m1.save()
  m2 = UserAddress(user_id=1, name='Max', city='Giventown')
  m2.save()
  ```
* Continue the previous question,
  what should we do if the object contains some fields better filled
  and some field worth filled?
  e.g. what should happen here:
  ```python
  m1 = UserAddress(user_id=1, name='Max Mustermann', city='Giventown',
                  street_address='Randomstreet')
  m1.save()
  m2 = UserAddress(user_id=1, name='Max', city='Giventown',
                   street_address='456 Randomstreet')
  m2.save()
  ```
