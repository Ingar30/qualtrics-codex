* Shared Stata pipeline for lab-style survey folders.
* Called by scripts/run_analysis.py with:
*   1 project root
*   2 survey key
*   3 input CSV or SAV file

version 16
set more off

args project_root survey_key input_file

if "`project_root'" == "" {
    display as error "Missing project root argument."
    exit 198
}

if "`survey_key'" == "" {
    display as error "Missing survey key argument."
    exit 198
}

if "`input_file'" == "" {
    display as error "Missing input file argument."
    exit 198
}

local project_root = subinstr("`project_root'", "\", "/", .)
local input_file = subinstr("`input_file'", "\", "/", .)

local cleaning_do "`project_root'/code/`survey_key'/cleaning/run.do"
local figures_do "`project_root'/code/`survey_key'/figures/run.do"

capture confirm file "`cleaning_do'"
if _rc {
    display as error "Project cleaning script not found: `cleaning_do'"
    exit 601
}

capture confirm file "`figures_do'"
if _rc {
    display as error "Project figure script not found: `figures_do'"
    exit 601
}

do "`cleaning_do'" "`project_root'" "`survey_key'" "`input_file'"
do "`figures_do'" "`project_root'" "`survey_key'"
