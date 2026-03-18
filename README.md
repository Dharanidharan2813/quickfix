<!-- ### QuickFix

repair-shop

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit -->


Create Two Sites Using 
```bash
bench new-site quickfix-dev.localhost
bench new-site quickfix-prod.localhost
```

Install quickfix app in both sites using
```bash

bench --site quickfix-dev.localhost install-app quickfix
bench --site quickfix-prod.localhost install-app quickfix
```
Set developer_mode:1 or True (Only for the quickfix-dev.localhost site)
go to 
    sites/quickfix-dev.localhost/site_config.json --> "developer_mode":1
    save and exit the page
    restart the bench

set a shared db_host value

    go to the common_site_config.json
    set db_host : 127.0.0.1

difference between for the site_config.json vs common_site_config.json

    site_config.json

        * It works only for the particular site
        * It does not affect any other sites
        example:
            If we enable the developer_mode for the dev site it enable the developer_mode only for the dev site

    common_site_config.json

        * It works for the all the site 
        * It applies the values or options for all the sites in bench
        example:
            If we enable the developer_mode in the common_site_config.json it enable the developer_mode for all the sites in the bench

    what breaks if you accidentally put a secret in common_site_config.json
        If accidentally me put an secret in common_site_config.json is shares to the all the sites so it is not secure , insted of putting in the common_site_config.json put it in the site_config.json file it only share with the specified site only

Bench Start launches:
    Web : Runs the HTTP server , it handles the request,APIs and render pages
    Worker : workers is to Execute the backgroud jobs (Tasks like email sending --> email sending is queue and prosess it one by one (asynchronously))
    Scheduler : Scheduler Trigger the time based job like (cron-job , enqueue)
    Socketio : it manages the real-time events between the server and clients via websocket