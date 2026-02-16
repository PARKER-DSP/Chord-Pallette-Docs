#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

git config core.hooksPath .githooks

Write-Host "Git hooks path configured: .githooks"
Write-Host "Pre-commit hook will run docs nav sync and validation checks."
