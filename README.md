# Farm Projection

Farm and dairy financial and product projections and planning software.

(C) 2024 by Tecla, all rights reserved.

## Usage and Requirements

### Requires python 3.x

Download python from here if it's not installed on your system:

https://www.python.org/downloads/

### Running

#### Linux and similar

`python bin/RunProjection.py [<scenario1>] [<scenario2>] ... [--datadir <directory>] [--reportdir <directory>] [--set <input> <value>]...`

#### Windows

Run the `RunProjection.bat` batch file, and modify it to suit your situation. It has instructions inside the file so you can edit it with a text editor such as notepad.

You may also run without the batch file:

`python bin\RunProjection.py [<scenario1>] [<scenario2>] ... [--datadir <directory>] [--reportdir <directory>] [--set <input> <value>]...`

### Special arguments

A special scenario named `all` can be specified, which will run all of the scenarios it can find in the `<datadir>/scenarios` subdirectory automatically and generate reports for each.

You can override one or more input values with `--set <input path> <value>` and use that argument any number of times. For example, to override the "years running" value to be past the amortization years and see the projection out past when any fixed cost loans are paid off, you might add the following command-line option:

`--set "farm/years running" 11`

### Results

Reports will be generated in the `<datadir>/reports` subdirectory unless the `--reportdir` argument is given. See the ***Reports*** section for more information on what the reports contain.

## Scenarios

Inside the data directory are some example scenarios for various sized dairy operations. These examples are based around a smaller homestead scaling up to a larger dairy, albeit the large dairy is quite small compared to typical operations targeting the USDA PMO. The data directory tree has this structure:

* `common`
  * JSON files with inputs describing parts of the operation common to all scenarios.
* `scenarios`
  * `scenarioName1`
    * JSON files with inputs particular to this scenario
  * `scenarioName2`
    * ...
  * ...

Each scenario combined with the common inputs describes multiple parts of the farm operation. Each JSON file is named according to that part of the farm. Currently supported are:

* `creamery.json`
  * Supports sales of butter, cheese, cream, buttermilk, ice cream, and yogurt
* `farm.json`
  * Loan rates and costs for facilities and major fixed expenses
* `livestock.json`
  * Supports offspring sales (but not meat sales yet)
* `milk.json`
  * Supports standard bottled milk sales for dairy
* `store.json`
  * Supports sales of third part items in addition to all sales above
* `structures.json`
  * Supports barn, dairy (stands, milkhouse), creamery (make facility and aging), storefront and farm truck
* `taxes.json`
  * USA-based tax rates and tables

More will be added in the future. The current complete set of operational inputs are contained in the example scenarios, so to create your own you should copy an existing scenario and modify it to suit your own projections. Note that you do not have to provide every input in your scenario, it will fall back to a default (zero, empty) input if you omit one. Also note that an input can be provided in a JSON file common to all your scenarios, or it can be provided in each individual scenario, it doesn't matter which you choose. But currently you cannot provide an input in both locations without generating an error.

Scenarios support adding multiple kinds of livestock. If one is added but zero animals are set for the input, the projection will flow through without them without issue.

You are encouraged to copy the data directory and customize the inputs to your needs, and then you can run with the `--datadir` command-line option to analyze your own scenarios.

## What It Doesn't Do

There are numerous areas missing from the projections at this point; this is, for a first pass, quite dairy-centric (and a raw-milk dairy at that). Various aspects not taken into account yet:

* *(planned)* Kill, butchery, and meat shop costs and income
* *(planned)* Culinary water / well cost
* *(planned)* Irrigation water cost
* *(planned)* Fuel and transportation cost
* *(planned)* Grain and garden operational costs and income
* Land cost
* Home and other personal costs (e.g. this is not for personal budgeting!)

There are bound to be more. We may add computational workflows and make available inputs for these types of costs in future development.

## Reports

The results of the projection are output to JSON and HTML files in the report directory (see the `--reportdir` command line option). One pair of JSON and HTML files are written for each projected scenario.

Reports currently generate information on potential product output (livestock sold, milk sold, cheese sold, etc), various production metrics and requirements, estimated employee pay and hours, and of course an estimate of the final bottom line that is left for the farm owner.

## Caveats

**Please keep in mind that the projections are only estimates, and real-world situations and financial numbers could vary significantly from these projections.** This is only an exploration tool to get a feel for what is possible and to narrow down your planning.

### The Usual Disclaimer

Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Contributing

Contributions, issues, etc to the project are welcome. You may be asked to assign copyright to Tecla if you contribute code or documentation or other resources. The only rule is that the project owner makes the rules, and there is no appeal from his decisions. Be humble, AKA don't be a dick, and all will go well for everyone.
