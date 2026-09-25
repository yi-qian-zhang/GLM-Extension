# GLM-Extension — 工作方式说明

## 文件在哪里、代码在哪里跑

- 这个目录是本地副本，通过 Mutagen（会话名 `glm-ext`）与服务器 `TJU_6004:/data/wh/yqdata/GLM-Extension` 双向实时同步，延迟通常几秒。
- **所有文件编辑都在本地做**，会自动同步到服务器。不要通过 SSH 在服务器上直接改代码。
- **所有需要 GPU、数据或项目 Python 环境的命令都在服务器上跑**，通过 SSH：

  ```bash
  ssh TJU_6004 "cd /data/wh/yqdata/GLM-Extension && <命令>"
  ```

  例如：
  ```bash
  ssh TJU_6004 "cd /data/wh/yqdata/GLM-Extension && source ~/.bashrc && conda activate <env> && python experiments/run_experiment.py --config config/ecoli_config.yaml"
  ```

- 长时间任务用 `nohup ... > outputs/<name>.log 2>&1 &` 或 tmux 放到后台，然后用 `ssh TJU_6004 "tail -n 50 /data/wh/yqdata/GLM-Extension/outputs/<name>.log"` 查看进度。
- 改完文件后再跑命令之前，可先确认已同步：`mutagen sync list glm-ext` 显示 `Status: Watching for changes` 即表示无待传输内容。 mutagen 不在 Git Bash 的 PATH 里，完整路径是 `C:/Users/ZYQ/AppData/Local/Programs/mutagen/mutagen.exe`（在 PowerShell 里调用）。

## 服务器环境

- Ubuntu 18.04，4 × RTX 4090 (24 GB)。`nvidia-smi` 查看空闲卡，用 `CUDA_VISIBLE_DEVICES=<n>` 指定。
- conda 在 `~/miniconda3`。**非交互 SSH 下 `source ~/.bashrc` 不生效**（`.bashrc` 有 `$PS1` 守卫，conda hook 不会执行），必须直接 source conda.sh：

  ```bash
  ssh TJU_6004_sync "source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm && cd /data/wh/yqdata/GLM-Extension && <命令>"
  ```

- **本项目的 conda 环境：`glm`**（位于 `/data/qsj/conda_envs/glm`，2026-09-25 验证）。Python 3.10.18，torch 2.1.1+cu121，CUDA 12.1，驱动 530.30.02，4 卡可见，bf16 可用，单卡 bf16 矩阵乘约 88 TFLOPS。已装：transformers 4.29.2、tokenizers 0.13.3、peft 0.13.2、opacus 1.4.0、biopython 1.86、numpy 1.24.3、scikit-learn 1.5.1、datasets 2.19.1。EVO 专用环境尚未创建（需要时按 `requirements/requirements_evo.txt` 另建）。
- 服务器多人共用，`/data` 43T 已用 87%；实验输出放 `outputs/`，checkpoint 只存 final，不存中间轮次。

## 不同步的内容（在服务器上直接看）

`.git/`、`__pycache__/`、`outputs/`、`data/genomes/`、`data/huggingface/`、`jobs/logs/`、`venv/`。
需要看实验输出时用 SSH 读服务器上的文件，例如：
```bash
ssh TJU_6004 "ls -la /data/wh/yqdata/GLM-Extension/outputs/"
```

## Git

- git 操作（status/commit/push）只在本地做；服务器上的 `.git` 是独立的，不要在服务器上 commit。
- 本地仓库已设置 `core.autocrlf=false`、`core.eol=lf`，新文件一律用 LF 换行，不要写入 CRLF。

## 注意

- 不要在服务器上运行 `claude` 或任何 Anthropic API 调用；Claude Code 只在本地运行。
- `ssh TJU_6004` 的配置带有 RemoteForward 17890，若报 "remote port forwarding failed" 说明该端口已被另一个会话占用，改用 `ssh TJU_6004_sync`（无转发）即可。
