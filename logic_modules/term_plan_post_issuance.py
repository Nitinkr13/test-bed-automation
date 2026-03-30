import calendar
import random
from datetime import date, timedelta

import pandas as pd

from logic_modules import term_plan_issuance as issuance

POST_ISSUANCE_EPICS_BY_PLAN = {
    "term plan": {
        "FLC": [
            "Freelook Cancellation Beyond 30 day period",
            "Freelook Cancellation Comms",
            "Freelook Cancellation for AD rider",
            "Freelook Cancellation GL Reports",
            "Freelook Cancellation iAssist quotation",
            "Freelook Cancellation iAssist Refund",
            "Freelook Cancellation with Medical Charges",
            "Freelook Cancellation within 30 days",
        ],
        "Grace": [
            "Grace for Annual Scenarios",
            "Grace for Half Yearly",
            "Grace for Quarterly",
            "Grace for Monthly",
        ],
        "Lapse": [
            "Check for policy Lapsation - Annual",
            "Check for policy Lapsation - Half Yearly",
            "Check for policy Lapsation - Quarterly",
            "Check for policy Lapsation - Monthly",
            "Check for policy Lapsation - Communication",
            "Check for policy Lapsation in Ops Console - Annual",
            "Check for policy Lapsation in Ops Console - Half Yearly",
            "Check for policy Lapsation in Ops Console - Quarterly",
            "Check for policy Lapsation in Ops Console - Monthly",
            "Check for policy Lapsation on iAssist",
        ],
    }
}


def get_post_issuance_epics_for_plan(plan_type):
    return POST_ISSUANCE_EPICS_BY_PLAN.get(plan_type, {})

MODULE_NAME = "Term Plan"
LIFECYCLE_STAGE = "post issuance"
PRODUCT_CODE = getattr(issuance, "PRODUCT_CODE", "")

EPIC_HEADERS = get_post_issuance_epics_for_plan("term plan")

EPIC_TEST_SCENARIO_MAP = {
    # FLC scenarios
    "Freelook Cancellation Beyond 30 day period": "To verify whether freelook cancellation request is rejected beyond 30 days of policy issuance.",
    "Freelook Cancellation Comms": "To check if communication is triggered to customer after freelook cancellation as per existing logic.",
    "Freelook Cancellation for AD rider": "To verify whether system allows Freelook Cancellation for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation GL Reports": "To check if correct activity,Breakdown  file generated for policy where Freelook cancellation is processed.",
    "Freelook Cancellation iAssist quotation": "To check if customer is able to view quotation on iAssist while giving request for Freelook cancellation",
    "Freelook Cancellation iAssist Refund": "To verify whether system allows Freelook Cancellation iAssist Refund based on Policy Acknowledgement timelines.",
    "Freelook Cancellation with Medical Charges": "To check if medical charges are fetched from datalake before processing freelook cancellation.",
    "Freelook Cancellation within 30 days": "To check if system allows to process Freelook cancellation within 30 days from Policy issuance.",
    # Grace scenarios
    "Grace for Annual Scenarios": "To verify grace applicability for Grace for Annual Scenarios with valid premium renewal timelines.",
    "Grace for Half Yearly": "To verify grace applicability for Grace for Half Yearly with valid premium renewal timelines.",
    "Grace for Quarterly": "To verify grace applicability for Grace for Quarterly with valid premium renewal timelines.",
    "Grace for Monthly": "To verify grace applicability for Grace for Monthly with valid premium renewal timelines.",
    # Lapse scenarios
    "Check for policy Lapsation - Annual": "To verify lapse trigger behavior for Check for policy Lapsation - Annual after grace completion.",
    "Check for policy Lapsation - Half Yearly": "To verify lapse trigger behavior for Check for policy Lapsation - Half Yearly after grace completion.",
    "Check for policy Lapsation - Quarterly": "To verify lapse trigger behavior for Check for policy Lapsation - Quarterly after grace completion.",
    "Check for policy Lapsation - Monthly": "To verify lapse trigger behavior for Check for policy Lapsation - Monthly after grace completion.",
    "Check for policy Lapsation - Communication": "To verify lapse trigger behavior for Check for policy Lapsation - Communication after grace completion.",
    "Check for policy Lapsation in Ops Console - Annual": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Annual after grace completion.",
    "Check for policy Lapsation in Ops Console - Half Yearly": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Half Yearly after grace completion.",
    "Check for policy Lapsation in Ops Console - Quarterly": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Quarterly after grace completion.",
    "Check for policy Lapsation in Ops Console - Monthly": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Monthly after grace completion.",
    "Check for policy Lapsation on iAssist": "To verify lapse trigger behavior for Check for policy Lapsation on iAssist after grace completion.",
}

