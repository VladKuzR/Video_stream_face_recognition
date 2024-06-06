import boto3
s3 = boto3.client('s3')

buckets_set = s3.list_buckets()
for bucket in buckets_set['Buckets']:
    if bucket['Name'] != 'torchvision-necessities':
        response = s3.list_objects(
            Bucket = bucket['Name']
        )
        try:
            list_for_deletion = []

            for obj in response['Contents']:
                dict = {}
                dict['Key'] = obj['Key']
                print(dict)
                list_for_deletion.append(dict)

            print(list_for_deletion)
            response = s3.delete_objects(
                Bucket = bucket['Name'], 
                Delete = {'Objects': list_for_deletion}
            )
            print(response)

        except Exception  as e:
            print(e)
