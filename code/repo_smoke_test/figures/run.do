* Survey-specific Stata figures for the repository smoke test.

version 16
set more off

args project_root survey_key

if "`project_root'" == "" {
    display as error "Missing project root argument."
    exit 198
}

if "`survey_key'" == "" {
    local survey_key "repo_smoke_test"
}

local project_root = subinstr("`project_root'", "\", "/", .)
local clean_file "`project_root'/data/`survey_key'/processed/clean.dta"
local inputs_dir "`project_root'/slides/`survey_key'/inputs"

capture confirm file "`clean_file'"
if _rc {
    display as error "Cleaned data not found: `clean_file'"
    exit 601
}

use "`clean_file'", clear
capture mkdir "`inputs_dir'"

file open summary_md using "`inputs_dir'/summary.md", write replace text
file write summary_md "| Variable | Nonmissing | Unique values |" _n
file write summary_md "| --- | ---: | ---: |" _n

file open summary_tex using "`inputs_dir'/summary.tex", write replace text
file write summary_tex "\begin{tabular}{lrr}" _n
file write summary_tex "\hline" _n
file write summary_tex "Variable & Nonmissing & Unique values \\" _n
file write summary_tex "\hline" _n

foreach spec in ///
    "role|Role" ///
    "workflow_familiarity|Workflow familiarity" ///
    "preferred_output|Preferred output" ///
    "confidence_running_pipeline|Pipeline confidence" {

    gettoken var label : spec, parse("|")
    local label = substr("`label'", 2, .)

    capture confirm variable `var'
    if _rc {
        file write summary_md "| `label' | missing | missing |" _n
        file write summary_tex "`label' & missing & missing \\" _n
        continue
    }

    quietly count if !missing(`var')
    local nonmissing = r(N)
    quietly levelsof `var' if !missing(`var'), local(levels)
    local unique : word count `levels'

    file write summary_md "| `label' | `nonmissing' | `unique' |" _n
    file write summary_tex "`label' & `nonmissing' & `unique' \\" _n

    graph hbar (count), over(`var', sort(1) descending label(labsize(small))) ///
        blabel(bar, format(%9.0g)) ///
        ytitle("Responses") ///
        title("`label'", size(medsmall)) ///
        graphregion(color(white)) plotregion(color(white)) ///
        bar(1, color("47 111 143"))

    graph export "`inputs_dir'/`var'.pdf", as(pdf) replace
    graph export "`inputs_dir'/`var'.png", as(png) width(1536) replace
}

file write summary_tex "\hline" _n
file write summary_tex "\end{tabular}" _n
file close summary_md
file close summary_tex
