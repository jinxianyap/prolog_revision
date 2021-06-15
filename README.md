
# Troop
Troop is an automated feedback generation tool for Prolog. Troop transforms Prolog programs into an ASP metarepresentation, then makes use of Theory Revision for Inductive Logic Programming (ILP) to generate revisions for a faulty program.

  
## Setting up Locally
Requirements: Python 3.7, pip v21.1.2, ILASP v4 (install [here](https://github.com/marklaw/ILASP-releases/releases), visit the [official website](http://www.ilasp.com) for more information)
  
Extract project files into chosen directory. Change into that directory.

To install required modules (flask, clingo) using pip, run `pip install -r requirements.txt`. If necessary, run `pip install --upgrade pip` to upgrade to the latest version.
  
## Usage
Troop takes in a model Prolog program and a student Prolog program, and attempts to identify errors in the student program and generate fixes. To run Troop with the interface, run
```python3 troop.py <model program filename> <user program filename>```
then navigate to http://127.0.0.1:5000/ on a web browser.

To run Troop from the command line, run the same command with an additional `-d` flag. The `--timeout` option can be used to set the timeout duration for Troop. The default is 30 seconds.

### Output
Here is a sample command line output:
```
---------------------------------------
RESULTS:

Original Student Program:
r1 - pet(X) :- animal(X), tame(X).
r2 - animal(snake).
r3 - animal(dog).
r4 - animal(tiger).
r5 - animal(bird).
r6 - mammal(dog).
r7 - mammal(tiger).
r8 - tame(dog).
r9 - tame(bird).

Similarity Score:			0.886

Erroneous Rule(s):			r1

Facts not derived:			None

Incorrect facts derived:	r1: pet(bird)

Revisions:					Rule: r1, Index: 2 - Replace with 'mammal(X)'.
							Rule: r1, Index: 3 - Extend with 'tame(X)'.

Revision Success:			True
```
Each rule in the student program is assigned a rule identifier. *Similarity Score* indicates how far the student's attempt differs from the given model program, in terms of syntactic and semantic differences and the number of revisions required. *Erroneous Rule(s)* refers to rule identifiers associated with rules that contain errors and should be amended. *Facts not derived* refers to those facts that are derivable from the model program, but not from the student program. *Incorrect facts derived* refers to those facts that are derivable from the student program, but not from the model program. *Revisions* indicate the necessary steps to amend the student program, giving the exact locations and corrections. *Revision Success* indicates whether or not the amended version of the student program, after applying the revisions generated, actually fulfils the specification defined by the model program. The HTML interface presents similar information, with erroneous rules in the original student program highlighted in red.

A collection of pairs of sample input programs have been included in the `sample_programs/` directory. For example, if a model program is named `add_body_1.lp`, then the corresponding student program is named `add_body_1_user.lp`.


## Evaluation Guide
The software archive also contains the evaluation script used to generate random programs for a specific programming objective. The evaluation module takes in as input a model program, defining the programming objective/task, and a specification file, which is used to generate randomised programs. The specification file contains information about the 'domain' of the programming task, specifically:
1. Background knowledge (this will be the same as that of the model program)
2. The 'objective' predicate of the programming task
3. Maximum number of rules
4. Maximum length of a rule body
5. Maximum number of variables (within a rule)
6. Predicate symbols and their arities

```
# Sample Specification File
BG:
animal(cat).
animal(dog).
animal(fish).
mammal(cat).
mammal(dog).

# OBJ: pet

# MAX_RULES: 2

# MAX_BODY_LENGTH:2

# MAX_VARIABLES:1

# PREDICATES:
pet: 1
animal: 1
mammal: 1
creature: 1
```

By running
```python3 evaluation.py <model filename> <specification filename>```
up to 100 random programs are generated, and the feedback generation process is executed for each random program against the model program. The random programs are stored in the `random_programs/` directory, and the evaluation results are recorded in `eval_data.csv`. There are some sample specification files given in the `spec_files/` directory, and each can be used with a model program from the `sample_programs/` directory, given that they share the same domain and background knowledge.

For any queries, please direct them to jin.yap18@imperial.ac.uk.