#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Tears down all Lambda Power Tuning demo functions
.DESCRIPTION
    Deletes all CloudFormation stacks and S3 buckets created during deployment
.PARAMETER Profile
    AWS CLI profile to use (default: default)
.PARAMETER Region
    AWS region (default: us-east-1)
.PARAMETER DeleteS3Bucket
    Also delete the managed S3 bucket created by SAM CLI
.EXAMPLE
    .\teardown.ps1 -Profile AWSDeveloper
#>

param(
    [string]$Profile = "default",
    [string]$Region = "us-east-1",
    [switch]$DeleteS3Bucket
)

$ErrorActionPreference = "Continue"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Lambda Power Tuning Demo - Teardown Script" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# List of all stacks to delete
$stacks = @(
    "power-tuning-demo-cpu-intensive-stack",
    "power-tuning-demo-io-bound-stack",
    "power-tuning-demo-network-bound-stack",
    "power-tuning-demo-memory-intensive-stack",
    "power-tuning-demo-simple-api-stack",
    "power-tuning-demo-cpu-intensive-arm64-stack",
    "power-tuning-demo-io-bound-arm64-stack",
    "power-tuning-demo-network-bound-arm64-stack",
    "power-tuning-demo-memory-intensive-arm64-stack",
    "power-tuning-demo-simple-api-arm64-stack"
)

Write-Host "This will delete the following stacks:" -ForegroundColor Yellow
$stacks | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
Write-Host ""

$confirmation = Read-Host "Are you sure you want to continue? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Teardown cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "Deleting CloudFormation stacks..." -ForegroundColor Cyan
Write-Host ""

$deletedCount = 0
$failedStacks = @()

foreach ($stack in $stacks) {
    Write-Host "Deleting $stack..." -ForegroundColor Yellow
    
    $deleteCmd = "aws cloudformation delete-stack --stack-name $stack --region $Region --profile $Profile"
    
    try {
        Invoke-Expression $deleteCmd 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Delete initiated for $stack" -ForegroundColor Green
            $deletedCount++
        } else {
            Write-Host "  ✗ Failed to delete $stack" -ForegroundColor Red
            $failedStacks += $stack
        }
    }
    catch {
        Write-Host "  ✗ Error deleting $stack : $_" -ForegroundColor Red
        $failedStacks += $stack
    }
}

Write-Host ""
Write-Host "Waiting for stacks to be deleted (this may take a few minutes)..." -ForegroundColor Cyan
Write-Host "You can check status with: aws cloudformation list-stacks --profile $Profile" -ForegroundColor Gray
Write-Host ""

# Optional: Delete the managed S3 bucket
if ($DeleteS3Bucket) {
    Write-Host "Finding managed S3 bucket..." -ForegroundColor Cyan
    
    $bucketQuery = "aws s3 ls --profile $Profile | Select-String 'aws-sam-cli-managed-default'"
    $bucket = Invoke-Expression $bucketQuery 2>&1 | Out-String
    
    if ($bucket -match 'aws-sam-cli-managed-default-samclisourcebucket-\w+') {
        $bucketName = $Matches[0]
        Write-Host "Found bucket: $bucketName" -ForegroundColor Yellow
        
        $bucketConfirm = Read-Host "Delete S3 bucket $bucketName and all its contents? (yes/no)"
        if ($bucketConfirm -eq "yes") {
            Write-Host "Emptying and deleting bucket..." -ForegroundColor Yellow
            aws s3 rb "s3://$bucketName" --force --profile $Profile
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ Bucket deleted successfully" -ForegroundColor Green
            } else {
                Write-Host "  ✗ Failed to delete bucket" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "  No managed S3 bucket found" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Teardown Summary" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Deletion initiated for: $deletedCount stacks" -ForegroundColor Green

if ($failedStacks.Count -gt 0) {
    Write-Host "Failed to delete: $($failedStacks.Count) stacks" -ForegroundColor Red
    $failedStacks | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
}

Write-Host ""
Write-Host "Note: Stack deletion happens asynchronously." -ForegroundColor Yellow
Write-Host "Monitor progress in the AWS Console or use:" -ForegroundColor Yellow
Write-Host "  aws cloudformation list-stacks --profile $Profile" -ForegroundColor Gray
Write-Host ""
