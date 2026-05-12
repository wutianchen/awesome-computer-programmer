# get aws credential through assume role

```bash
printf "export AWS_ACCESS_KEY_ID=%s  export AWS_SECRET_ACCESS_KEY=%s export AWS_SESSION_TOKEN=%s" $(aws sts assume-role --role-arn my_role_arn --role-session-name test --query "Credentials.[AccessKeyId,SecretAccessKey,SessionToken]" --output text)
```
