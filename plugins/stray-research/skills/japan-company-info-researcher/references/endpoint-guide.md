# gBizINFO Endpoint Guide

Map the user's question to the right gBizINFO data group before calling tools. Tool names follow the `hojin_get_*` and `hojin_update_info_*` patterns; verify the exact names from the configured `gbizinfo-mcp` tool list at runtime instead of assuming them.

## Data Group Map

| Data group | Answers questions about | Typical tool family |
|---|---|---|
| Search | Finding a company and its corporate number from a name, location, industry, or keyword | company search (`hojin` search) |
| Basic | Registered name, corporate number, address, status, representative | `hojin_get_*` basic info |
| Certification (認定・届出) | Government certifications and filings such as 経営革新, 健康経営 | `hojin_get_*` certification |
| Commendation (表彰) | Awards and commendations from ministries and agencies | `hojin_get_*` commendation/award |
| Finance (財務) | Published financial figures for companies that disclose them | `hojin_get_*` finance |
| Patent (特許) | Patents and applications attributed to the company in gBizINFO | `hojin_get_*` patent |
| Procurement (調達) | Government procurement contract awards | `hojin_get_*` procurement |
| Subsidy (補助金) | Subsidies granted to the company | `hojin_get_*` subsidy |
| Workplace (職場情報) | Workplace data such as employees, average age, diversity metrics | `hojin_get_*` workplace |
| Update info (更新情報) | Which records changed within a period | `hojin_update_info_*` |

## Usage Notes

- Always resolve the corporate number first (via search or user input) before detail retrieval; detail endpoints key off the corporate number.
- Retrieve only the data groups the question needs; do not sweep every endpoint per company.
- gBizINFO aggregates data from other government systems; coverage varies by company and data group. An empty result means "not present in gBizINFO," not "the activity never happened."
- Patent data here is a company-keyed convenience view; for real patent research use `global-patent-researcher`.
