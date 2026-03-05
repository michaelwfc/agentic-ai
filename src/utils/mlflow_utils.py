def get_mlflow_tracking_uri():
    return "http://localhost:8080"
    #return os.environ.get('DLAI_LOCAL_URL').format(port=8080) 