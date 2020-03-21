# Metadata store

## Overview

This repo contains a [Strapi](https://strapi.io) project configured
to act as metadata store for the COVID-19 data project.

## Installation

You can run the following commands to install all dependencies,
assuming Node.js >= 10.0 and Yarn are installed on your system.

```sh
yarn
```

## Running locally

To start Strapi in development mode, SQLite needs to be installed
on your system. If so, you can run the following command to start
the development server:

```sh
yarn develop
```

Once started, a browser window pointing to Strapi's admin environment 
will open automatically.

## Building the project

Run the following command to create a production build:

```sh
NODE_ENV=production yarn build
```

Alternatively, a docker container can be created as follows:

```sh
docker build -t c19d-metadata-store:latest .
```