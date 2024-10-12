# Farm Projection

Farm and dairy financial and product projections and planning

## Usage

**Requires python 3.x**

`python bin/RunProjection.py <scenario> [--datadir <dir>] [--report <report-path>] [--report_json] [--report_html]`

Example:

`python bin/RunProjection.py LargeDairy --report /tmp/report_largedairy --report_json --report_html`

You are encouraged to copy the data directory and customize the inputs to your needs, and then you can run with the `--datadir <path/to/data>` option for your own scenarios.

## Scenarios

Inside the data directory are some example scenarios for various sized dairy operations. These examples are based around a smaller homestead scaling up to a larger dairy, albeit the large dairy is quite small compared to typical operations targeting the USDA PMO. The data directory tree has this structure:

* common
  * JSON files with inputs describing parts of the operation common to all scenarios.
* scenarios
  * `scenarioName1`
    * JSON files with inputs particular to this scenario
  * `scenarioName2`
    * ...
  * ...

Each scenario combined with the common inputs describes multiple parts of the farm operation. Each JSON file is named according to that part of the farm. Currently supported are:

* farm
* structures
* livestock
* milk
* creamery
* store

More will be added in the future. The complete set of operational inputs are contained in the example scenarios, so to create your own you should copy an existing scenario and modify it to suit your own projections.

Scenarios support adding multiple kinds of livestock. If one is added but zero animals are set for the input, the projection will flow through without them without issue.

## What It Doesn't Do

There are numerous areas missing from the projections at this point; this is, for a first pass, quite dairy-centric (and a raw-milk dairy at that). Various things not taken into account yet:

* Land cost
* Culinary water / well cost
* Irrigation water cost
* Permanent fencing cost
* Fuel and transportation cost
* Kill, butchery, and meat shop costs and income
* Grain and garden operational costs and income
* Tractor and other external machinery costs
* Home and other personal costs (e.g. this is not for personal budgeting!)

There are bound to be more. We will add computational workflows and make available inputs for these types of costs in future development.

## Reports

Running the projection is most useful when reports are enabled. The results of the projection can be output to JSON format, HTML or both. The report files are written and automatically add the .json or .html file extension.

Reports currently generate information on potential product output (livestock sold, milk sold, cheese sold, etc), employee pay and hours, and of course an estimate of the final bottom line that is left for the farm owner. **Please keep in mind that this is only an estimate, and real-world situations and financial numbers could vary significantly from these projections.** This is only an exploration tool to get a feel for what is possible and to narrow down your planning.

## Contributing

Contributions, issues, etc are welcome. The only rule is that the project owner makes the rules, and there is no appeal from his decisions. Be humble, AKA don't be a dick, and all will go well for everyone.
