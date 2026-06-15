from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.contrib.admin.utils import get_deleted_objects
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model

from .models import Account, Organization

User = get_user_model()


class AccountInline(admin.StackedInline):
    """Inline Account in User admin"""

    model = Account
    can_delete = False
    verbose_name_plural = "Account"
    fk_name = "user"
    fields = (
        ("first_name", "last_name"),
        ("age", "sex"),
        ("email", "phone"),
        ("university", "major", "degree"),
        "organization",
        (
            "acuTest_permission",
            "valutest_permission",
            "belbinTest_permission",
            "hexacoTest_permission",
            "thinkTest_permission",
        ),
        "is_final",
    )


class CustomUserAdmin(BaseUserAdmin):
    """Extended User admin with Account inline"""

    inlines = (AccountInline,)
    list_display = (
        "username",
        "email",
        "get_full_name",
        "get_organization",
        "is_active",
    )
    list_select_related = ("account",)

    def get_full_name(self, obj):
        if hasattr(obj, "account"):
            return f"{obj.account.first_name} {obj.account.last_name}"
        return "-"

    get_full_name.short_description = "Full Name"

    def get_organization(self, obj):
        if hasattr(obj, "account") and obj.account.organization:
            return obj.account.organization.name
        return "-"

    get_organization.short_description = "Organization"


# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "account_count")
    search_fields = ("name",)
    ordering = ("name",)

    def account_count(self, obj):
        count = obj.accounts.count()
        return format_html(
            '<span style="color: {};">{}</span>',
            "green" if count > 0 else "gray",
            count,
        )

    account_count.short_description = "Accounts"


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "sex",
        "organization",
        "degree",
        "quiz_permissions",
        "is_final",
        "email",
        "user",
        "age",
    )
    list_display_links = ("id", "full_name")
    list_filter = (
        "sex",
        "degree",
        "organization",
        "acuTest_permission",
        "valuTest_permission",
        "belbinTest_permission",
        "hexacoTest_permission",
        "thinkTest_permission",
        "is_final",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "user__username",
        "university",
        "major",
    )
    list_select_related = ("user", "organization")
    ordering = ("-id",)
    list_per_page = 25

    fieldsets = (
        ("User Link", {"fields": ("user",)}),
        (
            "Personal Information",
            {
                "fields": (
                    ("first_name", "last_name"),
                    ("age", "sex"),
                    ("email", "phone"),
                )
            },
        ),
        (
            "Education",
            {
                "fields": (
                    "university",
                    ("major", "degree"),
                )
            },
        ),
        ("Organization", {"fields": ("organization",)}),
        (
            "Permissions & Status",
            {
                "fields": (
                    (
                        "acuTest_permission",
                        "valuTest_permission",
                        "belbinTest_permission",
                        "hexacoTest_permission",
                        "thinkTest_permission",
                    ),
                    "is_final",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("user",)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" or "-"

    full_name.short_description = "Name"

    def quiz_permissions(self, obj):
        perms = []
        if obj.acuTest_permission:
            perms.append("🖼️ Acu")
        if obj.valuTest_permission:
            perms.append("📝 Val")
        if obj.belbinTest_permission:
            perms.append("🎱 bel")
        if obj.hexacoTest_permission:
            perms.append("🔮 hex")
        if obj.thinkTest_permission:
            perms.append("think")
        return " | ".join(perms) if perms else "❌ None"

    quiz_permissions.short_description = "Quiz Permissions"

    actions = [
        "grant_acuTest_permission",
        "grant_valuTest_permission",
        "grant_belbinTest_permission",
        "grant_hexacoTest_permission",
        "revoke_all_permissions",
        "delete_associated_users",
        "reset_account_password",
    ]

    @admin.action(description="Grant AcuTest permission")
    def grant_acuTest_permission(self, request, queryset):
        updated = queryset.update(acuTest_permission=True)
        self.message_user(request, f"{updated} account(s) granted AcuTest permission.")

    @admin.action(description="Grant WIL permission")
    def grant_valuTest_permission(self, request, queryset):
        updated = queryset.update(valuTest_permission=True)
        self.message_user(request, f"{updated} account(s) granted WIL permission.")

    @admin.action(description="Grant BelbinTest permission")
    def grant_belbinTest_permission(self, request, queryset):
        updated = queryset.update(belbinTest_permission=True)
        self.message_user(
            request, f"{updated} account(s) granted BelbinTest permission."
        )

    @admin.action(description="Grant HexacoTest permission")
    def grant_hexacoTest_permission(self, request, queryset):
        updated = queryset.update(hexacoTest_permission=True)
        self.message_user(
            request, f"{updated} account(s) granted HexacoTest permission."
        )

    @admin.action(description="Revoke all quiz permissions")
    def revoke_all_permissions(self, request, queryset):
        updated = queryset.update(
            acuTest_permission=False,
            valuTest_permission=False,
            belbinTest_permission=False,
            hexacoTest_permission=False,
        )
        self.message_user(request, f"{updated} account(s) had permissions revoked.")

    @admin.action(description="Delete associated User")
    def delete_associated_users(self, request, queryset):
        # Get the users that are going to be deleted
        user_ids = queryset.values_list("user_id", flat=True)
        users_to_delete = User.objects.filter(id__in=user_ids)

        # 1. If confirmed, perform the deletion
        if request.POST.get("post"):
            deleted_count, _ = users_to_delete.delete()
            self.message_user(
                request,
                f"Successfully deleted {deleted_count} user(s) and their associated accounts.",
                level=messages.SUCCESS,
            )
            return None

        # 2. If NOT confirmed, gather all objects that will be cascade-deleted
        # get_deleted_objects traces all related CASCADE relationships
        deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
            users_to_delete, request, self.admin_site
        )

        # 3. Render the confirmation page with the cascade data
        context = {
            **self.admin_site.each_context(request),
            "title": "Are you sure you want to delete these users and all related data?",
            "deletable_objects": deletable_objects,
            "model_count": dict(model_count).items(),
            "queryset": queryset,
            "opts": self.model._meta,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            "action_name": "delete_associated_users",
        }

        return TemplateResponse(
            request, "admin/custom_delete_confirmation.html", context
        )

    @admin.action(description="Reset password to an easy 6-digit code")
    def reset_account_password(self, request, queryset):
        for account in queryset:
            user = account.user
            new_password = str(random.randint(100000, 999999))

            user.set_password(new_password)
            user.save()

            self.message_user(
                request,
                f"Password for {user.username} ({account.first_name} {account.last_name}) reset to: {new_password}",
                level=messages.SUCCESS,
            )
