* Survey-specific Stata cleaning for the repository smoke test.
* Supports either a Qualtrics CSV export or a Qualtrics SPSS .sav export.

version 16
set more off

args project_root survey_key input_file

if "`project_root'" == "" {
    display as error "Missing project root argument."
    exit 198
}

if "`survey_key'" == "" {
    local survey_key "repo_smoke_test"
}

if "`input_file'" == "" {
    display as error "Missing input CSV or SAV file argument."
    exit 198
}

local project_root = subinstr("`project_root'", "\", "/", .)
local input_file = subinstr("`input_file'", "\", "/", .)
local processed_dir "`project_root'/data/`survey_key'/processed"
local metadata_dir "`project_root'/data/`survey_key'/metadata"
local inputs_dir "`project_root'/slides/`survey_key'/inputs"

capture mkdir "`project_root'/data"
capture mkdir "`project_root'/data/`survey_key'"
capture mkdir "`processed_dir'"
capture mkdir "`metadata_dir'"
capture mkdir "`project_root'/slides"
capture mkdir "`project_root'/slides/`survey_key'"
capture mkdir "`inputs_dir'"

local lower_input = lower("`input_file'")
if substr("`lower_input'", -4, 4) == ".sav" {
    import spss using "`input_file'", clear case(lower)
}
else {
    import delimited using "`input_file'", clear varnames(1) stringcols(_all)
    rename *, lower
}

* Qualtrics CSV exports often include metadata rows after the header.
capture confirm variable responseid
if !_rc {
    keep if substr(responseid, 1, 2) == "R_"
}

drop if missing(role) & missing(workflow_familiarity) & missing(preferred_output) & missing(confidence_running_pipeline)

compress
save "`processed_dir'/clean.dta", replace
export delimited using "`processed_dir'/clean.csv", replace

local cleaned_rows = _N
local cleaned_vars = c(k)

file open report using "`inputs_dir'/cleaning_report.tex", write replace text
file write report "\begin{tabular}{lr}" _n
file write report "\hline" _n
file write report "Item & Value \\" _n
file write report "\hline" _n
file write report "Cleaned rows & `cleaned_rows' \\" _n
file write report "Variables & `cleaned_vars' \\" _n
file write report "\hline" _n
file write report "\end{tabular}" _n
file close report