EPIC_EXPECTED_RESULT_MAP = {
    # FLC scenarios
    "Freelook Cancellation Beyond 30 day period": "System should process Freelook Cancellation Beyond 30 day period as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation Comms": "System should process Freelook Cancellation Comms as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation for AD rider": "System should process Freelook Cancellation for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation GL Reports": "System should process Freelook Cancellation GL Reports as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation iAssist quotation": "System should process Freelook Cancellation iAssist quotation as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation iAssist Refund": "System should process Freelook Cancellation iAssist Refund as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation with Medical Charges": "System should process Freelook Cancellation with Medical Charges as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation within 30 days": "System should process Freelook Cancellation within 30 days as per freelook timelines and generate correct comms/ledger impact.",
    # Grace scenarios
    "Grace for Annual Scenarios": "System should keep policy in grace for Grace for Annual Scenarios until grace end date with correct status visibility.",
    "Grace for Half Yearly": "System should keep policy in grace for Grace for Half Yearly until grace end date with correct status visibility.",
    "Grace for Quarterly": "System should keep policy in grace for Grace for Quarterly until grace end date with correct status visibility.",
    "Grace for Monthly": "System should keep policy in grace for Grace for Monthly until grace end date with correct status visibility.",
    # Lapse scenarios
    "Check for policy Lapsation - Annual": "System should lapse policy for Check for policy Lapsation - Annual only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Half Yearly": "System should lapse policy for Check for policy Lapsation - Half Yearly only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Quarterly": "System should lapse policy for Check for policy Lapsation - Quarterly only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Monthly": "System should lapse policy for Check for policy Lapsation - Monthly only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Communication": "System should lapse policy for Check for policy Lapsation - Communication only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Annual": "System should lapse policy for Check for policy Lapsation in Ops Console - Annual only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Half Yearly": "System should lapse policy for Check for policy Lapsation in Ops Console - Half Yearly only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Quarterly": "System should lapse policy for Check for policy Lapsation in Ops Console - Quarterly only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Monthly": "System should lapse policy for Check for policy Lapsation in Ops Console - Monthly only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation on iAssist": "System should lapse policy for Check for policy Lapsation on iAssist only after grace expiry and reflect lapse status in all touchpoints.",
}

