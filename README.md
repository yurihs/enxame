# Enxame

Web app that provides an API for managing [Dokku](https://dokku.com/) (An open source PaaS alternative to Heroku).

> Note: This project is only a proof of concept.

By abstracting Dokku operations behind a web API, this app makes it easier to manage Dokku apps programmatically, potentially enabling:

- Automated app deployment and configuration
- Custom dashboards for Dokku management
- Integration with CI/CD pipelines

## Getting Started

To use this app, you'll need:

1. A server running Dokku (see [their documentation](https://dokku.com/docs/getting-started/installation/) for installation methods, including Docker)
2. SSH access to the Dokku server
3. Docker and Docker Compose installed in your local machine

Configure the app by setting the following environment variables:

- `DOKKU_HOSTNAME`: The hostname of your Dokku server
- `DOKKU_USERNAME`: The SSH username for accessing the Dokku server. The user must be able to run `dokku` commands.
- `DOKKU_SSH_KEY`: The contents of an SSH private key, encoded in PKCS#1 or PKCS#8 DER or PEM format or OpenSSH format

You can set these variables in a `.env` file in the project root.

After setting up the environment, you can run the app using Docker Compose.

For detailed API documentation, refer to the `/docs` endpoint when the app is running.

```
docker compose up -d
```
