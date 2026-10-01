#### Variables:

respondent_id:
    2023: `IOBS`
    2025: `ZID_AUTO`

wave:
    2023: derived = `2023`
    2025: derived = `2025`

post_ots:
    2023: derived = `0`
    2025: derived = `1`

survey_weight:
    2023: `WT1`
    2025: `WT3`

survey_method:
    2023: `P_METHOD_TYPE`
    2025: `P_METHOD_TYPE`

switched_landline_12m:
    2023: `QLLSUMA`
    2025: `QLLSUMA`

switched_broadband_12m:
    2023: `QBBSUMA`
    2025: `QBBSUMA`

switched_mobile_12m:
    2023: `QMPSUMA`
    2025: `QMPSUMA`

switched_paytv_12m:
    2023: `QPTVSUMA`
    2025: `QPTVSUMA`

age_group:
    2023: `S4`
    2025: `S4`

gender:
    2023: `S5`
    2025: `S5`

seg:
    2023: `QS6A` to `QS6D`
    2025: `QS6A` to `QS6D`

employment_status:
    2023: `QS7A` to `QS7G`
    2025: `QS7A` to `QS7G`

region:
    2023: `OS1B`
    2025: `OS1B`

income_band:
    2023: `C6`
    2025: `C6`

disability_flag:
    2023: `C1A` to `C1L`
    2025: `C1A` to `C1M` / `C1N`

---

#### Derived variable coding:

`wave`:
    2023 = `2023`
    2025 = `2025`

`post_ots`:
    2023 = `0`
    2025 = `1`

`age_group`:
    `S4` 1-2 = `16-34`
    `S4` 3-4 = `35-54`
    `S4` 5-7 = `55+`
    `S4` 8 = missing

`seg`:
    `QS6A` = `AB`
    `QS6B` = `C1`
    `QS6C` = `C2`
    `QS6D` = `DE`

`employment_status`:
    `QS7A` = `Full-time employed`
    `QS7B` = `Part-time employed`
    `QS7C` = `Unemployed`
    `QS7D` = `Student`
    `QS7E` = `Full-time responsibility for home/family`
    `QS7F` = `Retired`
    `QS7G` = `Other`
    `QS7H` = missing / prefer not to say
    `QS7I` = do not use; derived total employed indicator

`income_band`:
    1 = `Up to £10,399`
    2 = `£10,400-£15,599`
    3 = `£15,600-£25,999`
    4 = `£26,000-£36,399`
    5 = `£36,400-£51,999`
    6 = `£52,000-£77,999`
    7 = `£78,000+`
    8 = `Don't know`
    9 = `Prefer not to say`

`disability_flag`:
    1 = at least one reported impacting/limiting condition
    0 = no impacting/limiting condition
    missing = don't know / prefer not to say / indeterminate

`survey_method`:
    retain original `P_METHOD_TYPE` coding for diagnostics;
    do not include in the primary model initially.