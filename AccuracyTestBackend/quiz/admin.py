import math
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Quiztime,
    AcuTest_pic,
    AcuTest_text,
    ValuTest,
    BelbinTest,
    HexacoTest,
)


class BaseQuizAdmin(admin.ModelAdmin):
    """Base admin class for all quiz types"""

    list_select_related = (
        "account",
        "account__user",
        "account__organization",
        "quiz_time",
    )
    list_per_page = 25
    ordering = ("-id",)

    def account_name(self, obj):
        return f"{obj.account.first_name} {obj.account.last_name}"

    account_name.short_description = "Account"
    account_name.admin_order_field = "account__first_name"

    def organization(self, obj):
        if obj.account.organization:
            return obj.account.organization.name
        return "-"

    organization.short_description = "Organization"
    organization.admin_order_field = "account__organization__name"

    def start_time(self, obj):
        if obj.quiz_time and obj.quiz_time.start_time:
            return obj.quiz_time.start_time.strftime("%Y-%m-%d %H:%M")
        return "-"

    start_time.short_description = "Start Time"
    start_time.admin_order_field = "quiz_time__start_time"

    def duration(self, obj):
        if obj.quiz_time and obj.quiz_time.start_time and obj.quiz_time.finish_time:
            delta = obj.quiz_time.finish_time - obj.quiz_time.start_time
            total_seconds = int(delta.total_seconds())
            minutes, seconds = divmod(total_seconds, 60)
            return f"{minutes}m {seconds}s"
        return "-"

    duration.short_description = "Duration"

    def answers_count(self, obj):
        if obj.answers:
            return len(obj.answers)
        return 0

    answers_count.short_description = "# Answers"


@admin.register(AcuTest_pic)
class AcuTestPicAdmin(BaseQuizAdmin):
    list_display = (
        "id",
        "account_name",
        "organization",
        "start_time",
        "duration",
        "correct",
        "wrong",
        "score_display",
        "answers_count",
    )
    list_filter = (
        "account__organization",
        ("quiz_time__start_time", admin.DateFieldListFilter),
    )
    search_fields = (
        "account__first_name",
        "account__last_name",
        "account__user__username",
        "account__organization__name",
    )

    readonly_fields = (
        "score_display",
        "answers_display",
        "duration",
        "created_at",
    )

    fieldsets = (
        ("Account Information", {"fields": ("account",)}),
        ("Quiz Time", {"fields": ("quiz_time", "duration", "created_at")}),
        (
            "Results",
            {
                "fields": (
                    ("correct", "wrong"),
                    "score_display",
                )
            },
        ),
        (
            "Answers",
            {
                "fields": ("answers", "answers_display"),
                "classes": ("collapse",),
            },
        ),
    )

    def score_display(self, obj):
        total = obj.correct + obj.wrong
        if total > 0:
            percentage = (obj.correct / total) * 100
            color = (
                "green" if percentage >= 70 else "orange" if percentage >= 50 else "red"
            )
            # FIX: Pre-format the percentage before passing to format_html
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}%</span> ({}/{})',
                color,
                f"{percentage:.1f}",
                obj.correct,
                total,
            )
        return "-"

    score_display.short_description = "Score"

    def answers_display(self, obj):
        if obj.answers:
            return ", ".join(map(str, obj.answers))
        return "-"

    answers_display.short_description = "Answers (Readable)"


