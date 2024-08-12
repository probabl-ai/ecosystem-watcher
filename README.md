<img src="/docs/probabl.png" width="100" height="100" align="right" />

<br>

<h1 style="border-bottom: 0px;">Ecosystem Watcher</h1>

This repository collects statistics for scikit-learn related plugins. The goal is to offer resources for the community 
that gives an overview of useful tools, but it can also be helpful to track how projects develop over time. The goal of
this repository is to address both these needs. 

## Overview

This repository uses Github Actions to scrape relevant information on a daily basis. This data then
feeds an overview page that is hosted on the same repo. This is great because it means this page can
update daily and we have a way for folks to contribute at the same time. 

You can inspect the generated overview on [here](https://probabl-ai.github.io/ecosystem-watcher/).

## Add a project.

Feel free to make a PR if you believe that we're missing a relevant plugin. You can edit the
[repos.jsonl](https://github.com/probabl-ai/ecosystem-watcher/blob/main/repos.jsonl) file in
the root of this repository to add one. For our scraper to work, we need the Github repository
as well as the `pypi` name. Our goal is to be very accepting to new tools, but our goal
is to focus on plugins that interact or play nice with the scikit-learn pipeline.
