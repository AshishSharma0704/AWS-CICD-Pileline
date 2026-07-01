param(
  [string]$ArtifactsBucket,
  [string]$StackName = "local-sam-stack",
  [string]$Region = "us-east-1"
)

if (-not $ArtifactsBucket) {
  Write-Error "Provide ArtifactsBucket name as the first argument. Example: ./local_deploy.ps1 -ArtifactsBucket my-sam-artifacts-12345"
  exit 1
}

Write-Host "Building SAM application..."
sam build --template-file infrastructure/template.yaml

Write-Host "Packaging SAM application (uploading artifacts to S3 bucket: $ArtifactsBucket)..."
sam package --s3-bucket $ArtifactsBucket --output-template-file packaged.yaml

Write-Host "Deploying SAM stack: $StackName"
sam deploy --template-file packaged.yaml --stack-name $StackName --capabilities CAPABILITY_NAMED_IAM --region $Region

Write-Host "Deployment finished. Use AWS Console or 'aws cloudformation describe-stacks' to inspect results."
