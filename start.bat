@echo off
chcp 65001 >nul
echo ==============================================
echo          一键启动前端 + 后端服务
echo ==============================================
echo.

:: 启动后端（新开独立窗口）
echo 正在启动后端服务...
start "后端服务" cmd /k "cd /d E:\web\myweb\backend && call venv\Scripts\Activate.ps1 && python -m uvicorn main:app --reload"


:: 启动前端（新开独立窗口）
echo 正在启动前端服务...
start "前端服务" cmd /k "cd /d E:\web\myweb\frontend && pnpm dev"

:: 延迟1秒，避免窗口抢占
timeout /t 1 /nobreak >nul


echo.
echo 两个服务窗口已分别打开！
echo 关闭本提示窗口即可，前后端窗口保留运行
pause