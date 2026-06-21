#!/usr/bin/env python3
"""QC: Polymarket Report Freshness Check (TL-03)
Checks if Polymarket_FIFA2026_分析报告.md is >12h stale vs the latest match date.
Usage: python scripts/qc/verify_polymarket.py <path_to_report>
"""

import json, sys, os
from datetime import datetime, timedelta

REPO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_DIR)

def main(report_path: str):
    print(f'\n{"="*60}')
    print(f'  QC: Polymarket Report Freshness (TL-03)')
    print(f'{"="*60}\n')

    # 1. Parse report date
    report_date = None
    try:
        with open(report_path, encoding='utf-8') as f:
            for line in f:
                if '分析日期' in line:
                    # Format: "> 分析日期：2026年6月15日 · 距今 X 天 · ⚠️ 待更新"
                    import re
                    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', line)
                    if m:
                        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
                        report_date = datetime(y, mo, d)
                    print(f'  报告: {line.strip()}')
                    break
    except FileNotFoundError:
        print(f'  ❌ BLOCKER: 报告文件不存在: {report_path}')
        return 1

    if not report_date:
        print('  ❌ BLOCKER: 无法解析报告日期')
        return 1

    # 2. Find latest match date
    data_path = os.path.join(REPO_DIR, 'match_data.json')
    try:
        data = json.load(open(data_path, encoding='utf-8'))
    except FileNotFoundError:
        print(f'  ❌ BLOCKER: match_data.json 不存在')
        return 1

    scored = [m for m in data if m.get('is_result')]
    if not scored:
        print('  ⚠️  无已结束比赛数据')
        return 0

    latest = max(m['date'] for m in scored)
    latest_dt = datetime.strptime(latest, '%Y-%m-%d')

    # 3. Compute staleness
    now = datetime.now()
    hours_stale = (now - report_date).total_seconds() / 3600
    hours_since_match = (now - latest_dt).total_seconds() / 3600

    print(f'  报告日期: {report_date.strftime("%Y-%m-%d")}')
    print(f'  最新比赛: {latest} ({len(scored)}场已结束)')
    print(f'  报告距今: {hours_stale:.1f}小时')
    print(f'  最近比赛距今: {hours_since_match:.1f}小时')

    # 4. Verdict
    if hours_stale > 12:
        print(f'\n  🔴 BLOCKER: TL-03 报告超过12小时未更新！')
        print(f'     需要更新 Polymarket_FIFA2026_分析报告.md')
        print(f'     最新比分已有 {len(scored)} 场，报告仅覆盖 10 场')
        return 1
    elif hours_stale > 6:
        print(f'\n  🟡 WARN: 报告接近12小时阈值 ({hours_stale:.0f}h)')
        return 0
    else:
        print(f'\n  ✅ QC通过 (TL-03)')
        return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/qc/verify_polymarket.py <report_path>')
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
