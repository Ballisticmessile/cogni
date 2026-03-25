@echo off
setlocal enabledelayedexpansion

cd /d C:\Users\samruddhi\Desktop\cogni

echo Configuring Git...
C:\Program Files\Git\bin\git.exe config --global user.name ballisticmessile
C:\Program Files\Git\bin\git.exe config --global user.email ballisticmessile@github.com

echo Adding files...
C:\Program Files\Git\bin\git.exe add .

echo Creating commit...
C:\Program Files\Git\bin\git.exe commit -m "Cogni Quiz Platform - Initial commit"

echo Removing old remote...
C:\Program Files\Git\bin\git.exe remote remove origin 2>nul

echo Adding new remote...
set TOKEN=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
set URL=https://ballisticmessile:!TOKEN!@github.com/ballisticmessile/cogni.git
C:\Program Files\Git\bin\git.exe remote add origin !URL!

echo Pushing to GitHub...
C:\Program Files\Git\bin\git.exe push -u origin main -f

echo Done!
