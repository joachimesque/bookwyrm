""" moderation via flagged posts and users """
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from bookwyrm import forms, models


# pylint: disable=no-self-use
@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("bookwyrm.moderate_user", raise_exception=True),
    name="dispatch",
)
@method_decorator(
    permission_required("bookwyrm.moderate_post", raise_exception=True),
    name="dispatch",
)
class Reports(View):
    """ list of reports  """

    def get(self, request):
        """ view current reports """
        filters = {}

        resolved = request.GET.get("resolved") == "true"
        server = request.GET.get("server")
        if server:
            server = get_object_or_404(models.FederatedServer, id=server)
            filters["user__federated_server"] = server
        filters["resolved"] = resolved
        data = {
            "resolved": resolved,
            "server": server,
            "reports": models.Report.objects.filter(**filters),
        }
        return TemplateResponse(request, "moderation/reports.html", data)


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("bookwyrm.moderate_user", raise_exception=True),
    name="dispatch",
)
@method_decorator(
    permission_required("bookwyrm.moderate_post", raise_exception=True),
    name="dispatch",
)
class Report(View):
    """ view a specific report """

    def get(self, request, report_id):
        """ load a report """
        data = {
            "report": get_object_or_404(models.Report, id=report_id),
        }
        return TemplateResponse(request, "moderation/report.html", data)

    def post(self, request, report_id):
        """ comment on a report """
        report = get_object_or_404(models.Report, id=report_id)
        models.ReportComment.objects.create(
            user=request.user,
            report=report,
            note=request.POST.get("note"),
        )
        return redirect("settings-report", report.id)


@login_required
@permission_required("bookwyrm_moderate_user")
def deactivate_user(_, report_id):
    """ mark an account as inactive """
    report = get_object_or_404(models.Report, id=report_id)
    report.user.is_active = not report.user.is_active
    report.user.save()
    return redirect("settings-report", report.id)


@login_required
@permission_required("bookwyrm_moderate_post")
def resolve_report(_, report_id):
    """ mark a report as (un)resolved """
    report = get_object_or_404(models.Report, id=report_id)
    report.resolved = not report.resolved
    report.save()
    if not report.resolved:
        return redirect("settings-report", report.id)
    return redirect("settings-reports")


@login_required
@require_POST
def make_report(request):
    """ a user reports something """
    form = forms.ReportForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return redirect(request.headers.get("Referer", "/"))

    form.save()
    return redirect(request.headers.get("Referer", "/"))
