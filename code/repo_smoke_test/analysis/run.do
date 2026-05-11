version 16

* Survey-specific Stata analysis for the smoke-test workflow.
* The Python wrapper passes:
*   1. project root
*   2. survey key
*   3. CSV input path
args project_root survey_key input_csv

if "`project_root'" == "" {
    display as error "Missing project root argument."
    exit 198
}

if "`survey_key'" == "" {
    display as error "Missing survey key argument."
    exit 198
}

if "`input_csv'" == "" {
    display as error "Missing input CSV argument."
    exit 198
}

* Keep all generated files under survey-keyed folders.
local processed_dir "`project_root'/data/`survey_key'/processed"
local metadata_dir "`project_root'/data/`survey_key'/metadata"
local inputs_dir "`project_root'/slides/`survey_key'/inputs"

capture mkdir "`project_root'/data/`survey_key'"
capture mkdir "`processed_dir'"
capture mkdir "`metadata_dir'"
capture mkdir "`project_root'/slides/`survey_key'"
capture mkdir "`inputs_dir'"

capture log close _all
log using "`metadata_dir'/stata-analysis.log", replace text

* Import the Qualtrics CSV export. The smoke-test fixture already uses
* clean snake_case variable names; real surveys can add renaming here.
import delimited using "`input_csv'", clear varnames(1) stringcols(_all)

* Qualtrics CSV exports often include two metadata rows after the header.
* Real response IDs start with R_, so keep only those rows when ResponseId exists.
capture confirm variable responseid
if !_rc {
    keep if substr(responseid, 1, 2) == "R_"
}

drop if missing(role) & missing(workflow_familiarity) & missing(preferred_output) & missing(confidence_running_pipeline)

* Save a clean CSV so the fallback and review workflow can inspect it
* without requiring Stata-specific file formats.
export delimited using "`processed_dir'/clean.csv", replace

* Write a Markdown summary for the Python HTML fallback.
file open summary_md using "`inputs_dir'/summary.md", write replace text
file write summary_md "| Variable | Nonmissing | Unique values |" _n
file write summary_md "| --- | ---: | ---: |" _n

* Write a LaTeX summary for Beamer.
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
}

file write summary_tex "\hline" _n
file write summary_tex "\end{tabular}" _n
file close summary_md
file close summary_tex

* Generate both vector PDF figures for Beamer and PNG fallbacks for HTML.
foreach spec in ///
    "role|Role" ///
    "workflow_familiarity|Workflow familiarity" ///
    "preferred_output|Preferred output" ///
    "confidence_running_pipeline|Pipeline confidence" {

    gettoken var title : spec, parse("|")
    local title = substr("`title'", 2, .)

    capture confirm variable `var'
    if _rc {
        display as text "Skipping missing variable: `var'"
        continue
    }

    graph hbar (count), over(`var', sort(1) descending label(labsize(small))) ///
        blabel(bar, format(%9.0g)) ///
        ytitle("Responses") ///
        title("`title'", size(medsmall)) ///
        graphregion(color(white)) plotregion(color(white)) ///
        bar(1, color("47 111 143"))

    graph export "`inputs_dir'/`var'.pdf", as(pdf) replace
    graph export "`inputs_dir'/`var'.png", as(png) width(1536) replace
}

log close
