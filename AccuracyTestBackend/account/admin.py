from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from .forms import BulkCreateForm  # Assuming this form exists in forms.py
import csv
import secrets
import string
import io

from quiz.models import AcuTest_pic, AcuTest_text, Quiztime, ValuTest


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
        """The view for our custom admin page, now using bulk_create."""
        form = BulkCreateForm()

        if request.method == "POST":
            form = BulkCreateForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data["number_of_accounts"]
                organization = form.cleaned_data["organization"]
                acu_perm = form.cleaned_data["acuTest_permition"]
                val_perm = form.cleaned_data["valTest_permition"]

                users_to_create = []
                accounts_to_create = []
                csv_rows = [["username", "password"]]

                # 1. Get all existing usernames ONCE to check for conflicts in memory.
                # This is much faster than querying the DB for every new user.
                existing_usernames = set(
                    User.objects.values_list("username", flat=True)
                )

                for _ in range(number):
                    # 2. Generate credentials
                    password = secrets.token_urlsafe(12)
                    username = self.generate_unique_username(
                        existing_usernames, length=12
                    )

                    # Add to our set so the *next* username we generate
                    # doesn't conflict with one in this same batch.
                    existing_usernames.add(username)

                    # 3. Prepare the User object (without saving)
                    user = User(username=username)
                    user.set_password(password)  # Hash the password
                    users_to_create.append(user)

                    # Add to our list for the CSV
                    csv_rows.append([username, password])

                try:
                    # 4. Create all Users in ONE database query
                    # Note: bulk_create returns the list of created objects,
                    # (on most dbs, like Postgres) complete with their new IDs.
                    created_users = User.objects.bulk_create(users_to_create)

                    # 5. Prepare the Account objects
                    for user in created_users:
                        accounts_to_create.append(
                            models.Account(
                                user=user,
                                organization=organization,
                                acuTest_permition=acu_perm,
                                valTest_permition=val_perm,
                                is_final=False,
                            )
                        )

                    # 6. Create all Accounts in a SECOND database query
                    models.Account.objects.bulk_create(accounts_to_create)

                    qt_for_valu = Quiztime.objects.bulk_create(
                        [Quiztime() for _ in range(number)]
                    )
                    qt_for_pic = Quiztime.objects.bulk_create(
                        [Quiztime() for _ in range(number)]
                    )
                    qt_for_text = Quiztime.objects.bulk_create(
                        [Quiztime() for _ in range(number)]
                    )

                    # 4. Prepare the tests by associating users with their quiztimes
                    valu_tests = []
                    pic_tests = []
                    text_tests = []

                    for i, user in enumerate(created_users):
                        valu_tests.append(
                            ValuTest(
                                user=user, quiz_time=qt_for_valu[i], answers=[0] * 30
                            )
                        )
                        pic_tests.append(
                            AcuTest_pic(
                                user=user, quiz_time=qt_for_pic[i], answers=[0] * 42
                            )
                        )
                        text_tests.append(
                            AcuTest_text(
                                user=user, quiz_time=qt_for_text[i], answers=[0] * 90
                            )
                        )

                    # 5. Bulk create all the tests
                    ValuTest.objects.bulk_create(valu_tests)
                    AcuTest_pic.objects.bulk_create(pic_tests)
                    AcuTest_text.objects.bulk_create(text_tests)

                except Exception as e:
                    messages.error(request, f"Error during bulk creation: {e}")
                    return redirect(".")

                # 7. Create and return the CSV
                csv_buffer = io.StringIO()
                writer = csv.writer(csv_buffer)
                writer.writerows(csv_rows)

                messages.success(
                    request,
                    f"Successfully created {len(created_users)} accounts.",
                )

                csv_buffer.seek(0)
                response = HttpResponse(csv_buffer, content_type="text/csv")
                response["Content-Disposition"] = (
                    'attachment; filename="new_accounts.csv"'
                )
                return response

        # This context is needed for the admin template
        context = dict(
            self.admin_site.each_context(request),
            title="Bulk Create Accounts",
            form=form,
        )
        return render(request, "admin/accounts/account/bulk_create.html", context)

    def generate_unique_username(self, existing_usernames, length=10):
        """
        Generates a random, unique username by checking against an
        in-memory set of existing usernames.
        """
        alphabet = string.ascii_lowercase + string.digits
        while True:
            # We fix the bug here: check for "user_..." not just the random part
            username = "user_" + "".join(
                secrets.choice(alphabet) for _ in range(length)
            )
            if username not in existing_usernames:
                return username


# Register your models here
admin.site.register(models.Account, AccountAdmin)  # Use our new AccountAdmin
admin.site.register(models.Organization)