EPIC_TEST_SCENARIO_MAP_RIDER = {
    # FLC scenarios
    "Freelook Cancellation Beyond 30 day period": "To verify whether system allows Freelook Cancellation Beyond 30 day period for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation Comms": "To verify whether system allows Freelook Cancellation Comms for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation for AD rider": "To verify whether system allows Freelook Cancellation for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation GL Reports": "To verify whether system allows Freelook Cancellation GL Reports for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation iAssist quotation": "To verify whether system allows Freelook Cancellation iAssist quotation for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation iAssist Refund": "To verify whether system allows Freelook Cancellation iAssist Refund for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation with Medical Charges": "To verify whether system allows Freelook Cancellation with Medical Charges for AD rider based on Policy Acknowledgement timelines.",
    "Freelook Cancellation within 30 days": "To verify whether system allows Freelook Cancellation within 30 days for AD rider based on Policy Acknowledgement timelines.",
    # Grace scenarios
    "Grace for Annual Scenarios": "To verify grace applicability for Grace for Annual Scenarios for AD rider with valid premium renewal timelines.",
    "Grace for Half Yearly": "To verify grace applicability for Grace for Half Yearly for AD rider with valid premium renewal timelines.",
    "Grace for Quarterly": "To verify grace applicability for Grace for Quarterly for AD rider with valid premium renewal timelines.",
    "Grace for Monthly": "To verify grace applicability for Grace for Monthly for AD rider with valid premium renewal timelines.",
    # Lapse scenarios
    "Check for policy Lapsation - Annual": "To verify lapse trigger behavior for Check for policy Lapsation - Annual for AD rider after grace completion.",
    "Check for policy Lapsation - Half Yearly": "To verify lapse trigger behavior for Check for policy Lapsation - Half Yearly for AD rider after grace completion.",
    "Check for policy Lapsation - Quarterly": "To verify lapse trigger behavior for Check for policy Lapsation - Quarterly for AD rider after grace completion.",
    "Check for policy Lapsation - Monthly": "To verify lapse trigger behavior for Check for policy Lapsation - Monthly for AD rider after grace completion.",
    "Check for policy Lapsation - Communication": "To verify lapse trigger behavior for Check for policy Lapsation - Communication for AD rider after grace completion.",
    "Check for policy Lapsation in Ops Console - Annual": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Annual for AD rider after grace completion.",
    "Check for policy Lapsation in Ops Console - Half Yearly": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Half Yearly for AD rider after grace completion.",
    "Check for policy Lapsation in Ops Console - Quarterly": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Quarterly for AD rider after grace completion.",
    "Check for policy Lapsation in Ops Console - Monthly": "To verify lapse trigger behavior for Check for policy Lapsation in Ops Console - Monthly for AD rider after grace completion.",
    "Check for policy Lapsation on iAssist": "To verify lapse trigger behavior for Check for policy Lapsation on iAssist for AD rider after grace completion.",
}

EPIC_EXPECTED_RESULT_MAP_RIDER = {
    # FLC scenarios
    "Freelook Cancellation Beyond 30 day period": "System should process Freelook Cancellation Beyond 30 day period for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation Comms": "System should process Freelook Cancellation Comms for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation for AD rider": "System should process Freelook Cancellation for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation GL Reports": "System should process Freelook Cancellation GL Reports for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation iAssist quotation": "System should process Freelook Cancellation iAssist quotation for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation iAssist Refund": "System should process Freelook Cancellation iAssist Refund for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation with Medical Charges": "System should process Freelook Cancellation with Medical Charges for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    "Freelook Cancellation within 30 days": "System should process Freelook Cancellation within 30 days for AD rider as per freelook timelines and generate correct comms/ledger impact.",
    # Grace scenarios
    "Grace for Annual Scenarios": "System should keep policy in grace for Grace for Annual Scenarios for AD rider until grace end date with correct status visibility.",
    "Grace for Half Yearly": "System should keep policy in grace for Grace for Half Yearly for AD rider until grace end date with correct status visibility.",
    "Grace for Quarterly": "System should keep policy in grace for Grace for Quarterly for AD rider until grace end date with correct status visibility.",
    "Grace for Monthly": "System should keep policy in grace for Grace for Monthly for AD rider until grace end date with correct status visibility.",
    # Lapse scenarios
    "Check for policy Lapsation - Annual": "System should lapse policy for Check for policy Lapsation - Annual for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Half Yearly": "System should lapse policy for Check for policy Lapsation - Half Yearly for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Quarterly": "System should lapse policy for Check for policy Lapsation - Quarterly for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Monthly": "System should lapse policy for Check for policy Lapsation - Monthly for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation - Communication": "System should lapse policy for Check for policy Lapsation - Communication for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Annual": "System should lapse policy for Check for policy Lapsation in Ops Console - Annual for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Half Yearly": "System should lapse policy for Check for policy Lapsation in Ops Console - Half Yearly for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Quarterly": "System should lapse policy for Check for policy Lapsation in Ops Console - Quarterly for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation in Ops Console - Monthly": "System should lapse policy for Check for policy Lapsation in Ops Console - Monthly for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
    "Check for policy Lapsation on iAssist": "System should lapse policy for Check for policy Lapsation on iAssist for AD rider only after grace expiry and reflect lapse status in all touchpoints.",
}

