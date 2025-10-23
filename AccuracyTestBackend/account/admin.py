# in the accounts admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from .forms import BulkCreateForm
import csv
import secrets
import string
import io


class AccountAdmin(admin.ModelAdmin):
    # This tells the admin to use our custom template for the changelist (to add the button)
    change_list_template = "admin/accounts/account/changelist.html"

    def get_urls(self):
        """Adds our custom URL to the admin URLs."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "create-bulk/",
                self.admin_site.admin_view(self.bulk_create_view),
                name="accounts-bulk-create",
            ),
        ]
        return custom_urls + urls

    def bulk_create_view(self, request):
        """The view for our custom admin page."""
        form = BulkCreateForm()

        if request.method == "POST":
            form = BulkCreateForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data["number_of_accounts"]
                organization = form.cleaned_data["organization"]
                acu_perm = form.cleaned_data["acuTest_permition"]
                val_perm = form.cleaned_data["valTest_permition"]

                # Use io.StringIO to create the CSV in memory
                csv_buffer = io.StringIO()
                writer = csv.writer(csv_buffer)
                writer.writerow(["username", "password"])

                created_accounts = []

                for _ in range(number):
                    # Generate a secure random password
                    password = secrets.token_urlsafe(8)

                    # Generate a unique username
                    username = self.generate_unique_username(length=8)

                    try:
                        # Create the User
                        user = User.objects.create_user(
                            username=username, password=password
                        )

                        # Create the Account
                        models.Account.objects.create(
                            user=user,
                            organization=organization,
                            acuTest_permition=acu_perm,
                            valTest_permition=val_perm,
                            is_final=False,
                        )

                        # Add to our list for the CSV
                        writer.writerow([username, password])
                        created_accounts.append(username)

                    except Exception as e:
                        # If something goes wrong, report it
                        messages.error(request, f"Error creating user: {e}")
                        break

                if created_accounts:
                    messages.success(
                        request,
                        f"Successfully created {len(created_accounts)} accounts.",
                    )

                    # Set up the HTTP response to be a CSV download
                    csv_buffer.seek(0)
                    response = HttpResponse(csv_buffer, content_type="text/csv")
                    response["Content-Disposition"] = (
                        'attachment; filename="new_accounts.csv"'
                    )
                    return response

                # Redirect back to the form if no accounts were created
                return redirect(".")

        # This context is needed for the admin template
        context = dict(
            self.admin_site.each_context(request),
            title="Bulk Create Accounts",
            form=form,
        )
        return render(request, "admin/accounts/account/bulk_create.html", context)

    def generate_unique_username(self, length=10):
        """Generates a random, unique username."""
        alphabet = string.ascii_lowercase + string.digits
        while True:
            username = "".join(secrets.choice(alphabet) for _ in range(length))
            if not User.objects.filter(username=username).exists():
                return f"user_{username}"


# Register your models here
admin.site.register(models.Account, AccountAdmin)  # Use our new AccountAdmin
admin.site.register(models.Organization)