@admin.register(AcuTest_text)
class AcuTestTextAdmin(BaseQuizAdmin):
    list_display = (
        "id",
        "account_name",
        "organization",
        "start_time",
        "duration",
        "correct",
        "wrong",
        "score_display",
        "yes_no_summary",
    )
    list_filter = (
        "account__organization",
        ("quiz_time__start_time", admin.DateFieldListFilter),
    )
    search_fields = (
        "account__first_name",
        "account__last_name",
        "account__user__username",
        "account__organization__name",
    )

    readonly_fields = (
        "score_display",
        "answers_display",
        "duration",
        "yes_no_breakdown",
        "created_at",
    )

    fieldsets = (
        ("Account Information", {"fields": ("account",)}),
        ("Quiz Time", {"fields": ("quiz_time", "duration", "created_at")}),
        (
            "Basic Results",
            {
                "fields": (
                    ("correct", "wrong"),
                    "score_display",
                )
            },
        ),
        (
            "Yes/No Analysis",
            {
                "fields": (
                    ("num_of_yes", "num_of_no"),
                    ("yes_yes", "yes_no"),
                    ("no_no", "no_yes"),
                    "yes_no_breakdown",
                )
            },
        ),
        (
            "Answers",
            {
                "fields": ("answers", "answers_display"),
                "classes": ("collapse",),
            },
        ),
    )

    def score_display(self, obj):
        total = obj.correct + obj.wrong
        if total > 0:
            percentage = (obj.correct / total) * 100
            color = (
                "green" if percentage >= 70 else "orange" if percentage >= 50 else "red"
            )
            # FIX: Pre-format the percentage before passing to format_html
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}%</span> ({}/{})',
                color,
                f"{percentage:.1f}",
                obj.correct,
                total,
            )
        return "-"

    score_display.short_description = "Score"

    def yes_no_summary(self, obj):
        return format_html(
            "Yes: <b>{}</b> | No: <b>{}</b>", obj.num_of_yes, obj.num_of_no
        )

    yes_no_summary.short_description = "Yes/No"

    def yes_no_breakdown(self, obj):
        return format_html(
            """
            <table style="border-collapse: collapse;">
                <tr>
                    <td></td>
                    <th style="padding: 5px; border: 1px solid #ddd;">Expected Yes</th>
                    <th style="padding: 5px; border: 1px solid #ddd;">Expected No</th>
                </tr>
                <tr>
                    <th style="padding: 5px; border: 1px solid #ddd;">Answered Yes</th>
                    <td style="padding: 5px; border: 1px solid #ddd; background: #d4edda;">{}</td>
                    <td style="padding: 5px; border: 1px solid #ddd; background: #f8d7da;">{}</td>
                </tr>
                <tr>
                    <th style="padding: 5px; border: 1px solid #ddd;">Answered No</th>
                    <td style="padding: 5px; border: 1px solid #ddd; background: #f8d7da;">{}</td>
                    <td style="padding: 5px; border: 1px solid #ddd; background: #d4edda;">{}</td>
                </tr>
            </table>
            """,
            obj.yes_yes,
            obj.yes_no,
            obj.no_yes,
            obj.no_no,
        )

    yes_no_breakdown.short_description = "Confusion Matrix"

    def answers_display(self, obj):
        if obj.answers:
            return ", ".join(map(str, obj.answers))
        return "-"

    answers_display.short_description = "Answers (Readable)"


