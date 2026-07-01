# AWS Pipeline and deployment

This repository includes a SAM template and a simple `buildspec.yml` to build,
package and deploy four Lambda functions plus their S3 raw buckets and DynamoDB
tables.

Quick steps to deploy manually (locally or in a CodeBuild job):

1. Create an S3 bucket to hold packaged artifacts (replace with your name):

```bash
aws s3 mb s3://my-sam-artifacts-12345 --region us-east-1
``` 

2. Package and deploy using SAM:

```bash
export ARTIFACTS_BUCKET=my-sam-artifacts-12345
export STACK_NAME=my-aws-pipeline-stack
sam build --template-file infrastructure/template.yaml
sam package --s3-bucket $ARTIFACTS_BUCKET --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM
```

3. To wire this into an AWS CodePipeline/CodeBuild job, use `buildspec.yml` as the
   buildspec for the CodeBuild step and set the environment variable
   `ARTIFACTS_BUCKET` and `STACK_NAME` in the CodeBuild project.

Notes and next steps:
- The SAM template uses `CodeUri` paths pointing at `lambdas/<name>/` so the
  pipeline must run from the repository root.
- The pipeline/source provider is left generic — common choices are CodeCommit,
  GitHub, or Bitbucket. I can add a `AWS::CodePipeline` CloudFormation
  definition (with CodeCommit source) if you want a fully-managed pipeline in
  CloudFormation.

GitHub pipeline (CloudFormation)
--------------------------------
The repo includes `infrastructure/pipeline.yaml` which creates a CodePipeline
that uses GitHub as the source and a CodeBuild project that runs the
`buildspec.yml` to build and deploy the SAM template.

Steps to prepare and deploy the pipeline:

1. Create a secret in Secrets Manager that contains your GitHub personal
  access token (scope: `repo` or narrower). Store the token under the key
  `token`.

```bash
aws secretsmanager create-secret --name my/github/token --secret-string '{"token":"<GITHUB_TOKEN>"}'
``` 

2. Deploy the pipeline CloudFormation stack (provide the GitHub owner, repo,
  branch and the secret ARN):

```bash
export GITHUB_OWNER=your-account-or-org
export GITHUB_REPO=your-repo
export GITHUB_BRANCH=main
export GITHUB_SECRET_ARN=arn:aws:secretsmanager:...:secret:my/github/token
aws cloudformation deploy --template-file infrastructure/pipeline.yaml --stack-name my-pipeline-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides GitHubOwner=$GITHUB_OWNER GitHubRepo=$GITHUB_REPO GitHubBranch=$GITHUB_BRANCH GitHubTokenSecretArn=$GITHUB_SECRET_ARN
```

3. The pipeline will use the repository root; ensure `buildspec.yml` is at
  the root and `infrastructure/template.yaml` points to `lambdas/*/` code
  locations.

Security note: keep the Secrets Manager secret ARN private and restrict who
can read it. The pipeline uses the secret only as an OAuth token for the
GitHub source action.

Local manual test (safe first push)
-------------------------------
Before pushing changes to GitHub, you can run a local SAM test deploy which
builds, packages and deploys the SAM template using your AWS credentials.

1. Create an artifacts S3 bucket if you don't have one:

```powershell
aws s3 mb s3://my-sam-artifacts-12345 --region us-east-1
```

2. Run the local deploy script (PowerShell):

```powershell
.
\scripts\local_deploy.ps1 -ArtifactsBucket my-sam-artifacts-12345 -StackName my-test-stack -Region us-east-1
```

This performs:
- `sam build` – builds the Lambda packages under `.aws-sam/build`.
- `sam package` – uploads artifacts to the S3 bucket and writes `packaged.yaml`.
- `sam deploy` – runs CloudFormation to create/update the resources defined in `infrastructure/template.yaml`.

Troubleshooting notes:
- If `sam package` fails with missing bucket, confirm the S3 bucket exists and your AWS credentials have `s3:PutObject` permission.
- If `sam deploy` fails with access errors, ensure your AWS user/role has `cloudformation:*`, `dynamodb:*`, `s3:*`, and `lambda:*` rights (or run the deploy from an administrator account while testing).


