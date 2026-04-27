# The Open Data Scotland Project
Open Data Scotland is a volunteer-run open source project to collate open data sources published in Scotland and make them easier to find and use.

See it in action: [opendata.scot](https://opendata.scot/)


There are 4 objectives for the Open Data Scotland project
1. Find: Help public users find a data source they can use
2. Learn: Understand how Open Data is in Scotland
3. Showcase: Promote the projects using these data
4. Connect: Close the feedback loop between data publishers and users

# Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```sh
uv sync
```

# Running

```sh
uv run python main.py
uv run python merge_data.py
uv run python export2jkan.py
```

Or run all steps at once via the shell script:

```sh
uv run bash run.sh
```

## Output Files

Source pipeline steps now emit both CSV and JSON files side-by-side in the source output folders under `data/`.

- Existing CSV outputs are preserved.
- JSON outputs contain dataset-level fields with a nested `resources` array for resource-level fields.

This dual-output mode is intended to support manual inspection of JSON during migration from CSV.

# Running with Docker

```sh
docker build -t the-od-bods .
docker run the-od-bods
```

# Testing (out of date - needs maintenance)

```sh
uv run pytest
```

# More info
Read [the docs](https://docs.opendata.scot/) to find our more about the project, its history, the tools we are using, and how to contribute

# Contact Us
* on Mastodon [@opendatascotland@mastodon.scot](https://mstdn.social/@opendatascotland@mastodon.scot)
* on [LinkedIn](https://www.linkedin.com/company/opendatascotland)
* on [Slack: Open Data Scotland](https://join.slack.com/t/opendatascotland/shared_invite/zt-yfcc64tg-xIF1cOxkWbKZqI8ZBPzkGg) #ods-website

We are looking for contributors!