@admin.register(ValuTest)
class ValuTestAdmin(BaseQuizAdmin):
    list_display = (
        "id",
        "account_name",
        "organization",
        "start_time",
        "duration",
        "values_summary",
        "top_value",
    )
    list_filter = (
        "account__organization",
        ("quiz_time__start_time", admin.DateFieldListFilter),
    )
    search_fields = (
        "account__first_name",
        "account__last_name",
        "account__user__username",
        "account__organization__name",
    )

    readonly_fields = (
        "answers_display",
        "duration",
        "values_chart",
        "top_value",
        "created_at",
    )

    fieldsets = (
        ("Account Information", {"fields": ("account",)}),
        ("Quiz Time", {"fields": ("quiz_time", "duration", "created_at")}),
        (
            "Values Results",
            {
                "fields": (
                    ("sharayet_kari", "hemayat"),
                    ("ravabet", "pishraft"),
                    ("esteghlal", "tofigh"),
                    "values_chart",
                    "top_value",
                )
            },
        ),
        (
            "Answers",
            {
                "fields": ("answers", "answers_display"),
                "classes": ("collapse",),
            },
        ),
    )

    def values_summary(self, obj):
        return format_html(
            "شرایط:{} | حمایت:{} | روابط:{} | پیشرفت:{} | استقلال:{} | توفیق:{}",
            obj.sharayet_kari,
            obj.hemayat,
            obj.ravabet,
            obj.pishraft,
            obj.esteghlal,
            obj.tofigh,
        )

    values_summary.short_description = "Values"

    def top_value(self, obj):
        values = {
            "شرایط کاری": obj.sharayet_kari,
            "حمایت": obj.hemayat,
            "روابط": obj.ravabet,
            "پیشرفت": obj.pishraft,
            "استقلال": obj.esteghlal,
            "توفیق": obj.tofigh,
        }
        if any(values.values()):
            top = max(values, key=values.get)
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span> ({})',
                top,
                values[top],
            )
        return "-"

    top_value.short_description = "Top Value"

    def values_chart(self, obj):
        """Visual bar chart for values"""
        values = [
            ("شرایط کاری", obj.sharayet_kari, "#FF6B6B"),
            ("حمایت", obj.hemayat, "#4ECDC4"),
            ("روابط", obj.ravabet, "#45B7D1"),
            ("پیشرفت", obj.pishraft, "#96CEB4"),
            ("استقلال", obj.esteghlal, "#FFEAA7"),
            ("توفیق", obj.tofigh, "#DDA0DD"),
        ]
        max_val = max(v[1] for v in values) if any(v[1] for v in values) else 1

        rows = []
        for name, value, color in values:
            width = int((value / max_val * 200)) if max_val > 0 else 0
            rows.append(
                f'<div style="margin: 5px 0;">'
                f'<span style="display: inline-block; width: 80px; text-align: right; margin-right: 10px;">{name}:</span>'
                f'<span style="display: inline-block; width: {width}px; height: 20px; background: {color}; border-radius: 3px;"></span>'
                f'<span style="margin-left: 5px;">{value}</span>'
                f"</div>"
            )

        html = '<div style="font-family: sans-serif;">' + "".join(rows) + "</div>"
        return format_html(html)

    values_chart.short_description = "Values Chart"

    def answers_display(self, obj):
        if obj.answers:
            return ", ".join(map(str, obj.answers))
        return "-"

    answers_display.short_description = "Answers (Readable)"


@admin.register(Quiztime)
class QuiztimeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_time",
        "finish_time",
        "duration_display",
        "linked_quiz",
    )
    list_filter = (("start_time", admin.DateFieldListFilter),)
    search_fields = ("id",)
    ordering = ("-start_time",)
    date_hierarchy = "start_time"

    readonly_fields = ("duration_display", "linked_quiz")

    fieldsets = (
        (
            "Time Information",
            {
                "fields": (
                    ("start_time", "finish_time"),
                    "duration_display",
                )
            },
        ),
        (
            "Linked Quiz",
            {
                "fields": ("linked_quiz",),
                "classes": ("collapse",),
            },
        ),
    )

    def duration_display(self, obj):
        if obj.start_time and obj.finish_time:
            duration = obj.finish_time - obj.start_time
            total_seconds = int(duration.total_seconds())
            minutes, seconds = divmod(total_seconds, 60)
            hours, minutes = divmod(minutes, 60)

            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        return "-"

    duration_display.short_description = "Duration"

    def linked_quiz(self, obj):
        """Show which quiz this time belongs to"""
        if hasattr(obj, "acutest_pic") and obj.acutest_pic:
            return format_html(
                '<a href="/admin/quiz/acutest_pic/{}/change/">AcuTest_pic #{}</a>',
                obj.acutest_pic.id,
                obj.acutest_pic.id,
            )
        elif hasattr(obj, "acutest_text") and obj.acutest_text:
            return format_html(
                '<a href="/admin/quiz/acutest_text/{}/change/">AcuTest_text #{}</a>',
                obj.acutest_text.id,
                obj.acutest_text.id,
            )
        elif hasattr(obj, "valutest") and obj.valutest:
            return format_html(
                '<a href="/admin/quiz/valutest/{}/change/">ValuTest #{}</a>',
                obj.valutest.id,
                obj.valutest.id,
            )
        return "-"

    linked_quiz.short_description = "Linked Quiz"


