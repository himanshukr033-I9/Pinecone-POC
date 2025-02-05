import json
import os
import glob
import argparse

def convert_json_to_markdown(data):
    """
    Converts a JSON object (with organization data) into a standardized markdown string.
    The markdown follows a fixed schema, even when some keys are missing.
    """
    lines = []
    # ---------------------------------------------------------------------------
    # Section 0: Organization Title
    org_name = (data.get("organizationCoreInformation", {}).get("organizationName")
                or data.get("organizationName")
                or "Organization Name Unknown")
    lines.append(f"# Organization Data: *{org_name}*")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 1: Leadership Information
    lines.append("## 1. Leadership Information")
    lines.append("")
    leadership = data.get("leadershipInformation", {})
    # Sort years numerically if possible
    for i, year in enumerate(sorted(leadership.keys(), key=lambda x: int(x)), start=1):
        lines.append(f"### 1.{i}. {year}")
        leaders = leadership.get(year, [])
        for j, leader in enumerate(leaders, start=1):
            lines.append(f"#### 1.{i}.{j}. Leader {j}")
            leaderName = leader.get("leaderName", "")
            position = leader.get("position", "")
            compensation = leader.get("compensation", "")
            lines.append(f"- **leaderName:** {leaderName}")
            lines.append(f"- **position:** {position}")
            lines.append(f"- **compensation:** {compensation}")
            lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 2: Expense Breakdown
    lines.append("## 2. Expense Breakdown")
    expense = data.get("expenseBreakdown", {})
    if expense:
        for i, year in enumerate(sorted(expense.keys(), key=lambda x: int(x)), start=1):
            exp = expense.get(year, {})
            lines.append(f"### 2.{i}. {year}")
            fundraising = exp.get("fundraising", "")
            management = exp.get("management_general", "")
            program = exp.get("program", "")
            year_field = exp.get("year", year)
            lines.append(f"- **fundraising:** {fundraising}")
            lines.append(f"- **management_general:** {management}")
            lines.append(f"- **program:** {program}")
            lines.append(f"- **year:** {year_field}")
            lines.append("")
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 3: Revenue Breakdown
    lines.append("## 3. Revenue Breakdown")
    revenue = data.get("revenueBreakdown", {})
    if revenue:
        for i, year in enumerate(sorted(revenue.keys(), key=lambda x: int(x)), start=1):
            rev = revenue.get(year, {})
            lines.append(f"### 3.{i}. {year}")
            totalContrib = rev.get("TotalContributionsAmt", "")
            other_contrib = rev.get("other_contributions", "")
            prog_rev = rev.get("program_revenue", "")
            govt_grants = rev.get("government_grants", "")
            invest_income = rev.get("investment_income", "")
            other_rev = rev.get("other_revenue", "")
            year_field = rev.get("year", year)
            lines.append(f"- **TotalContributionsAmt:** {totalContrib}")
            lines.append(f"- **other_contributions:** {other_contrib}")
            lines.append(f"- **program_revenue:** {prog_rev}")
            lines.append(f"- **government_grants:** {govt_grants}")
            lines.append(f"- **investment_income:** {invest_income}")
            lines.append(f"- **other_revenue:** {other_rev}")
            lines.append(f"- **year:** {year_field}")
            lines.append("")
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    

    # ---------------------------------------------------------------------------
    # Section 4: Revenue (Total)
    lines.append("## 4. Revenue (Total)")
    rev_total = data.get("revenue", {})
    if rev_total:
        for i, year in enumerate(sorted(rev_total.keys(), key=lambda x: int(x)), start=1):
            tot = rev_total.get(year, {})
            lines.append(f"### 4.{i}. {year}")
            amount = tot.get("amount", "")
            year_field = tot.get("year", year)
            lines.append(f"- **amount:** {amount}")
            lines.append(f"- **year:** {year_field}")
            lines.append("")
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 5: Expense (Total)
    lines.append("## 5. Expense (Total)")
    exp_total = data.get("expense", {})
    if exp_total:
        for i, year in enumerate(sorted(exp_total.keys(), key=lambda x: int(x)), start=1):
            tot = exp_total.get(year, {})
            lines.append(f"### 5.{i}. {year}")
            amount = tot.get("amount", "")
            year_field = tot.get("year", year)
            lines.append(f"- **amount:** {amount}")
            lines.append(f"- **year:** {year_field}")
            lines.append("")
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 6: Organization Core Information
    lines.append("## 6. Organization Core Information")
    # 6.1 Basic Details
    lines.append("### 6.1. Basic Details")
    core = data
    organizationName = core.get("organizationName", "")
    employer_id = core.get("employer_id", "")
    founded_year = core.get("founded_year", "")
    location = core.get("location", "")
    zip_code = core.get("zip", "")
    state = core.get("state", "")
    city = core.get("city", "")
    lines.append(f"- **organizationName:** {organizationName}")
    lines.append(f"- **employer_id:** {employer_id}")
    lines.append(f"- **founded_year:** {founded_year}")
    lines.append(f"- **location:** {location}")
    lines.append(f"- **zip:** {zip_code}")
    lines.append(f"- **state:** {state}")
    lines.append(f"- **city:** {city}")
    lines.append("")
    # 6.2 Mission
    lines.append("### 6.2. Mission")
    mission = data.get("mission", "")
    lines.append(f"- **mission:** {mission}")
    lines.append("")
    # 6.3 Key Activities
    lines.append("### 6.3. Key Activities")
    activities_data = data.get("keyActivities", [])
    if isinstance(activities_data, str):
        activities = [line.strip() for line in activities_data.splitlines() if line.strip()]
    else:
        activities = activities_data
    for idx in range(1, len(activities) + 1):
        act = activities[idx-1] if idx-1 < len(activities) else ""
        lines.append(f"- **Activity {idx}:** {act}")
    lines.append("")

    # 6.4 Potential Risks
    lines.append("### 6.4. Potential Risks")
    risks_data = data.get("potentialRisks", [])
    if isinstance(risks_data, str):
        risks = [line.strip() for line in risks_data.splitlines() if line.strip()]
    else:
        risks = risks_data
    for idx in range(1, len(risks) + 1):
        risk = risks[idx-1] if idx-1 < len(risks) else ""
        lines.append(f"- **Risk {idx}:** {risk}")

    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 7: Funders
    lines.append("## 7. Funders")
    raw_funders = data.get("funders", {})
    # Filter out keys that are not valid years (i.e. non-digit keys like "None")
    funders = {k: v for k, v in raw_funders.items() if k.isdigit()}
    if funders:
        for i, year in enumerate(sorted(funders.keys(), key=lambda x: int(x)), start=1):
            funder_list = funders.get(year, [])
            lines.append(f"### 7.{i}. {year}")
            for j, funder in enumerate(funder_list, start=1):
                lines.append(f"#### 7.{i}.{j}. Funder {j}")
                funderName = funder.get("funderName", "")
                amountFunded = funder.get("amountFunded", "")
                lines.append(f"- **funderName:** {funderName}")
                lines.append(f"- **amountFunded:** {amountFunded}")
                lines.append("")
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 8: Outcome Metrics
    lines.append("## 8. Outcome Metrics")
    metrics = data.get("outcomeMetrics", {})
    if metrics:
        for i, year in enumerate(sorted(metrics.keys(), key=lambda x: int(x)), start=1):
            metric_list = metrics.get(year, [])
            lines.append(f"### 8.{i}. {year}")
            for j, metric in enumerate(metric_list, start=1):
                lines.append(f"- **Metric {j}:** {metric}")
            lines.append("")
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    

    # ---------------------------------------------------------------------------
    # Section 9: Organization Type
    lines.append("## 9. Organization Type")
    types = data.get("organizationType", [])
    for idx in range(1, len(types) + 1):
        t = types[idx-1] if idx-1 < len(types) else ""
        lines.append(f"- **Type {idx}:** {t}")
    lines.append("")

    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 10: Demographics
    lines.append("## 10. Demographics")
    demographics = data.get("demographics", [])
    for idx in range(1, len(demographics) + 1):
        d = demographics[idx-1] if idx-1 < len(demographics) else ""
        lines.append(f"- **Demographic {idx}:** {d}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 11: Annual Impact Report
    lines.append("## 11. Annual Impact Report")
    reports = data.get("annualImpactReport", {}).get("reports", [])
    if reports:
        # Group reports by year
        group = {}
        for rep in reports:
            yr = rep.get("year", "")
            group.setdefault(yr, []).append(rep)
        sorted_years = sorted(group.keys(), key=lambda x: int(x) if x.isdigit() else x)
        report_count = 1
        lines.append("### 11.1. Reports")
        for yr in sorted_years:
            for rep in group[yr]:
                lines.append(f"#### 11.1.{report_count}. {yr}")
                fileLink = rep.get("fileLink", "")
                lines.append(f"- **year:** {yr}")
                lines.append(f"- **fileLink:** {fileLink}")
                lines.append("")
                report_count += 1
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 12: Tax Filing Documents
    lines.append("## 12. Tax Filing Documents")
    tax_docs = data.get("taxFilingDocuments", [])
    if tax_docs:
        sorted_docs = sorted(tax_docs, key=lambda x: int(x.get("year", "0")) if x.get("year", "0").isdigit() else x.get("year", ""))
        for i, doc in enumerate(sorted_docs, start=1):
            year_field = doc.get("year", "")
            fileLink = doc.get("fileLink", "")
            lines.append(f"### 12.{i}. {year_field}")
            lines.append(f"- **year:** {year_field}")
            lines.append(f"- **fileLink:** {fileLink}")
            lines.append("")
    else:
        # lines.append("No data available.")
        lines.append("")
    lines.append("---")
    lines.append("")
    

    # ---------------------------------------------------------------------------
    # Section 13: Location Data
    lines.append("## 13. Location Data")
    lines.append("### 13.1. Coordinates")
    latitude = data.get("latitude", "")
    longitude = data.get("longitude", "")
    lines.append(f"- **latitude:** {latitude}")
    lines.append(f"- **longitude:** {longitude}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 14: Logo
    lines.append("## 14. Logo")
    lines.append("### 14.1. Logo Information")
    logo = data.get("logo", "")
    lines.append(f"- **logo:** {logo}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 15: Issue Area
    lines.append("## 15. Issue Area")
    lines.append("### 15.1. Primary Issue")
    issueArea = data.get("issueArea", [])
    issues = ", ".join(issueArea)
    lines.append(f"- **Issue:** {issues}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 16: Website
    lines.append("## 16. Website")
    lines.append("### 16.1. URL")
    website = data.get("website", "")
    lines.append(f"- **website:** {website}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 17: Sub Issue Area
    lines.append("## 17. Sub Issue Area")
    lines.append("### 17.1. Areas")
    sub_issues = data.get("subIssueArea", [])
    for idx, area in enumerate(sub_issues, start=1):
        lines.append(f"- **Sub Issue Area {idx}:** {area}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 18: Story Video Links
    lines.append("## 18. Story Video Links")
    video_links = data.get("storyVideoLinks", [])
    for idx, link in enumerate(video_links, start=1):
        lines.append(f"### 18.{idx}. Video {idx}")
        lines.append(f"- **URL:** {link}")
        lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---------------------------------------------------------------------------
    # Section 19: Score
    lines.append("## 19. Score")
    lines.append("### 19.1. Rating")
    score = data.get("score", "")
    lines.append(f"- **score:** {score}")
    lines.append("")
    
    return "\n".join(lines)

def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    markdown_content = convert_json_to_markdown(data)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Converted {input_file} to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON organization data files to markdown with a fixed schema."
    )
    parser.add_argument("input", help="Input JSON file or directory containing JSON files.")
    parser.add_argument("output", help="Output markdown file or directory.")
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        # When input is a directory, output must be a directory
        if not os.path.isdir(args.output):
            print("When input is a directory, the output must also be a directory.")
            return
        json_files = glob.glob(os.path.join(args.input, "*.json"))
        for json_file in json_files:
            base = os.path.splitext(os.path.basename(json_file))[0]
            output_file = os.path.join(args.output, f"{base}.md")
            process_file(json_file, output_file)
    else:
        # Single file input
        if os.path.isdir(args.output):
            base = os.path.splitext(os.path.basename(args.input))[0]
            output_file = os.path.join(args.output, f"{base}.md")
        else:
            output_file = args.output
        process_file(args.input, output_file)

if __name__ == "__main__":
    main()