EPIC_MAP = {
    epic_name: epic_name
    for header_data in EPIC_HEADERS.values()
    for epic_name in header_data
}
EPIC_MAP_RIDER = {
    epic_name: epic_name
    for header_data in EPIC_HEADERS.values()
    for epic_name in header_data
}

FREQUENCY_INTERVAL_MONTHS = {
    1: 12,
    2: 6,
    3: 3,
    4: 1,
    5: 0,
    "annual": 12,
    "yearly": 12,
    "half yearly": 6,
    "half-yearly": 6,
    "quarterly": 3,
    "monthly": 1,
    "single": 0,
}


def _generate_seed_positive_rows(case_count):
    if case_count <= 0:
        return pd.DataFrame(columns=issuance.column_order)

    seed_epic_counts = {
        "PaymentFrequency": {
            "positive": case_count,
            "negative": 0,
            "payment_frequency_options": [1, 2, 3, 4, 5],
        }
    }
    seed_df = issuance.generate_test_cases(
        epic_counts=seed_epic_counts,
        selected_epics=["PaymentFrequency"],
        epic_counts_rider={},
        selected_epics_rider=[],
    )

    if seed_df.empty:
        return pd.DataFrame(columns=issuance.column_order)

    positive_seed_df = seed_df[seed_df["Test_Type"] == "Positive"].copy()
    return positive_seed_df.head(case_count)


def _get_positive_count(counts):
    counts = counts or {}
    if "positive" in counts:
        return int(counts.get("positive", 0) or 0)

    ppt_pos_counts = counts.get("ppt_pos_counts", {})
    if isinstance(ppt_pos_counts, dict):
        return sum(int(value or 0) for value in ppt_pos_counts.values())

    return 0


def _generate_seed_positive_rider_rows(counts):
    positive_count = _get_positive_count(counts)
    if positive_count <= 0:
        return pd.DataFrame(columns=issuance.column_order)
    return _generate_seed_positive_rows(positive_count)


def _resolve_header(selected_header, epic_name):
    if selected_header in EPIC_HEADERS:
        return selected_header

    for header_name, epic_names in EPIC_HEADERS.items():
        if epic_name in epic_names:
            return header_name

    return "Post Issuance"


def _resolve_epic_metadata(header_name, epic_name, isrider=False):
    test_scenario_map = EPIC_TEST_SCENARIO_MAP_RIDER if isrider else EPIC_TEST_SCENARIO_MAP
    expected_result_map = EPIC_EXPECTED_RESULT_MAP_RIDER if isrider else EPIC_EXPECTED_RESULT_MAP
    return {
        "API_Operation": epic_name,
        "Test_Scenario": test_scenario_map.get(epic_name, f"{header_name} - {epic_name}"),
        "Expected_Result": expected_result_map.get(epic_name, issuance.EXPECTED_RESULT_MAP.get("Positive", "")),
    }


def _format_date(value):
    return value.strftime("%d/%m/%Y")


def _add_months(base_date, month_delta):
    target_month_index = (base_date.month - 1) + month_delta
    target_year = base_date.year + target_month_index // 12
    target_month = (target_month_index % 12) + 1
    target_day = min(base_date.day, calendar.monthrange(target_year, target_month)[1])
    return date(target_year, target_month, target_day)


def _months_between(start_date, end_date):
    total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if end_date.day < start_date.day:
        total_months -= 1
    return max(total_months, 0)