@admin.register(BelbinTest)
class BelbinTestAdmin(admin.ModelAdmin):
    # 1. شبیه‌سازی List Display مشابه با ValuTestAdmin
    list_display = (
        "id",
        "account",
        # "organization", # در صورت وجود در مدل، از کامنت خارج کنید
        # "start_time",   # در صورت وجود در مدل، از کامنت خارج کنید
        # "duration",     # در صورت وجود در مدل، از کامنت خارج کنید
        "roles_summary",
        "top_role",
        "created_at",
    )

    readonly_fields = ("sh", "co", "pl", "ri", "me", "imp", "tw", "cf", "belbin_chart")

    # 2. اضافه کردن خلاصه نمرات برای نمایش در لیست
    @admin.display(description="خلاصه نمرات")
    def roles_summary(self, obj):
        return format_html(
            '<span style="font-size:11px; white-space:nowrap; direction:ltr; display:inline-block;">'
            "<b>SH:</b>{} | <b>CO:</b>{} | <b>PL:</b>{} | <b>RI:</b>{} | "
            "<b>ME:</b>{} | <b>IMP:</b>{} | <b>TW:</b>{} | <b>CF:</b>{}"
            "</span>",
            obj.sh or 0,
            obj.co or 0,
            obj.pl or 0,
            obj.ri or 0,
            obj.me or 0,
            obj.imp or 0,
            obj.tw or 0,
            obj.cf or 0,
        )

    # 3. محاسبه و نمایش نقش برتر برای لیست
    @admin.display(description="نقش برتر")
    def top_role(self, obj):
        data = [
            ("SH (شکل دهنده)", obj.sh or 0),
            ("CO (هماهنگ کننده)", obj.co or 0),
            ("PL (ایده پرداز)", obj.pl or 0),
            ("RI (منبع یاب)", obj.ri or 0),
            ("ME (ارزیاب ها)", obj.me or 0),
            ("IMP (اجرا کننده)", obj.imp or 0),
            ("TW (عضو گروه کاری)", obj.tw or 0),
            ("CF (تمام کننده)", obj.cf or 0),
        ]
        top = max(data, key=lambda x: x[1])
        if top[1] == 0:
            return "-"
        return f"{top[0]} ({top[1]})"

    # 4. نمودارها به همراه برچسب‌های متنی داخل دایره
    @admin.display(description="گزارش گرافیکی بلبین")
    def belbin_chart(self, obj):
        data = [
            ("شکل دهنده (SH)", "SH", obj.sh or 0, "#4a72a5"),
            ("هماهنگ کننده (CO)", "CO", obj.co or 0, "#a54a4a"),
            ("ایده پرداز (PL)", "PL", obj.pl or 0, "#86a54a"),
            ("منبع یاب (RI)", "RI", obj.ri or 0, "#604a7a"),
            ("ارزیاب ها (ME)", "ME", obj.me or 0, "#4a95a5"),
            ("اجرا کننده (IMP)", "IMP", obj.imp or 0, "#d48a42"),
            ("عضو گروه کاری (TW)", "TW", obj.tw or 0, "#8fa0c9"),
            ("تمام کننده (CF)", "CF", obj.cf or 0, "#c99696"),
        ]

        total = sum(item[2] for item in data)
        max_val = max([item[2] for item in data] + [1])

        html = '<div dir="rtl" style="display: flex; flex-direction: column; gap: 30px; color: var(--body-fg); padding: 10px 0;">'

        # --- نمودار میله‌ای ---
        html += """
        <div style="background: var(--body-bg); border: 1px solid var(--hairline-color); border-radius: 8px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h3 style="margin-top: 0; border-bottom: 1px solid var(--hairline-color); padding-bottom: 10px; color: var(--body-fg);">مقایسه نمرات نقش‌ها (نمودار میله‌ای)</h3>
        """
        for label, short_lbl, value, color in data:
            bar_width = (value / max_val) * 100
            html += f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-weight: bold; font-size: 13px;">
                    <span>{label}</span>
                    <span>{value}</span>
                </div>
                <div style="background-color: var(--darkened-bg, rgba(128,128,128,0.2)); border-radius: 4px; height: 14px; width: 100%; overflow: hidden;">
                    <div style="background-color: {color}; width: {bar_width}%; height: 100%; border-radius: 4px;"></div>
                </div>
            </div>
            """
        html += "</div>"

        # --- نمودار دایره‌ای ---
        html += """
        <div style="background: var(--body-bg); border: 1px solid var(--hairline-color); border-radius: 8px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h3 style="margin-top: 0; border-bottom: 1px solid var(--hairline-color); padding-bottom: 10px; color: var(--body-fg);">سهم هر نقش (نمودار دایره‌ای)</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 40px; justify-content: center; align-items: center; margin-top: 20px;">
        """

        if total > 0:
            gradient_stops = []
            labels_html = ""
            current_percent = 0
            legend_html = (
                '<div style="display: flex; flex-direction: column; gap: 12px;">'
            )

            for label, short_lbl, value, color in data:
                percent = value / total * 100
                if percent > 0:
                    next_percent = current_percent + percent
                    gradient_stops.append(f"{color} {current_percent}% {next_percent}%")

                    # محاسبه موقعیت متن روی نمودار با استفاده از مثلثات (اگر سهم بیش از ۴٪ باشد تا متن‌ها روی هم نیفتند)
                    if percent > 4:
                        mid_percent = current_percent + (percent / 2)
                        # تبدیل درصد به رادیان
                        angle = math.radians(mid_percent * 3.6)
                        r = 35  # شعاع متون (نسبت به مرکز)
                        # محاسبه مختصات x و y
                        x = 50 + r * math.sin(angle)
                        y = 50 - r * math.cos(angle)

                        labels_html += f"""
                        <div style="
                            position: absolute; left: {x}%; top: {y}%; 
                            transform: translate(-50%, -50%); 
                            color: white; font-weight: bold; font-size: 11px; 
                            text-align: center; line-height: 1.2;
                            text-shadow: 1px 1px 2px rgba(0,0,0,0.8); 
                            pointer-events: none;
                        ">{short_lbl}<br dir="ltr">{percent:.1f}%</div>
                        """
                    current_percent = next_percent

                # راهنمای نمودار
                legend_html += f"""
                <div style="display: flex; align-items: center; gap: 10px; font-size: 13px;">
                    <div style="width: 16px; height: 16px; background-color: {color}; border-radius: 3px;"></div>
                    <span>{label}: <strong dir="ltr">{percent:.1f} %</strong></span>
                </div>
                """
            legend_html += "</div>"

            gradient_str = ", ".join(gradient_stops)

            # کانتینر نسبی برای نمودار که متون روی آن قرار می‌گیرند
            html += f"""
            <div style="position: relative; width: 240px; height: 240px;">
                <div style="
                    width: 100%; height: 100%; 
                    border-radius: 50%; 
                    background: conic-gradient({gradient_str});
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                "></div>
                {labels_html}
            </div>
            """
            html += legend_html
        else:
            html += "<p>داده‌ای برای نمایش وجود ندارد.</p>"

        html += "</div></div>"

        return format_html(html)


@admin.register(HexacoTest)
class HexacoTestAdmin(BaseQuizAdmin):
    list_display = ("id", "account", "created_at")
    search_fields = ("account__username", "account__email")


# Customize admin site header
admin.site.site_header = "Quiz Management Admin"
admin.site.site_title = "Quiz Admin"
admin.site.index_title = "Welcome to Quiz Management"
