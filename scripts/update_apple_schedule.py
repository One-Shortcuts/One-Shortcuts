from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.request
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


HTML_PATH = Path(os.environ.get("HTML_PATH", "today-at-apple.html"))
START_MARKER = "<!-- APPLE_SCHEDULE_START -->"
END_MARKER = "<!-- APPLE_SCHEDULE_END -->"
STORES = [
    {
        "key": "iconsiam",
        "short_name": "Iconsiam",
        "name": "Apple Iconsiam",
        "calendar_url": "https://www.apple.com/th/today/calendar/iconsiam/?sn=R728",
        "sn": "R728",
    },
    {
        "key": "centralworld",
        "short_name": "Central World",
        "name": "Apple Central World",
        "calendar_url": "https://www.apple.com/th/today/calendar/centralworld/?sn=R733",
        "sn": "R733",
    },
]


def clean_text(value: str | None) -> str:
    value = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", value or "")
    return re.sub(r"\s+", " ", value).strip()


def fetch_calendar_html(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def extract_json_object(source: str, marker: str) -> dict:
    marker_index = source.find(marker)
    if marker_index < 0:
        raise ValueError(f"Could not find {marker}")

    start = source.find("{", marker_index + len(marker) - 2)
    if start < 0:
        raise ValueError(f"Could not find object start after {marker}")

    depth = 0
    for index in range(start, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                raw = source[start : index + 1]
                unescaped = (
                    raw.replace('\\\\\"', "__ESCAPED_BACKSLASH_QUOTE__")
                    .replace('\\"', '"')
                    .replace("__ESCAPED_BACKSLASH_QUOTE__", '\\\\"')
                )
                return json.loads(unescaped)

    raise ValueError(f"Could not find object end after {marker}")


def extract_json_array(source: str, marker: str) -> list:
    marker_index = source.find(marker)
    if marker_index < 0:
        raise ValueError(f"Could not find {marker}")

    start = source.find("[", marker_index + len(marker) - 2)
    if start < 0:
        raise ValueError(f"Could not find array start after {marker}")

    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                raw = source[start : index + 1]
                unescaped = (
                    raw.replace('\\\\\"', "__ESCAPED_BACKSLASH_QUOTE__")
                    .replace('\\"', '"')
                    .replace("__ESCAPED_BACKSLASH_QUOTE__", '\\\\"')
                )
                return json.loads(unescaped)

    raise ValueError(f"Could not find array end after {marker}")


def thai_weekday_short(display_date: dict) -> str:
    label = clean_text(
        (display_date.get("weekdayLong") or {}).get("lower")
        or display_date.get("dateLongDay")
        or display_date.get("date")
    )
    mapping = [
        ("อาทิตย์", "อา"),
        ("จันทร์", "จ"),
        ("อังคาร", "อ"),
        ("พุธ", "พ"),
        ("พฤหัส", "พฤ"),
        ("ศุกร์", "ศ"),
        ("เสาร์", "ส"),
    ]
    for needle, short in mapping:
        if needle in label:
            return short
    return ""


def thai_date_label(calendar_date: dict) -> str:
    start_date = calendar_date.get("startDate")
    if start_date:
        date = datetime.fromtimestamp(start_date / 1000, ZoneInfo("Asia/Bangkok")).date()
        today = datetime.now(ZoneInfo("Asia/Bangkok")).date()
        if date == today:
            return "วันนี้"
        if (date - today).days == 1:
            return "พรุ่งนี้"

    full_date = clean_text(calendar_date.get("fullDate"))
    return re.sub(r"\s+\d{4}$", "", full_date)


def date_key_from_calendar_date(calendar_date: dict) -> str:
    start_date = calendar_date.get("startDate")
    if not start_date:
        return ""
    return datetime.fromtimestamp(start_date / 1000, ZoneInfo("Asia/Bangkok")).date().isoformat()


def build_event_url(course: dict, schedule_id: str, store: dict) -> str:
    slug = clean_text(course.get("urlTitle"))
    if slug:
        return f"https://www.apple.com/th/today/event/{slug}/{schedule_id}/?sn={store['sn']}"
    return store["calendar_url"]


def build_card(schedule: dict, course: dict, store: dict) -> str:
    display_date = (schedule.get("displayDate") or [{}])[0]
    time_label = clean_text(display_date.get("timeRange"))
    title = clean_text(course.get("name") or course.get("title") or "Today at Apple Session")
    description = clean_text(course.get("shortDescription"))
    if len(description) > 155:
        description = description[:155].rstrip() + "..."
    url = build_event_url(course, schedule["id"], store)

    return f'''        <a href="{html.escape(url)}" class="session-card">
          <div class="session-time">{html.escape(time_label)}</div>
          <div class="session-title">{html.escape(title)}</div>
          <div class="session-desc">{html.escape(description)}</div>
        </a>'''


def build_store_panel(store: dict, calendar_html: str, is_active: bool) -> str:
    calendar_dates = extract_json_array(calendar_html, '\\"calendarDates\\":[')
    courses = extract_json_object(calendar_html, '\\"courses\\":{')
    schedules = extract_json_object(calendar_html, '\\"schedules\\":{')

    grouped: OrderedDict[str, dict] = OrderedDict()
    for calendar_date in calendar_dates:
        date_key = date_key_from_calendar_date(calendar_date)
        if not date_key:
            continue
        grouped.setdefault(
            date_key,
            {
                "weekday": clean_text(calendar_date.get("day")),
                "day": str(calendar_date.get("date") or ""),
                "label": thai_date_label(calendar_date),
                "items": [],
            },
        )

    for schedule in sorted(schedules.values(), key=lambda item: item.get("startTime", 0)):
        display_date = (schedule.get("displayDate") or [{}])[0]
        date_key = clean_text(schedule.get("displayStartTime", ""))[:10]
        if not date_key:
            continue
        grouped.setdefault(
            date_key,
            {
                "weekday": thai_weekday_short(display_date),
                "day": clean_text(display_date.get("dayNumber")),
                "label": clean_text(display_date.get("relativeDate") or display_date.get("date")),
                "items": [],
            },
        )
        course = courses.get(schedule.get("courseId"), {})
        grouped[date_key]["items"].append(build_card(schedule, course, store))

    first_key = next(iter(grouped), "")
    date_buttons = []
    day_sections = []
    store_key = html.escape(store["key"])
    for date_key, group in grouped.items():
        active = " active" if date_key == first_key else ""
        hidden = "" if date_key == first_key else " hidden"
        safe_date = html.escape(date_key)
        date_buttons.append(
            f'''        <button class="date-choice{active}" onclick="showScheduleDate('{store_key}', '{safe_date}')" data-date-key="{safe_date}" aria-label="{html.escape(group['label'])}">
          <span class="date-weekday">{html.escape(group['weekday'])}</span>
          <span class="date-number">{html.escape(group['day'])}</span>
        </button>'''
        )
        day_sections.append(
            f'''      <div class="schedule-day{hidden}" data-schedule-day="{safe_date}">
        <div class="schedule-day-title">{html.escape(group['label'])}</div>
{chr(10).join(group["items"]) or '        <div class="session-card"><div class="session-title">ไม่พบเซสชั่น</div><div class="session-desc">โปรดดูตารางทั้งหมดบน Apple หรือกลับมาใหม่ภายหลัง</div></div>'}
      </div>'''
        )

    active = "" if is_active else " hidden"
    return f'''    <div class="schedule-card store-panel{active}" data-store-panel="{store_key}" data-store-name="{html.escape(store['name'])}" data-store-url="{html.escape(store['calendar_url'])}">
      <div class="date-strip" aria-label="Session dates">
{chr(10).join(date_buttons)}
      </div>
{chr(10).join(day_sections)}
      <a href="{html.escape(store['calendar_url'])}" class="full-schedule-link" data-en="View full schedule on Apple" data-th="ดูตารางทั้งหมดบน Apple">View full schedule on Apple</a>
    </div>'''


def build_schedule_block() -> str:
    store_options = "\n".join(
        f'''      <button class="store-option{' active' if index == 0 else ''}" onclick="setActiveStore('{html.escape(store['key'])}', true)" data-store-option="{html.escape(store['key'])}">{html.escape(store['short_name'])}</button>'''
        for index, store in enumerate(STORES)
    )
    panels = "\n".join(
        build_store_panel(store, fetch_calendar_html(store["calendar_url"]), is_active=index == 0)
        for index, store in enumerate(STORES)
    )
    first_store = html.escape(STORES[0]["name"])

    return f'''{START_MARKER}
    <div class="store-summary">
      <div>
        <div id="active-store-name" class="store-name">{first_store}</div>
      </div>
      <div id="schedule-actions" class="schedule-actions">
        <button class="action-btn" onclick="toggleScheduleQR()" data-en="QR Code" data-th="QR Code">QR Code</button>
        <a id="schedule-open-link" class="action-btn primary" href="{html.escape(STORES[0]['calendar_url'])}" data-en="Open Safari" data-th="เปิด Safari">Open Safari</a>
      </div>
    </div>
    <div id="schedule-qr-wrap" style="display:none;text-align:center;margin:0 0 10px;">
      <div id="schedule-qr" style="display:inline-block;background:#fff;padding:12px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.12);"></div>
      <div style="font-size:12px;color:var(--text2);margin-top:8px;" data-en="Scan to open" data-th="สแกนเพื่อเปิด">Scan to open</div>
    </div>
    <div class="store-toggle" aria-label="Choose Apple Store">
{store_options}
    </div>
{panels}
    {END_MARKER}'''


def update_html_file() -> bool:
    page = HTML_PATH.read_text(encoding="utf-8")
    start = page.find(START_MARKER)
    end = page.find(END_MARKER)
    if start < 0 or end < 0:
        raise ValueError(f"{HTML_PATH} must contain {START_MARKER} and {END_MARKER}")

    end += len(END_MARKER)
    schedule_block = build_schedule_block()
    updated = page[:start] + schedule_block + page[end:]

    if updated == page:
        return False

    HTML_PATH.write_text(updated, encoding="utf-8")
    return True


if __name__ == "__main__":
    try:
        changed = update_html_file()
    except Exception as exc:
        print(f"Failed to update Apple schedule: {exc}", file=sys.stderr)
        sys.exit(1)

    print("Schedule updated." if changed else "Schedule already up to date.")
