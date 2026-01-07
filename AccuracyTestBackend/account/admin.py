from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Account, Organization


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
        ("acuTest_permission", "valutest_permission"),
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
        "user",
        "age",
        "sex",
        "organization",
        "degree",
        "quiz_permissions",
        "is_final",
    )
    list_display_links = ("id", "full_name")
    list_filter = (
        "sex",
        "degree",
        "organization",
        "acuTest_permission",
        "valuTest_permission",
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
                    ("acuTest_permission", "valuTest_permission"),
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
        return " | ".join(perms) if perms else "❌ None"

    quiz_permissions.short_description = "Quiz Permissions"

    actions = [
        "grant_acuTest_permission",
        "grant_valuTest_permission",
        "revoke_all_permissions",
    ]

    @admin.action(description="Grant AcuTest permission")
    def grant_acuTest_permission(self, request, queryset):
        updated = queryset.update(acuTest_permission=True)
        self.message_user(request, f"{updated} account(s) granted AcuTest permission.")

    @admin.action(description="Grant ValuTest permission")
    def grant_valuTest_permission(self, request, queryset):
        updated = queryset.update(valuTest_permission=True)
        self.message_user(request, f"{updated} account(s) granted ValuTest permission.")

    @admin.action(description="Revoke all quiz permissions")
    def revoke_all_permissions(self, request, queryset):
        updated = queryset.update(acuTest_permission=False, valutest_permission=False)
        self.message_user(request, f"{updated} account(s) had permissions revoked.")
