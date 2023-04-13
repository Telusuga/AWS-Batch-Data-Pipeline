import json
import requests
import datetime
import boto3

s3=boto3.client('s3')
bucket_name='rapid-ur-s3-redshift'

def lambda_handler(event, context):
    # TODO implement
    url="https://moviesdatabase.p.rapidapi.com/titles/x/titles-by-ids"
    headers = {
	"X-RapidAPI-Key": "32f0bd65ffmshc8b8f556b5bc1f2p158cdbjsn41e9f6e10186",
	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    querystring = {"idsList":"tt0001702,tt0001856,tt0001856"}
    res=requests.get(url, headers=headers, params=querystring)
    final=json.loads(res.content)
    print(final)
    d={}
    d['id']=final['results'][0]['id']
    d['is_series']=final['results'][0]['titleType']['isSeries']
    d['Title']=final['results'][0]['titleText']['text']
    year=int(final['results'][0]['releaseDate']['year'])
    month=int(final['results'][0]['releaseDate']['month'])
    day=int(final['results'][0]['releaseDate']['day'])
    o=datetime.datetime(year,month,day)
    d['Release_Date']=str(o.date())
    print('Data load to s3 in progress')
    dt=datetime.datetime.now()
    s3.put_object(Body=json.dumps(d),Bucket=bucket_name,Key=f'inbox/{str(dt)}_movie.json')
    print('Data load into S3 successful')
    return d