def _frequency_interval_in_months(row):
    freq_candidates = [row.get("paymentFreqW"), row.get("paymentFreq"), row.get("paymentFreqC")]

    for value in freq_candidates:
        if pd.isna(value):
            continue

        try:
            int_value = int(value)
            if int_value in FREQUENCY_INTERVAL_MONTHS:
                return FREQUENCY_INTERVAL_MONTHS[int_value]
        except (TypeError, ValueError):
            pass

        normalized = str(value).strip().lower().replace("_", " ")
        if normalized in FREQUENCY_INTERVAL_MONTHS:
            return FREQUENCY_INTERVAL_MONTHS[normalized]

    return 12


def _generate_rcd(today_value):
    months_back = random.randint(13, 36)
    return _add_months(today_value, -months_back)


def _generate_ptd_and_renewal_count(rcd_date, interval_months, today_value):
    if interval_months <= 0:
        return rcd_date, 0

    max_interval_steps = _months_between(rcd_date, today_value) // interval_months
    if max_interval_steps <= 0:
        return rcd_date, 0

    renewal_count = random.randint(1, max_interval_steps)
    ptd_date = _add_months(rcd_date, renewal_count * interval_months)

    if ptd_date >= today_value and renewal_count > 0:
        renewal_count -= 1
        ptd_date = _add_months(rcd_date, renewal_count * interval_months)

    return ptd_date, max(renewal_count, 0)


def _build_post_issuance_dates(row):
    today_value = date.today()
    interval_months = _frequency_interval_in_months(row)

    rcd_date = _generate_rcd(today_value)
    ptd_date, renewal_count = _generate_ptd_and_renewal_count(rcd_date, interval_months, today_value)

    flc_date = rcd_date + timedelta(days=30)
    grace_days = 15 if interval_months == 1 else 30
    grace_date = ptd_date + timedelta(days=grace_days)
    lapse_date = grace_date + timedelta(days=1)

    return {
        "rcd_date": rcd_date,
        "ptd_date": ptd_date,
        "flc_date": flc_date,
        "grace_date": grace_date,
        "lapse_date": lapse_date,
        "renewal_count": renewal_count,
    }


def _build_scenario_with_dates(base_scenario, date_context):
    scenario_lines = [
        base_scenario,
        f"RCD date: {_format_date(date_context['rcd_date'])}",
        f"PTD date: {_format_date(date_context['ptd_date'])}",
        f"Renewal count: {date_context['renewal_count']}",
        f"FLC date: {_format_date(date_context['flc_date'])}",
        f"Grace date: {_format_date(date_context['grace_date'])}",
        f"Lapse date: {_format_date(date_context['lapse_date'])}",
    ]

    return "\n".join(scenario_lines)


def _apply_post_issuance_overrides(row, epic_name, selected_header, tuid_counter, isrider=False):
    header_name = _resolve_header(selected_header, epic_name)
    metadata = _resolve_epic_metadata(header_name, epic_name, isrider=isrider)
    date_context = _build_post_issuance_dates(row)

    row["TUID"] = f"TC_{MODULE_NAME.replace(' ', '')}_POST_{tuid_counter:03d}"
    row["API_Mode"] = "Base plan + AD" if isrider else "Base plan"
    row["API_Operation"] = metadata.get("API_Operation", epic_name)
    row["Test Scenario"] = _build_scenario_with_dates(
        metadata.get("Test_Scenario", f"{header_name} - {epic_name}"),
        date_context,
    )
    row["Test_Type"] = "Positive"
    row["Expected_Result"] = metadata.get(
        "Expected_Result",
        issuance.EXPECTED_RESULT_MAP.get("Positive", row.get("Expected_Result")),
    )
    row["inceptionDate"] = _format_date(date_context["rcd_date"])
    row["FLC date"] = _format_date(date_context["flc_date"])
    row["Grace date"] = _format_date(date_context["grace_date"])
    row["Lapse date"] = _format_date(date_context["lapse_date"])

    return row


def _group_epics_by_header(epics, counts_dict, selected_header):
    grouped = {"FLC": [], "Grace": [], "Lapse": []}
    for epic_name in epics:
        counts = (counts_dict or {}).get(epic_name, {})
        header_name = counts.get("header") or selected_header or _resolve_header(None, epic_name)
        resolved_header = _resolve_header(header_name, epic_name)
        if resolved_header in grouped:
            grouped[resolved_header].append(epic_name)
    return grouped


