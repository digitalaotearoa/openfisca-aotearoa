Thank you for wanting to contribute to OpenFisca Aotearoa! :smiley:

TL;DR: [GitHub Flow](https://guides.github.com/introduction/flow/), [SemVer](http://semver.org/).

## Contents:
 - [Pull Requests](#pullrequests)
 - [Advertising changes](#advertisingchanges)
 - [Coding guide: naming, structure and patterns](#codingguide)
   -  [Naming Variables](#namingvariables)
   -  [Coding Variables](#codingvariables)
   -  [Structure](#structure)
   -  [Patterns](#patterns)

$~$
<a name="pullrequests"></a>

# Pull requests

We follow the [GitHub Flow](https://guides.github.com/introduction/flow/): all code contributions are submitted via a pull request towards the `master` branch.

Opening a Pull Request means you want that code to be merged. If you want to only discuss it, send a link to your branch along with your questions through whichever communication channel you prefer.

## Peer reviews

All pull requests must be reviewed by someone else than their original author.

> In case of a lack of available reviewers, one may review oneself, but only after at least 24 hours have passed without working on the code to review.

To help reviewers, make sure to add to your PR a **clear text explanation** of your changes.

In case of breaking changes, you **must** give details about what features were deprecated.

> You must also provide guidelines to help users adapt their code to be compatible with the new version of the package.

$~$
<a name="advertisingchanges"></a>

# Advertising changes

## Version number

We follow the [semantic versioning](http://semver.org/) spec: any change impacts the version number, and the version number conveys API compatibility information **only**.

Examples:

### Patch bump

- Fixing or improving an already existing calculation.

### Minor bump

- Adding a variable to the tax and benefit system.

### Major bump

- Renaming or removing a variable from the tax and benefit system.

$~$

## Changelog

OpenFisca-Aotearoa changes must be understood by users who don't necessarily work on the code. The Changelog must therefore be as explicit as possible.

Each change must be documented with the following elements:

- On the first line appears as a title the version number, as well as a link towards the Pull Request introducing the change. The title level must match the incrementation level of the version.


> For instance :
> # 13.0.0 - [#671](https://github.com/digitalaotearoa/openfisca-aotearoa/pull/671)
>
> ## 13.2.0 - [#676](https://github.com/digitalaotearoa/openfisca-aotearoa/pull/676)
>
> ### 13.1.5 - [#684](https://github.com/digitalaotearoa/openfisca-aotearoa/pull/684)

- The second line indicates the type of the change. The possible types are:
 - `Tax and benefit system evolution`: Calculation improvement, fix, or update. Impacts the users interested in calculations.
 - `Technical improvement`: Performances improvement, installing process change, formula syntax change… Impacts the users who write legislation and/or deploy their own instance.
 - `Crash fix`: Impact all reusers.
 - `Minor change`: Refactoring, metadata… Has no impact on users.

- In the case of a `Tax and benefit system evolution`, the following elements must then be specified:
  - The periods impacted by the change. To avoid any ambiguity, the start day and/or the end day of the impacted periods must be precised. For instance, `from 01/01/2017` is correct, but `from 2017` is not, as it is ambiguous: it is not clear wheter 2017 is included or not in the impacted period.
  - The tax and benefit system areas impacted by the change. These areas are described by the relative paths to the modified files, without the `.py` extension.

> For instance :
> - Impacted periods: Until 31/12/2015.
> - Impacted areas: `benefits/healthcare/universal_coverage`

- Finally, for all cases except `Minor Change`, the changes must be explicited by details given from a user perspective: in which case was an error or a problem was noticed ? What is the new available feature ? Which new behaviour is adopted.

> For instance:
>
> * Details :
>   - These variables now return a yearly amount (instead of monthly):
>     - `middle_school_scholarship`
>     - `high_school_scholarship`
>   - _The previous monthly amounts were just yearly amounts artificially divided by 12_
>
> or :
>
> * Details :
>  - Use OpenFisca-Core `12.0.0`
>  - Change the syntax used to declare parameters:
>      - Remove "fuzzy" attribute
>      - Remove "end" attribute
>      - All parameters are assumed to be valid until and end date is explicitely specified with an `<END>` tag

When a Pull Request contains several disctincts changes, several paragraphs may be added to the Changelog. To be properly formatted in Markdown, these paragraphs must be separated by `<!-- -->`.

$~$
<a name="codingguide"></a>

# Coding guide: naming, structure and patterns
$~$
<a name="namingvariables"></a>

## Naming variables

$~$

> There are only two hard things in Computer Science: cache invalidation and naming things.
>
>  -Phil Karlton

$~$

To determine a name for a variable utilise the following strategy.
 1) determine if the variable represents a global input beyond the scope of the body of legislation you're coding. Age is an excellent example of this, others are more unclear. If the concept is declared in the definitions/interpretation section of the Act then don't utilise a global input
 2) If you determine it is a global input - add it to the `/variables/demographics` section in the most appropriate file with an explanatory name (also check it doesn't already exist).
 3) If you determine it's not a global input then you'll want to name it in the format `prefix__variable_name`. Note the two underscores seperating the prefix from the variable name. The variable name should be suitably explanatory to determine the concept it represents. The prefix should utilise one of the of the prefixes defined in `openfisca_aotearoa/structure.json`. If a suitable prefix doesn't exist add it to the `structure.json` file before utilising it.

### Things to avoid

Avoid using words like `has` and `is`. I.e. the bool `has_dependent_child` is more aptly named `dependent_child`.

<a name="codingvariables"></a>

## Coding variables

$~$

The goal of the approach outlined is to aid future people studying the variable you're coding in matching it to how you interpreted the natural language rules.


Take a look at the `/variables/acts/social_security/residency.py` and considered it a __"best practice"__ approach.

The variable `social_security__residential_requirement` in this file that we will be referring to is supporting both the 1964 and the 2018 Social Security Acts.
It's declaration looks like this:

```
class social_security__residential_requirement(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Residential requirements for certain benefits, calculates for the 1964 and the 2018 Social Security Acts"
    definition_period = periods.MONTH
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"
```
- Note the two references (2018 and 1964). They link to the specific section of the act on legislation.govt.nz
- Note the descriptive label
- Note the naming convention as described in [Naming Variables](#namingvariables)

The variable has two formulas:
```
    def formula_1964_12_04(persons, period, parameters):
```
```
    def formula_2018_11_26(persons, period, parameters):
```
This is an OpenFisca feature that ensures the correct formula will be automatically applied depending on the date supplied with the scenario.

What is unique to this project is how we intend to code the content of these formulas.

_At the time of writing variables within this project ARE NOT coded this way save for the example we will refer to below._

This approach is designed to aid the person coding the interpretation and more especially those coming after them (or their future selves) who need to review it, update it or add to it. We will just be looking at the 2018 formula.

The first thing to recognise is it references the `section 16` of the Social Security Act. Section 16 in the natural language is ordered into 5 parts with parts 2 and 5 further seperated into sub parts.

We choose to structure the code accordingly. This looks like this:

```
# ssa16_1 - Descriptive, not requiring coding.

ssa16_2_a = persons("immigration__citizen_or_resident", period) * \
    persons("social_security__ordinarily_resident_in_new_zealand", period)

ssa16_2_a_i = persons("social_security__resided_continuously_nz_2_years_citizen_or_resident", periods.ETERNITY)

ssa16_2_a_ii = persons("immigration__recognised_refugee", period) + \
    persons("immigration__protected_person", period)

ssa16_2_b = persons("social_security__ordinarily_resident_in_country_with_reciprocity_agreement", period) * (persons("years_resided_continuously_in_new_zealand", period) >= 2)

# ssa16_3 - TODO Useful would be a list of countrys this applies to... we could make country an input.
# ssa16_4 - MSD can refuse or cancel benefit if person not ordinarily in NZ...
# ssa16_5 - The Governer-General may by Order in Council make regulations for the purposes of section 16 that specify circumstances in which:...
#           Note the content of the list in this section is identical to the list in 421_1_c

return (ssa16_2_a * (ssa16_2_a_i + ssa16_2_a_ii)) + ssa16_2_b

```
 - Firstly create local variables based on the structure that enable a person reading it to understand the reference - see `ssa16_1`
 - Comment out the ones not coded and supply a comment as to why.
 - List **ALL** the possible local variables as just described as it helps future people to understand how what's interpreted and how.
 - Order them on the page in the same order as the natural language text
 - Introduce the OpenFisca variables that make up the concepts strictly within the sections as they appear.
 - Finally handle the `and` and `or` and other language of the natural language text to return the final computation utilising those local variables.


$~$
<a name="structure"></a>

## Structure

In order to facilitate understanding, navigation and future management of the openfisca-aotearoa code base, we're utilising the above naming convention which is supported by the added `structure.json` file (unique to the openfisca_aotearoa project).

This allows us to map the extent and reach of the project. The `structure.json` file allows us to create a tree like map of the project utilising the `prefix` approach as described in the previous section.

### structure.json

An array of entries, one for each prefix utilised in the code base. In the format as follows:
```
{
    "Title": "Accident Compensation Act 2001",
    "Prefix": "acc",
    "Type": "Act",
    "Reference": "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM99494.html",
    "Children": [
        "acc_sched_1",
        "acc_part_2",
        "acc_part_4"
    ]
}
```
Title, Prefix, Type and Reference are all required.
 - Title: The legal title of the legal artifact
 - Prefix: The prefix utilised within the openfisca_aotearoa code base
 - Type: One of the following: `Act`, `Schedule`, `Part`, `Section`, `Regulation`, `Policy`
 - Reference: A url or otherwise description of the source material.
 - Children is optional, an array and maps to other prefixes in the array.


### Folder structure

The folder names refer to the prefix's created in the `structure.json` file.

Variables relating to acts as follows:
 - `openfisca_aotearoa/variables/acts/{act prefix}/`
 - `openfisca_aotearoa/variables/acts/{act prefix}/{section prefix}/`

Variables relating to regulations as follows:
 - `openfisca_aotearoa/variables/regulation/{reg prefix}/`
 - `openfisca_aotearoa/variables/regulation/{reg prefix}/{section prefix}/`

Parameters as follows:
 - `openfisca_aotearoa/parameters/{prefix}/`
 - `openfisca_aotearoa/parameters/{prefix}/{section prefix}/`

Tests as follows:
 - `openfisca_aotearoa/tests/{prefix}/`

Other legal instruments that don't fit the above:
 - `openfisca_aotearoa/variables/other/`

$~$
<a name="patterns"></a>

## Patterns

The best approach when interpreting natural language law in code is to mimic the structure of the natural language text as closely as possible.

This project currently utilises one specific pattern however for benefit calculations. The following is an example based on the `Social Security Act 2018` > `Job Seeker Support` benefit.

- `jobseeker_support__entitled` (true/false) - or - `jobseeker_support__eligible` (true/false)
- `jobseeker_support__base` (float)
- `jobseeker_support__cutoff` (float)
- `jobseeker_support__reduction` (float)
- `jobseeker_support__benefit` (float)

i.e. the formula for `jobseeker_support__benefit` would be:
 ```
 jobseeker_support__entitled * min(jobseeker_support__base - jobseeker_support__reduction, jobseeker_support__cutoff)
 ```


