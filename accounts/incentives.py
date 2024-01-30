from rest_framework.decorators import api_view
from django.db.models import Count,Q
from accounts.models import (
    Case,
    Factory,
    AwarenessProgram
)
from accounts.constants import CaseStatus
from rest_framework.response import Response
from accounts.utils import current_time


@api_view(["GET"])
def winner(request):
    company = request.query_params.get("Company")
    current_month = current_time().month
    current_year = current_time().year
    if current_month != 1:
        previous_month = current_month - 1
        year = current_year
    else:
        previous_month = 12
        year = current_year - 1

    factory = Factory.objects.filter(Company=company)

    awareness_programs = AwarenessProgram.objects.filter(
        Factory__in=factory, 
        Date__month=previous_month, 
        Date__year=year
    ).annotate(
        breached_count=Count('pk', filter=Q(Breached=False))
    )

    min_programs_map = {ap.Factory_id: ap.programStatus["Required"] for ap in awareness_programs if ap.programStatus}

    cases = Case.objects.filter(
        Date__month=previous_month, 
        Date__year=year, 
        Factory__in=factory, 
        Company=company, 
        CaseValidation=True
    ).annotate(
        closed_cases=Count('pk', filter=Q(CaseStatus=CaseStatus.CLOSED)),
        resolved_cases=Count('pk', filter=Q(CaseStatus=CaseStatus.RESOLVED)),
        non_breached_cases=Count('pk', filter=Q(Breached=False) & (Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED))),
        reopened_cases=Count('pk', filter=Q(reopened=True))
    )

    results = {}
    for case in cases:
        fac = case.Factory
        min_programs = min_programs_map.get(fac.id, 4)
        resolved_closed_cases = case.closed_cases + case.resolved_cases
        percent = (case.non_breached_cases / resolved_closed_cases) * 100 if resolved_closed_cases else 0
        repercent = (case.reopened_cases / (resolved_closed_cases + case.reopened_cases)) * 100 if (resolved_closed_cases + case.reopened_cases) else 0

        programs = awareness_programs.get(Factory=fac).breached_count if fac in min_programs_map else 0

        if percent == 100.0 and repercent <= 10 and resolved_closed_cases >= 3 and programs >= min_programs:
            results[fac.Code] = case.closed_cases

    try:
        max_value = max(results.values())
        winner = [key for key, value in results.items() if value == max_value]
    except ValueError:
        winner = []

    return Response({"Winner": winner})