def _append_base_cases_for_header(epic_names, header_name, epic_counts, selected_header, scenarios, tuid_counter):
    for epic_name in epic_names:
        counts = (epic_counts or {}).get(epic_name, {})
        positive_count = _get_positive_count(counts)
        if positive_count <= 0:
            continue

        seed_rows = _generate_seed_positive_rows(positive_count)
        header_label = counts.get("header") or selected_header or header_name
        for _, seed_row in seed_rows.iterrows():
            tuid_counter += 1
            row = seed_row.to_dict()
            row = _apply_post_issuance_overrides(row, epic_name, header_label, tuid_counter, isrider=False)
            scenarios.append(row)

    return tuid_counter


def _append_rider_cases_for_header(epic_names, header_name, epic_counts_rider, selected_header, scenarios, tuid_counter):
    for epic_name in epic_names:
        counts = (epic_counts_rider or {}).get(epic_name, {})
        seed_rows = _generate_seed_positive_rider_rows(counts)
        header_label = counts.get("header") or selected_header or header_name
        for _, seed_row in seed_rows.iterrows():
            tuid_counter += 1
            row = seed_row.to_dict()
            row = _apply_post_issuance_overrides(row, epic_name, header_label, tuid_counter, isrider=True)
            scenarios.append(row)

    return tuid_counter


def generate_test_cases(epic_counts, selected_epics=None, epic_counts_rider=None, selected_epics_rider=None, selected_header=None):
    selected_epics = selected_epics or list((epic_counts or {}).keys())
    selected_epics_rider = selected_epics_rider or list((epic_counts_rider or {}).keys())
    if not selected_epics and not selected_epics_rider:
        return pd.DataFrame(columns=issuance.column_order)

    scenarios = []
    tuid_counter = 0

    base_grouped_epics = _group_epics_by_header(selected_epics, epic_counts, selected_header)
    rider_grouped_epics = _group_epics_by_header(selected_epics_rider, epic_counts_rider, selected_header)

    for header_name in ["FLC", "Grace", "Lapse"]:
        if header_name == "FLC":
            tuid_counter = _append_base_cases_for_header(
                base_grouped_epics["FLC"],
                "FLC",
                epic_counts,
                selected_header,
                scenarios,
                tuid_counter,
            )
        if header_name == "Grace":
            tuid_counter = _append_base_cases_for_header(
                base_grouped_epics["Grace"],
                "Grace",
                epic_counts,
                selected_header,
                scenarios,
                tuid_counter,
            )
        if header_name == "Lapse":
            tuid_counter = _append_base_cases_for_header(
                base_grouped_epics["Lapse"],
                "Lapse",
                epic_counts,
                selected_header,
                scenarios,
                tuid_counter,
            )

    for header_name in ["FLC", "Grace", "Lapse"]:
        if header_name == "FLC":
            tuid_counter = _append_rider_cases_for_header(
                rider_grouped_epics["FLC"],
                "FLC",
                epic_counts_rider,
                selected_header,
                scenarios,
                tuid_counter,
            )
        if header_name == "Grace":
            tuid_counter = _append_rider_cases_for_header(
                rider_grouped_epics["Grace"],
                "Grace",
                epic_counts_rider,
                selected_header,
                scenarios,
                tuid_counter,
            )
        if header_name == "Lapse":
            tuid_counter = _append_rider_cases_for_header(
                rider_grouped_epics["Lapse"],
                "Lapse",
                epic_counts_rider,
                selected_header,
                scenarios,
                tuid_counter,
            )

    if not scenarios:
        return pd.DataFrame(columns=issuance.column_order)

    result_df = pd.DataFrame(scenarios)
    for col in issuance.column_order:
        if col not in result_df.columns:
            result_df[col] = ""

    return result_df[issuance.column_order]
