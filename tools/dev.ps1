#!/usr/bin/env pwsh

param(
  [ValidateSet("nav", "check", "build", "serve", "ci")]
  [string]$Task = "check"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

switch ($Task) {
  "nav" { python tools/docs_tool.py generate-nav }
  "check" { python tools/docs_tool.py check-all }
  "build" { python tools/docs_tool.py build }
  "serve" { python tools/docs_tool.py serve }
  "ci" { python tools/docs_tool.py ci }
}
