import os

def Populate():
	gas = AddType('Gas')

	g = AddBill(gas, 'gas example')

	electricity = AddType('Elctricity')

	e = AddBill(electricity, 'electricity example')
	e1 = AddBill(electricity, 'electricity example1')
	e2 = AddBill(electricity, 'electricity example2')
	e3 = AddBill(electricity, 'electricity example3')
	e4 = AddBill(electricity, 'electricity example4')
	e5 = AddBill(electricity, 'electricity example5')

	rent = AddType('Rent')

	r = AddBill(rent, 'rent example')

	# Print out what we have added to the user.
	for t in Type.objects.all():
		for b in Bill.objects.all():
			if b.m_type==t:
				print "- {0} - {1}".format(str(t), str(b))

def AddBill(_type, _name):
    newBill = Bill.objects.get_or_create(m_type=_type, m_name=_name)[0]
    return newBill

def AddType(_name):
    newType = Type.objects.get_or_create(m_name=_name)[0]
    return newType

# Start execution here!
if __name__ == '__main__':
    print "Starting bills population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payaway.settings')
    from bills.models import Bill, Type
    Populate()