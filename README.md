# dbmanager
Incomplete and (probably) unstable ORM to work with sqlite3

documentation will be complete someday, and if that happens it will be on:

**https://denysdt.xyz/dbmanager/docs**

## IMPORTANT
please for gods sake don't use it in any place where dropping database would ruine your life, sqlite3 doesn't
have any built in protection from SQL injection and until I add it myself it's not safe to use in projects where
database is shared between users and developer

_(local programs should be more than just fine tho)_
