# termitrad
Repository for the TERMITRAD project

## Organization of the repository
- kw\_and\_term\_extraction: Contains the files related to the first Work Package
- traduction: Contains the files related to the second Work Package
- term\_alignment: Contains the files related to the third Work Package

## Good pratices for working with branches
Each work package has a global branch, from which specific branch goes:
- the global branch is: `epic/<task\_name>` (i.e. kw\_and\_term\_extraction, traduction or term\_alignment)
- specific branches are: `feature/<task\_name>/<feature_name>`. These branch are to merge with the related epic branch.
