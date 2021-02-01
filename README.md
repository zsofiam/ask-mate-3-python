# AskMate (sprint 2)

## Story

Last week you created a pretty good site from scratch. It already has some features but it's a bit difficult to maintain due to the fact that we store data in csv files and we also need some more features to make it more usable and more appealing to users.

The management decided to move further as users requested new features like ability to comment on answers and tag questions (and here is the issue with csv files as well). There are several other feature requests which you can find in the user stories.

As last week the management is handing out a **prioritized list** of new user stories that you should add to the unfinished stories from last week on your product backlog. Try to estimate these new stories as well and based on the estimations decide how many your team can finish until the demo. As the order is important, you should choose from the beginning of the list as much as you can.

## What are you going to learn?

- how to use `psycopg2` to connect to a PostgreSQL database from Python,
- SQL basic commands (`SELECT`, `UPDATE`, `DELETE`, `INSERT`)
- CSS basics
- how to work according to the Scrum framework,
- how to create a _sprint plan_.

## Tasks

1. As you will work in a new repository but you need the code from the previous sprint, add the `ask-mate-2` repository as a new remote to the previous sprint's repository, then pull (merge) and push your changes into it.
    - There is a merge commit in the project's repository that contains code from the previous sprint

2. Make the application use a database instead of CSV files.
    - The application uses a PostgreSQL database instead of CSV files
    - The application respects the `PSQL_USER_NAME`, `PSQL_PASSWORD`, `PSQL_HOST` and `PSQL_DB_NAME` environment variables
    - The database structure (tables) is the same as in the provided SQL file (`sample_data/askmatepart2-sample-data.sql`)

3. Allow the user to add comments to a question.
    - There is a `/question/<question_id>/new-comment` page
    - The page is linked from the question's page
    - There is a form with `message` field, and issues `POST` requests
    - After submitting, you are redirected back to the question detail page, and the new comment appears together with submission time

4. Allow the user to add comments to an answer.
    - There is a `/answer/<answer_id>/new-comment` page
    - The page is linked from the question's page, next to or below the answer
    - There is a form with `message` field, and issues `POST` requests
    - After submitting, you are redirected back to the question detail page, and the new comment appears together with submission time

5. Implement searching in questions and answers. (Hint: [Passing data from browser](https://learn.code.cool/web-python/#/../pages/web/passing-data-from-browser))

    - There is a search box and "Search" button on the main page
    - When you write something and press the button, you see a results list of questions (same data as in the list page)
    - The results list contains questions for which the title or description contain the searched phrase
    - The results list also contains questions which have answers for which the message contains the searched phrase
    - The results list has the following URL: `/search?q=<search phrase>`

6. Allow the user to edit the posted answers.
    - There is a `/answer/<answer_id>/edit` page
    - The page is linked from the answer's page
    - There is a form with a `message` field, and issues a `POST` request
    - The field is pre-filled with existing answer's data
    - After submitting, you are redirected back to the question detail page, and the answer is updated

7. Allow the user to edit comments.
    - The page URL is `/comment/<comment_id>/edit`
    - There is a link to the edit page next to each comment
    - The page contains a `POST` form with a `message` field
    - The field pre-filled with current comment message
    - After submitting, you are redirected back to question detail page, and the new comment appears
    - The submission time is updated
    - There is a message that says "Edited `<number_of_editions>` times." next to or below the comment

8. Allow the user to delete comments.
    - There is a recycle bin icon next to the comment
    - Clicking the icon asks the user to confirm the deletion
    - The deletion itself is implemented by the `/comments/<comment_id>/delete` endpoint (which does not ask for confirmation anymore)
    - After deleting, you are redirected back to question detail page, and the comment is not showed anymore

9. Display latest 5 questions on the main page (`/`).
    - The main page (`/`) displays the latest 5 submitted questions
    - The main page contains a link to all of the questions (`/list`)

10. Implement sorting for the question list. [If you did this user story in the previous sprint, now you only have to rewrite it to use SQL]


### Database and sample data

To init the database use the `sample_data/askmatepart2-sample-data.sql` file in your repository.

## Background materials

### Git

- <i class="far fa-exclamation"></i> [Working with the `git remote` command](https://git-scm.com/docs/git-remote)
- <i class="far fa-book-open"></i> [Merge vs rebase](project/curriculum/materials/pages/git/merge-vs-rebase.md)
- <i class="far fa-book-open"></i> [Mastering git](project/curriculum/materials/pages/git/mastering-git.md)

### SQL

- <i class="far fa-exclamation"></i> [Installing and setting up PostgreSQL](project/curriculum/materials/pages/tools/installing-postgresql.md)
- <i class="far fa-exclamation"></i> [Installing psycopg2](project/curriculum/materials/pages/tools/installing-psycopg2.md)
- <i class="far fa-exclamation"></i> [Best practices for Python/Psycopg/Postgres](project/curriculum/materials/pages/python/tips-python-psycopg-postgres.md)
- [Setting up a database connection in PyCharm](project/curriculum/materials/pages/tools/pycharm-database.md)
- [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page on Queries](https://www.postgresql.org/docs/current/queries.html)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page Data Manipulation](https://www.postgresql.org/docs/current/dml.html)

### Agile/SCRUM

- [Agile project management](project/curriculum/materials/pages/methodology/agile-project-management.md)
- <i class="far fa-book-open"></i> [Planning poker](https://en.wikipedia.org/wiki/Planning_poker)

### Web basics (Flask/Jinja/HTML/CSS)

- <i class="far fa-exclamation"></i> [Flask/Jinja Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- <i class="far fa-exclamation"></i> [Passing data from browser](project/curriculum/materials/pages/web/passing-data-from-browser.md)
- [Collection of web resources](project/curriculum/materials/pages/web/resources.md)
- <i class="far fa-book-open"></i> [Pip and VirtualEnv](project/curriculum/materials/pages/python/pip-and-virtualenv.md)
- <i class="far fa-book-open"></i> [A web-framework for Python: Flask](project/curriculum/materials/pages/python/python-flask.md)
- <i class="far fa-book-open"></i> [Flask documentation](http://flask.palletsprojects.com/) (the Quickstart gives a good overview)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)

