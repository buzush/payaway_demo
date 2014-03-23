from django.shortcuts import render

from django.http import HttpResponse

from django.template import RequestContext		# chapter 4 - templates
from django.shortcuts import render_to_response # chapter 4 - templates

from bills.models import Type, Bill   # chapter 6 - models templates and views

from bills.forms import TypeForm, BillForm    # chapter 7 - fun with forms

from bills.forms import UserForm, UserProfileForm    # chapter 8 - user authentication
from django.contrib.auth import authenticate, login, logout     # chapter 8 - user authentication
from django.http import HttpResponseRedirect, HttpResponse      # chapter 8 - user authentication
from django.contrib.auth.decorators import login_required       # chapter 8 - user authentication

from datetime import datetime   # chapter 10 - cookies and sessions

from bills.bing_search import run_query     # chapter 12 - external search API with BING

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

# chapter 13 - exercises
def get_type_list():
    type_list = Type.objects.order_by('m_name')
    for type in type_list:
        # type.url = type.m_name.replace(' ', '_')
        type.url = encode_url(type.m_name)

    return type_list

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # chapter 10 - cookies and sessions
    # request.session.set_test_cookie()

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    # context_dict = {'boldmessage': "Noy Erlich is the greatest :)"}
    bill_list = Bill.objects.order_by('m_payDate')[:5]

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for bill in bill_list:
        # bill.url = bill.m_name.replace(' ', '_')
        bill.url = encode_url(bill.m_name)

    context_dict = {'bills' : bill_list}

    context_dict['types'] = get_type_list()

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # return render_to_response('bills/index.html', context_dict, context)
    
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    # Render and return the rendered response back to the user.
    return render_to_response('bills/index.html', context_dict, context)

    # chapter 10 - cookies and sessions
    # Obtain our Response object early so we can add cookie information.
    response = render_to_response('bills/index.html', context_dict, context)

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    visits = int(request.COOKIES.get('visits', '0'))

    # Does the cookie last_visit exist?
    if request.COOKIES.has_key('last_visit'):
        # Yes it does! Get the cookie's value.
        last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).days > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            response.set_cookie('visits', visits+1)
            # ...and update the last visit cookie, too.
            response.set_cookie('last_visit', datetime.now())
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        response.set_cookie('last_visit', datetime.now())

    # Return response back to the user, updating any cookies that need changed.
    return response
    #### END NEW CODE ####

def about(request):
    # to send to render_to_response at the return
    context = RequestContext(request)
    visits = request.session.get('visits', 0)
    # visits = request.session.get('visits', 0)
    # use as templates in about.html
    context_dict = {'visits': visits}
    # first parameter is the template we wish to use.
    return render_to_response('bills/about.html', context_dict, context)

# created in chapter 6
@login_required
def type(request, type_name_url):
    # Request our context from the request passed to us
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    # type_name = type_name_url.replace('_', ' ')
    type_name = decode_url(type_name_url)

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'type_name': type_name, 'type_name_url': type_name_url}

    try:
        # Can we find a type with the given name?
        # if we can't, the .get() method raises a DoesNotExit exception
        # So the .get() method returns one model instance or raises an exception
        type = Type.objects.get(m_name=type_name)

        # retrieve all of the associated bills
        # Note that filter returns >= 1 model instance.
        bills = Bill.objects.filter(m_type=type)

        # Adds our results list to the template context under name bills
        context_dict['bills'] = bills

        #we also add the type object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['type'] = type
    except Type.DoesNotExit:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('bills/type.html', context_dict, context)

@login_required
def addType(request):
    # get the context from the request
    context = RequestContext(request)

    # A HTTP POST
    if request.method == 'POST':
        form = TypeForm(request.POST)

        # have we provided with a valid form?
        if form.is_valid():
            # save the new type to the database
            form.save(commit=True)

            # now call the index() views
            # the user will be shpwn the message
            return index(request)
        else:
            # the supplied form containde errors - just print them to the terminal
            print form.errors
    else:
        # if the request was not a POST,  display the form to enter details
        form = TypeForm()

    # bad form (or form details), no form supplied..
    # render the form with error messages (if any).
    return render_to_response('bills/addType.html', {'form': form}, context)

@login_required
def addBill(request, type_name_url):
    context = RequestContext(request)

    # type_name = type_name_url.replace('_', ' ')
    type_name = decode_url(type_name_url)

    if request.method == 'POST':
        form = BillForm(request.POST)

        if form.is_valid():
            # this ti,e we cannot commit straight away
            # not all fields are automatically populated
            bill = form.save(commit=False)

            # retrieve the associated Type object so we can add it
            # wrap the code in a try block - check if the type actually exists
            try:
                typ = Type.objects.get(m_name=type_name)
                bill.m_type = typ
            except Type.DoesNotExist:
                # If we get here, the type does not exist.
                # Go back and render the add type form as a way of saying the category does not exist.
                return render_to_response('bills/addBill.html', {}, context)
            # Also, create a default value for the number of views.
            bill.m_price = 0
            typ.m_numOfBills = typ.m_numOfBills + 1

            bill.save()
            typ.save()

            # now that the bill is saved, display the type
            return type(request, type_name_url)
        else:
            print form.errors
    else:
        form = BillForm()

    return render_to_response('bills/addBill.html',
            {'type_name_url': type_name_url,
            'type_name': type_name, 'form': form},
            context)

# chapter 8 - user authentication
def register(request):
    context = RequestContext(request)
    # chapter 10 - cookies and sessions
    # if request.session.test_cookie_worked():
    #     print ">>>> TEST COOKIE WORKED!"
    #     request.session.delete_test_cookie()

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            # linking the UserProfile with the User instance
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'bills/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

#chapter 8.5 - creating login
def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/bills/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Bills account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('bills/login.html', {}, context)


@login_required
def restricted(request):
    context = RequestContext(request)
    return render_to_response('bills/restricted.html', {}, context)
    # return HttpResponse("Since you're logged in, you can see this text!")


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/bills/')


# chapter 12 - external search API with BING
def search(request):
    context = RequestContext(request)
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render_to_response('bills/search.html', {'result_list': result_list}, context)
