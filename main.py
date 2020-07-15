from datetime import datetime


FIXED_TAX = 0.36
MINUTE_TAX = 0.09
TAXABLE_START_HOUR = 6
TAXABLE_END_HOUR = 22


def classify_by_phone_number(calls_list):
    totals = {}
    for call in calls_list:
        if call['source'] not in totals:
            totals[call['source']] = 0

        totals[call['source']] += calculate_tax(call)

    result = []
    for k in sorted(totals, key=totals.get, reverse=True):
        result.append({'source': k, 'total': round(totals[k], 2)})

    return result


def calculate_tax(call):
    start_datetime = datetime.fromtimestamp(call['start'])
    end_datetime = datetime.fromtimestamp(call['end'])

    if is_free_call(start_datetime, end_datetime):
        return FIXED_TAX

    # Ignore the free periods
    if start_datetime.hour < TAXABLE_START_HOUR:
        start_datetime = start_datetime.replace(
            hour=TAXABLE_START_HOUR, minute=0, second=0)
    if end_datetime.hour >= TAXABLE_END_HOUR:
        hour = TAXABLE_END_HOUR - 1 if TAXABLE_END_HOUR != 0 else 23
        end_datetime = end_datetime.replace(hour=hour, minute=59, second=59)

    call_minutes = (end_datetime.timestamp() - start_datetime.timestamp()) / 60

    # Ignore the seconds since they are not charged
    call_minutes = int(call_minutes)

    return FIXED_TAX + (MINUTE_TAX * call_minutes)


def is_free_call(start: datetime, end: datetime):
    """
    Returns "true" if the call was made during the free period.
    Since the calls always begins and ends at the same day, the logic for this
    function becomes much more easier.
    """
    return start.hour >= TAXABLE_END_HOUR or end.hour <= TAXABLE_START_HOUR
