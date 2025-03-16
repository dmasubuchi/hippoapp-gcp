# Public Access Verification Report

## Cloud Run Service

- **URL**: https://hippoapp-546tyu2ata-uw.a.run.app
- **Status**: Access restricted by organization policy

## API Endpoints

### Health Check
```
<html><head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>403 Forbidden</title>
</head>
<body text=#000000 bgcolor=#ffffff>
<h1>Error: Forbidden</h1>
<h2>Your client does not have permission to get URL <code>/api/health</code> from this server.</h2>
<h2></h2>
</body></html>
```

### Languages API
```
<html><head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>403 Forbidden</title>
</head>
<body text=#000000 bgcolor=#ffffff>
<h1>Error: Forbidden</h1>
<h2>Your client does not have permission to get URL <code>/api/languages</code> from this server.</h2>
<h2></h2>
</body></html>
```

## Organization Policy Status

The Cloud Run service is currently restricted by the organization policy. To allow public access, follow the instructions in the [Cloud Run Public Access Guide](CLOUD_RUN_PUBLIC_ACCESS.md).

## Local Testing

The application can be tested locally using:

```bash
./run-local.sh
```

This will start the application with mock data and allow you to test the functionality without requiring organization policy changes.
