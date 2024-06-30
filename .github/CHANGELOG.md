## v0.1.0
### October 2, 2023
One of the development stages.</br>
<i>A full list of changes will be recorded after the alpha version of the project is implemented.</i>


## v0.2.0-alpha - prerelease 
### November 15, 2023
At this stage, the front-end component is being finalized.</br>
This release represents testing of the functional component of the product before introducing a full alpha version.


## v0.2.1-alpha (unstable)
### January 29, 2024

- Added the ability to change languages in the telegram chatbot.
- Time is now taken into account in UTC+0.
- Fixed SQL queries.
- Improved validators.
- Changed the visual part of some pages of the site.
- Setup testing via GitHub Actions.
- Bugs fixed.

## v0.3.0-alpha (stable)
### ETC

#### Global changes:
 - Database moved to PostgreSQL
 - Build the application via Docker Compose
 - Logs are now anonymized
 - Code coverage by tests has increased significantly
 - The number of GitHub Actions events for assembly testing has increased (pylint, codeQL, GitMerge, flake8, BuildTest)
 - Reduced the number of external code dependencies
 - Added caching of the user's language and his registration status. Functions execution time has decreased by 100 times:
 ```
   Before:
          Number of queries to the database: 4
          user_is_registered: 0.15s
          check_user_language: 0.19s
    Now:
          Number of queries to the database: 2
          user_is_registered: 0.115s
          check_user_language: 0.002s
 ```
#### Functional changes:
 - Added localization into 6 languages (English, Spanish, Russian, German, French, Icelandic)
 - Added the ability to download all data in .csv format
 - Fixed errors in counting funds when deleting old entries in the table
 - Queries are optimized by adding the necessary PostgreSQL indexes

#### Plans before release:
  - Increase the number of languages supported
  - Logs should be stored in separate storages
  - Add PGAdmin4 for remote database control
  - Possibility of restoring a group after deletion within six months
  - Caching tables in different upload formats
  - Add upload in .xlsx format
  - Ability to download tables in .rar and .zip archives
  - Add tests for interacting with the database
  - Expand test coverage for generating .csv files