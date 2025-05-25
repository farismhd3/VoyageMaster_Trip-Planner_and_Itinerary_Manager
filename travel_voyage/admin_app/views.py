from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_app.models import Register



@login_required
def admin_dashboard(request):
    # Ensure only admins can access this page
    if request.session.get('ut') != 1:  # usertype = 1 indicates admin
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')

    # Fetch all regular users (usertype=0) for viewing
    users = Register.objects.filter(usertype=0)

    # Fetch pending, approved, and rejected travel agencies (usertype=2)
    pending_agencies = Register.objects.filter(usertype=2, is_approved=False, status='pending')
    approved_agencies = Register.objects.filter(usertype=2, is_approved=True, status='approved')
    rejected_agencies = Register.objects.filter(usertype=2, status='rejected')

    if request.method == 'POST':
        action = request.POST.get('action')
        agency_id = request.POST.get('agency_id')

        try:
            agency = Register.objects.get(id=agency_id, usertype=2)  # Ensure it's a travel agency

            if action == 'approve':
                agency.is_approved = True
                agency.is_active = True
                agency.status = 'approved'
                agency.save()
                messages.success(request, f"Travel agency '{agency.username}' has been approved.")
            elif action == 'reject':
                agency.is_approved = False
                agency.status = 'rejected'
                agency.save()
                messages.success(request, f"Travel agency '{agency.username}' has been rejected.")
            else:
                messages.error(request, "Invalid action selected.")
        except Register.DoesNotExist:
            messages.error(request, "Travel agency not found.")

        return redirect('admin_dashboard')

    context = {
        'users': users,
        'pending_agencies': pending_agencies,
        'approved_agencies': approved_agencies,
        'rejected_agencies': rejected_agencies,
    }
    return render(request, 'admin_dashboard.html', context)